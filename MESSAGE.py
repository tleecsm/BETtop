import PARAMETERS
import IRS

async def handler(message):
    if message.content.startswith(f'{PARAMETERS.COMMAND_PREFIX}BANKER'):
        await message.channel.send('Banker Request Received.')
    elif message.content.startswith(f'{PARAMETERS.COMMAND_PREFIX}BOOKIE'):
        await message.channel.send('Bookie Request Received.')
    else:
        # Send this off to the IRS to handle
        await IRS.handler(message)
