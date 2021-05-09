import PARAMETERS
import IRS
import BANKER
import BOOKIE

async def handler(message):
    if message.content.startswith(f'{PARAMETERS.COMMAND_PREFIX}BOOKIE'):
        await BOOKIE.handler(message)
    elif message.content.startswith(f'{PARAMETERS.COMMAND_PREFIX}BANKER'):
        await BANKER.handler(message)
    else:
        # Send this off to the IRS to handle
        await IRS.handler(message)
