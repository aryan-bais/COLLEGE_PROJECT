import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()
llm = ChatGroq(
    model="llama-3.1-8b-instant",
  api_key=os.getenv("GROQ_API_KEY")
)




def skill_node(state):
    text = state.get("text", "")
    if not text:
        return {"skills": ""}

    prompt = f"""
    You are an expert recruiter.
    Extract all technical skills from the following resume:
    {text}
    List them as comma-separated values.
    """
    try:
        res = llm.invoke(prompt)
        return {"skills": res.content.strip()}
    except Exception as e:
        print("Error in skill_node:", e)
        return {"skills": ""}

def domain_node(state):
    skills = state.get("skills", "")
    if not skills:
        return {"domain": ""}
    prompt = f"""
    You are an industry expert.
    Identify the most relevant domain/industry for these skills:
    {skills}
    Provide a single domain name.
    """
    try:
        res = llm.invoke(prompt)
        return {"domain": res.content.strip()}
    except Exception as e:
        print("Error in domain_node:", e)
        return {"domain": ""}

def question_node(state):
    skills = state.get("skills", "")
    domain = state.get("domain", "")
    if not skills or not domain:
        return {"questions": ""}
    prompt = f"""
    You are an expert interviewer.
    Generate 5 interview questions for skills: {skills} in the domain: {domain}.
    Return each question on a new line.
    """
    try:
        res = llm.invoke(prompt)
        return {"questions": res.content.strip()}
    except Exception as e:
        print("Error in question_node:", e)
        return {"questions": ""}

def evaluation_node(state):
    questions = state.get("questions", "")
    answer = state.get("answer", "No answer provided")
    if not questions:
        return {"evaluation": "No questions to evaluate."}
    prompt = f"""
    You are an expert interviewer.
    Evaluate the following answer:
    Questions:
    {questions}
    Answer:
    {answer}
    Provide a score out of 10 and constructive feedback.
    """
    try:
        res = llm.invoke(prompt)
        return {"evaluation": res.content.strip()}
    except Exception as e:
        print("Error in evaluation_node:", e)
        return {"evaluation": "Evaluation failed due to an error."}
    
