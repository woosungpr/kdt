# %% [markdown]
# # Translate(번역)
# 

# %% [markdown]
# ## 1) translate 패키지 설치
# - translate 패키지는 내부적으로 **무료 번역 엔진** 중 하나를 사용하여 번역을 수행함
#     - Google Translate API
#     - Microsoft Bing Translator API
#     - Yandex Translator

# %%
!pip install translate

# %% [markdown]
# ## 2) text 번역하기
# - translator은 translate **패키지**의 핵심 클래스이다. 번역하려는 언어를 설정하고 번역을 수행한다.
# 
#     - to_lang: 번역할 목표 언어 설정
#     - from_lang: 원본 텍스트의 언어 설정
#     - translate(): 번역하려는 텍스트를 입력받아 지정된 언어로 번역된 결과 반환

# %%
from translate import  Translator

text = '안녕하세요. 제 이름은 인공지능 스피커입니다.'

# Translator 객체 생성
translator = Translator(to_lang='ja', from_lang='ko')

# %%
# 번역 실행
result = translator.translate(text) # 한국어를 영어로 번역

print('원본 텍스트 :', text)
print("번역된 텍스트 :", result)


