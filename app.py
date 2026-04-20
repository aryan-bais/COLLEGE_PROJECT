import streamlit as st
from streamlit_autorefresh import st_autorefresh
from nodes import interview_node
from my_parser import extract_text
from camera import start_camera
from tts import speak
from auto_voice import auto_listen
import time

st.set_page_config(page_title="AI Auto Interview", layout="centered")

st.title("🤖 Fully Automatic AI Interview")

uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf"])

if uploaded_file:
    text = extract_text(uploaded_file)

    company = st.selectbox("🏢 Company", ["General", "Google", "Amazon", "TCS"])

    # 🔁 Auto refresh every 3 sec
    st_autorefresh(interval=3000, key="refresh")

    # 🧠 SESSION STATE INIT
    if "step" not in st.session_state:
        st.session_state.step = "ask"
        st.session_state.question = ""
        st.session_state.answer = ""
        st.session_state.feedback = {}
        st.session_state.q_count = 0

    # 📷 CAMERA ALWAYS ON
    st.subheader("📷 Live Camera")
    start_camera()

    # 🧠 STEP 1: ASK QUESTION
    if st.session_state.step == "ask":
        q = interview_node({
            "text": text,
            "company": company,
            "answer": ""
        })

        st.session_state.question = q.get("question", "Tell me about yourself.")
        st.session_state.step = "speak"

    # 🔊 STEP 2: SPEAK
    elif st.session_state.step == "speak":
        st.subheader("🧠 Question")
        st.write(st.session_state.question)

        speak(st.session_state.question)

        time.sleep(2)
        st.session_state.step = "listen"

    # 🎤 STEP 3: LISTEN
    elif st.session_state.step == "listen":
        st.info("🎤 Listening... Speak now")

        answer = auto_listen(6)
        st.session_state.answer = answer

        st.write("You said:", answer)

        st.session_state.step = "evaluate"

    # 📊 STEP 4: EVALUATE
    elif st.session_state.step == "evaluate":
        res = interview_node({
            "text": text,
            "company": company,
            "question": st.session_state.question,
            "answer": st.session_state.answer
        })

        st.session_state.feedback = res
        st.session_state.step = "feedback"

    # 📊 STEP 5: SHOW FEEDBACK
    elif st.session_state.step == "feedback":
        st.subheader("📊 Feedback")
        st.write("Score:", st.session_state.feedback.get("score", "0"))
        st.write("Feedback:", st.session_state.feedback.get("feedback", ""))
        st.write("Better Answer:", st.session_state.feedback.get("better_answer", ""))

        st.session_state.q_count += 1

        time.sleep(3)

        # 🎯 STOP AFTER 5 QUESTIONS
        if st.session_state.q_count >= 5:
            st.success("✅ Interview Completed")
        else:
            st.session_state.step = "ask"
            
       