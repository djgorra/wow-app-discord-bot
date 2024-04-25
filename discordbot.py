import discord
import os
from dotenv import load_dotenv




def handle_user_messages(msg) ->str:
    message = msg.lower() #Converts all inputs to lower case
    print(message)
    if(message == '<@1232040337652973652>'):
        return 'Intro message'
    else:
        return 'Hello user. Welcome'

async def processMessage(message, user_message):
    try:
        botfeedback = handle_user_messages(user_message)
        await message.channel.send(botfeedback)
    except Exception as error:
        print(error)

def runBot():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print({client.user}, 'is live')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        await processMessage(message, message.content)

    @client.event
    async def on_raw_reaction_add(payload):
        print(payload)
        # print(payload.member.name)
        # print(payload.emoji.name)
        # print(payload.message)

    client.run(TOKEN)