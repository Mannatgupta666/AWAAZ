# AWS Credits Usage Guide for Awaaz Project

## Overview
Your AWS credits can significantly enhance the Awaaz system. Here's how to use them effectively.

---

## 🎯 Priority AWS Services to Use (Recommended Order)

### 1. **Amazon Bedrock** (HIGHEST PRIORITY)
**Cost**: ~$0.003 per 1K tokens (Claude models)
**Monthly estimate**: $20-50 for moderate usage

**Why**: Core AI reasoning engine for scheme matching and conversation
**Setup**:
```bash
# Enable Bedrock in AWS Console
# Region: us-east-1 or us-west-2
# Model: Claude 3 Haiku (cheapest) or Claude 3.5 Sonnet (best)
```

**Integration**:
```python
import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

response = bedrock.invoke_model(
    modelId='anthropic.claude-3-haiku-20240307-v1:0',
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [{"role": "user", "content": user_message}],
        "max_tokens": 1000
    })
)
```

---

### 2. **Amazon S3** (ESSENTIAL)
**Cost**: ~$0.023 per GB/month
**Monthly estimate**: $5-10

**Why**: Store documents, scheme data, generated PDFs
**Buckets to create**:
- `awaaz-user-documents` - Uploaded documents
- `awaaz-scheme-data` - Government scheme JSON files
- `awaaz-generated-forms` - PDFs and affidavits

**Setup**:
```bash
aws s3 mb s3://awaaz-user-documents
aws s3 mb s3://awaaz-scheme-data
aws s3 mb s3://awaaz-generated-forms
```

---

### 3. **AWS Lambda + API Gateway** (RECOMMENDED)
**Cost**: First 1M requests free, then $0.20 per 1M
**Monthly estimate**: $10-20

**Why**: Serverless backend - no server management needed
**Functions to create**:
- `awaaz-chat-handler`
- `awaaz-speech-processor`
- `awaaz-ocr-processor`
- `awaaz-pdf-generator`

**Deployment**:
```bash
# Package FastAPI with Mangum adapter
pip install mangum
# Deploy using AWS SAM or Serverless Framework
```

---

### 4. **Amazon DynamoDB** (RECOMMENDED)
**Cost**: $1.25 per million write requests
**Monthly estimate**: $5-15

**Why**: Fast, scalable user profile storage
**Tables to create**:
- `awaaz-users` - User profiles
- `awaaz-sessions` - Chat sessions
- `awaaz-applications` - Application tracking

---

### 5. **Amazon Textract** (OPTIONAL - Better than Tesseract)
**Cost**: $1.50 per 1000 pages
**Monthly estimate**: $10-30

**Why**: Superior OCR compared to Tesseract, especially for Indian documents
**Use for**: Aadhaar, PAN, Voter ID, Driving License

**Integration**:
```python
import boto3

textract = boto3.client('textract')

response = textract.detect_document_text(
    Document={'S3Object': {'Bucket': 'awaaz-user-documents', 'Name': 'aadhaar.jpg'}}
)
```

---

### 6. **Amazon Transcribe** (OPTIONAL - Alternative to Bhashini)
**Cost**: $0.024 per minute
**Monthly estimate**: $15-40

**Why**: Backup for Bhashini, supports Hindi and other Indian languages
**Use when**: Bhashini API is down or slow

---

### 7. **Amazon Polly** (OPTIONAL - Alternative to Bhashini)
**Cost**: $4 per 1M characters
**Monthly estimate**: $5-15

**Why**: Backup TTS, supports Hindi (Aditi voice)
**Use when**: Bhashini TTS is unavailable

---

### 8. **Amazon Translate** (OPTIONAL)
**Cost**: $15 per million characters
**Monthly estimate**: $10-20

**Why**: Translate between Indian languages
**Supports**: Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi

---

### 9. **AWS EC2** (If not using Lambda)
**Cost**: t3.small = $0.0208/hour = ~$15/month
**Monthly estimate**: $15-50

**Why**: Host FastAPI backend if you prefer traditional server
**Recommended**: t3.small or t3.medium in Mumbai region (ap-south-1)

---

### 10. **Amazon CloudWatch** (ESSENTIAL for Monitoring)
**Cost**: First 5GB logs free
**Monthly estimate**: $5-10

**Why**: Monitor application health, debug issues
**Setup**: Automatic with Lambda/EC2

---

## 💰 Estimated Monthly AWS Costs

### Minimal Setup (Lambda + Bedrock + S3)
- Lambda: $5
- Bedrock: $30
- S3: $5
- DynamoDB: $5
- CloudWatch: $5
**Total**: ~$50/month

### Full Setup (All services)
- Lambda: $10
- Bedrock: $50
- S3: $10
- DynamoDB: $10
- Textract: $20
- Transcribe: $20
- Polly: $10
- CloudWatch: $10
**Total**: ~$140/month

---

## 🚀 Quick Start Deployment

### Option 1: Serverless (Recommended)
```bash
# Install AWS CLI
pip install awscli

# Configure credentials
aws configure

# Deploy using SAM
sam init
sam build
sam deploy --guided
```

### Option 2: EC2 Traditional Server
```bash
# Launch EC2 instance (Mumbai region)
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.small \
  --key-name awaaz-key \
  --security-groups awaaz-sg

# SSH and deploy
ssh -i awaaz-key.pem ubuntu@<instance-ip>
git clone <your-repo>
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 🔐 Security Best Practices

1. **Use IAM roles** - Don't hardcode credentials
2. **Enable S3 encryption** - Protect user documents
3. **Use VPC** - Isolate backend resources
4. **Enable CloudTrail** - Audit all API calls
5. **Use Secrets Manager** - Store Bhashini API keys

---

## 📊 Cost Optimization Tips

1. **Use Lambda instead of EC2** - Pay only for usage
2. **Enable S3 lifecycle policies** - Delete old documents after 90 days
3. **Use DynamoDB on-demand** - No upfront capacity planning
4. **Cache Bedrock responses** - Reduce duplicate AI calls
5. **Compress images before OCR** - Reduce Textract costs
6. **Use CloudWatch alarms** - Get notified if costs spike

---

## 🎓 AWS Free Tier Benefits (First 12 Months)

- **Lambda**: 1M requests/month free
- **S3**: 5GB storage free
- **DynamoDB**: 25GB storage free
- **EC2**: 750 hours/month t2.micro free
- **CloudWatch**: 10 custom metrics free

---

## 📝 Next Steps

1. **Create AWS account** (if not done)
2. **Apply AWS credits** to your account
3. **Enable Bedrock** in us-east-1 region
4. **Create S3 buckets** for storage
5. **Deploy Lambda functions** or EC2 instance
6. **Set up CloudWatch** monitoring
7. **Test with small workload** first
8. **Monitor costs daily** in AWS Cost Explorer

---

## 🆘 Support Resources

- AWS Free Tier: https://aws.amazon.com/free/
- Bedrock Pricing: https://aws.amazon.com/bedrock/pricing/
- AWS India Support: https://aws.amazon.com/contact-us/
- Cost Calculator: https://calculator.aws/

---

## ⚠️ Important Notes

- **Mumbai region (ap-south-1)** is closest to India - use for lowest latency
- **Bedrock is NOT available in Mumbai** - use us-east-1 or us-west-2
- **Set billing alarms** - Get notified at $50, $100, $150
- **Review costs weekly** - Use AWS Cost Explorer
- **Keep Bhashini as primary** - AWS services are backup/enhancement
