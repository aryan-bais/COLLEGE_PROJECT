import speech_recognition as sr

def auto_listen(seconds=5):
    r = sr.Recognizer()

    try:
        mic = sr.Microphone()

        with mic as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, phrase_time_limit=seconds)

        try:
            return r.recognize_google(audio)
        except:
            return ""

    except Exception as e:
        print("MIC ERROR:", e)
        return ""