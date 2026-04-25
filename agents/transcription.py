from providers.base import TranscriptionProvider


class TranscriptionAgent:
    def __init__(self, provider: TranscriptionProvider):
        self._provider = provider

    def transcribe(self, audio_path: str, language: str = "auto") -> str:
        return self._provider.transcribe(audio_path, language)