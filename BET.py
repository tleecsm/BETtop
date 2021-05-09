import discord
import datetime
import asyncio
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
import IRS

intents = discord.Intents().all()
client = discord.Client(intents=intents, guild_subscriptions=True)

@client.event
async def on_ready():
    print(f'!BETtop READY!')


@client.event
async def on_message(message):
    if message.author.bot:
        return
    await MESSAGE.handler(message)


async def daily_tasks():
    while True:
        try:
            # target_time = tomorrow at midnight
            """
            target_time = datetime.datetime.utcnow().replace(
                hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
            """
            target_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            current_time = datetime.datetime.utcnow()
            time_to_midnight = target_time - current_time
            time_to_midnight = time_to_midnight.total_seconds()
            await asyncio.sleep(time_to_midnight)
            print('!CALLING IRS TO START DAILY MANAGEMENT!')
            IRS.daily_management()
            print('!DAILY MANAGEMENT CONCLUDED!')
        except Exception as e:
            print(f'!ERROR HAS OCCURRED WITHIN DAILY LOOP!\n{e}')
            print('!RESTARTING DAILY LOOP!')

client.loop.create_task(daily_tasks())
client.run(PARAMETERS.BOT_TOKEN)
