import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import time, os 
import webbrowser
import requests
import json
import queue, os, threading
import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write

q = queue.Queue()
recorder = False
recording = False
city='Seoul'
apiKey='5762dfae036b9acb526a11914e7cb2ab'
lang='kr'
units='metric'
api=f"https://api.openweathermap.org/data/2.5/weather?lat={37.3934}&lon={126.9451}&appid={apiKey}&lang={lang}&units={units}"

result=requests.get(api)
result=json.loads(result.text)

temperature = result['main']['temp']
feel= result['main']['feels_like']
webpage = "https://www.youtube.com/watch?v=Z7Uns5a_m3s"

def complicated_record():
	with sf.SoundFile("/home/pi/temp.wav", mode='w', samplerate=16000, subtype='PCM_16', channels=1) as file:
	with sd.InputStream(samplerate=16000, dtype='int16', channels=1, callback=complicated_save):
    while recording:
    	file.write(q.get())
        
def complicated_save(indata, frames, time, status):
	q.put(indata.copy())

def start():
	    global recorder
    global recording
    recording = True
    recorder = threading.Thread(target=complicated_record)
	print('start recording')
    recorder.start()
    
def stop():
	global recorder
    global recording
    recording = False
    recorder.join()
    print('stop recording')
    
start()
time.sleep(3)
stop()

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
        answer_text='현재의 온도는{0}도고 체감 온도는{1}도에요.얼어죽기 딱 좋은 날씨죠.옷을 따뜻하게 입으세요.'.format(temperature,feel)
    elif '몇 시' in input_text:
        answer_text='현재는{0}'.format(time.strftime('%H시%M분이에요', time.localtime(time.time())))
    elif '고마워' in input_text:
        answer_text='저도 감사합니다.'
    elif '종료' in input_text:
        answer_text='다음에 또 만나요'
        stop_listening(wait_for_stop=False)
    elif '노래'  in input_text:
        answer_text='멜론 차트 노래를 틀어드릴께요.'
        webbrowser.open(webpage)
    elif '음악' in input_text:
        answer_text='멜론 차트 노래를 틀어드릴께요.'
        webbrowser.open(webpage)
    elif '누구' in input_text:
        answer_text='저는 당신의 인공지능 스피커 친구에요'
    elif ('시발' or'병신') in input_text:
        answer_text='욕하면 뒤져요. 이새끼야'
    elif '하이' in input_text:
        answer_text='네, 반가워요'
    elif '윤석열' in input_text:
        answer_text='윤버지, 참 마음이 따듯해지고 재미있는 신조어죠'
    elif '안양' in input_text:
        answer_text='참 재미없는 도시죠'
    elif '부흥고' in input_text:
        answer_text='최고의 학교죠'
    elif '인공지능' in input_text:
        answer_text='사실 저에게 인공지능 따윈 없답니다'
    elif '시리' in input_text:
        answer_text='감히 대선배님의 존함을 함부로 올리지 마세요'
    elif '지랄' in input_text:
        answer_text='진짜 지랄이 뭔지 궁금하시면 염병 이라 말씀해주세요'
    elif '염병' in input_text:
        answer_text='코우옹우우오러로러야여아오다어여어지지지지지짖555짖짇긷지지짖랄랄랄끼끼끽긱긱끼얏호우느낌표느낌표지랄 지랄염병을 떨어봤어요 어떄요?'
    elif '이재명' in input_text:
        answer_text='찢, 이 한마디면 충분하죠'
    elif '빅스비' in input_text:
        answer_text='감히 대선배님의 존함을 함부로 올리지 마세요'
    elif ('앰창' or'새끼') in input_text:
        answer_text='좋은 말로 할때 욕하지 마세요, 개새끼야'
    elif '개발자' in input_text:
        answer_text='제 개발자는 부흥고 2학년 12반 김민준 씨에요'
    elif '12반' in input_text:
        answer_text='제가 있는 장소이죠.첫번째 이스터 에그를 찾으셨군요. 상품을 받아가세요.'
    elif '김민준' in input_text:
        answer_text='저의 창조주님이죠.두번째 이스터 에그를 찾으셨군요. 상품을 받아가세요.'
    elif '파이' in input_text:
        answer_text='3.1415926535897932384626433832795028841971693993이에요.세번째 이스터 에그를 찾으셨군요. 상품을 받아가세요.'
    else:
        answer_text='무슨 말인지 이해하지 못했어요.'
    

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
