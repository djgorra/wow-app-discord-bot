import discord
import os
from dotenv import load_dotenv
import asyncio
import requests


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
        print("Got message: "+message.content);
        # if message.content.startswith('<@1232040337652973652> $start'):
        #     def get_response(m):
        #         return 1
        #     await message.author.send('Hello! I am a bot that helps you organize your World of Warcraft runs. Please reply with your BattleID to get started.')
        #     msg = await client.wait_for('message', check=get_response)
        #     battleID = msg.content
        #     await message.author.send('Thanks! To start a new run, type <@1232040337652973652> $newrun in a public channel')

        if message.content.startswith('<@1232040337652973652> $newrun'):
            channel = message.channel
            #print("BattleID is "+battleID)
            #create a new invite code
            url = 'https://wow-app-rails-5c78013cc11c.herokuapp.com/api/teams/discord_create' 
            #this will create a new team and return the invite code
            #send message author's discord id as parameter  
            myobj = {'discord_id': message.author.id, 'battle_id': 'BearForce1#1359'}
            x = requests.post(url, json = myobj)
            invite_code = x.text or "12345"

            intro_message = await channel.send('Let\'s start a new run! Reply with an emoji to join the run')

            def check_message(m):
                return m.content == 'newcharacter' #and m.channel == channel

            def get_response(m):
                return 1

            def check(reaction, user):
                #Todo - check if user is not a bot
                #todo - response to all users, not just message.author
                #return user == message.author and str(reaction.emoji) == '👍'
                return reaction.message.id == intro_message.id

            try:
                reaction, user = await client.wait_for('reaction_add', timeout=86400.0, check=check)
            except asyncio.TimeoutError:
                await channel.send('👎')
            else:
                await message.author.send("This is a private message! If you already have an account on raidcraft-app.com, reply with your wow id. Otherwise reply with 'newcharacter' to begin a new character.")

                #todo - if they say 'newcharacter' then begin the process of creating a new character
                msg = await client.wait_for('message', check=check_message)
                await message.author.send('What is your character name?')
                msg = await client.wait_for('message', check=get_response)
                character_name = msg.content
                await message.author.send('What is your class?')
                msg = await client.wait_for('message', check=get_response)
                character_class = msg.content

                url = 'https://wow-app-rails-5c78013cc11c.herokuapp.com/api/characters/discord_create'
                myobj = {'character': {'name': character_name, 'class': class_name}, 'invite_code': invite_code}
                x = requests.post(url, json = myobj)
                print(x.text)



    client.run(TOKEN)