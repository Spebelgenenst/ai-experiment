import json
from google import genai
from io import StringIO
import sys
from discord_webhook import DiscordWebhook

with open('config.json', 'r') as file:
    config = json.load(file)

#Wenn du bestimmte Bibliotheken verwenden möchtest musst du sie mit subprosses installieren.
with open('promt.json', 'r') as file:
    promt = json.load(file)

client = genai.Client(api_key=config[0])

ai_model = "gemini-2.5-flash"


def ai(ai_model, promt):
    response = client.models.generate_content(
        model=ai_model,
        contents=promt
    )

    return response

def extract_code(response):
    extract = response[response.find("```python")+10:]
    extract = extract[:extract.find("```")]
    return extract

def execute_code(code):
    output = StringIO()
    sys.stdout = output
    try:
        exec(extract_code(response))
        error = None
    except:
        error = "error"
    sys.stdout = sys.__stdout__

    return output.getvalue()

if __name__ ==  "__main__":
    response = str(ai(ai_model,promt))
    code = extract_code(response)
    console_output = execute_code(code)

    #log in discord webhook
    webhook = DiscordWebhook(url=config[1], content=f"""
-----------------------------------code-----------------------------------
{code}
""")
    webhook.execute()

    webhook = DiscordWebhook(url=config[1], content=f"""
----------------------------------console---------------------------------
{console_output}
""")
    webhook.execute()