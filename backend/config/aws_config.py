"""
AWS Configuration and Client Management
Centralized AWS service initialization
"""
import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class AWSConfig:
    """Singleton class for AWS service clients"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AWSConfig, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
            self.aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
            self.aws_region = os.getenv("AWS_REGION", "us-east-1")
            self.bedrock_region = os.getenv("BEDROCK_REGION", "us-east-1")
            
            # S3 bucket names
            self.documents_bucket = os.getenv("AWAAZ_DOCUMENTS_BUCKET", "awaaz-documents")
            self.schemes_bucket = os.getenv("AWAAZ_SCHEMES_BUCKET", "awaaz-schemes")
            self.generated_bucket = os.getenv("AWAAZ_GENERATED_BUCKET", "awaaz-generated")
            
            # Bedrock model
            self.bedrock_model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
            
            # Initialize clients
            self._init_clients()
            self._initialized = True
    
    def _init_clients(self):
        """Initialize AWS service clients"""
        try:
            # S3 Client
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.aws_region
            )
            
            # Bedrock Runtime Client
            self.bedrock_client = boto3.client(
                'bedrock-runtime',
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.bedrock_region
            )
            
            # Textract Client
            self.textract_client = boto3.client(
                'textract',
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.aws_region
            )
            
            # DynamoDB Client (optional)
            self.dynamodb_client = boto3.client(
                'dynamodb',
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.aws_region
            )
            
            logger.info("AWS clients initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize AWS clients: {str(e)}")
            raise
    
    def create_buckets_if_not_exist(self):
        """Create S3 buckets if they don't exist"""
        buckets = [
            self.documents_bucket,
            self.schemes_bucket,
            self.generated_bucket
        ]
        
        for bucket_name in buckets:
            try:
                self.s3_client.head_bucket(Bucket=bucket_name)
                logger.info(f"Bucket {bucket_name} already exists")
            except ClientError:
                try:
                    if self.aws_region == 'us-east-1':
                        self.s3_client.create_bucket(Bucket=bucket_name)
                    else:
                        self.s3_client.create_bucket(
                            Bucket=bucket_name,
                            CreateBucketConfiguration={'LocationConstraint': self.aws_region}
                        )
                    logger.info(f"Created bucket: {bucket_name}")
                except ClientError as e:
                    logger.error(f"Failed to create bucket {bucket_name}: {str(e)}")
    
    def upload_to_s3(self, file_path, bucket_name, object_name=None):
        """Upload file to S3"""
        if object_name is None:
            object_name = os.path.basename(file_path)
        
        try:
            self.s3_client.upload_file(file_path, bucket_name, object_name)
            logger.info(f"Uploaded {file_path} to {bucket_name}/{object_name}")
            return f"s3://{bucket_name}/{object_name}"
        except ClientError as e:
            logger.error(f"Failed to upload to S3: {str(e)}")
            raise
    
    def download_from_s3(self, bucket_name, object_name, file_path):
        """Download file from S3"""
        try:
            self.s3_client.download_file(bucket_name, object_name, file_path)
            logger.info(f"Downloaded {bucket_name}/{object_name} to {file_path}")
            return file_path
        except ClientError as e:
            logger.error(f"Failed to download from S3: {str(e)}")
            raise
    
    def get_s3_url(self, bucket_name, object_name, expiration=3600):
        """Generate presigned URL for S3 object"""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': object_name},
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {str(e)}")
            raise

# Global instance
aws_config = AWSConfig()
