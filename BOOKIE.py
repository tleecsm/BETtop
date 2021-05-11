import PARAMETERS
import RESPONSE
import csv


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
    pass


async def check(message):
    pass


async def close(message):
    pass


async def delete(message):
    pass


BOOKIE_COMMANDS = {
        'MAKE': make,
        'BET': bet,
        'RESOLVE': resolve,
        'CHECK':check,
        'CLOSE':close,
        'DELETE':delete
}