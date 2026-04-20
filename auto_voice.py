import speech_recognition as sr

def auto_listen(seconds=5):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, phrase_time_limit=seconds)

    try:
        text = r.recognize_google(audio)
        return text
    except:
        return ""