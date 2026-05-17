from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

class BugRequest(BaseModel):
    error: str

@app.get("/")
def home():
    return {"message": "AI Bug Assistant Running"}

@app.post("/analyze")
def analyze_bug(request: BugRequest):

    try:

        prompt = f"""
        You are a senior debugging assistant.

        Analyze this software error:

        {request.error}

        Explain:
        1. Root cause
        2. Possible fix
        3. Debugging steps
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return {
            "analysis": response.choices[0].message.content
        }

    except Exception as e:
        return {
            "error": str(e)
        }