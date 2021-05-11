import PARAMETERS
import RESPONSE
import csv


async def handler(message):
    if message.content.startswith(f'{PARAMETERS.COMMAND_PREFIX}BANKER'):
        message_split = message.content.split()
        if len(message_split) < 2:
            return
        if message_split[1] in BANKER_COMMANDS:
                await BANKER_COMMANDS[message_split[1]](message)        


async def leaderboard(message):
    message_split = message.content.split()
    if len(message_split) < 3:
            return
    if message_split[2] in LEADERBOARD_COMMANDS:
            await LEADERBOARD_COMMANDS[message_split[2]](message)  


async def all_time(message):
    IRS_form = []
    with open('IRS_FORM.csv', newline='') as form:
        IRS_form = list(csv.reader(form, delimiter=','))
    # We don't need the first row of headers
    IRS_form = IRS_form[1:]
    unsorted_users = []
    for user_row in IRS_form:
        user = user_row[PARAMETERS.USER_ID_POSITION]
        currency = int(user_row[PARAMETERS.USER_ALL_TIME_CURRENCY])
        unsorted_users.append((user,currency))
    pass
    sorted_users = sorted(unsorted_users, key=lambda tup: tup[1], reverse=True)
    message_fields = []
    for user_tuple in sorted_users:
        message_field = {}
        user_id = int(user_tuple[0])
        user_currency = user_tuple[1]
        username = message.guild.get_member(user_id)
        output_string = f'{user_currency} lifetime {PARAMETERS.CURRENCY_NAME}'
        message_field['name'] = username
        message_field['value'] = output_string
        message_field['inline'] = False
        message_fields.append(message_field)
    await RESPONSE.send_embedded_reply(message, 
                                       title='ALL-TIME LEADERBOARDS',
                                       description=f'Who has made the most {PARAMETERS.CURRENCY_NAME} in the history of the server?',
                                       fields=message_fields)


async def current(message):
    #TODO: Don't duplicate logic, bake this into the above function 
    IRS_form = []
    with open('IRS_FORM.csv', newline='') as form:
        IRS_form = list(csv.reader(form, delimiter=','))
    # We don't need the first row of headers
    IRS_form = IRS_form[1:]
    unsorted_users = []
    for user_row in IRS_form:
        user = user_row[PARAMETERS.USER_ID_POSITION]
        currency = int(user_row[PARAMETERS.USER_CURRENCY_POSITION])
        unsorted_users.append((user,currency))
    sorted_users = sorted(unsorted_users, key=lambda tup: tup[1], reverse=True)
    message_fields = []
    for user_tuple in sorted_users:
        message_field = {}
        user_id = int(user_tuple[0])
        user_currency = user_tuple[1]
        username = message.guild.get_member(user_id)
        output_string = f'{user_currency} {PARAMETERS.CURRENCY_NAME}\n'
        message_field['name'] = username
        message_field['value'] = output_string
        message_field['inline'] = False
        message_fields.append(message_field)
    await RESPONSE.send_embedded_reply(message, 
                                       title='CURRENT LEADERBOARDS',
                                       description=f'Who currently has the most {PARAMETERS.CURRENCY_NAME}?',
                                       fields=message_fields)


async def account(message):
    message_split = message.content.split()
    if len(message_split) < 3:
            return
    if message_split[2] in ACCOUNT_COMMANDS:
            await ACCOUNT_COMMANDS[message_split[2]](message)  


async def wallet(message):
    user_id = str(message.author.id) 
    username = message.guild.get_member(message.author.id).display_name
    IRS_form = []
    with open('IRS_FORM.csv', newline='') as form:
        IRS_form = list(csv.reader(form, delimiter=','))
    user_found = False
    for user_row in IRS_form:
        if user_id in user_row:
            user_found = True
            user_currency = user_row[PARAMETERS.USER_CURRENCY_POSITION]
            legacy_currency = user_row[PARAMETERS.USER_ALL_TIME_CURRENCY]
    if not user_found:
        return
    message_fields = [{'name':f'Current {PARAMETERS.CURRENCY_NAME}',
                       'value':user_currency,
                       'inline':False},
                      {'name':f'All-time {PARAMETERS.CURRENCY_NAME}',
                       'value':legacy_currency,
                       'inline':False}]
    await RESPONSE.send_embedded_reply(message, 
                                       title=f"{username.upper()}'S WALLET",
                                       description=f'How many {PARAMETERS.CURRENCY_NAME} do you currently have?',
                                       fields=message_fields)

BANKER_COMMANDS = {
        'LEADERBOARD': leaderboard,
        'ACCOUNT': account,
}

LEADERBOARD_COMMANDS = {
        'ALL-TIME': all_time,
        'CURRENT': current,
}

ACCOUNT_COMMANDS = {
        'WALLET': wallet,
}