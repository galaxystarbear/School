from gtts import gTTS

#영어
# text='can i help you?'
file_name='sample.mp3'
# tts_en=gTTS(text=text,lang='en')
# tts_en.save(file_name)

#한글
# text='안녕하십니까?'
# tts_ko=gTTS(text=text,lang="ko")
# tts_ko.save(file_name)



#긴문장
with open('sample.txt','r',encoding='utf8') as f:
    text =f.read()

tts_ko=gTTS(text=text,lang='ko')
tts_ko.save(file_name)



#소리재생
from playsound import playsound
playsound(file_name)