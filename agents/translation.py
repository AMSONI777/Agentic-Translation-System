from typing import List
from providers.base import LLMProvider
from agents.detection import LanguageDetectionAgent
from core.models import ConversationEntry


class TranslationAgent:
    def __init__(self, llm: LLMProvider):
        self._llm = llm
        self._detection_agent = LanguageDetectionAgent()

    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        history: List[ConversationEntry] = None
    ) -> tuple[str, str]:
        history_block = self._build_history_block(history)
        prompt = self._detection_agent.build_translation_prompt(text, source_lang, target_lang)

        if history_block:
            prompt = f"{history_block}\n\n{prompt}"

        response = self._llm.generate(prompt)

        if source_lang == "auto":
            return self._parse_auto_response(response)
        else:
            return response.strip(), "unknown"

    def _build_history_block(self, history: List[ConversationEntry]) -> str:
        if not history:
            return ""
        lines = ["Previous translations for context:"]
        for entry in history:
            lines.append(f"{entry.role}: {entry.content}")
        return "\n".join(lines)

    def _parse_auto_response(self, response: str) -> tuple[str, str]:
        detected = "unknown"
        translation = response.strip()

        lines = response.strip().splitlines()
        for line in lines:
            if line.lower().startswith("detected:"):
                detected = line.split(":", 1)[1].strip()
            elif line.lower().startswith("translation:"):
                translation = line.split(":", 1)[1].strip()

        return translation, detected