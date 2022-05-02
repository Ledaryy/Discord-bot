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
    
    crime = random.choice([True, False])
    if crime:
        discord.send_message(WORK_CHANNEL_ID, ",crime")
    
    sleep(random.randint(10, 30))
    discord.send_message(WORK_CHANNEL_ID, ",collect")


if __name__ == '__main__':

    print('Enter your token:')
    TOKEN = input()

    discord = Discord(token=TOKEN)
    time = datetime.now()
    delay_minutes = random.randint(10, 30)
    
    # Initial Delay
    initial_delay_seconds = 60 * 60 * random.randint(1, 3) # 1-3 hours
    print(f"Initial delay: {initial_delay_seconds * 60 * 60} hours")
    sleep(initial_delay_seconds)    
    
    while True:
        if (datetime.now() - time) > timedelta(hours=4, minutes=delay_minutes):
            start_process(discord)
            time = datetime.now()
            delay_minutes = random.randint(10, 30)
        else:
            print(f"Waiting... {(datetime.now() - time)} remaining")
            sleep(10)
