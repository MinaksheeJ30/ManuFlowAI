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
    with open("prompts/planner_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

SYSTEM_PROMPT = load_prompt()

REQUIRED_FIELDS = [
    "part_name",
    "material",
    "quantity",
    "machine",
    "deadline"
]

def planner_agent(user_input: str):

    prompt = f"""{SYSTEM_PROMPT}

Manufacturing Request:

{user_input}
"""

    response = llm.invoke(prompt)

    data = parse_llm_json(response.content)


    missing = []

    for field in REQUIRED_FIELDS:
        if field not in data:
            data[field] = None

    for field in REQUIRED_FIELDS:
        value = data[field]

        if value is None:
            missing.append(field)

        elif isinstance(value, str) and value.strip() == "":
            missing.append(field)

    data["missing_fields"] = missing
    data["completed"] = len(missing) == 0


    return data