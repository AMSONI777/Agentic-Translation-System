from dataclasses import dataclass
from datetime import datetime


@dataclass
class TextTranslationRequest:
    text: str
    source_lang: str
    target_lang: str
    session_id: str = "default"


@dataclass
class AudioTranslationRequest:
    audio_path: str
    source_lang: str
    target_lang: str
    session_id: str = "default"


@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    detected_language: str = "unknown"


@dataclass
class AudioTranslationResult:
    transcription: str
    translated_text: str
    detected_language: str = "unknown"


@dataclass
class ConversationEntry:
    role: str
    content: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()