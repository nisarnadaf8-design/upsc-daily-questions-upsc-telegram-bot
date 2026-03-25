import requests
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = """
Generate 3 UPSC GS1 Society + 3 GS4 Ethics questions.
- UPSC PYQ standard
- Mention 150/250 words
- No answers
"""

res = client.chat.completions.create(
    model="gpt-5.3",
    messages=[{"role": "user", "content": prompt}]
)

if not res or not res.choices:
    raise Exception("OpenAI response failed")

text = "📘 UPSC MAINS QUESTIONS (10 AM)\n\n" + res.choices[0].message.content

bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

requests.post(url, data={"chat_id": chat_id, "text": text})
print("API KEY:", os.getenv("OPENAI_API_KEY"))
print("BOT:", os.getenv("BOT_TOKEN"))
print("CHAT:", os.getenv("CHAT_ID"))
