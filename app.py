import streamlit as st
from nodes import interview_node
from my_parser import extract_text

st.set_page_config(page_title="AI Interviewer", layout="centered")

st.title("🤖 AI Resume Interviewer")


uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    text = extract_text(uploaded_file)

    st.success("✅ Resume uploaded successfully!")

    
    company = st.selectbox(
        "🏢 Select Company",
        [
            "General",
            "TCS", "Infosys", "Wipro", "Capgemini", "Accenture",
            "Cognizant", "HCL", "Tech Mahindra",
            "Google", "Amazon", "Microsoft", "Cisco", "Adobe",
            "Flipkart", "Paytm", "Zoho"
        ]
    )

    
    if st.button("🚀 Generate Interview"):
        result = interview_node({
            "text": text[:2000],   
            "company": company,
            "answer": ""           
        })

        st.session_state["result"] = result.get("result", "")

   
    if "result" in st.session_state:
        st.subheader("📄 Interview Output")
        st.write(st.session_state["result"])

        
        st.subheader("✍️ Write Your Answer")
        user_answer = st.text_area("Enter your answer here...")

        
        if st.button("📊 Evaluate Answer"):
            result_eval = interview_node({
                "text": text[:2000],
                "company": company,
                "answer": user_answer
            })

            st.subheader("📊 Evaluation")
            st.write(result_eval.get("result", "No evaluation"))