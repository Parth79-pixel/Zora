import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ZoraAI:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )

        self.system_prompt = (
            "You are Zora, a smart, fast, and concise voice assistant. "
            "Explain technical topics in very simple words. "
            "Keep answers short unless the user asks for details."
        )

        self.history = []

    def ask(self, user_text: str) -> str:
        try:
            messages = [{"role": "system", "content": self.system_prompt}]
            messages += self.history[-6:]
            messages.append({"role": "user", "content": user_text})

            response = self.client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
                messages=messages,
                temperature=0.5,
                max_tokens=300
            )

            reply = response.choices[0].message.content.strip()

            self.history.append({"role": "user", "content": user_text})
            self.history.append({"role": "assistant", "content": reply})

            return reply

        except Exception:
            return "Sorry, I am having trouble connecting right now."