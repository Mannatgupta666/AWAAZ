# 🔐 How to Add Your AWS Credentials

## ⚠️ IMPORTANT: First Secure Your Account!

Before adding credentials, you MUST:

1. **Delete the old exposed credentials**
   - Go to: https://console.aws.amazon.com/iam/
   - Find access key: `AKIA4AXZCTKJCP3NIGRW`
   - Click Actions → Deactivate → Delete

2. **Create NEW credentials**
   - In IAM → Users → Your user → Security credentials
   - Click "Create access key"
   - Choose "Application running outside AWS"
   - Copy both keys (you'll only see them once!)

---

## 📝 Step-by-Step: Add Credentials to .env File

### Option 1: Using VS Code (Easiest)

1. Open VS Code
2. Open file: `AWAAZ/backend/.env`
3. Replace these lines:
   ```env
   AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_HERE
   AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_KEY_HERE
   ```
   
   With your NEW credentials:
   ```env
   AWS_ACCESS_KEY_ID=AKIA4AXZCTKJ...  (your new key)
   AWS_SECRET_ACCESS_KEY=wJalr...     (your new secret)
   ```

4. Save the file (Cmd + S)

### Option 2: Using Terminal

```bash
# Open the file
cd ~/aiforbharat\ hackathon/AWAAZ/backend
nano .env

# Edit the file:
# - Replace YOUR_AWS_ACCESS_KEY_HERE with your actual key
# - Replace YOUR_AWS_SECRET_KEY_HERE with your actual secret

# Save and exit:
# Press Ctrl + X
# Press Y
# Press Enter
```

---

## ✅ What Your .env File Should Look Like:

```env
# AWS Credentials
AWS_ACCESS_KEY_ID=AKIA4AXZCTKJNEWKEY123
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=us-east-1

# S3 Bucket Names
AWAAZ_DOCUMENTS_BUCKET=awaaz-docs-shagun
AWAAZ_SCHEMES_BUCKET=awaaz-schemes-shagun
AWAAZ_GENERATED_BUCKET=awaaz-generated-shagun

# Amazon Bedrock Configuration
BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
BEDROCK_REGION=us-east-1

# Bhashini API (Optional)
BHASHINI_API_KEY=your_bhashini_key_here
BHASHINI_USER_ID=your_bhashini_user_id_here

# Application Settings
ENVIRONMENT=development
DEBUG=true
```

---

## 🔒 Security Checklist

- [ ] Deleted old exposed credentials from AWS
- [ ] Created NEW credentials
- [ ] Added NEW credentials to `.env` file
- [ ] `.env` file is in `.gitignore` (already done ✅)
- [ ] Never shared credentials in chat/email/Slack

---

## ✅ Verify It Works

After adding credentials, test the connection:

```bash
cd ~/aiforbharat\ hackathon/AWAAZ/backend

# Test AWS connection
python -c "from config.aws_config import aws_config; print('✅ AWS connected!')"
```

If you see "✅ AWS connected!" - you're good to go!

---

## 🆘 Troubleshooting

### "AWS credentials not found"
- Make sure `.env` file is in `backend/` folder
- Check that you replaced the placeholder text
- No spaces around the `=` sign

### "Invalid credentials"
- Make sure you're using the NEW credentials (not old ones)
- Copy-paste carefully (no extra spaces)
- Check if credentials are active in AWS Console

### "Access denied"
- Make sure your IAM user has these permissions:
  - AmazonS3FullAccess
  - AmazonBedrockFullAccess
  - AmazonTextractFullAccess

---

## 📞 Quick Reference

**AWS Console:** https://console.aws.amazon.com/
**IAM Users:** https://console.aws.amazon.com/iam/
**Bedrock:** https://console.aws.amazon.com/bedrock/

**File Location:**
```
~/aiforbharat hackathon/AWAAZ/backend/.env
```

---

## ⚡ Next Steps

After adding credentials:

1. ✅ Test AWS connection
2. ✅ Enable Bedrock model access
3. ✅ Start the backend: `uvicorn main:app --reload`
4. ✅ Open test page and verify everything works
5. ✅ Record your demo!

---

**Remember: NEVER commit the .env file to GitHub!** ✅ Already protected by .gitignore
