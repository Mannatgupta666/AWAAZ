"""
Scheme Matching Engine using Amazon Bedrock
"""
import json
import sys
sys.path.append('..')
from config.aws_config import aws_config
import logging

logger = logging.getLogger(__name__)

class SchemeEngine:
    """AI-powered scheme matching using Amazon Bedrock"""
    
    def __init__(self):
        self.bedrock_client = aws_config.bedrock_client
        self.model_id = aws_config.bedrock_model_id
    
    def extract_user_info(self, message: str, language: str = "en") -> dict:
        """Extract user information from message using Bedrock"""
        
        prompt = f"""Extract user information from this message and return as JSON.
Message: {message}
Language: {language}

Extract:
- occupation
- income (in lakhs)
- age
- gender
- state
- district
- category (General/OBC/SC/ST)
- disability (yes/no)
- land_ownership (yes/no)

Return only valid JSON, no explanation."""

        try:
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 500,
                    "temperature": 0.3
                })
            )
            
            result = json.loads(response['body'].read())
            content = result['content'][0]['text']
            
            # Parse JSON from response
            user_data = json.loads(content)
            return user_data
            
        except Exception as e:
            logger.error(f"Bedrock extraction failed: {str(e)}")
            # Fallback to basic extraction
            return self._basic_extraction(message)
    
    def _basic_extraction(self, message: str) -> dict:
        """Fallback extraction without AI"""
        import re
        message_lower = message.lower()
        user_data = {}
        
        # Extract occupation
        if "farmer" in message_lower or "kisan" in message_lower:
            user_data["occupation"] = "farmer"
        elif "student" in message_lower or "studying" in message_lower or "college" in message_lower or "school" in message_lower:
            user_data["occupation"] = "student"
        elif "worker" in message_lower or "labour" in message_lower:
            user_data["occupation"] = "worker"
        elif "pregnant" in message_lower or "expecting" in message_lower or "mother" in message_lower:
            user_data["occupation"] = "any"
            user_data["gender"] = "female"  # Set gender for pregnant women
        else:
            user_data["occupation"] = "any"
        
        # Extract category (SC/ST/OBC)
        if "sc" in message_lower or "scheduled caste" in message_lower:
            user_data["category"] = "SC"
        elif "st" in message_lower or "scheduled tribe" in message_lower:
            user_data["category"] = "ST"
        elif "obc" in message_lower or "other backward" in message_lower:
            user_data["category"] = "OBC"
        else:
            user_data["category"] = "General"
        
        # Extract age
        age_match = re.search(r'(\d+)\s*(?:year|yr|old)', message_lower)
        if age_match:
            user_data["age"] = int(age_match.group(1))
        else:
            # Default age based on occupation
            if user_data.get("occupation") == "student":
                user_data["age"] = 20
            else:
                user_data["age"] = 30
        
        # Extract income
        income_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:lakh|lac)', message_lower)
        if income_match:
            user_data["income"] = float(income_match.group(1))
        else:
            user_data["income"] = 2  # Default low income
        
        # Extract gender - IMPORTANT: Check if not already set
        if "gender" not in user_data:
            if "woman" in message_lower or "female" in message_lower or "mahila" in message_lower or "girl" in message_lower or "pregnant" in message_lower or "mother" in message_lower:
                user_data["gender"] = "female"
            elif "man" in message_lower or "male" in message_lower or "boy" in message_lower:
                user_data["gender"] = "male"
            else:
                # Default to male for farmers/workers (most common case)
                if user_data.get("occupation") in ["farmer", "worker"]:
                    user_data["gender"] = "male"
                else:
                    user_data["gender"] = "any"
        
        # Extract state
        states = ["punjab", "haryana", "delhi", "uttar pradesh", "up", "bihar", "maharashtra"]
        for state in states:
            if state in message_lower:
                user_data["state"] = state.title()
                break
        
        # Land ownership for farmers
        if user_data.get("occupation") == "farmer":
            if "acre" in message_lower or "land" in message_lower or "hectare" in message_lower:
                user_data["land_ownership"] = "yes"
        
        return user_data
    
    def match_schemes(self, user_data: dict) -> list:
        """Match user to eligible schemes using Bedrock"""
        
        # Load scheme database (from S3 or local)
        schemes = self._load_schemes()
        
        prompt = f"""Given this user profile:
{json.dumps(user_data, indent=2)}

And these available schemes:
{json.dumps(schemes, indent=2)}

Return a JSON array of eligible schemes with eligibility scores (0-100).
Format: [{{"name": "scheme_name", "score": 95, "reason": "why eligible"}}]

Return only valid JSON."""

        try:
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.3
                })
            )
            
            result = json.loads(response['body'].read())
            content = result['content'][0]['text']
            
            matched_schemes = json.loads(content)
            return sorted(matched_schemes, key=lambda x: x['score'], reverse=True)
            
        except Exception as e:
            logger.error(f"Bedrock matching failed: {str(e)}")
            return self._rule_based_matching(user_data, schemes)
    
    def _rule_based_matching(self, user_data: dict, schemes: list) -> list:
        """Fallback rule-based matching"""
        matched = []
        
        for scheme in schemes:
            score = 0
            reasons = []
            
            # Check occupation
            target_occ = scheme.get("target_occupation")
            user_occ = user_data.get("occupation")
            
            if target_occ == "any":
                score += 20  # Lower score for "any" occupation
            elif user_occ == target_occ:
                score += 50  # Higher score for exact occupation match
                reasons.append("Occupation matches")
            
            # Check gender (STRICT filtering - higher priority)
            scheme_gender = scheme.get("gender", "any")
            user_gender = user_data.get("gender", "any")
            
            # CRITICAL: If scheme is gender-specific and user gender doesn't match, SKIP
            if scheme_gender != "any" and user_gender != "any":
                if user_gender != scheme_gender:
                    # Gender mismatch - skip this scheme entirely
                    continue
                else:
                    # Gender matches
                    score += 25
                    reasons.append(f"Gender-specific scheme for {user_gender}")
            elif scheme_gender == "any":
                score += 5
            elif user_gender == "any":
                # User gender unknown, but scheme is gender-specific
                # Only include if score is already high from other factors
                score += 5
            
            # Check category (SC/ST/OBC)
            scheme_category = scheme.get("category", "any")
            user_category = user_data.get("category", "General")
            
            if scheme_category == "any":
                score += 15
            elif isinstance(scheme_category, list):
                if user_category in scheme_category:
                    score += 20
                    reasons.append(f"{user_category} category eligible")
                else:
                    # Category doesn't match - skip this scheme
                    continue
            elif scheme_category == user_category:
                score += 20
                reasons.append(f"{user_category} category eligible")
            
            # Check income
            user_income = user_data.get("income", 2)
            max_income = scheme.get("max_income", 999)
            if user_income <= max_income:
                score += 10
                reasons.append("Income eligible")
            
            # Check age
            user_age = user_data.get("age", 30)
            if scheme.get("min_age", 0) <= user_age <= scheme.get("max_age", 999):
                score += 10
            else:
                # Age doesn't match - skip this scheme
                continue
            
            # Lower threshold for matching
            if score >= 40:
                matched.append({
                    "name": scheme["name"],
                    "score": score,
                    "reason": ", ".join(reasons) if reasons else "Eligible based on profile"
                })
        
        return sorted(matched, key=lambda x: x['score'], reverse=True)
    
    def generate_response(self, user_data: dict, schemes: list, language: str = "en") -> str:
        """Generate conversational response using Bedrock"""
        
        if not schemes:
            return "I couldn't find any schemes matching your profile. Can you provide more details?"
        
        prompt = f"""You are Awaaz, a helpful government scheme assistant.

User profile: {json.dumps(user_data)}
Eligible schemes: {json.dumps(schemes[:3])}  # Top 3
Language: {language}

Generate a warm, conversational response in {language} that:
1. Acknowledges the user
2. Mentions the top scheme they're eligible for
3. Briefly explains the benefit
4. Asks if they want to proceed with application

Keep it under 100 words. Be friendly and encouraging."""

        try:
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 300,
                    "temperature": 0.7
                })
            )
            
            result = json.loads(response['body'].read())
            return result['content'][0]['text']
            
        except Exception as e:
            logger.error(f"Response generation failed: {str(e)}")
            # Fallback response
            top_scheme = schemes[0]
            return f"Good news! You may be eligible for {top_scheme['name']}. Would you like to apply?"
    
    def _load_schemes(self) -> list:
        """Load schemes from SQLite database"""
        import sqlite3
        import os
        
        try:
            # Database path
            db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'schemes.db')
            
            # Connect to database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Fetch all schemes
            cursor.execute('''
                SELECT name, target_occupation, max_income, gender, min_age, max_age, category, benefit, description, application_url
                FROM schemes
            ''')
            
            schemes = []
            for row in cursor.fetchall():
                # Parse category (can be comma-separated for multiple categories)
                category = row[6]
                if category and ',' in category:
                    category = category.split(',')
                elif category and category != 'any':
                    category = [category]
                else:
                    category = 'any'
                
                schemes.append({
                    "name": row[0],
                    "target_occupation": row[1],
                    "max_income": row[2],
                    "gender": row[3],
                    "min_age": row[4],
                    "max_age": row[5],
                    "category": category,
                    "benefit": row[7],
                    "description": row[8],
                    "application_url": row[9]
                })
            
            conn.close()
            
            logger.info(f"Loaded {len(schemes)} schemes from database")
            return schemes
            
        except Exception as e:
            logger.error(f"Failed to load schemes from database: {str(e)}")
            # Fallback to hardcoded schemes if database fails
            return self._load_schemes_fallback()
    
    def _load_schemes_fallback(self) -> list:
        """Fallback: Load hardcoded schemes if database fails"""
        return [
            {
                "name": "PM Kisan",
                "target_occupation": "farmer",
                "max_income": 2,
                "gender": "any",
                "min_age": 18,
                "max_age": 999,
                "category": "any",
                "benefit": "Rs 6000 per year direct to bank account"
            },
            {
                "name": "Ayushman Bharat",
                "target_occupation": "any",
                "max_income": 5,
                "gender": "any",
                "min_age": 0,
                "max_age": 999,
                "category": "any",
                "benefit": "Free health insurance up to Rs 5 lakh"
            },
            {
                "name": "Post Matric Scholarship (SC/ST)",
                "target_occupation": "student",
                "max_income": 2.5,
                "gender": "any",
                "min_age": 16,
                "max_age": 30,
                "category": ["SC", "ST"],
                "benefit": "Scholarship for higher education"
            },
            {
                "name": "National Scholarship Portal (OBC)",
                "target_occupation": "student",
                "max_income": 3,
                "gender": "any",
                "min_age": 16,
                "max_age": 30,
                "category": ["OBC"],
                "benefit": "Merit-based scholarship for OBC students"
            },
            {
                "name": "Pradhan Mantri Matru Vandana Yojana",
                "target_occupation": "any",
                "max_income": 5,
                "gender": "female",
                "min_age": 18,
                "max_age": 45,
                "category": "any",
                "benefit": "Rs 5000 for pregnant and lactating mothers"
            },
            {
                "name": "Beti Bachao Beti Padhao",
                "target_occupation": "student",
                "max_income": 5,
                "gender": "female",
                "min_age": 0,
                "max_age": 21,
                "category": "any",
                "benefit": "Financial support for girl child education"
            }
        ]
    
    def get_all_schemes(self) -> list:
        """Return all available schemes"""
        return self._load_schemes()
