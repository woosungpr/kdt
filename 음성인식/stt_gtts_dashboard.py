# !pip install streamlit speechrecognition googletrans==4.0.0-rc1 gTTS pyaudio

import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import tempfile

# 번역 객체
translator = Translator()

st.title("🎤 음성 번역 대시보드")

st.write("버튼을 누르고 말하면 자동 번역됩니다.")

target_lang = st.selectbox(
    "번역 언어 선택",
    ["en", "ja", "zh-cn", "ko"]
)

if st.button("🎤 음성 번역 시작"):

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        st.write("🎙 말하세요...")
        audio = recognizer.listen(source)

    try:
        # STT (음성 → 텍스트)
        text = recognizer.recognize_google(audio, language="ko")
        st.success(f"인식된 텍스트: {text}")

        # 번역
        translated = translator.translate(text, dest=target_lang)
        translated_text = translated.text

        st.info(f"번역 결과: {translated_text}")

        # TTS (텍스트 → 음성)
        tts = gTTS(translated_text, lang=target_lang)

        # 임시 mp3 저장
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp_file.name)

        # 대시보드에서 음성 재생
        st.audio(tmp_file.name)

    except Exception as e:
        st.error("음성을 인식하지 못했습니다.")

# 실행방법 
# streamlit run stt_gtts_dashboard.py
