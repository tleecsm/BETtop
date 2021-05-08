import PARAMETERS
import csv


async def handler(message):
    if message.content.startswith(f'{PARAMETERS.COMMAND_PREFIX}IRS'):
        message_split = message.content.split()
        # Check if this is an IRS command
        if len(message_split) < 2:
            return
        if message_split[1] == 'ENROLL':
            await enroll(message)
        elif message.author.guild_permissions.administrator:
            if len(message_split) < 3:
                return
            if message_split[1] in IRS_COMMANDS:
                await IRS_COMMANDS[message_split[1]](message)
    generate_income(message)


async def generate_income(message):
    with open('IRS_FORM.csv', newline='') as form:
        IRS_form = list(csv.reader(form, delimiter=','))

    # Check if message is from a legal user
    legal_users = [row[PARAMETERS.USER_ID_POSITION] for row in IRS_form]
    if str(message.author.id) in legal_users:
        # Check if message is in a legal channel
        if str(message.channel.id) in IRS_form[0]:
            # Grab their award for the post
            user_position = legal_users.index(str(message.author.id))
            channel_position = IRS_form[0].index(str(message.channel.id))
            award = IRS_form[user_position][channel_position]

            # Reduce their next award for this channel
            if award == PARAMETERS.UNIQUE_CHANNEL_AWARD:
                # This was their first post of the day here
                IRS_form[user_position][channel_position] = PARAMETERS.REPEAT_CHANNEL_AWARD
            elif 0 < award <= PARAMETERS.REPEAT_CHANNEL_AWARD:
                # This is not their first post
                IRS_form[user_position][channel_position] -= PARAMETERS.REPEAT_CHANNEL_DIMINISH
            else:
                # They've hit their max posts in this channel
                return

            # Check their daily max
            current_profit = IRS_form[user_position][PARAMETERS.USER_MAX_POSITION]
            if current_profit < PARAMETERS.DAILY_CURRENCY_MAX:
                current_profit += award
                if current_profit > PARAMETERS.DAILY_CURRENCY_MAX:
                    # Do not let them exceed the max daily income
                    current_profit = PARAMETERS.DAILY_CURRENCY_MAX
                IRS_form[user_position][PARAMETERS.USER_MAX_POSITION] = current_profit
                with open('IRS_FORM.csv', 'w', newline='') as form:
                    IRS_writer = csv.writer(form, delimiter=',')
                    IRS_writer.writerows(IRS_form)
            else:
                # They've hit the max daily income
                return


async def watch_channel(message):
    message_split = message.content.split()[2:]
    IRS_form = []
    with open('IRS_FORM.csv', newline='') as form:
        IRS_form = list(csv.reader(form, delimiter=','))

    for channel in message_split:
        # Sanitize the input
        channel = channel[2:-1]
        # Check if the channel is already tracked
        if channel in IRS_form[0]:
            continue
        # Add the channel to the headers
        IRS_form[0].append(channel)
        # Give each user a new value for this channel
        for row in range(1,len(IRS_form)):
            IRS_form[row].append(PARAMETERS.UNIQUE_CHANNEL_AWARD)

    with open('IRS_FORM.csv', 'w', newline='') as form:
        IRS_writer = csv.writer(form, delimiter=',')
        IRS_writer.writerows(IRS_form)

    current_channel_string = ''
    for channel in IRS_form[0][2:]:
        current_channel_string += f'<#{channel}>'

    await message.channel.send(f'UPDATED MY WATCHLIST.  ' + 
                               f'I AM CURRENTLY WATCHING THESE CHANNELS:\n' +
                               current_channel_string)


async def forget_channel(message):
    message_split = message.content.split()[2:]
    IRS_form = []
    with open('IRS_FORM.csv', newline='') as form:
        IRS_form = list(csv.reader(form, delimiter=','))

    for channel in message_split:
        # Sanitize the input
        channel = channel[2:-1]
        # Only continue if the channel is tracked
        if not channel in IRS_form[0]:
            continue
        # Find its position
        remove_index = IRS_form[0].index(channel)
        # Remove each value in this column
        for row in range(len(IRS_form)):
            IRS_form[row].pop(remove_index)

    with open('IRS_FORM.csv', 'w', newline='') as form:
        IRS_writer = csv.writer(form, delimiter=',')
        IRS_writer.writerows(IRS_form)

    current_channel_string = ''
    for channel in IRS_form[0][2:]:
        current_channel_string += f'<#{channel}>'

    await message.channel.send(f'UPDATED MY WATCHLIST.  ' + 
                               f'I AM CURRENTLY WATCHING THESE CHANNELS:\n' +
                               current_channel_string)


async def enroll(message):
    user = str(message.author.id)
    IRS_form = []
    with open('IRS_FORM.csv', newline='') as form:
        IRS_form = list(csv.reader(form, delimiter=','))

    # Check to make sure the user isn't already enrolled
    for row in IRS_form:
        if user in row:
            return

    # Add the user to the form
    new_user_row = ([user, PARAMETERS.ENROLL_AWARD, PARAMETERS.ENROLL_AWARD] + 
                    [PARAMETERS.UNIQUE_CHANNEL_AWARD for i in range(len(IRS_form[0])-2)])

    IRS_form.append(new_user_row)

    with open('IRS_FORM.csv', 'w', newline='') as form:
        IRS_writer = csv.writer(form, delimiter=',')
        IRS_writer.writerows(IRS_form)

    await message.channel.send(f'YOUR ACCOUNT HAS BEEN OPENED.')

def daily_management():
    # This function handles all daily tasks (run at UTC Midnight)
    IRS_form = []
    with open('IRS_FORM.csv', newline='') as form:
        IRS_form = list(csv.reader(form, delimiter=','))

    for i in range(1,len(IRS_form)):
        # Add daily pay
        user_row = IRS_form[i]
        user_row[PARAMETERS.USER_CURRENCY_POSITION] += PARAMETERS.DAILY_CURRENCY
        user_row[PARAMETERS.USER_ALL_TIME_CURRENCY] += PARAMETERS.DAILY_CURRENCY
        # Add payout from yesterday
        user_row[PARAMETERS.USER_CURRENCY_POSITION] += user_row[PARAMETERS.USER_MAX_POSITION]
        user_row[PARAMETERS.USER_ALL_TIME_CURRENCY] += user_row[PARAMETERS.USER_MAX_POSITION]
        # Reset payout for today
        user_row[PARAMETERS.USER_MAX_POSITION] = 0
        for j in range(PARAMETERS.USER_ALL_TIME_CURRENCY+1, len(user_row)):
            user_row[j] = PARAMETERS.UNIQUE_CHANNEL_AWARD
        IRS_form[i] = user_row

    with open('IRS_FORM.csv', 'w', newline='') as form:
        IRS_writer = csv.writer(form, delimiter=',')
        IRS_writer.writerows(IRS_form)


IRS_COMMANDS = {
        'WATCH_CHANNEL': watch_channel,
        'FORGET_CHANNEL': forget_channel,
}