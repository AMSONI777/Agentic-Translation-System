from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 1024) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


class TranscriptionProvider(ABC):
    @abstractmethod
    def transcribe(self, audio_path: str, language: str = "auto") -> str:
        pass