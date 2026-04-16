import os
import datetime
from zoneinfo import ZoneInfo

import requests
from google import genai
from google.genai import types


ist_now = datetime.datetime.now(ZoneInfo("Asia/Kolkata"))
today = ist_now.strftime("%d %B %Y")
seed = int(ist_now.strftime("%Y%m%d"))

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

prompt = f"""Today is {today}.
Generate 3 fresh UPSC Mains GS1 (Indian Society) and 3 GS4 (Ethics) questions for this exact date.
- UPSC PYQ standard
- Mention 150/250 words for each question
- Do NOT repeat questions from previous days
- Output only the questions. No answers. No explanations. No preamble.
"""

config = types.GenerateContentConfig(temperature=0.9, seed=seed)


def ask(model: str) -> str:
    resp = client.models.generate_content(model=model, contents=prompt, config=config)
    text = (getattr(resp, "text", "") or "").strip()
    if not text:
        raise RuntimeError(f"{model} returned empty response")
    return text


try:
    body = ask("gemini-2.5-flash")
    used = "gemini-2.5-flash"
except Exception as e_flash:
    print(f"[warn] gemini-2.5-flash failed: {e_flash!r} - falling back to gemini-2.5-pro")
    body = ask("gemini-2.5-pro")
    used = "gemini-2.5-pro"

message = f"\U0001F4D8 UPSC MAINS QUESTIONS \u2014 {today} (10 AM IST)\n\n{body}"
message = message[:4000]

url = f"https://api.telegram.org/bot{os.environ['BOT_TOKEN']}/sendMessage"
r = requests.post(
    url,
    data={"chat_id": os.environ["CHAT_ID"], "text": message},
    timeout=30,
)
r.raise_for_status()
print(f"Sent via {used}")
