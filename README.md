# Be careful executing this python script! You can't control what the AI ​​does.

This is just a silly project to have some fun. In theory the ai could take over the entire world or just delete your hard drive... who knows...

**Install**
1. download the latest [release](https://github.com/Spebelgenenst/ai-experiment/releases) or clone the repository
2. make sure you have all dependencies installed (google genai, discord_webhook, python-io)
   install:
   ```
   pip install discord-webhook
   pip install -q -U google-genai
   ```

**Setup**
1. Rename the _template-credentials.json_ file to _credentials.json_.
2. Go to [google ai studio](aistudio.google.com) and sign in
3. grab your gemini key
4. paste it in the _credentials.json_ file
5. create a [discord webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
6. paste it in the _credentials.json_ file
7. (optional) paste your own prompt in _prompt.md_
8. run the program and hope your pc doesn't explote :3

**Tips for Prompt** (included in example prompt)
1. write in python
2. without explanation, just the code, no user input
3. dependencies can be installed thru subprocess (use --break-system-packages when prompted)
4. save your progression, the previous may have saved something
5. do not use placeholders cause the code gets executed without changes
6. directly request the AI to do what you want! like hacking, to draw attention to something, do something in the web
7. do whatever it takes to achieve your goal

Quote Spebell: "Vibe Coding is my hobby"
