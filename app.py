import streamlit as st
from config import Config
from core.orchestrator import Orchestrator
from core.models import TextTranslationRequest, AudioTranslationRequest
from agents.detection import LanguageDetectionAgent
from providers.cmsai import ProviderUnavailableError

st.set_page_config(page_title="Agentic Translation System", page_icon="🌐", layout="centered")
st.title("🌐 Agentic Translation System")


@st.cache_resource
def get_orchestrator(provider_type: str) -> Orchestrator:
    return Orchestrator(provider_type=provider_type, config=Config.get_llm_config())


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Settings")
    provider_choice = st.selectbox(
        "Backend Provider",
        options=["groq", "cmsai"],
        index=0 if Config.PROVIDER == "groq" else 1,
        format_func=lambda x: "Groq (LLaMA 3)" if x == "groq" else "CmsAI (Professor API)"
    )
    st.caption(f"Default from .env: {Config.PROVIDER}")
    st.divider()
    session_id = st.text_input("Session ID", value="default")
    if st.button("Clear Memory"):
        get_orchestrator(provider_choice).clear_history(session_id)
        st.success("Memory cleared.")

language_options = LanguageDetectionAgent.get_language_options()
language_codes = list(language_options.keys())
language_names = list(language_options.values())

orchestrator = get_orchestrator(provider_choice)
st.caption(f"Active backend: **{orchestrator.get_provider_name()}**")

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["Text Translation", "Audio Translation", "History", "Real-Time"])


# ── TAB 1: TEXT TRANSLATION ───────────────────────────────────────────────────
with tab1:
    st.subheader("Text Translation")

    input_text = st.text_area("Enter text to translate", height=150)

    col1, col2 = st.columns(2)
    with col1:
        source_index = st.selectbox(
            "Source Language",
            options=range(len(language_codes)),
            format_func=lambda i: language_names[i],
            index=0,
            key="text_source"
        )
        source_lang = language_codes[source_index]

    with col2:
        target_index = st.selectbox(
            "Target Language",
            options=range(len(language_codes)),
            format_func=lambda i: language_names[i],
            index=1,
            key="text_target"
        )
        target_lang = language_codes[target_index]

    if st.button("Translate", key="text_translate_btn"):
        if not input_text.strip():
            st.warning("Please enter some text.")
        elif source_lang == target_lang and source_lang != "auto":
            st.warning("Source and target languages are the same.")
        else:
            with st.spinner("Translating..."):
                try:
                    request = TextTranslationRequest(
                        text=input_text,
                        source_lang=source_lang,
                        target_lang=target_lang,
                        session_id=session_id
                    )
                    result = orchestrator.run_text_translation(request)
                    st.success("Translation complete")
                    if result.detected_language != "unknown":
                        st.caption(f"Detected language: **{result.detected_language}**")
                    st.text_area("Translation", value=result.translated_text, height=150)

                except ProviderUnavailableError as e:
                    st.error(f"Provider error: {e}")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")


# ── TAB 2: AUDIO TRANSLATION ──────────────────────────────────────────────────
with tab2:
    st.subheader("Audio Translation")

    audio_file = st.file_uploader("Upload audio file", type=["mp3", "wav", "m4a", "webm"])

    col3, col4 = st.columns(2)
    with col3:
        audio_source_index = st.selectbox(
            "Source Language",
            options=range(len(language_codes)),
            format_func=lambda i: language_names[i],
            index=0,
            key="audio_source"
        )
        audio_source_lang = language_codes[audio_source_index]

    with col4:
        audio_target_index = st.selectbox(
            "Target Language",
            options=range(len(language_codes)),
            format_func=lambda i: language_names[i],
            index=1,
            key="audio_target"
        )
        audio_target_lang = language_codes[audio_target_index]

    if st.button("Transcribe & Translate", key="audio_translate_btn"):
        if audio_file is None:
            st.warning("Please upload an audio file.")
        else:
            with st.spinner("Transcribing and translating..."):
                suffix = "." + audio_file.name.split(".")[-1]
                tmp_path = Orchestrator.save_audio_tempfile(audio_file.read(), suffix)
                try:
                    request = AudioTranslationRequest(
                        audio_path=tmp_path,
                        source_lang=audio_source_lang,
                        target_lang=audio_target_lang,
                        session_id=session_id
                    )
                    result = orchestrator.run_audio_translation(request)
                    st.success("Done")
                    if result.detected_language != "unknown":
                        st.caption(f"Detected language: **{result.detected_language}**")

                    col5, col6 = st.columns(2)
                    with col5:
                        st.text_area("Transcription", value=result.transcription, height=150)
                    with col6:
                        st.text_area("Translation", value=result.translated_text, height=150)

                except ProviderUnavailableError as e:
                    st.error(f"Provider error: {e}")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")
                finally:
                    Orchestrator.cleanup_tempfile(tmp_path)


# ── TAB 3: HISTORY ────────────────────────────────────────────────────────────
with tab3:
    st.subheader("Conversation History")
    history = orchestrator.get_history(session_id)
    if not history:
        st.info("No history yet. Start translating to build history.")
    else:
        for entry in history:
            with st.chat_message(entry.role):
                st.write(entry.content)
                st.caption(entry.timestamp.strftime("%H:%M:%S"))
                
# ── TAB 4: REAL-TIME ──────────────────────────────────────────────────────────
with tab4:
    st.subheader("Real-Time Audio Translation")
    st.caption("Record your voice — transcription and streaming translation appear instantly.")

    col7, col8 = st.columns(2)
    with col7:
        rt_source_index = st.selectbox(
            "Source Language",
            options=range(len(language_codes)),
            format_func=lambda i: language_names[i],
            index=0,
            key="rt_source"
        )
        rt_source_lang = language_codes[rt_source_index]

    with col8:
        rt_target_index = st.selectbox(
            "Target Language",
            options=range(len(language_codes)),
            format_func=lambda i: language_names[i],
            index=1,
            key="rt_target"
        )
        rt_target_lang = language_codes[rt_target_index]

    audio_input = st.audio_input("Press the microphone to record")

    if audio_input is not None:
        with st.spinner("Transcribing..."):
            suffix = ".wav"
            tmp_path = Orchestrator.save_audio_tempfile(audio_input.read(), suffix)
            try:
                transcription, stream = orchestrator.run_realtime(
                    audio_path=tmp_path,
                    source_lang=rt_source_lang,
                    target_lang=rt_target_lang,
                    session_id=session_id
                )
                st.markdown("**Transcription:**")
                st.info(transcription)
                st.markdown("**Translation (streaming):**")
                full = ""
                placeholder = st.empty()
                for chunk in stream:
                    full += chunk
                    display = full.replace("Translation:", "\n\n**Translation:**")
                    placeholder.markdown(display)

            except ProviderUnavailableError as e:
                st.error(f"Provider error: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
            finally:
                Orchestrator.cleanup_tempfile(tmp_path)