import json
from google import genai
from io import StringIO
import sys
from discord_webhook import DiscordWebhook

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
        return "print(\"no python code found\")"
    
    print("---------raw-----------")
    print(response)
    print("---------code----------")
    print(code)

    return code

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
    prompt_feedback = "None"
    while True:
        response = ai(ai_model, prompt + prompt_feedback)
        if not response.text:
            continue

        code = extract_code(response.text)

        webhook = DiscordWebhook(url=credentials["discordWebHook"], content=str(counter)+". code")
        webhook.add_file(file=code, filename="code.py")

        webhook.execute()

        console_output, error = execute_code(code)

        #print("---------------------------")
        #print(console_output)

        # log in discord webhook
        webhook = DiscordWebhook(url=credentials["discordWebHook"], content=str(counter)+". output")
        webhook.add_file(file=console_output, filename="output.log")
        if error:
            #print(error)
            webhook.add_file(file=str(error), filename="error.log")
            webhook.content = str(counter)+". output+error"

        webhook.execute()

        prompt_feedback = f"last Console Output: {console_output} \n last Error: {error}"
        counter += 1
