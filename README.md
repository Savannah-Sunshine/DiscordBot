# DiscordBot

You must run in anaconda 
Use this to get the right enviroment `conda create -c conda-forge -n skill-bot python=3.11 discord.py`


### To configure a discord bot
1. Go to https://discord.com/developers/applications and click the New Application button at the top right.
2. Scroll down to Message Content Intent and check the button. This is so the bot knows what is sent
3. OAuth2->URL Generator link on the left sidebar. This will present a table of check boxes. Select bot. Add these permissions
- Send Messages
- Create Public Threads
- Send Messages in Threads
- Embed Links
- Attach Files
- Add Reactions
4. Copy the generated URL found at the bottom of the page.


### Add to your code's secrets.env file
1. copy the Token displayed next to your bot's icon.
DISCORD_TOKEN=<paste token here>
2. Get the channel id and put it in secrets.env