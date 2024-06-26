import discord
import os
from dotenv import load_dotenv
import asyncio
import requests
import json


def runBot():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print({client.user}, 'is live')

    @client.event
    async def on_message(message):
        print("Got message: "+message.content);
        channel = message.channel
        def get_input(m):
            return m.author == message.author
        if message.content.startswith('<@1232040337652973652>') and "help" in message.content:
            #i.e. if the message is @Raidcraft-bot help, then send the intro message
            await channel.send('Hello! I am a bot that helps you organize your World of Warcraft runs. To start a new run, type @Raidcraft-bot $newrun in a public channel. Please create an account on https://www.raidcraft-app.com/ and get your BattleID ready. I will ask you for it in a private message.')
        elif message.content.startswith('<@1232040337652973652> $newrun'):
            message = message
            await message.author.send('Looks like you want to start a new run, but I don\'t have your BattleID. Please reply with your BattleID to get started.')
            battle_id_msg = await client.wait_for('message', check=get_input)
            battleID = battle_id_msg.content
            #todo: Save the discord_id and battle_id in the database, so that we don't have to ask for the Battle ID again 
            x = requests.post('https://wow-app-rails-5c78013cc11c.herokuapp.com/api/users/battletag' , json = {'discord_id': message.author.id, 'battletag': battleID })
            response = x.text
            parsed = json.loads(response)
            if "errors" in parsed:
                await message.author.send('Sorry, I couldn\'t find your account. Please create an account on https://www.raidcraft-app.com/ and try again.')
                return
            else:
                teams = parsed["teams"]
                await message.author.send('Got it! Choose a Team:')
                i = 0
                for team in teams:
                    i += 1
                    await message.author.send(i+") " + team["name"] + " - ")

                response = await client.wait_for('message', check=get_input)
                chosen_team = teams[int(response.content)-1]
                if chosen_team:
                    intro_message = await channel.send('Let\'s start a new run! Reply with an emoji to join the run')

                    def check_reaction(reaction, user):
                        return reaction.message.id == intro_message.id

                    try:
                        reaction, user = await client.wait_for('reaction_add', timeout=86400.0, check=check_reaction)
                    except asyncio.TimeoutError:
                        await channel.send('No reactions in time. 👎')
                    else:
                        await reaction.message.author.send("Get ready to raid! Just click this link to add your character: https://www.raidcraft-app.com/characters/new?invite_code="+chosen_team["invite_code"])
                else:
                    await message.author.send('Sorry, something went wrong. Please try again later.')

    client.run(TOKEN)