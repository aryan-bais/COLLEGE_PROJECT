from fastapi import FastAPI
from pydantic import BaseModel
from my_parser import extract_text
from nodes import skill_node, domain_node, question_node, evaluation_node

app = FastAPI()

class RequestData(BaseModel):
    file_path: str
    answer: str

@app.get("/")
def home():
    return {"message": "Resume AI API is running"}

@app.post("/analyze")
def analyze(data: RequestData):
    text = extract_text(data.file_path)

    state = {
        "text": text,
        "answer": data.answer
    }

    state.update(skill_node(state))
    state.update(domain_node(state))
    state.update(question_node(state))
    state.update(evaluation_node(state))

    return state