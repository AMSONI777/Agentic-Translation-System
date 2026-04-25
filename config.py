import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    PROVIDER = os.getenv("PROVIDER", "groq")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    CMSAI_BASE_URL = os.getenv("CMSAI_BASE_URL", "http://cmsai:8000/generate/")
    CMSAI_TIMEOUT = int(os.getenv("CMSAI_TIMEOUT", "30"))

    @classmethod
    def get_llm_config(cls) -> dict:
        return {
            "groq_api_key": cls.GROQ_API_KEY,
            "base_url": cls.CMSAI_BASE_URL,
            "timeout": cls.CMSAI_TIMEOUT
        }

    @classmethod
    def get_transcription_config(cls) -> dict:
        return {
            "groq_api_key": cls.GROQ_API_KEY
        }