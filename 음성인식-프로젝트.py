import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import time, os 
import webbrowser

webpage = "https://www.youtube.com/watch?v=Z7Uns5a_m3s"


#음성인식(듣기,STT)
def listen(recognizer, audio):
    try:
        text=recognizer.recognize_google(audio,language ='ko' )
        print('[사용자]'+text)
        answer(text)
    except sr.UnknownValueError:
        print('인식 실패')
    except sr.RequestError as e:
        print('요청 실패:{0}'.format(e))


#대답(TTS)
def answer(input_text):
    answer_text = ''
    if '안녕' in input_text:
        answer_text="안녕하세요"
    elif '날씨' in input_text:
        answer_text='오늘의 날씨는 좋아요'
    elif '몇 시' in input_text:
        answer_text='현재는{0}'.format(time.strftime('현재는 %H시%M분이에요', time.localtime(time.time())))
    elif '고마워' in input_text:
        answer_text='저도 감사합니다.'
    elif '종료' in input_text:
        answer_text='다음에 또 만나요'
        stop_listening(wait_for_stop=False)
    elif '노래'  in input_text:
        answer_text='멜론 차트 노래를 틀어드릴께요.'
        webbrowser.open(webpage)
    elif  '음악' in input_text:
        answer_text='멜론 차트 노래를 틀어드릴께요.'
        webbrowser.open(webpage)
    elif '누구' in input_text:
        answer_text='저는 당신의 인공지능 스피커 친구에요'
    elif ('시발' or'병신') in input_text:
        answer_text='욕하면 뒤져요. 이새끼야'
    else:
        answer_text='다시 한번 말씀해주세요.'

    speak(answer_text)

#소리내어 읽기(TTS)
def speak(text):
    print('[인공지능]'+text)
    file_name='voice.mp3'
    tts=gTTS(text=text,lang='ko')
    tts.save(file_name)
    playsound(file_name)
    if os.path.exists(file_name):
        os.remove(file_name)


r = sr.Recognizer()
m= sr.Microphone()
speak('무엇을 도와드릴까요?')
stop_listening = r.listen_in_background(m,listen)
while True:
    time.sleep(0.1)
