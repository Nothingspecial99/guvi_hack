import json
from typing import Dict, Any, Optional
from app.models.schemas import ExtractedIntelligence

session_store: Dict[str, Dict[str, Any]] = {}

class SessionManager:
    @staticmethod
    def get_session(session_id: str) -> Dict[str, Any]:
        if session_id not in session_store:
            session_store[session_id] = {
                "scam_detected": False,
                "messages_exchanged": 0,
                "history": [],
                "extracted_intelligence": {
                    "bankAccounts": [],
                    "upiIds": [],
                    "phishingLinks": [],
                    "phoneNumbers": [],
                    "suspiciousKeywords": []
                },
                "agent_goal": "assess_intent"
            }
        return session_store[session_id]

    @staticmethod
    def update_session(session_id: str, updates: Dict[str, Any]):
        if session_id in session_store:
            session_store[session_id].update(updates)

    @staticmethod
    def add_intelligence(session_id: str, new_data: ExtractedIntelligence):
        session = session_store.get(session_id)
        if not session:
            return
            
        current = session["extracted_intelligence"]
        
        for field in new_data.model_dump():
            if field in current:
                new_items = getattr(new_data, field)
                existing_items = current[field]
                current[field] = list(set(existing_items + new_items))
        
        session_store[session_id]["extracted_intelligence"] = current
