from playsound import playsound 
from gtts import gTTS
import speech_recognition as sr 
import os

def speak(string, lang='tr'):
    tts = gTTS(text=string, lang=lang, slow=False)
    file = 'answer.mp3'
    tts.save(file)
    playsound(file)
    os.remove(file)

r = sr.Recognizer()
def record(ask = False):
    print('hi')
    with sr.Microphone() as source:
        audio = r.listen(source)
        voice = ""
        try:
            voice = r.recognize_google(audio, language='tr-TR')
            print(voice)
        except: pass
        return voice