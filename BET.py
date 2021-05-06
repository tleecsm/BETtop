import discord
from os import path
import SETUP

print('!STARTING BETtop!')

if (not path.exists("PARAMETERS.py")) or (not SETUP.parameters_sanitary()):
    # Parameters need to be generated/regenerated
    print('!PARAMETERS NOT FOUND OR UNSANITARY!')
    SETUP.generate_parameters()

# These need to be imported after the above check
import PARAMETERS
import MESSAGE

client = discord.Client()


@client.event
async def on_ready():
    print(f'!BETtop READY!')


@client.event
async def on_message(message):
    if message.author.bot:
        return
    await MESSAGE.handler(message)

client.run(PARAMETERS.BOT_TOKEN)
