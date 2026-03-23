import streamlit as st
from graph import app_graph
from utils import extract_text_from_pdf

st.set_page_config(page_title="AI Interviewer", layout="centered")

st.title("🤖 AI Resume Interviewer")

# Upload Resume
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_file:
    st.success("Resume uploaded successfully!")

    # Extract text
    text = extract_text_from_pdf(uploaded_file)

    # Run AI pipeline
    workflow = app_graph()
    result = workflow.invoke({
        "text": text,
        "answer": "Machine learning improves with more data"
    })

    # Display outputs
    st.subheader("🛠 Skills")
    st.write(result.get("skills", "No skills found"))

    st.subheader("💼 Domain")
    st.write(result["domain"])

    st.subheader("❓ Questions")
    st.write(result["questions"])

    # Answer input
    user_answer = st.text_area("✍️ Your Answer")

    if st.button("Evaluate Answer"):
        result = workflow.invoke({
            "text": text,
            "answer": user_answer
        })

        st.subheader("📊 Evaluation")
        st.write(result["evaluation"])