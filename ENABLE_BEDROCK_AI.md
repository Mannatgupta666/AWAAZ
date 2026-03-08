# Enable Amazon Bedrock AI (Claude)

## Current Status
✅ AWS credentials configured  
✅ Bedrock client initialized  
❌ **Claude model access NOT enabled**

Your app is currently using **fallback rule-based matching** instead of AI.

## Error Message
```
Model use case details have not been submitted for this account. 
Fill out the Anthropic use case details form before using the model.
```

## How to Enable Claude AI

### Step 1: Go to AWS Bedrock Console
1. Open your browser and go to: https://console.aws.amazon.com/bedrock/
2. Make sure you're in the **us-east-1** region (top right corner)

### Step 2: Request Model Access
1. In the left sidebar, click **"Model access"**
2. Click the orange **"Manage model access"** button
3. Find **"Anthropic"** in the list
4. Check the box next to **"Claude 3 Haiku"**
5. Click **"Request model access"** at the bottom

### Step 3: Fill Out Use Case Form
AWS will ask you to fill out a form about your use case:

**Example answers for your hackathon project:**

- **Use case description**: 
  ```
  AI for Bharat Hackathon project - Government scheme assistant for Indian citizens.
  Using Claude AI to understand user queries in natural language and match them 
  with eligible government schemes (PM Kisan, Ayushman Bharat, etc.).
  ```

- **Industry**: Government / Public Sector

- **Will you use it for**: Research & Development / Education

- **Expected monthly usage**: Low (under 1000 requests)

- **Data handling**: No sensitive personal data will be sent to the model

### Step 4: Wait for Approval
- **Instant approval**: Some accounts get instant approval
- **Manual review**: May take 15 minutes to 24 hours
- You'll receive an email when approved

### Step 5: Verify Access
Once approved, run this command to test:

```bash
cd ~/aiforbharat\ hackathon/AWAAZ/backend
python3 test_bedrock.py
```

You should see:
```
🎉 BEDROCK AI IS WORKING!
Your app is using Claude AI for intelligent scheme matching.
```

## Alternative: Use Without AI (Current Setup)

Your app **already works** without Bedrock AI! It uses:
- ✅ Rule-based scheme matching (works well)
- ✅ Keyword extraction from user messages
- ✅ Eligibility scoring based on occupation, income, age

**For your demo**, you can:
1. Continue using the fallback system (it works!)
2. OR enable Bedrock AI for more intelligent responses

## Cost Estimate

**Claude 3 Haiku pricing:**
- Input: $0.25 per 1M tokens
- Output: $1.25 per 1M tokens

**For your demo:**
- ~100 test queries = ~$0.05
- Your $100 credits = 200,000+ queries

**You have plenty of credits!**

## What Changes With AI Enabled?

### Without AI (Current):
```
User: "I am a farmer"
System: Extracts keyword "farmer" → Matches PM Kisan
```

### With AI (After enabling):
```
User: "I am a 35 year old farmer from Punjab with 2 acres of land"
System: AI extracts:
  - occupation: farmer
  - age: 35
  - state: Punjab
  - land_ownership: yes
  - income: (inferred from context)
→ Matches PM Kisan with detailed reasoning
→ Generates natural conversational response
```

## Need Help?

If you get stuck:
1. Check AWS region is **us-east-1**
2. Verify your AWS credentials are correct
3. Make sure you're logged into the correct AWS account
4. Try a different model (Claude 3.5 Sonnet) if Haiku is not available

## Quick Links

- AWS Bedrock Console: https://console.aws.amazon.com/bedrock/
- Model Access Page: https://console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess
- Bedrock Pricing: https://aws.amazon.com/bedrock/pricing/

---

**For your hackathon demo, the current system works fine!**  
Enabling AI is optional but makes responses more intelligent.
