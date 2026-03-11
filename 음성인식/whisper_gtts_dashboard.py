#! pip install streamlit openai-whisper googletrans==4.0.0-rc1 gTTS sounddevice soundfile numpy
#! pip install ffmpeg-python

import streamlit as st
import whisper
import sounddevice as sd
import numpy as np
import soundfile as sf
import tempfile
from googletrans import Translator
from gtts import gTTS

st.title("🎤 실시간 음성 번역 대시보드")

# Whisper 모델 로드
# model = whisper.load_model("base")
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

translator = Translator()

# 번역 언어 선택
target_lang = st.selectbox(
    "번역 언어 선택",
    ["en", "ja", "zh-cn", "ko"]
)

# 녹음 함수
def record_audio(duration=5, fs=16000):
    st.write("🎙 말하세요...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    return audio, fs

if st.button("🎤 음성 번역 시작"):

    audio, fs = record_audio()

    # 임시 wav 저장
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(tmp_file.name, audio, fs)

    # Whisper STT
    result = model.transcribe(tmp_file.name)
    text = result["text"]

    st.success(f"인식된 텍스트: {text}")

    # 번역
    translated = translator.translate(text, dest=target_lang)

    st.info(f"번역 결과: {translated.text}")

    # TTS 생성
    tts = gTTS(translated.text, lang=target_lang)

    tts_file = "tts_output.mp3"
    tts.save(tts_file)

    # 음성 출력
    st.audio(tts_file)

# 실행방법
# streamlit run whisper_gtts_dashboard.py
