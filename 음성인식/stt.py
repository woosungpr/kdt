import speech_recognition as sr

# 음성인식 객체 생성
recognizer = sr.Recognizer()
# 오디오 파일 로드
audio_file = 'vad_recorded.wav'

with sr.AudioFile(audio_file) as source:
  print("음성을 인식 중입니다....")
  audio_data = recognizer.record(source)

text = recognizer.recognize_google(audio_data, language='ko')
print("변환된 텍스트:",text)