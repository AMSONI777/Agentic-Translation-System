import requests
from providers.base import LLMProvider


class ProviderUnavailableError(Exception):
    pass


class CmsAIProvider(LLMProvider):
    def __init__(self, base_url: str = "http://cmsai:8000/generate/", timeout: int = 30):
        self._base_url = base_url
        self._timeout = timeout

    def generate(self, prompt: str, max_tokens: int = 1024) -> str:
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens
        }
        try:
            response = requests.post(self._base_url, json=payload, timeout=self._timeout)
            if response.status_code == 200:
                data = response.json()
                if "response" in data:
                    return data["response"]
                raise ProviderUnavailableError(f"Unexpected response format: {data}")
            raise ProviderUnavailableError(f"Request failed with status code: {response.status_code}")
        except requests.exceptions.ConnectionError:
            raise ProviderUnavailableError("CmsAI API unreachable. Are you on campus? Try switching to Groq.")
        except requests.exceptions.Timeout:
            raise ProviderUnavailableError("CmsAI API timed out. Try switching to Groq.")

    def get_name(self) -> str:
        return "CmsAI"