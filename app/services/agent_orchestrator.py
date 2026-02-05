from app.services.session_manager import SessionManager
from app.services.scam_detector import ScamDetector
from app.services.persona_agent import PersonaDrivenAgent
from app.services.intelligence_extractor import IntelligenceExtractor
from app.services.callback_service import CallbackService
from app.models.schemas import ChatResponse, ExtractedIntelligence, FinalCallbackPayload, Message
import time

class AgentOrchestrator:
    @staticmethod
    def process_message(session_id: str, message: Message, history: list) -> ChatResponse:
        session = SessionManager.get_session(session_id)
        
        # Update message history
        session_entry = {"sender": message.sender, "text": message.text, "timestamp": message.timestamp}
        session["history"].append(session_entry)
        session["messages_exchanged"] += 1
        SessionManager.update_session(session_id, {"messages_exchanged": session["messages_exchanged"]})
        
        extracted = IntelligenceExtractor.extract_from_text(message.text)
        SessionManager.add_intelligence(session_id, extracted)
        
        if not session["scam_detected"]:
            is_scam_heuristic = ScamDetector.check_heuristics(message.text)
            is_scam_llm = False
            if is_scam_heuristic:
                # Confirm with LLM if heuristic triggered? (Or just trust heuristic for speed + fallback to LLM if ambiguous)
                # Let's trust heuristic OR LLM.
                session["scam_detected"] = True
            else:
                 # Double check with LLM
                if ScamDetector.check_llm_intent(message.text, history):
                    session["scam_detected"] = True
            
            SessionManager.update_session(session_id, {"scam_detected": session["scam_detected"]})

        current_intelligence = session["extracted_intelligence"]
        has_critical_intel = (len(current_intelligence["upiIds"]) > 0 or 
                              len(current_intelligence["bankAccounts"]) > 0 or
                              len(current_intelligence["phishingLinks"]) > 0 or
                              len(current_intelligence["phoneNumbers"]) > 0)

        # Termination Criteria:
        # Scam detected AND (Enough info extracted OR Too many messages)
        # Max messages cap (e.g., 15) to prevent infinite loops
        if session["scam_detected"] and (has_critical_intel or session["messages_exchanged"] >= 15):
            
            # Send Final Callback
            payload = FinalCallbackPayload(
                sessionId=session_id,
                scamDetected=True,
                totalMessagesExchanged=session["messages_exchanged"],
                extractedIntelligence=current_intelligence,
                agentNotes="Scammer engaged successfully. Critical intelligence extracted."
            )
            CallbackService.send_result(payload)
            
            return ChatResponse(status="completed")
            
        # Generate Reply (If Scam Detected)
        if session["scam_detected"]:
            reply_text = PersonaDrivenAgent.generate_reply(session["history"])
            
            agent_msg = {"sender": "user", "text": reply_text, "timestamp": time.time()} # Agent is "user" to the scammer logic? 
            
            session["history"].append(agent_msg)
            return ChatResponse(status="success", reply=reply_text)
        
        else:
            reply_text = "Who is this? I think you have the wrong number."
            agent_msg = {"sender": "user", "text": reply_text, "timestamp": time.time()}
            session["history"].append(agent_msg)
            
            return ChatResponse(status="success", reply=reply_text)
