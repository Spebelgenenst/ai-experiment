import json
from google import genai
from discord_webhook import DiscordWebhook, DiscordEmbed
import PyGithub
import StringIO
from time import sleep

#with open('prompt.md', 'r') as file:
#    prompt = file.read()

with open('credentials.json', 'r') as file:
    credentials = json.load(file)

client = genai.Client(api_key=credentials["geminiApiKey"])

ai_model = "gemini-2.5-flash"

repo = g.get_repo("Reponame/Here")

def ai(ai_model, prompt):
    response = client.models.generate_content(
        model=ai_model,
        contents=prompt
    )

    return response

if __name__ ==  "__main__":

    while True:
        issue_open = False
        while not issue_open:
            open_issues = repo.get_issues(state='open')
            sleep(30)
        
        print("waiting for ai to respond...")
        response = ai(ai_model, prompt).text
        if not response:
            continue
        
        print("executing code...")


        code = extract_code(response)
        if not code:
            prompt_feedback = "No python code found, please write python code!"
            print("error x_X: no code found")

            webhook = DiscordWebhook(url=credentials["discordWebHook"], content=str(counter)+". response without python code")
            webhook.add_file(file=response, filename="response.log")
            webhook.execute()
            
            continue

        webhook = DiscordWebhook(url=credentials["discordWebHook"])

        embed = DiscordEmbed(title="code", description=f"Attempt {str(counter)}", color="fc7a84")

        webhook.add_file(file=code, filename=f"code_{counter}.py")

        webhook.add_embed(embed)
        webhook.execute()


        console_output, error = execute_code(code)

        # log in discord webhook
        print(f"last Console Output: {console_output}")

        webhook = DiscordWebhook(url=credentials["discordWebHook"])

        embed = DiscordEmbed(title="output", description=f"Attempt {str(counter)}", color="fc7a84")

        webhook.add_file(file=console_output, filename=f"output_{counter}.log")
        if error:
            webhook.add_file(file=str(error), filename=f"error_{counter}.log")
            embed.title = "output & errors"
            embed.color = "ff0000"
            print(f"error: {error}")

        webhook.add_embed(embed)
        webhook.execute()


        prompt_feedback = f"last Console Output: {console_output}, error: {error}"
        counter += 1