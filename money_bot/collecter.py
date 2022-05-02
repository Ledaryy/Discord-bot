import random
from datetime import datetime, timedelta
from time import sleep
from discord import Discord

from settings import (
    WORK_CHANNEL_ID
)

def start_process(discord):
    print("Starting process...")
    discord.send_message(WORK_CHANNEL_ID, ",work")
    sleep(random.randint(10, 30))
    discord.send_message(WORK_CHANNEL_ID, ",collect")


if __name__ == '__main__':

    print('Enter your token:')
    TOKEN = input()

    discord = Discord(token=TOKEN)
    time = datetime.now()
    delay_minutes = random.randint(10, 30)
    # start_process(discord)

    while True:
        if (datetime.now() - time) > timedelta(hours=4, minutes=delay_minutes):
            start_process(discord)
            time = datetime.now()
            delay_minutes = random.randint(10, 30)
        else:
            print("Waiting...")
            print(datetime.now() - time)
            sleep(10)
