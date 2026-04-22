import pyttsx3
import pythoncom

def speak(text):
    try:
        pythoncom.CoInitialize()  # ✅ FIX

        engine = pyttsx3.init()
        engine.setProperty('rate', 170)
        engine.say(text)
        engine.runAndWait()

        pythoncom.CoUninitialize()  # ✅ CLEANUP

    except Exception as e:
        print("TTS ERROR:", e)