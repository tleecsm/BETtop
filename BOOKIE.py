import PARAMETERS
import csv


async def handler(message):
    if message.content.startswith(f'{PARAMETERS.COMMAND_PREFIX}BANKER'):
        message_split = message.content.split()
        if len(message_split) < 2:
            return
        if message_split[1] in BOOKIE_COMMANDS:
                await BOOKIE_COMMANDS[message_split[1]](message)        


async def make(message):
    pass


async def bet(message):
    pass


async def resolve(message):
    pass


BOOKIE_COMMANDS = {
        'MAKE': make,
        'BET': bet,
        'RESOLVE': resolve,
}