import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)


def interview_node(state):
    text = state.get("text", "")
    answer = state.get("answer", "")
    company = state.get("company", "General")

    
    if not answer:
        prompt = f"""
        You are an expert AI interviewer.

        Resume:
        {text}

        Company: {company}

        Tasks:
        1. Extract technical skills
        2. Identify domain
        3. Generate 5 technical interview questions based on resume skills
        4. If company is not "General", slightly tailor questions for {company}

        Return format:

        Skills:
        Domain:
        Questions:
        """

    
    else:
        prompt = f"""
        You are an expert AI interviewer.

        Resume:
        {text}

        Company: {company}

        Candidate Answer:
        {answer}

        Tasks:
        1. Evaluate the answer
        2. Give score out of 10
        3. Provide feedback
        4. Suggest better answer

        Return format:

        Score:
        Feedback:
        Better Answer:
        """

    try:
        res = llm.invoke(prompt)
        return {"result": res.content.strip()}

    except Exception as e:
        print("ERROR:", e)
        return {"result": f"❌ Error: {str(e)}"}