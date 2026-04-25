class LanguageDetectionAgent:
    LANGUAGES = {
        "auto": "Auto-Detect",
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
        "zh": "Chinese",
        "ja": "Japanese",
        "ko": "Korean",
        "ar": "Arabic",
        "hi": "Hindi",
        "ru": "Russian",
        "tr": "Turkish",
        "nl": "Dutch",
        "pl": "Polish",
        "ur": "Urdu"
    }

    def build_translation_prompt(self, text: str, source_lang: str, target_lang: str) -> str:
        target_name = self.LANGUAGES.get(target_lang, target_lang)

        if source_lang == "auto":
            return (
                f"Detect the language of the following text and translate it to {target_name}. "
                f"Respond with two lines only:\n"
                f"Detected: <detected language name>\n\n"
                f"Translation: <translated text>\n\n"
                f"Text: {text}"
            )
        else:
            source_name = self.LANGUAGES.get(source_lang, source_lang)
            return (
                f"Translate the following text from {source_name} to {target_name}. "
                f"Respond with the translation only, no extra text.\n\n"
                f"Text: {text}"
            )

    @classmethod
    def get_language_options(cls) -> dict:
        return cls.LANGUAGES