# %%
!pip install click==8.1.8

# %%
!pip install gTTS

# %%
!pip install translate

# %% [markdown]
# - translate 패키지는 내부적으로 무료 번역 엔진 중 하나를 사용하여 번역을 수행함
#   - Google Translate API
#   - Microsoft Bing Translator API
#   - Yandex Translator API

# %% [markdown]
# 2) TEXT 번역하기

# %%
from translate import Translator

text = '안녕하세요. 제 이름은 인공지능 스피커입니다.'

# translator 객체 생성
translator= Translator(to_lang="ja", from_lang='ko')
# translation = translator.translate("Hello World!")
# print(translation)

# %%
# 번역 실행
result = translator.translate(text) # 한국어를 영어로 번역

print('원본 텍스트 :', text)
print('번역된 텍스트:',result)

# %% [markdown]
# 

# %%
from gtts import gTTS
#  텍스트 문장 사운드 파일 생성 및 저장
file_name = 'japanese1.mp3'
tts_en = gTTS(text=result, lang='ja')
tts_en.save(file_name)

# %%
#  코랩 환경에서 .mp3 파일 재생
from IPython.display import Audio
sound = Audio(file_name, autoplay=True)
sound


