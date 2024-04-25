import discord
import os
from dotenv import load_dotenv
import asyncio



# def handle_user_messages(msg) ->str:
#     message = msg.lower() #Converts all inputs to lower case
#     print(message)
#     if(message == '<@1232040337652973652>'):
#         return 'Intro message'
#     else:
#         return 'Hello user. Welcome'

# async def processMessage(message, user_message):
#     try:
#         botfeedback = handle_user_messages(user_message)
#         await message.channel.send(botfeedback)
#     except Exception as error:
#         print(error)

def runBot():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print({client.user}, 'is live')

    # @client.event
    # async def on_message(message):
    #     if message.author == client.user:
    #         return
    #     await processMessage(message, message.content)

    # @client.event
    # async def on_raw_reaction_add(payload):
    #     print(payload)
    #     print(payload.member.name)
    #     print(payload.emoji.name)
    #     print(payload.message)

    @client.event
    async def on_message(message):
        print(message.content);
        if message.content.startswith('<@1232040337652973652> $newrun'):
            channel = message.channel
            await channel.send('Let\'s start a new run! Reply with an emoji to join the run')

            def check_message(m):
                return m.content == 'newcharacter' #and m.channel == channel

            def check(reaction, user):
                #Todo - check if user is not a bot
                #todo - response to all users, not just message.author
                #todo - reply with any emoji, not just thumbs up
                return user == message.author and str(reaction.emoji) == '👍'

            try:
                #todo - remove timeout
                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await channel.send('👎')
            else:
                await message.author.send("This is a private message! If you already have an account on raidcraft-app.com, reply with your wow id. Otherwise reply with 'newcharacter' to begin a new character.")

                #todo - if they say 'newcharacter' then begin the process of creating a new character
                msg = await client.wait_for('message', check=check_message)
                await message.author.send(f'Hello {msg.author}!')

    client.run(TOKEN)