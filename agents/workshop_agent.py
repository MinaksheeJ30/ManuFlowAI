from dotenv import load_dotenv
from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY
from app.json_utils import parse_llm_json

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY
)


def load_prompt():
    with open("prompts/workshop_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()


SYSTEM_PROMPT = load_prompt()


def workshop_agent(job):

    prompt = f"""
{SYSTEM_PROMPT}

Part Name: {job.part_name}
Material: {job.material}
Quantity: {job.quantity}
Machine: {job.machine}
"""

    response = llm.invoke(prompt)


    return parse_llm_json(response.content)