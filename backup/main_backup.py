import json
from google import genai
from io import StringIO
import sys
from discord_webhook import DiscordWebhook
import traceback

with open('prompt.md', 'r') as file:
    prompt = file.read()

with open('credentials.json', 'r') as file:
    credentials = json.load(file)

client = genai.Client(api_key=credentials["geminiApiKey"])

ai_model = "gemini-2.5-flash"

def ai(ai_model, prompt):
    response = client.models.generate_content(
        model=ai_model,
        contents=prompt
    )

    return response

def extract_code(response):
    start = response.find("```python")
    if start  != -1:
        code = response[start+10:]
        code = code[:code.find("```")]
    else:
        return None
    
    #print("---------raw-----------")
    #print(response)
    #print("---------code----------")
    #print(code)

    return code

def execute_code(code):
    error = None
    custom_globals = {"__builtins__": __builtins__}
    custom_locals = {}
    output = StringIO()
    sys.stdout = output

    try:
        exec(code, custom_globals, custom_locals)
    except Exception:
        error = traceback.format_exc()
    sys.stdout = sys.__stdout__

    return output.getvalue(), error

if __name__ ==  "__main__":
    counter = 0
    prompt_feedback = "None"
    while True:
        response = ai(ai_model, prompt + prompt_feedback).text
        if not response:
            continue

        code = extract_code(response)
        if not code:
            prompt_feedback = "No python code found, please write python code!"

            webhook = DiscordWebhook(url=credentials["discordWebHook"], content=str(counter)+". response without python code")
            webhook.add_file(file=response, filename="response.log")
            webhook.execute()
            
            continue

        webhook = DiscordWebhook(url=credentials["discordWebHook"], content=str(counter)+". code")
        webhook.add_file(file=code, filename="code.py")

        webhook.execute()

        console_output, error = execute_code(code)

        print("---------------------------")
        print(console_output)

        # log in discord webhook
        webhook = DiscordWebhook(url=credentials["discordWebHook"], content=str(counter)+". output")
        webhook.add_file(file=console_output, filename="output.log")
        if error:
            print(error)
            webhook.add_file(file=str(error), filename="error.log")
            webhook.content = str(counter)+". output+error"

        webhook.execute()

        prompt_feedback = f"last Console Output: {console_output} \n last Error: {error}"
        counter += 1
