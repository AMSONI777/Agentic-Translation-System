from groq import Groq
from providers.base import TranscriptionProvider
from providers.cmsai import ProviderUnavailableError


class GroqWhisperProvider(TranscriptionProvider):
    def __init__(self, api_key: str, model: str = "whisper-large-v3"):
        self._client = Groq(api_key=api_key)
        self._model = model

    def transcribe(self, audio_path: str, language: str = "auto") -> str:
        try:
            with open(audio_path, "rb") as audio_file:
                response = self._client.audio.transcriptions.create(
                    model=self._model,
                    file=audio_file,
                    language=None if language == "auto" else language
                )
            return response.text
        except FileNotFoundError:
            raise ProviderUnavailableError(f"Audio file not found: {audio_path}")
        except Exception as e:
            raise ProviderUnavailableError(f"Groq Whisper error: {str(e)}")