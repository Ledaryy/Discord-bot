import random
from datetime import datetime, timedelta
from time import sleep
from sender import Sender


def start_process(discord):
    print("Starting process...")
    discord.send_message(",work")
    sleep(random.randint(10, 30))
    discord.send_message(",collect")


if __name__ == '__main__':

    print('Enter your token:')
    TOKEN = input()

    discord = Sender(token=TOKEN)
    start_process(discord)

    time = datetime.now()
    while True:
        delay_minutes = random.randint(10, 30)
        if (datetime.now() - time) > timedelta(hours=4, minutes=delay_minutes):
            start_process(discord)
            time = datetime.now()
        else:
            print("Waiting...")
            print(datetime.now() - time)
            sleep(10)
