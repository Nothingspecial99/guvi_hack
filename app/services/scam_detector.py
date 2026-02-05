from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

class ScamDetector:
    @staticmethod
    def check_heuristics(message_text: str) -> bool:
        keywords = ["lottery", "winner", "kyc", "block", "expired", "urgent", "otp", "cvv", "card number"]
        lower_text = message_text.lower()
        if any(w in lower_text for w in keywords):
            return True
        return False

    @staticmethod
    def check_llm_intent(message_text: str, history: list) -> bool:
        prompt = f"""
        Analyze the following conversation and determine if the 'user' (scammer) is demonstrating SCAM INTENT.
        
        Scam Intent includes:
        - Phishing (asking for credentials, OTPs)
        - Financial fraud (lottery, fake refunds, KYC updates)
        - Urgency/Threats
        
        Return ONLY the word "SCAM" if it is a scam, or "SAFE" if it is not.
        
        Last Message: "{message_text}"
        """
        
        try:
            completion = client.chat.completions.create(
                model=settings.GROQ_MODEL, 
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=10
            )
            result = completion.choices[0].message.content.strip().upper()
            return "SCAM" in result
        except Exception as e:
            print(f"Scam detection error: {e}")
            return False
