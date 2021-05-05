def generate_parameters():
    parameters = []
    bot_token = f'BOT_TOKEN = "{input("Please enter your bot token: ")}"\n'
    parameters.append(bot_token)
    command_prefix = f'COMMAND_PREFIX = "{input("Please enter a command prefix: ")}"\n'
    parameters.append(command_prefix)
    with open('PARAMETERS.py', 'w') as P:
        P.writelines(parameters)