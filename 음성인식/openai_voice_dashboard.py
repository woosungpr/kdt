# pip install streamlit
# pip install SpeechRecognition
# pip install gtts
# pip install openai
# pip install google-generativeai
# pip install SpeechRecognition
# pip install python-dotenv
# pip install streamlit-mic-recorder
# pip install pydub

import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import openai
import os
from dotenv import load_dotenv
from streamlit_mic_recorder import mic_recorder
from pydub import AudioSegment

load_dotenv()

# OpenAI API KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("🎤 AI 음성 비서 대시보드")
st.write("마이크 버튼을 눌러 질문하면 AI가 답하고 음성으로 읽어줍니다.")

# =============================
# 마이크 녹음
# =============================

audio = mic_recorder(
    start_prompt="🎙️ 녹음 시작",
    stop_prompt="⏹️ 녹음 종료",
    key="recorder"
)

if audio:

    st.success("녹음 완료")

    # =============================
    # 1️⃣ webm 파일 저장
    # =============================

    temp_audio = "temp_audio.webm"

    with open(temp_audio, "wb") as f:
        f.write(audio["bytes"])

    # =============================
    # 2️⃣ webm → wav 변환
    # =============================

    audio_path = "input.wav"

    sound = AudioSegment.from_file(temp_audio)
    sound.export(audio_path, format="wav")

    # =============================
    # 3️⃣ STT
    # =============================

    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        st.write("🔎 음성을 인식 중입니다...")
        audio_data = recognizer.record(source)

    try:

        user_text = recognizer.recognize_google(audio_data, language="ko")

        st.success(f"👤 사용자 질문: {user_text}")

        # =============================
        # 4️⃣ LLM 질문
        # =============================

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 친절한 AI 비서입니다."},
                {"role": "user", "content": user_text}
            ]
        )

        answer = response["choices"][0]["message"]["content"]

        # =============================
        # 5️⃣ TEXT 출력
        # =============================

        st.info(f"🤖 AI 답변: {answer}")

        # =============================
        # 6️⃣ TTS
        # =============================

        tts = gTTS(text=answer, lang="ko")

        tts_file = "answer.mp3"
        tts.save(tts_file)

        # =============================
        # 7️⃣ 음성 출력
        # =============================

        st.audio(tts_file)

    except Exception as e:
        st.error(f"음성 인식 실패: {e}")

# 실행방법
# streamlit run openai_voice_dashboard.py