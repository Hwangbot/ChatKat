from openai import OpenAI
import os
from dotenv import load_dotenv

# ✅ Load .env file
load_dotenv()

# ✅ Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def generate_prompt(summary: str) -> str:
    return f"""Here is a dataset summary:\n{summary}\n\nWrite 3 clear business insights in plain English with a suggested action for each."""

def get_insights_from_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
