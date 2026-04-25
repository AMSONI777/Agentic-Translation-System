import tempfile
import os
from agents.streaming import StreamingTranslationAgent
from providers.factory import ProviderFactory
from agents.translation import TranslationAgent
from agents.transcription import TranscriptionAgent
from core.models import (
    TextTranslationRequest,
    AudioTranslationRequest,
    TranslationResult,
    AudioTranslationResult,
    ConversationEntry
)
from core.memory import MemoryStore, InMemoryStore


class Orchestrator:
    def __init__(self, provider_type: str, config: dict, memory: MemoryStore = None):
        llm = ProviderFactory.create_llm(provider_type, config)
        transcription_provider = ProviderFactory.create_transcription(config)

        self._translation_agent = TranslationAgent(llm)
        self._transcription_agent = TranscriptionAgent(transcription_provider)
        self._memory = memory if memory is not None else InMemoryStore()
        self._provider_name = llm.get_name()
        self._streaming_agent = StreamingTranslationAgent(
            api_key=config.get("groq_api_key", "")
        )

    def get_provider_name(self) -> str:
        return self._provider_name

    def get_history(self, session_id: str):
        return self._memory.load(session_id)

    def clear_history(self, session_id: str):
        self._memory.clear(session_id)

    def run_text_translation(self, request: TextTranslationRequest) -> TranslationResult:
        history = self._memory.load(request.session_id)

        translated_text, detected_language = self._translation_agent.translate(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            history=history
        )

        self._memory.save(request.session_id, ConversationEntry(
            role="user", content=f"Translate: {request.text}"
        ))
        self._memory.save(request.session_id, ConversationEntry(
            role="assistant", content=f"Translation: {translated_text}"
        ))

        return TranslationResult(
            original_text=request.text,
            translated_text=translated_text,
            detected_language=detected_language
        )

    def run_audio_translation(self, request: AudioTranslationRequest) -> AudioTranslationResult:
        history = self._memory.load(request.session_id)

        transcription = self._transcription_agent.transcribe(
            audio_path=request.audio_path,
            language=request.source_lang
        )

        translated_text, detected_language = self._translation_agent.translate(
            text=transcription,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            history=history
        )

        self._memory.save(request.session_id, ConversationEntry(
            role="user", content=f"Audio transcription: {transcription}"
        ))
        self._memory.save(request.session_id, ConversationEntry(
            role="assistant", content=f"Translation: {translated_text}"
        ))

        return AudioTranslationResult(
            transcription=transcription,
            translated_text=translated_text,
            detected_language=detected_language
        )
        
    def run_realtime(
        self,
        audio_path: str,
        source_lang: str,
        target_lang: str,
        session_id: str = "default"
    ):
        transcription = self._transcription_agent.transcribe(
            audio_path=audio_path,
            language=source_lang
        )
        stream = self._streaming_agent.translate_stream(
            text=transcription,
            source_lang=source_lang,
            target_lang=target_lang
        )

        # Consume stream and collect full translation for memory
        full_translation = ""
        def stream_and_store():
            nonlocal full_translation
            for chunk in stream:
                full_translation += chunk
                yield chunk
            self._memory.save(session_id, ConversationEntry(
                role="user", content=f"Real-time audio: {transcription}"
            ))
            self._memory.save(session_id, ConversationEntry(
                role="assistant", content=f"Translation: {full_translation}"
            ))

        return transcription, stream_and_store()

    @staticmethod
    def save_audio_tempfile(audio_bytes: bytes, suffix: str) -> str:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        tmp.write(audio_bytes)
        tmp.close()
        return tmp.name

    @staticmethod
    def cleanup_tempfile(path: str) -> None:
        try:
            os.remove(path)
        except OSError:
            pass