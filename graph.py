import os
import json
import time
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# -------------------------------
# SAFE JSON PARSER
# -------------------------------
def safe_json_parse(content):
    try:
        start = content.find("{")
        end = content.rfind("}") + 1

        if start == -1 or end == -1:
            return {}

        return json.loads(content[start:end])
    except:
        return {}

# -------------------------------
# MAIN FUNCTION
# -------------------------------
def interview_node(state):
    text = state.get("text", "")
    answer = state.get("answer", "")
    domain = state.get("domain", "General")
    question = state.get("question", "")
    mode = state.get("mode", "analyze")

    # =========================
    # 1. ANALYZE RESUME
    # =========================
    if mode == "analyze":
        prompt = f"""
        Analyze this resume:

        {text[:1000]}

        Return ONLY JSON:
        {{
          "skills": "comma separated skills",
          "domain": "frontend/backend/devops/aiml"
        }}
        """

        try:
            res = llm.invoke(prompt)
            data = safe_json_parse(res.content)

            return {
                "skills": data.get("skills", "Not detected"),
                "domain": data.get("domain", "General")
            }

        except Exception as e:
            print("ANALYZE ERROR:", e)
            return {"skills": "Not detected", "domain": "General"}

    # =========================
    # 2. GENERATE QUESTION
    # =========================
    elif mode == "question":
        prompt = f"""
        Generate ONE interview question for {domain} domain.

        Only return question text.
        """

        try:
            try:
                res = llm.invoke(prompt)
            except:
                time.sleep(2)
                res = llm.invoke(prompt)

            content = res.content.strip()

            if not content or len(content) < 5:
                content = "Explain your recent project."

            return {"question": content}

        except Exception as e:
            print("QUESTION ERROR:", e)
            return {"question": "Explain your recent project."}

    # =========================
    # 3. EVALUATE ANSWER
    # =========================
    elif mode == "evaluate":
        prompt = f"""
        Question: {question}
        Answer: {answer}

        Return JSON:
        {{
          "score": "0-10",
          "feedback": "short feedback",
          "better_answer": "improved answer"
        }}
        """

        try:
            res = llm.invoke(prompt)
            data = safe_json_parse(res.content)

            return {
                "score": data.get("score", "0"),
                "feedback": data.get("feedback", "Could not evaluate"),
                "better_answer": data.get("better_answer", "")
            }

        except Exception as e:
            print("EVAL ERROR:", e)
            return {
                "score": "0",
                "feedback": "Evaluation failed",
                "better_answer": ""
            }

    return {}