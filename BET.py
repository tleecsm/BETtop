import discord
from os import path
import SETUP

if not (path.exists("PARAMETERS.py") or SETUP.parameters_sanitary()) :
    # Parameters need to be generated/regenerated
    SETUP.generate_parameters()

import PARAMETERS

client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(PARAMETERS.BOT_TOKEN)