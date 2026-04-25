from groq import Groq
from providers.base import LLMProvider
from providers.cmsai import ProviderUnavailableError


class GroqProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self._client = Groq(api_key=api_key)
        self._model = model

    def generate(self, prompt: str, max_tokens: int = 1024) -> str:
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise ProviderUnavailableError(f"Groq API error: {str(e)}")

    def get_name(self) -> str:
        return "Groq (LLaMA 3)"