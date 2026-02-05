import requests
from app.core.config import settings
from app.models.schemas import FinalCallbackPayload

class CallbackService:
    @staticmethod
    def send_result(payload: FinalCallbackPayload):
        try:
            print(f"Sending callback to {settings.CALLBACK_URL}")
            print(payload.model_dump_json(indent=2)) # Debug
            
            response = requests.post(
                settings.CALLBACK_URL,
                json=payload.model_dump(),
                timeout=10
            )
            response.raise_for_status()
            print("Callback sent successfully.")
        except Exception as e:
            print(f"Failed to send callback: {e}")
