# pip install streamlit
# pip install SpeechRecognition
# pip install gtts
# pip install openai
# pip install python-dotenv
# pip install streamlit-mic-recorder

import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import openai
import os
from dotenv import load_dotenv
from streamlit_mic_recorder import mic_recorder

# 환경 변수 로드
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# =========================
# Streamlit UI
# =========================

st.title("🎤 ChatGPT 음성 대화 대시보드")

st.write("마이크 버튼을 누르고 질문하세요.")

# 대화 기록
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# 대화 기록 출력
# =========================

st.subheader("💬 대화 기록")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"👤 **사용자:** {msg['content']}")
    else:
        st.markdown(f"🤖 **AI:** {msg['content']}")

# =========================
# 마이크 녹음
# =========================

audio = mic_recorder(
    start_prompt="🎙️ 녹음 시작",
    stop_prompt="⏹️ 녹음 종료",
    key="recorder"
)

# =========================
# 음성 처리
# =========================

if audio:

    audio_file = "input.wav"

    with open(audio_file, "wb") as f:
        f.write(audio["bytes"])

    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        st.write("🔎 음성 인식 중...")
        audio_data = recognizer.record(source)

    try:
        user_text = recognizer.recognize_google(audio_data, language="ko")

        st.success(f"👤 사용자: {user_text}")

        # 대화 기록 저장
        st.session_state.messages.append({
            "role": "user",
            "content": user_text
        })

        # =========================
        # LLM 호출
        # =========================

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        )

        answer = response["choices"][0]["message"]["content"]

        # AI 메시지 저장
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        st.info(f"🤖 AI 답변:\n\n{answer}")

        # =========================
        # TTS
        # =========================

        tts = gTTS(text=answer, lang="ko")

        tts_file = "answer.mp3"

        tts.save(tts_file)

        st.audio(tts_file)

    except Exception as e:
        st.error("음성 인식 실패")

