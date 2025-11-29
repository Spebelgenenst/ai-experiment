import json
from google import genai
from discord_webhook import DiscordWebhook
import subprocess

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

    return code

def execute_code(code):
    
    with open("code.py", "w") as f:
        f.write(code)

    output = subprocess.run(["python3","code.py"], text=True, capture_output=True)

    print(output)

    return output.stdout, output.stderr

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
        webhook.add_file(file=code, filename=f"code{counter}.py")

        webhook.execute()

        console_output, error = execute_code(code)

        # log in discord webhook
        webhook = DiscordWebhook(url=credentials["discordWebHook"], content=str(counter)+". output")
        webhook.add_file(file=console_output, filename=f"output{counter}.log")
        if error:
            webhook.add_file(file=str(error), filename=f"error{counter}.log")
            webhook.content = str(counter)+". output+error"

        webhook.execute()

        prompt_feedback = f"last Console Output: {console_output}, error: {error}"
        counter += 1