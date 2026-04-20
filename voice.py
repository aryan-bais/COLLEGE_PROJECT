import speech_recognition as sr
import streamlit as st

def speech_to_text():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening...")
            audio = r.listen(source, timeout=5)

        text = r.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "Speech service error"
    except Exception as e:
        return str(e)