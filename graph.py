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
    question = state.get("question", "")

    import json

    # 🎯 STEP 1: GENERATE QUESTION
    if answer == "":
        prompt = f"""
        You are an AI interviewer.

        Resume:
        {text[:2000]}

        Company: {company}

        Generate ONE interview question.

        STRICT:
        Return ONLY plain text question.
        """

        try:
            res = llm.invoke(prompt)
            q = res.content.strip()

            # ✅ ALWAYS return question key
            return {"question": q}

        except Exception as e:
            print("ERROR:", e)
            return {"question": "Tell me about yourself."}

    # 🎯 STEP 2: EVALUATE
    else:
        prompt = f"""
        Evaluate this answer.

        Question: {question}
        Answer: {answer}

        Return JSON ONLY:

        {{
          "score": "0-10",
          "feedback": "short feedback",
          "better_answer": "improved answer"
        }}
        """

        try:
            res = llm.invoke(prompt)
            content = res.content.strip()

            # 🧠 Extract JSON safely
            start = content.find("{")
            end = content.rfind("}") + 1
            json_str = content[start:end]

            data = json.loads(json_str)

            # ✅ Ensure keys exist
            return {
                "score": data.get("score", "0"),
                "feedback": data.get("feedback", ""),
                "better_answer": data.get("better_answer", "")
            }

        except Exception as e:
            print("ERROR:", e)

            return {
                "score": "0",
                "feedback": "Evaluation failed",
                "better_answer": ""
            }