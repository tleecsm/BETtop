EXPECTED_PARAMETERS = {
    "BOT_TOKEN": "BOT TOKEN",
    "COMMAND_PREFIX": "COMMAND PREFIX",
    "CURRENCY_NAME": "CURRENCY NAME"
}


def generate_parameters():
    print('!GENERATING NEW PARAMETERS!')
    parameters = []
    for key in EXPECTED_PARAMETERS:
        parameter = f'{key} = "{input(f"PLEASE ENTER YOUR {EXPECTED_PARAMETERS[key]}: ")}"\n'
        parameters.append(parameter)
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
