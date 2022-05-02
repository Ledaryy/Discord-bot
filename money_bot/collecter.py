import random
import argparse
from datetime import datetime, timedelta
from time import sleep
from discord import Discord

from settings import (
    WORK_CHANNEL_ID
)


def start_process(discord):
    print("Starting process...")
    discord.send_message(WORK_CHANNEL_ID, ",work")

    crime = random.choice([True, False])
    if crime:
        print("Crime!")
        sleep(random.randint(10, 30))
        discord.send_message(WORK_CHANNEL_ID, ",crime")

    sleep(random.randint(10, 30))
    discord.send_message(WORK_CHANNEL_ID, ",collect")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Collecter module')

    parser.add_argument('-d', '--no_delay',
                        help='Removes initial delay', required=False)
    parser.add_argument('-t', '--token', help='Adds token', required=False)

    args = vars(parser.parse_args())

    if args['no_delay']:
        print("No delay!")
        DELAY = False
    else:
        DELAY = True

    if args['token']:
        print("Token added!")
        TOKEN = args['token']
    else:
        TOKEN = None

    if not TOKEN:
        print('Enter your token:')
        TOKEN = input()

    discord = Discord(token=TOKEN)
    time = datetime.now()
    delay_minutes = random.randint(10, 30)

    # Initial Delay
    if DELAY:
        initial_delay_seconds = 60 * 60 * random.randint(1, 3)  # 1-3 hours
        print(f"Initial delay: {initial_delay_seconds / 60 / 60} hours")
        sleep(initial_delay_seconds)
        start_process(discord)
    else:
        start_process(discord)

    while True:
        if (datetime.now() - time) > timedelta(hours=4, minutes=delay_minutes):
            start_process(discord)
            time = datetime.now()
            delay_minutes = random.randint(10, 30)
        else:
            print(f"Waiting... {(datetime.now() - time)} passed")
            sleep(30)
