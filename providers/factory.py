from providers.base import LLMProvider, TranscriptionProvider
from providers.cmsai import CmsAIProvider
from providers.groq_llm import GroqProvider
from providers.groq_whisper import GroqWhisperProvider


class ProviderFactory:
    @staticmethod
    def create_llm(provider_type: str, config: dict) -> LLMProvider:
        if provider_type == "cmsai":
            return CmsAIProvider(
                base_url=config.get("base_url", "http://cmsai:8000/generate/"),
                timeout=config.get("timeout", 30)
            )
        elif provider_type == "groq":
            return GroqProvider(
                api_key=config["groq_api_key"],
                model=config.get("model", "llama-3.3-70b-versatile")
            )
        else:
            raise ValueError(f"Unknown LLM provider type: {provider_type}")

    @staticmethod
    def create_transcription(config: dict) -> TranscriptionProvider:
        return GroqWhisperProvider(
            api_key=config["groq_api_key"],
            model=config.get("whisper_model", "whisper-large-v3")
        )