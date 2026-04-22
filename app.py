import streamlit as st
from graph import interview_node
from my_parser import extract_text
from camera import start_camera
from auto_voice import auto_listen
import streamlit as st

# 🔊 Browser TTS (NO CRASH)
def speak(text):
    st.audio(
        f"https://api.streamelements.com/kappa/v2/speech?voice=Brian&text={text}"
    )

st.set_page_config(page_title="AI Interviewer", layout="centered")

st.title("🤖 AI Interview System")

uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf"])

# =========================
# SESSION INIT
# =========================
if "step" not in st.session_state:
    st.session_state.step = "upload"

if "spoken" not in st.session_state:
    st.session_state.spoken = False

if "listening_done" not in st.session_state:
    st.session_state.listening_done = False

if "answer" not in st.session_state:
    st.session_state.answer = ""

if "question" not in st.session_state:
    st.session_state.question = None

# =========================
# STEP 1: ANALYZE
# =========================
if uploaded_file and st.session_state.step == "upload":
    text = extract_text(uploaded_file)

    result = interview_node({
        "text": text,
        "mode": "analyze"
    })

    st.write("DEBUG:", result)

    st.session_state.skills = result.get("skills", "Not detected")
    st.session_state.domain = result.get("domain", "General")

    st.session_state.step = "domain_select"

# =========================
# STEP 2: DOMAIN SELECT
# =========================
if st.session_state.step == "domain_select":
    st.subheader("🧠 Extracted Info")
    st.write("Skills:", st.session_state.skills)
    st.write("Detected Domain:", st.session_state.domain)

    st.subheader("🎯 Choose Domain")

    domains = ["Frontend", "Backend", "DevOps", "AI/ML"]

    for d in domains:
        if st.button(d):
            st.session_state.selected_domain = d
            st.session_state.step = "interview"

# =========================
# STEP 3: INTERVIEW
# =========================
if st.session_state.step == "interview":
    st.subheader("📷 Camera")

    # Start camera first
    start_camera()

    # Initialize interview ONCE when camera opens
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = True

        q = interview_node({
            "mode": "question",
            "domain": st.session_state.selected_domain
        })

        st.session_state.question = q.get("question", "Explain your project.")
        st.session_state.answer = ""
        st.session_state.spoken = False
        st.session_state.listening_done = False

        # 🔊 Speak immediately when camera starts
        speak(st.session_state.question)
        st.session_state.spoken = True

    # Show question
    st.subheader("❓ Question")
    st.write(st.session_state.question)

    # 🎤 Listen once
    if not st.session_state.listening_done:
        st.info("🎤 Listening... Speak now")

        answer = auto_listen(6)

        st.session_state.answer = answer
        st.session_state.listening_done = True
    else:
        answer = st.session_state.answer

    # Evaluate
    if answer:
        st.success(f"🗣 You said: {answer}")

        res = interview_node({
            "mode": "evaluate",
            "question": st.session_state.question,
            "answer": answer
        })

        st.session_state.feedback = res
        st.session_state.step = "result"

# =========================
# STEP 4: RESULT
# =========================
if st.session_state.step == "result":
    st.subheader("📊 Feedback")

    score = st.session_state.feedback.get("score", "0")
    feedback = st.session_state.feedback.get("feedback", "")
    better = st.session_state.feedback.get("better_answer", "")

    st.write("Score:", score)
    st.write("Feedback:", feedback)
    st.write("Better Answer:", better)

    # 🔊 Speak feedback
    if "feedback_spoken" not in st.session_state:
        speak(f"Your score is {score}. {feedback}")
        st.session_state.feedback_spoken = True

    # Next question
    if st.button("🔁 Next Question"):
        st.session_state.question = None
        st.session_state.answer = ""
        st.session_state.spoken = False
        st.session_state.listening_done = False
        st.session_state.feedback_spoken = False
        st.session_state.step = "interview"