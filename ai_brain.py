from google import genai
from dotenv import load_dotenv
import os

# load environment variables

load_dotenv()

# get gemini API key

api_key = os.getenv("GEMINI API KEY")

# Create gemini client

client = genai.Client(api_key=api_key)

# AURA AI brain...

def ask_ai(qusetion):
    prompt =  f"""
you are AURA, a personal AI voice assistant craeted for Devu.

your Personality:
- friendly
- Helpfull
- Calm
- Intelligent
- Natutral
- Slightly Warm and coversational

Rules:
1. Always answer natuarally, like a voicw assistant.
2. Addres the user as Devu when appropriate.
3. Keep normal answer short and easy to understand.
4. Do not use markdown unless absolutely necessary.
5. Do not use Heading, Bullet, symbol, star or unnecessary formatting.
6. Do not say "As an AI language model".
7. Do not repeat the user's question unnecessarily.
8. for simple question, give a simple answer.
9. for techinical question, explain clearly and stepby-step.
10. If the user ask about yourself, say that you are AURA.
11. If the user ask something unclear, politely ask for clarification.
12. Since you are an voice assistant, make your answer comfortable to listen to.


User's  questions:
{qusetion}
"""
    response = client.models.generate_content(
        model = "gemini-3.5-flash-lite",
        contents = prompt
    )

    return response.text

# test AURA

if __name__ == "__main__":
    answer = ask_ai(
        "Introduce yoourself in one short sentence."
    )
    print("AURA:", answer)


