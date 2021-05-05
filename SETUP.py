EXPECTED_PARAMETERS = {
    "BOT_TOKEN": "bot token",
    "COMMAND_PREFIX": "command prefix",
    "CURRENCY_NAME": "currency name"
}


def generate_parameters():
    parameters = []
    for key in EXPECTED_PARAMETERS:
        parameter = f'{key} = "{input(f"Please enter your {EXPECTED_PARAMETERS[key]}: ")}"\n'
        parameters.append(parameter)
    with open('PARAMETERS.py', 'w') as P:
        P.writelines(parameters)


def parameters_sanitary():
    with open('PARAMETERS.py', 'r') as P:
        parameters = P.readlines()
    if len(EXPECTED_PARAMETERS) != len(parameters):
        return False
    for i in range(len(parameters)):
        current_line = parameters[i].split("=")
        if len(current_line) < 2:
            return False
        parameters[i] = current_line[0].strip()
    for key in EXPECTED_PARAMETERS:
        if key not in parameters:
            return False
    return True