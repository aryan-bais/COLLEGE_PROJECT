import streamlit as st
from graph import app_graph
from my_parser import extract_text

st.set_page_config(page_title="AI Interviewer", layout="centered")

st.title("🤖 AI Resume Interviewer")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])

if uploaded_file:
    text = extract_text(uploaded_file)

    company = st.selectbox(
        "Choose Company",
        ["TCS", "Infosys", "Wipro", "Google", "Amazon", "Cisco",
         "Microsoft", "Apple", "Meta", "General"]
    )

    user_answer = st.text_area("Write your answer")

    if st.button("Start Interview"):
        workflow = app_graph()

        result = workflow.invoke({
            "text": text,
            "answer": user_answer,
            "company": company
         })
        
        
        

        st.subheader("📊 AI Interview Report")
        st.write(result["result"])
        
        text = extract_text(uploaded_file)[:2000]