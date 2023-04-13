import speech_recognition as sr
#마이크로 음성 듣기
r= sr.Recognizer()
with sr.Microphone() as source:
    print('듣고있어요')
    audio =r.listen(source)

#음성 파일로 음성 불러오기(wav, aiff, flac는 가능, mp3는 불가)
r=sr.Recognizer()
with sr.AudioFile('sample.wav') as source:
     audio =r.record(source)

try:
    #영어
    #text= r.recognize_google(audio, language='en-US')
    #print(text)
    #한글
    text= r.recognize_google(audio, language='ko')
    print(text)
except sr.UnknownValueError:
    print('인식 실패')
except sr.RequestError as e:
    print('요청 실패:{0}'.format(e))