import PARAMETERS
import RESPONSE
import csv
from os import path, listdir


async def handler(message):
    if message.content.startswith(f'{PARAMETERS.COMMAND_PREFIX}BOOKIE'):
        message_split = message.content.split()
        if len(message_split) < 2:
            return
        if message_split[1] in BOOKIE_COMMANDS:
            await BOOKIE_COMMANDS[message_split[1]](message)


async def make(message):
    # Create a new file that will manage a bet
    # Create it based on the current template
    template = []
    with open('BETS/BET_TEMPLATE.csv', newline='') as form:
        template = list(csv.reader(form, delimiter=','))
    message_split = message.content.split()
    if len(message_split) < 3:
        return
    bet_name = message_split[2]
    stances = message_split[3:]
    # Replace "stance" in the template with user defined stances
    template[0] = template[0][:-1] + stances
    with open(f'BETS/{bet_name}.csv', 'w', newline='') as form:
        template_writer = csv.writer(form, delimiter=',')
        template_writer.writerows(template)
    await RESPONSE.send_embedded_reply(message,
                                           title='BET CREATED',
                                           description=f"Bet has been created successfully!")


async def bet(message):
    message_split = message.content.split()
    if len(message_split) < 4:
        return
    user_id = str(message.author.id)
    bet_name = message_split[2]
    value = int(message_split[3])
    if not value > 0:
        await RESPONSE.send_embedded_reply(message,
                                           title='BET CANNOT BE PLACED',
                                           description=f"Bet value must be a positive integer!")
        return
    if not check_bet_status(message, bet_name):
        return
    stance = message_split[4]
    bet = []
    with open(f'BETS/{bet_name}.csv', newline='') as form:
        bet = list(csv.reader(form, delimiter=','))
    IRS_form = []
    with open('IRS_FORM.csv', newline='') as form:
        IRS_form = list(csv.reader(form, delimiter=','))

    # Ensure they have entered a valid stance
    if stance not in bet[0]:
        await RESPONSE.send_embedded_reply(message,
                                           title='BET CANNOT BE PLACED',
                                           description=f"{stance} is not a valid stance in this bet!")
        return
    stance_position = bet[0].index(stance)
    for user_row in IRS_form:
        if user_id in user_row:
            # Check to ensure they have enough current currency to make bet
            current_currency = int(user_row[PARAMETERS.USER_CURRENCY_POSITION])
            if current_currency < value:
                await RESPONSE.send_embedded_reply(message,
                                                   title='BET CANNOT BE PLACED',
                                                   description=f"You do not have enough {PARAMETERS.CURRENCY_NAME}!")
                return
            user_row[PARAMETERS.USER_CURRENCY_POSITION] = current_currency - value
    user_found = False
    for row in bet:
        if (user_id in row) and (stance in row):
            row[1] = int(row[1]) + value
            value = row[1]
            user_found = True
    if not user_found:
        # If we are here, the user hasn't entered this bet and needs to be added.
        new_row = [None for col in bet[0]]
        new_row[0] = user_id
        new_row[1] = value
        new_row[stance_position] = stance
        bet.append(new_row)

    await RESPONSE.send_embedded_reply(message,
                                       title='BET PLACED',
                                       description=f"You've placed your bet!",
                                       fields=[{'name':f'Value',
                                                'value':value,
                                                'inline':False},
                                               {'name':f'Stance',
                                                'value':stance,
                                                'inline':False}])

    with open('IRS_FORM.csv', 'w', newline='') as form:
        IRS_writer = csv.writer(form, delimiter=',')
        IRS_writer.writerows(IRS_form)

    with open(f'BETS/{bet_name}.csv', 'w', newline='') as form:
        bet_writer = csv.writer(form, delimiter=',')
        bet_writer.writerows(bet)


async def resolve(message):
    message_split = message.content.split()
    if len(message_split) < 4:
        return
    bet_name = message_split[2]
    winning_stance = message_split[3]

    if not check_bet_status(message, bet_name, check_closed=False):
        return

    bet = []
    with open(f'BETS/{bet_name}.csv', newline='') as form:
        bet = list(csv.reader(form, delimiter=','))
    IRS_form = []
    with open('IRS_FORM.csv', newline='') as form:
        IRS_form = list(csv.reader(form, delimiter=','))

    if winning_stance not in bet[0]:
        await RESPONSE.send_embedded_reply(message,
                                           title='BET CANNOT BE RESOLVED',
                                           description=f"{winning_stance} is not a valid stance in this bet!")

    winning_users = {}  # key: user_id (str), val: value bet (int)
    total_pool = 0
    winning_pool = 0
    for user_row in bet:
        if user_row[0] == 'User' or len(user_row) < 2:
            # this is a header or CLOSED row
            continue
        if winning_stance in user_row:
            winning_users[user_row[0]] = int(user_row[1])
            winning_pool += int(user_row[1])
        total_pool += int(user_row[1])
    odds = winning_pool/total_pool

    message_fields = []
    for user_row in IRS_form:
        if user_row[PARAMETERS.USER_ID_POSITION] in winning_users:
            bet_value = winning_users[user_row[PARAMETERS.USER_ID_POSITION]]
            winnings = int(bet_value/odds)
            user_row[PARAMETERS.USER_CURRENCY_POSITION] = int(user_row[PARAMETERS.USER_CURRENCY_POSITION]) + winnings
            user_row[PARAMETERS.USER_ALL_TIME_CURRENCY] = int(user_row[PARAMETERS.USER_ALL_TIME_CURRENCY]) + winnings
            username = message.guild.get_member(int(user_row[PARAMETERS.USER_ID_POSITION]))
            message_field = {'name':f'{username}',
                             'value':f'Bet {bet_value} {PARAMETERS.CURRENCY_NAME} and won {winnings} {PARAMETERS.CURRENCY_NAME}!',
                             'inline':False}
            message_fields.append(message_field)
    await RESPONSE.send_embedded_reply(message,
                                       title='BET RESOLVED',
                                       description=f"{bet_name} has been resolved with {winning_stance} as the outcome!",
                                       fields=message_fields)

    # Lock this bet
    bet = ['RESOLVED'] + bet

    with open('IRS_FORM.csv', 'w', newline='') as form:
        IRS_writer = csv.writer(form, delimiter=',')
        IRS_writer.writerows(IRS_form)

    with open(f'BETS/{bet_name}.csv', 'w', newline='') as form:
        bet_writer = csv.writer(form, delimiter=',')
        bet_writer.writerows(bet)


async def check(message):
    message_split = message.content.split()
    if len(message_split) < 2:
        return
    if len(message_split) == 2:
        # Special case, return all bets
        await check_all(message)
        return
    bet_name = message_split[2]

    if not check_bet_status(message, bet_name):
        return

    bet = []
    with open(f'BETS/{bet_name}.csv', newline='') as form:
        bet = list(csv.reader(form, delimiter=','))

    message_fields = []
    stances = ''
    for stance in bet[0][2:]:
        stances += f'{stance}\n'
    message_field = {'name':f'Betting Stances Available:',
                     'value':stances,
                     'inline':False}
    message_fields.append(message_field)
    for user_row in bet[1:]:
        username = message.guild.get_member(int(user_row[0]))
        user_stance = None
        for stance in user_row[2:]:
            if stance is not None:
                user_stance = stance
        value = user_row[1]
        message_field = {'name':f'{username}',
                         'value':f'Stance: {user_stance}\nBet: {value}',
                         'inline':True}
        message_fields.append(message_field)
    await RESPONSE.send_embedded_reply(message,
                                       title=f'{bet_name}',
                                       description=f"An overview for {bet_name}",
                                       fields=message_fields)


async def check_all(message):
    message_split = message.content.split()
    all_bets = listdir('./BETS')
    all_bets.remove('BET_TEMPLATE.csv')
    open_bets = {}
    closed_bets = {}
    for bet_name in all_bets:
        bet = []
        with open(f'BETS/{bet_name}.csv', newline='') as form:
            bet = list(csv.reader(form, delimiter=','))
        if 'RESOLVED' in bet[0]:
            continue
        elif 'CLOSED' in bet[0]:
            closed_bets[bet_name] = bet
        else:
            open_bets[bet_name] = bet
    message_fields = []
    # Handle printing the open bets first
    for bet_name in open_bets:
        bet = open_bets[bet_name]
        stances = ''
        for stance in bet[0][2:]:
            stances += f'{stance} '
        message_field = {'name':f'{bet_name}',
                         'value':f'Stances:\n{stances}',
                         'inline':False}
        message_fields.append(message_field)
    # Handle printing the open bets first
    for bet_name in closed_bets:
        bet = closed_bets[bet_name]
        message_field = {'name':f'{bet_name}',
                         'value':f'Betting on {bet_name} has been closed.',
                         'inline':False}
        message_fields.append(message_field)
    await RESPONSE.send_embedded_reply(message,
                                       title=f'CURRENT BETS',
                                       description=f"An overview of all outstanding bets",
                                       fields=message_fields)


async def close(message):
    pass


async def delete(message):
    pass


async def check_bet_status(message, bet_name, check_closed=True):
    # Returns true if bet is open
    # Returns false otherwise
    bet = []
    if not path.exists(f'BETS/{bet_name}.csv'):
        await RESPONSE.send_embedded_reply(message,
                                           title='BET CANNOT BE ACCESSED',
                                           description=f"This bet does not exist!")
        return False
    with open(f'BETS/{bet_name}.csv', newline='') as form:
        bet = list(csv.reader(form, delimiter=','))
    if len(bet[0]) == 1:
        if 'RESOLVED' in bet[0]:
            await RESPONSE.send_embedded_reply(message,
                                               title='BET CANNOT BE ACCESSED',
                                               description=f"This bet has already been resolved!")
            return False 
        elif 'CLOSED' in bet[0] and check_closed:
            await RESPONSE.send_embedded_reply(message,
                                               title='BET CANNOT BE ACCESSED',
                                               description=f"This bet has already been closed!")
            return False
    return True


BOOKIE_COMMANDS = {
        'MAKE': make,
        'BET': bet,
        'RESOLVE': resolve,
        'CHECK':check,
        'CLOSE':close,
        'DELETE':delete
}