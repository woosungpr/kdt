# %% [markdown]
# # STT(Speech To Text)
# - 사람의 말을 문자로 바꿔주는 기술
# - 예시
#     - 유튜브 자막 자동 생성
#     - 스마트폰 음성 입력: “카카오톡 보내줘~” 말하면 자동 입력됨
#     - 콜센터 녹취 자동 기록
#     - 회의 녹음 → 회의록 자동 생성

# %% [markdown]
# ## 1) SpeechRecognition(음성인식) 패키지 설치

# %%
!pip install SpeechRecognition

# %% [markdown]
# ## 2) mp3 파일을 .wav로 변환하기
# - gTTS는 mp3 파일만 생성하지만 SpeechRecognition 라이브러리는 .wav 확장자 사운드 파일만 인식할 수 있음

# %%
!pip install pydub

# %%
!pip install gtts

# %%
from pydub import  AudioSegment

mp3_file = 'sample.mp3'
wav_file = 'sample.wav'

from gtts import gTTS

#  한글문장 사운드 파일 생성 및 저장
text = '안녕하세요 인공지능 스피커'
tts_txt = gTTS(text=text, lang='ko')
tts_txt.save(mp3_file)

sound = AudioSegment.from_mp3(mp3_file)
sound.export(wav_file, format='wav', parameters=['-ac', '1', '-ar', '16000'])
sound

# %%


# %% [markdown]
# ## 3) wav 파일로부터 STT

# %%
import speech_recognition as sr

# 음성 인식 객체 생성
recognizer = sr.Recognizer()

# 오디오 파일 로드
audio_file = 'sample.wav'

with sr.AudioFile(audio_file) as source:
    print("음성을 인식 중입니다....")
    audio_data = recognizer.record(source)

text = recognizer.recognize_google(audio_data, language='ko')
print("변환된 텍스트 : ", text)

# %% [markdown]
# ## 4) 실시간 녹음과 STT

# %%
import speech_recognition as sr
from IPython.display import display, Javascript
from base64 import b64decode
from io import BytesIO
from pydub import AudioSegment
import google.colab.output as output

# 브라우저에게 전달할 JavaScript 코드
RECORD = '''
window.sleep = time => new Promise((resolve) => setTimeout(resolve, time));

window.b2text = blob => new Promise((resolve) => {
  const reader = new FileReader();
  reader.onloadend = (e) => resolve(e.srcElement.result);
  reader.readAsDataURL(blob);
});

window.record = time => new Promise(async (resolve) => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const recorder = new MediaRecorder(stream);
  const chunks = [];

  recorder.ondataavailable = (e) => chunks.push(e.data);
  recorder.start();

  await sleep(time);

  recorder.onstop = async () => {
    const blob = new Blob(chunks);
    const text = await b2text(blob);
    resolve(text);
  };

  recorder.stop();
});

'''

# 자바스크립트 코드 실행
display(Javascript(RECORD))

# 녹음 시작
print("녹음 시작")
sound = output.eval_js('record(5000)')  # 녹음 시간 (밀리초)
print("녹음 끝")


# 녹음된 오디오 데이터를 저장
file_path = "recorded.wav"
b = b64decode(sound.split(',')[1])  # Base64로 인코딩된 오디오 데이터를 디코딩
audio = AudioSegment.from_file(BytesIO(b))  # 오디오 데이터를 AudioSegment 객체로 변환
audio.export(file_path, format="wav")

# 음성 인식 객체 생성
recognizer = sr.Recognizer()

# 오디오 파일 열고 데이터를 인식기로 읽기
with sr.AudioFile(file_path) as source:
  audio_data = recognizer.record(source)

# 한국어로 TTS
text = recognizer.recognize_google(audio_data, language="ko")
print("변환된 텍스트:", text)

# %%



