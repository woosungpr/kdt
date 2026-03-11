# %% [markdown]
# # TTS(Text To Speech)
# - 글자를 소리(음성)로 바꾸는 기술
# - 예시
#     - 네비게이션: "500m 앞 우회전입니다~" 라고 말해줌
#     - 스마트 스피커: "오늘 날씨는 맑고 기온은 25도입니다."
#     - 전자책 앱: 책 내용을 음성으로 읽어줌

# %% [markdown]
# - 강의 자료 링크 : https://www.notion.so/01-15e117802625814ba504e4a45f41d9a4?source=copy_link

# %% [markdown]
# ## 1) gTTS 패키지 설치
# - Google Text-to-Speech API를 사용하여 텍스트를 자연스러운 음성으로 변환하는 파이썬 라이브러리
# - 구글 번역기에서 체험 가능 : https://translate.google.co.kr/

# %%

!pip install click==8.2.1


# %%
!pip install gtts --no-deps

# %%
!pip install gTTS

# %% [markdown]
# ## 2) 한글 문장 사운드 파일 생성 및 저장
# - gTTS 클래스는 텍스트를 음성으로 변환하는 주요 클래스이다.

# %%
from gtts import gTTS

# %%
#  한글문장 사운드 파일 생성 및 저장
text = '안녕하세요 인공지능 스피커'
file_name = 'sample.mp3'
tts_en = gTTS(text=text, lang='ko')
tts_en.save(file_name)


# %% [markdown]
# 3) 코랩 환경에서 .mp3 파일 재생

# %%
#  코랩 환경에서 .mp3 파일 재생
from IPython.display import Audio
sound = Audio(file_name, autoplay=True)


# %%
from IPython.display import Audio, display
sound = display(Audio(file_name, autoplay=True))

# %% [markdown]
# ## 4) 한글 문장 TTS

# %% [markdown]
# - gTTS 주요 옵션
# 
# | 속성         | 설명                                     | 타입  | 기본값    |
# |--------------|------------------------------------------|--------|------------|
# | `text`       | 음성으로 변환할 텍스트                  | `str` | **필수**   |
# | `lang`       | 언어 코드 (예: `"ko"`, `"en"`, `"ja"`, `"fr"`) | `str` | `"en"`     |
# | `slow`       | 음성 속도 (느리게 출력 여부)             | `bool` | `False`    |
# | `lang_check` | 언어 코드 유효성 확인 여부               | `bool` | `True`     |
# | `tld`        | Google TTS 서버의 Top-Level Domain<br>(글로벌: `com`, 한국: `co.kr`) | `str` | `"com"`     |
# 

# %% [markdown]
# 1) SpeechRecongintion(음성인식) 패키지 설치

# %%
!pip install SpeechRecognition

# %% [markdown]
# 2) mp3 파일을 .wav 로 변환하기

# %%
!pip install pydub

# %%
from pydub import AudioSegment

mp3_file = 'sample.mp3'
wav_file = 'sample.wav'

sound = AudioSegment.from_mp3(mp3_file)
sound.export(wav_file, format='wav', parameters=['-ac','1','-ar','16000'])

# %%
import speech_recognition as sr

# 음성인식 객체 생성
recognizer = sr.Recognizer()
# 오디오 파일 로드
audio_file = 'sample.wav'

with sr.AudioFile(audio_file) as source:
  print("음성을 인식 중입니다....")
  audio_data = recognizer.record(source)

text = recognizer.recognize_google(audio_data, language='ko')
print("변환된 텍스트:",text)

# %% [markdown]
# ## 5) 텍스트 파일로부터 TTS

# %%
sample_text = """
간장공장 공장장은 강 공장장이고
된장공장 공장장은 장 공장장이다.
내가 그린 기린 그림은 잘 그린 기린 그림이고
나는 그린 기린을 보는 것이다.
"""

# sample3.txt 라는 이름으로 저장
with open('sample3.txt', 'w') as f:
  f.write(sample_text)

# %%
# 텍스트
with open('sample3.txt', 'r') as f:
  text = f.read()
tts = gTTS(text=text, lang='ko')
tts.save('sample3.mp3')

# %%
file_name = 'sample3.mp3'
from IPython.display import Audio
sound = Audio(file_name, autoplay=True)
sound
# from IPython.display import Audio, display
# sound = display(Audio(file_name, autoplay=True))
# sound = AudioSegment.from_mp3(mp3_file)
# sound.export(wav_file, format='wav', parameters=['-ac','1','-ar','16000'])

# %%


# %%
from pydub import AudioSegment

mp3_file = 'sample3.mp3'
wav_file = 'sample3.wav'

sound = AudioSegment.from_mp3(mp3_file)
sound.export(wav_file, format='wav', parameters=['-ac','1','-ar','16000'])

# %%
import speech_recognition as sr
# 음성인식 객체 생성
recognizer = sr.Recognizer()
# 오디오 파일 로드
audio_file = 'sample3.wav'

with sr.AudioFile(audio_file) as source:
  print("음성을 인식 중입니다....")
  audio_data = recognizer.record(source)

text = recognizer.recognize_google(audio_data, language='ko')
print("변환된 텍스트:",text)

# %% [markdown]
# 4) 실시간 녹음과 STTS

# %%
!pip install SpeechRecognition
!apt-get install ffmpeg
!pip install pydub


# %%
import speech_recognition as sr
from IPython.display import display, Javascript
from base64 import b64decode
from io import BytesIO
from pydub import AudioSegment
from google.colab import output
# from types import new_class


# %% [markdown]
# 

# %%
# 브라우저에게 전달할 Javascript 코드
# RECORD = '''
# window.sleep = time => new Promise((resolve) => setTimeout(resolve, time));

# window.b2text = blob => new Promise(async (resolve, reject) => {
#   const reader = new FileReader();
#   reader.onloadend = (e) => resolve(b64)
#   reader.readAsDataURL(blob);
# });

# window.record = time => new Promise(async (resolve) => {
#     const stream = await navigator.mediaDevices.getUserMedia({audio: true});
#     const recorder = new MediaRecorder(stream);
#     const chunks = [];
#     recorder.ondataavailable = e => chunks.push(e.data);
#     recorder.start();

#     await sleep(time);

#     recorder.onstop = async () => {
#       const blob = new Blob(chunks);
#       const text = await b2text(blob);
#       resolve(text);
#     };
# });
# '''

# %%
RECORD = """
window.record = async function(time) {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const recorder = new MediaRecorder(stream);
  const chunks = [];

  recorder.ondataavailable = e => chunks.push(e.data);
  recorder.start();

  await new Promise(resolve => setTimeout(resolve, time));

  recorder.stop();

  return await new Promise(resolve => {
    recorder.onstop = async () => {
      const blob = new Blob(chunks);
      const reader = new FileReader();
      reader.readAsDataURL(blob);
      reader.onloadend = () => resolve(reader.result);
    };
  });
}
"""

# %% [markdown]
# # To activate this environment, use
# #
# #     $ conda activate kdt0310
# #
# # To deactivate an active environment, use
# #
# #     $ conda deactivate

# %%
# 자바스크립트 코드 실행
# display(Javascript(filename='record.js'))
display(Javascript(RECORD))
# 녹음시작
print("녹음시작")
sound = output.eval_js('record(5000)') # 녹음 시간(밀리초)
print("녹음 끝")

b = b64decode(sound.split(',')[1])
audio = AudioSegment.from_file(BytesIO(b))

# 녹음된 오디오 데이터를 저장
file_path = "recorded_audio.wav"
b = b64decode(sound.split(',')[1]) # Base64를 인코딩된 오디오 데이터를 디코딩
audio.export(file_path, format="wav")

# 음성 인식 객체 생성
recognizer = sr.Recognizer()

# 오디오 파일 열고 데이터를 인식기로 읽기
with sr.AudioFile(file_path) as source:
  audio_data = recognizer.record(source)

# 한국어로 TTS
text = recognizer.recognize_google(audio_data, language='ko')
print("변환된 텍스트:",text)


# %%
# 전체 수정된 핵심 코드
# display(Javascript(RECORD))

# print("녹음시작")
# sound = output.eval_js('record(5000)')
# print("녹음 끝")

# b = b64decode(sound.split(',')[1])

# audio = AudioSegment.from_file(BytesIO(b))

# file_path = "recorded_audio.wav"
# audio.export(file_path, format="wav")


