from pydantic import BaseModel
from typing import List, Optional, Literal, Dict

class Message(BaseModel):
    sender: Literal["scammer", "user"]
    text: str
    timestamp: float

class Metadata(BaseModel):
    channel: str
    language: str
    locale: str

class ChatRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[Message]
    metadata: Metadata

class ChatResponse(BaseModel):
    status: Literal["success", "completed"]
    reply: Optional[str] = None

class ExtractedIntelligence(BaseModel):
    bankAccounts: List[str] = []
    upiIds: List[str] = []
    phishingLinks: List[str] = []
    phoneNumbers: List[str] = []
    suspiciousKeywords: List[str] = []

class FinalCallbackPayload(BaseModel):
    sessionId: str
    scamDetected: bool
    totalMessagesExchanged: int
    extractedIntelligence: ExtractedIntelligence
    agentNotes: str
