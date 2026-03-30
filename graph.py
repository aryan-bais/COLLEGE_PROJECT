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

    prompt = f"""
    You are an expert AI interviewer.

    Resume:
    {text[:2000]}

    Company: {company}

    Candidate Answer:
    {answer}

    Perform ALL tasks:
    1. Extract technical skills
    2. Identify domain
    3. Generate 5 company-oriented interview questions
    4. Evaluate candidate answer
    5. Give score out of 10
    6. Suggest better answer

    Return STRICT JSON:

    {{
      "skills": "...",
      "domain": "...",
      "questions": "...",
      "score": "...",
      "feedback": "...",
      "better_answer": "..."
    }}
    """

    try:
        res = llm.invoke(prompt)

        import json
        data = json.loads(res.content)

        return data

    except Exception as e:
        print("ERROR:", e)
        return {
            "skills": "Error",
            "domain": "Error",
            "questions": "Error",
            "score": "0",
            "feedback": "API failed",
            "better_answer": ""
        }