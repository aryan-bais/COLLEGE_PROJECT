import streamlit as st
from my_parser import extract_text
from nodes import skill_node, domain_node, question_node, evaluation_node

st.title("📄 Resume Analyzer AI")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
answer = st.text_area("Enter your answer")

if st.button("Analyze"):
    if uploaded_file is not None:
        # Save file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        text = extract_text("temp.pdf")

        state = {
            "text": text,
            "answer": answer
        }

        state.update(skill_node(state))
        state.update(domain_node(state))
        state.update(question_node(state))
        state.update(evaluation_node(state))

        st.subheader("Skills")
        st.write(state["skills"])

        st.subheader("Domain")
        st.write(state["domain"])

        st.subheader("Questions")
        st.write(state["questions"])

        st.subheader("Evaluation")
        st.write(state["evaluation"])