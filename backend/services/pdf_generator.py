"""
PDF Generation Module for Document Processing
Handles PDF generation from templates using Jinja2 and ReportLab.
"""

import os
import boto3
from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from botocore.exceptions import ClientError


@dataclass
class PDFGenerationResult:
    """Result of PDF generation operation."""
    status: str
    pdf_path: Optional[str]
    s3_url: Optional[str]
    error_message: Optional[str]
    generation_timestamp: datetime


class TemplateEngine:
    """Load and render Jinja2 templates with user data."""
    
    def __init__(self, template_dir: str):
        """Initialize template engine with template directory."""
        self.template_dir = template_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def render_template(self, template_name: str, data: Dict[str, Any]) -> str:
        """Render template with provided data."""
        try:
            template = self.get_template(template_name)
            rendered = template.render(**data)
            return rendered
        except TemplateNotFound:
            raise Exception(f"Template not found: {template_name}")
        except Exception as e:
            raise Exception(f"Template rendering error: {str(e)}")
    
    def get_template(self, template_name: str) -> Template:
        """Load template by name."""
        return self.env.get_template(template_name)


class PDFRenderer:
    """Render HTML/text content to PDF using ReportLab."""
    
    def render_to_pdf(self, content: str, output_path: str) -> str:
        """Render content to PDF file."""
        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Configure styles
            styles = self.configure_styles()
            
            # Build story (content elements)
            story = []
            
            # Split content into paragraphs
            paragraphs = content.split('\n\n')
            
            for para_text in paragraphs:
                if para_text.strip():
                    # Determine style based on content
                    if para_text.strip().isupper() or len(para_text) < 50:
                        style = styles['Heading']
                    else:
                        style = styles['Normal']
                    
                    para = Paragraph(para_text.strip(), style)
                    story.append(para)
                    story.append(Spacer(1, 0.2 * inch))
            
            # Build PDF
            doc.build(story)
            
            return output_path
        
        except Exception as e:
            raise Exception(f"PDF rendering error: {str(e)}")
    
    def configure_styles(self) -> Dict[str, Any]:
        """Configure PDF styles (fonts, spacing, etc.)."""
        styles = getSampleStyleSheet()
        
        # Customize heading style
        styles.add(ParagraphStyle(
            name='Heading',
            parent=styles['Heading1'],
            fontSize=14,
            textColor='black',
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Customize normal style
        styles['Normal'].fontSize = 11
        styles['Normal'].leading = 14
        styles['Normal'].alignment = TA_LEFT
        
        return styles


class S3StorageClient:
    """Handle S3 upload operations for PDFs."""
    
    def __init__(self, aws_config: Dict[str, str]):
        """Initialize S3 client with AWS credentials."""
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_config.get('aws_access_key_id'),
            aws_secret_access_key=aws_config.get('aws_secret_access_key'),
            region_name=aws_config.get('aws_region', 'us-east-1')
        )
        self.bucket_name = aws_config.get('s3_bucket_name')
    
    def upload_pdf(self, pdf_path: str, file_key: str, max_retries: int = 3) -> str:
        """Upload PDF to S3 with retry logic."""
        if not self.bucket_name:
            raise Exception("S3 bucket name not configured")
        
        for attempt in range(max_retries):
            try:
                with open(pdf_path, 'rb') as f:
                    self.s3_client.put_object(
                        Bucket=self.bucket_name,
                        Key=file_key,
                        Body=f,
                        ContentType='application/pdf'
                    )
                
                s3_url = f"https://{self.bucket_name}.s3.amazonaws.com/{file_key}"
                return s3_url
            
            except ClientError as e:
                if attempt == max_retries - 1:
                    raise Exception(f"S3 upload failed after {max_retries} attempts: {str(e)}")
                continue
            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(f"S3 upload failed after {max_retries} attempts: {str(e)}")
                continue
    
    def generate_file_key(self, user_id: str, template_type: str) -> str:
        """Generate unique S3 key for PDF."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{user_id}/pdfs/{template_type}_{timestamp}.pdf"


class PDFGenerator:
    """Main service class for PDF generation from templates."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize PDF generator with configuration."""
        self.config = config
        self.template_dir = config.get('template_directory', './templates')
        self.output_dir = config.get('pdf_output_directory', './output')
        self.use_templates = config.get('use_templates', False)
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Only initialize template engine if using templates
        if self.use_templates:
            os.makedirs(self.template_dir, exist_ok=True)
            self.template_engine = TemplateEngine(self.template_dir)
        
        self.pdf_renderer = PDFRenderer()
        self.s3_client = S3StorageClient(config)
    
    def _generate_content_from_data(self, user_data: Dict[str, Any], template_type: str) -> str:
        """Generate PDF content directly from user data without templates."""
        if template_type == 'affidavit':
            content = f"""AFFIDAVIT

I, {user_data.get('name', 'N/A')}, hereby declare the following:

Applicant Name: {user_data.get('name', 'N/A')}

Scheme Applied For: {user_data.get('scheme', 'N/A')}

Annual Income: {user_data.get('income', 'N/A')}

Address: {user_data.get('address', 'N/A')}

I hereby declare that all the information provided above is true and correct to the best of my knowledge.

Date: {user_data.get('date', datetime.now().strftime('%Y-%m-%d'))}

Signature: _________________
{user_data.get('name', 'N/A')}"""
        
        elif template_type == 'scheme_application':
            content = f"""GOVERNMENT SCHEME APPLICATION FORM

Application Details

Applicant Name: {user_data.get('name', 'N/A')}

Scheme Name: {user_data.get('scheme', 'N/A')}

Annual Income: {user_data.get('income', 'N/A')}

Address: {user_data.get('address', 'N/A')}

Contact Information

Phone: {user_data.get('phone', 'Not Provided')}

Email: {user_data.get('email', 'Not Provided')}

Document Details

Aadhaar Number: {user_data.get('aadhaar_number', 'Not Provided')}

Certificate Number: {user_data.get('certificate_number', 'Not Provided')}

Declaration

I hereby declare that all the information provided in this application is true and correct to the best of my knowledge. I understand that any false information may result in rejection of my application.

Date: {user_data.get('date', datetime.now().strftime('%Y-%m-%d'))}

Applicant Signature: _________________

For Office Use Only

Application ID: _________________

Received Date: _________________

Verified By: _________________

Status: _________________"""
        
        else:
            content = f"""DOCUMENT

Generated for: {user_data.get('name', 'N/A')}

"""
            for key, value in user_data.items():
                content += f"{key.replace('_', ' ').title()}: {value}\n\n"
        
        return content
    
    def generate_pdf(self, user_data: Dict[str, Any], template_type: str) -> Dict[str, Any]:
        """Generate PDF from template or directly from data."""
        try:
            # Generate content
            if self.use_templates:
                # Use template files
                template_map = {
                    'affidavit': 'affidavit_template.txt',
                    'scheme_application': 'scheme_application_template.txt'
                }
                
                template_name = template_map.get(template_type)
                if not template_name:
                    return {
                        'status': 'error',
                        'pdf_path': None,
                        's3_url': None,
                        'error_message': f"Unknown template type: {template_type}"
                    }
                
                rendered_content = self.template_engine.render_template(template_name, user_data)
            else:
                # Generate content directly from data
                rendered_content = self._generate_content_from_data(user_data, template_type)
            
            # Generate output path
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"{template_type}_{timestamp}.pdf"
            output_path = os.path.join(self.output_dir, output_filename)
            
            # Render to PDF
            pdf_path = self.pdf_renderer.render_to_pdf(rendered_content, output_path)
            
            # Upload to S3
            try:
                user_id = user_data.get('user_id', 'unknown')
                file_key = self.s3_client.generate_file_key(user_id, template_type)
                s3_url = self.s3_client.upload_pdf(pdf_path, file_key)
            except Exception as e:
                s3_url = None
            
            return {
                'status': 'success',
                'pdf_path': pdf_path,
                's3_url': s3_url,
                'error_message': None
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'pdf_path': None,
                's3_url': None,
                'error_message': f"PDF generation error: {str(e)}"
            }


# Example usage
if __name__ == "__main__":
    # Configuration
    config = {
        'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
        'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
        'aws_region': os.getenv('AWS_REGION', 'us-east-1'),
        's3_bucket_name': os.getenv('S3_BUCKET_NAME'),
        'template_directory': './templates',
        'pdf_output_directory': './output',
        'use_templates': False  # Set to True to use template files, False to generate directly
    }
    
    # Initialize generator
    generator = PDFGenerator(config)
    
    # Sample data
    user_data = {
        'user_id': 'user123',
        'name': 'Ram Kumar',
        'scheme': 'PM-KISAN',
        'income': '1.2 lakh',
        'address': 'Village Rampur, District Sitapur'
    }
    
    # Generate PDF
    result = generator.generate_pdf(user_data, 'scheme_application')
    
    print(f"Status: {result['status']}")
    print(f"PDF Path: {result['pdf_path']}")
    print(f"S3 URL: {result['s3_url']}")
