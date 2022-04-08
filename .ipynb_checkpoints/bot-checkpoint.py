import discord
from dotenv import load_dotenv
import os 
import json
load_dotenv()

token = os.environ.get("bot-token")
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$scrapehistory'):
        print("Scraping history of chat logs...")
        history = await scrape_history(message)
        
        print("Finished scraping chat logs")
        with open("message_logs.json", 'w') as outfile:
            json.dump(history, outfile)

        await message.delete()
        #await message.channel.send(history)

async def scrape_history(message):
    author_dict = {}
    history = await message.channel.history(limit = 30000).flatten()
    for message in history:
        if (message.author.bot):
            continue

        if (message.author.name in author_dict):
            author_dict[message.author.name].append(message.content)
        else:
            author_dict[message.author.name] = [message.content]
        #print(f"{message.author}: {message.content}")

    #print(author_dict)
    return author_dict

client.run(token)