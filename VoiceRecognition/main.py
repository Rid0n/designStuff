from PIL import Image
import json, os
import pyttsx3, vosk, pyaudio, requests


tts = pyttsx3.init()
voices = tts.getProperty('voices')
tts.setProperty('voices', 'en')

for voice in voices:

    if voice.name == 'Microsoft Zira Desktop - English (UnitedStates)':
        tts.setProperty('voice', voice.id)

model = vosk.Model('model_small')

record = vosk.KaldiRecognizer(model, 16000)
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=4000)
stream.start_stream()

def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if record.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(record.Result())
            if answer['text']:
                yield answer['text']

def speak(say):
    tts.say(say)
    tts.runAndWait()

print('start')
img = ''
for text in listen():
    if text == 'new dog':
        req = requests.get('https://dog.ceo/api/breeds/image/random')
        data = req.json()
        img = data['message']
        print('Retrieved dog image URL: ' + img)
        if img:
            dogImage = Image.open(requests.get(img, stream=True).raw)
            dogBreed = img.split('/')[4]
        else:
            print('message empty!')
    elif text == 'display':
        if img:
            dogImage.show()
        else:
            speak('hhh nothing to show')
    elif text == 'resolution':
        if img:
            w, h = dogImage.size
            print('Dog resolution: ' + str(w) + "x" + str(h))
        else:
            speak('hhh no image')
    elif text == 'breed':
        if img:
            print('hhh Dog breed: ' + dogBreed)
        else:
            speak('hhh no breed to show')
    elif text == 'save':
        if img:
            dogImage.save(dogBreed + ".jpg")
            speak('Dog ' + dogBreed + ' was saved')
        else:
            speak('hhh nothing to save')
    elif text == 'exit':
        speak('hhh exiting the program')
        quit()
    else:
        speak('hhh' + text)