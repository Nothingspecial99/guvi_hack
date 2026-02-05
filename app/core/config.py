from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Agentic Honeypot"
    API_V1_STR: str = "/api/v1"
    
    API_KEY: str
    
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    
    # Callback
    CALLBACK_URL: str = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

    class Config:
        env_file = ".env"

settings = Settings()
