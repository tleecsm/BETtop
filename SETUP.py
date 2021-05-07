EXPECTED_PARAMETERS = {
    "BOT_TOKEN": "BOT TOKEN",
    "COMMAND_PREFIX": "COMMAND PREFIX",
    "CURRENCY_NAME": "CURRENCY NAME",
    "DAILY_CURRENCY": "DAILY CURRENCY",
    "DAILY_CURRENCY_MAX": "DAILY CURRENCY MAX",
    "UNIQUE_CHANNEL_AWARD": "UNIQUE CHANNEL AWARD",
    "REPEAT_CHANNEL_AWARD": "REPEAT CHANNEL AWARD",
    "REPEAT_CHANNEL_DIMINISH": "REPEAT CHANNEL DIMINISH",
    "ENROLL_AWARD": "ENROLL AWARD",
}


def generate_parameters():
    print('!GENERATING NEW PARAMETERS!')
    parameters = []
    for key in EXPECTED_PARAMETERS:
        parameter = f'{key} = "{input(f"PLEASE ENTER YOUR {EXPECTED_PARAMETERS[key]}: ")}"\n'
        parameters.append(parameter)
    # Add additional non-user defined parameters
    parameters.append(f'USER_ID_POSITION = 0')
    parameters.append(f'USER_CURRENCY_POSITION = 1')
    parameters.append(f'USER_MAX_POSITION = 2')
with open('PARAMETERS.py', 'w') as P:
        P.writelines(parameters)


def parameters_sanitary():
    print('!CHECKING FOR SANITARY PARAMETERS!')
    with open('PARAMETERS.py', 'r') as P:
        parameters = P.readlines()
    if len(EXPECTED_PARAMETERS) != len(parameters):
        return False
    for i in range(len(parameters)):
        current_line = parameters[i].strip().split(" = ")
        if len(current_line) < 2:
            return False
        parameters[i] = current_line[0].strip()
    for key in EXPECTED_PARAMETERS:
        if key not in parameters:
            return False
    return True
