import pyttsx3 as t2s
import speech_recognition as sr
engine = t2s.init('sapi5')
voices = engine.getProperty('voices')
voice = engine.setProperty('voice',voices[0].id)
engine.setProperty('rate',170)


def listen():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Listening...")
		r.adjust_for_ambient_noise(source)
		audio = r.listen(source)
	try:
		print('Recognizing')
		qn = r.recognize_google(audio)
	except Exception as e:
		print('Network Not Connected / may be slow connection')
		return ""
	return qn


def speak(audio):
	engine.say(audio)
	engine.runAndWait() 