import json
from openai import OpenAI
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
with open(f"{BASE_DIR.parent}/.creds/openai-creds.json", "r") as openai_creds:
    SECRET_KEY = json.loads(openai_creds.read())['SECRET_KEY']
client = OpenAI(api_key=SECRET_KEY)

def generate_message(role, prompt, previous_messages=[]):
    AI = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        *previous_messages,
        {"role": "system", "content": role},
        {"role": "user", "content": prompt}
    ]
    )

    return AI.choices[0].message.content