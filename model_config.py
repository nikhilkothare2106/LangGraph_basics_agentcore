from dotenv import load_dotenv
import os
from pydantic import SecretStr
from langchain_groq import ChatGroq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=SecretStr(api_key) if api_key else None,
)
