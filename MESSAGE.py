import PARAMETERS


async def handler(message):
    if message.content.startswith(f'{PARAMETERS.COMMAND_PREFIX}BANKER'):
        await message.channel.send('Banker Request Received.')
    elif message.content.startswith(f'{PARAMETERS.COMMAND_PREFIX}BOOKIE'):
        await message.channel.send('Bookie Request Received.')
