from discord import Discord

from settings import (
    WORK_CHANNEL_ID
)

if __name__ == '__main__':
    print('Enter your token:')
    TOKEN = input()
    discord = Discord(token=TOKEN)
    
    while True:
        print("Enter message:")
        payload_message = input()
        discord.send_message(WORK_CHANNEL_ID, payload_message)
        