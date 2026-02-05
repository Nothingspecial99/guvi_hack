import re
from typing import List, Dict
from app.models.schemas import ExtractedIntelligence

class IntelligenceExtractor:
    @staticmethod
    def extract_from_text(text: str) -> ExtractedIntelligence:
        intelligence = ExtractedIntelligence()
        
        # Regex Patterns
        
        # UPI ID: alphanumeric@bank or phone@bank
        upi_pattern = r"[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}"
        intelligence.upiIds = re.findall(upi_pattern, text)
        
        # Indian Phone Numbers: +91 followed by 10 digits or just 10 digits starting with 6-9
        phone_pattern = r"(?:\+91[\-\s]?)?[6-9]\d{9}"
        intelligence.phoneNumbers = re.findall(phone_pattern, text)
        
        # URLs
        url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
        intelligence.phishingLinks = re.findall(url_pattern, text)
        
        # Bank Account Numbers
        acc_pattern = r"\b\d{9,18}\b" 
        
        # Suspicious Keywords
        suspicious_list = ["urgent", "lottery", "winner", "kyc", "block", "suspend", "expire", "refund"]
        found_keywords = []
        lower_text = text.lower()
        for word in suspicious_list:
            if word in lower_text:
                found_keywords.append(word)
        intelligence.suspiciousKeywords = found_keywords
        
        return intelligence
