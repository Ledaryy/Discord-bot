from datetime import datetime, timedelta
from time import sleep

from sender import Sender

discord = Sender()

def start_process():
    print("Starting process...")
    discord.send_message(",work")
    sleep(31)
    discord.send_message(",crime")
    sleep(31)
    discord.send_message(",collect")


if __name__ == '__main__':
    start_process()
    time = datetime.now()
    while True:
        if (datetime.now() - time) > timedelta(hours=4):
            start_process()
            time = datetime.now()
        else:
            print("Waiting...")
            print(datetime.now() - time)
            sleep(10)



