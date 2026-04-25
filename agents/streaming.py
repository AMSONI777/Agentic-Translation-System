from typing import Iterator
from groq import Groq
from agents.detection import LanguageDetectionAgent


class StreamingTranslationAgent:
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self._client = Groq(api_key=api_key)
        self._model = model
        self._detection_agent = LanguageDetectionAgent()

    def translate_stream(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> Iterator[str]:
        prompt = self._detection_agent.build_translation_prompt(
            text, source_lang, target_lang
        )
        stream = self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            stream=True
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta