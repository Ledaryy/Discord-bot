import re
import json
import random
from datetime import datetime, timedelta
from time import sleep
from discord import Discord

from settings import (
    BUMP_CHANNEL_ID,
    BUMP_NAMES,
    ANIHOUSE_BOT_ID,
    BOT_NAME_TAG
)


def get_next_target(discord):
    print("Starting process...")
    discord.send_message(BUMP_CHANNEL_ID, "когда")
    sleep(5)
    response = discord.get_latest_messages(BUMP_CHANNEL_ID, 10)

    message = message_finder(
        message_json=response,
        author_id=ANIHOUSE_BOT_ID,
        embeds_mentions=BOT_NAME_TAG
    )

    up_time, bump_time, like_time = time_extractor(
        message["embeds"][0]["description"])

    BUMP_NAMES["UP"] = up_time
    BUMP_NAMES["BUMP"] = bump_time
    BUMP_NAMES["LIKE"] = like_time

    minimal_time = min(up_time, bump_time, like_time)

    for key, val in BUMP_NAMES.items():
        if val == minimal_time:
            next_target = key

    return BUMP_NAMES, next_target


def message_finder(
    message_json,
    author_id,
    embeds_mentions=None,
):

    messages = message_json
    _messages = []

    # Finds the messages with the correct author
    for message in message_json:
        if message['author']['id'] == author_id:
            _messages.append(message)
    if _messages == []:
        raise Exception("Author sorting error")

    messages = _messages
    _messages = []

    # Finds the messages with the correct embeds
    if embeds_mentions:
        for message in messages:
            if "embeds" in message:
                if message["embeds"] != []:
                    if "author" in message['embeds'][0]:
                        if message['embeds'][0]['author']['name'] == embeds_mentions:
                            _messages.append(message)
    if _messages == []:
        raise Exception("Embeds sorting error")

    messages = _messages
    _messages = []

    if len(messages) == 0:
        raise Exception("No messages found")
    elif len(messages) >= 1:
        return messages[0]
    else:
        raise Exception("Unknown error")


def time_extractor(message):
    message_list = message.split("\n")
    clear_message_list = []
    up_time, bump_time, like_time = None, None, None

    # Exstracts the correct lines from the message
    for line in message_list:
        for key, val in BUMP_NAMES.items():
            if val in line:
                clear_message_list.append(line)

    # Fault check
    if len(clear_message_list) != 3:
        print(clear_message_list)
        raise Exception("Lenth is less than 3, incorrect message.")

    # Extracts the times from the message
    for line in clear_message_list:
        hours, minutes, seconds = 0, 0, 0
        if "час" in line:
            numbers = re.findall(r'\d+', f"{line}")
            hours = int(numbers[0])
            minutes = int(numbers[1])
            seconds = int(numbers[2])

            time_timedelta = timedelta(
                hours=hours, minutes=minutes, seconds=seconds)

        elif "минут" in line:
            numbers = re.findall(r'\d+', f"{line}")
            minutes = int(numbers[0])
            seconds = int(numbers[1])

            time_timedelta = timedelta(minutes=minutes, seconds=seconds)

        elif "секунд" in line:
            seconds = int(re.findall(r'\d+', f"{line}")[0])

            time_timedelta = timedelta(seconds=seconds)

        elif "проспали!" in line:

            time_timedelta = timedelta(hours=12)
        else:
            print(line)
            raise Exception("Cannot find times, incorrect message.")

        if time_timedelta.total_seconds() <= 0:
            print(f"{time_timedelta} is wrong")
            raise Exception("Incorrect time")

        if BUMP_NAMES["UP"] in line:
            up_time = time_timedelta
        elif BUMP_NAMES["BUMP"] in line:
            bump_time = time_timedelta
        elif BUMP_NAMES["LIKE"] in line:
            like_time = time_timedelta
        else:
            print(line)
            raise Exception("Cannot find BUMP namings, incorrect message.")

    if up_time and bump_time and like_time:
        return up_time, bump_time, like_time
    else:
        print(f"{up_time}, {bump_time}, {like_time}")
        raise Exception("Cannot find all times, incorrect message.")


if __name__ == '__main__':

    print('Enter your token:')
    TOKEN = input()

    discord = Discord(token=TOKEN)
    values, target = get_next_target(discord)

    print(values, target)
