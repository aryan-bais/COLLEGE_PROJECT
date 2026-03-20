import os
from dotenv import load_dotenv
from langchain_ollama.chat_models import ChatOllama

llm = ChatOllama(
    model="llama3",
    
    api_key = os.getenv("OLLAMA_API_KEY")
)


def skill_node(state):
    text = state["text"]

    res = llm.invoke(f"Extract technical skills from this resume:\n{text}")
    return {"skills": res.content}



def domain_node(state):
    skills = state["skills"]

    res = llm.invoke(f"Identify domain from these skills: {skills}")
    return {"domain": res.content}



def question_node(state):
    skills = state["skills"]
    domain = state["domain"]

    res = llm.invoke(
        f"Generate 5 interview questions for skills {skills} in domain {domain}"
    )
    return {"questions": res.content}



def evaluation_node(state):
    questions = state["questions"]
    answer = state.get("answer", "No answer provided")

    res = llm.invoke(
        f"Evaluate this answer:\nQ:{questions}\nA:{answer}\nGive score out of 10 and feedback"
    )
    return {"evaluation": res.content}

