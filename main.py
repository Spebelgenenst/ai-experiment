import json
from google import genai
from io import StringIO
import sys
from discord_webhook import DiscordWebhook

with open('config.json', 'r') as file:
    config = json.load(file)

client = genai.Client(api_key=config["geminiApiKey"])

ai_model = "gemini-2.5-flash"

def ai(ai_model, prompt):
    response = client.models.generate_content(
        model=ai_model,
        contents=prompt
    )

    return response # "```python print(\"hello world\") ```" #this is just used for testing

def extract_code(response):
    extract = response[response.find("```python")+10:]
    extract = extract[:extract.find("```")]
    return extract

def execute_code(code):
    output = StringIO()
    sys.stdout = output
    try:
        exec(code)
        error = None
    except Exception as e:
        error = e
    sys.stdout = sys.__stdout__

    return output.getvalue(), error

if __name__ ==  "__main__":
    counter = 0
    prompt = config["prompt"]
    while True:
        response = str(ai(ai_model,prompt))
        code = extract_code(response)
        console_output, error = execute_code(code)

        prompt = f"Console Output: {console_output} \n Error: {error}"

        # log in discord webhook
        webhook = DiscordWebhook(url=config["discordWebHook"], content=str(counter))
        webhook.add_file(file=code, filename="code.py")
        webhook.add_file(file=console_output, filename="output.log")
        if error:
            webhook.add_file(file=str(error), filename="error.log")

        webhook.execute()
        counter += 1
