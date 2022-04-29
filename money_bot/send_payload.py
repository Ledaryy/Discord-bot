from sender import Sender

if __name__ == '__main__':
    print('Enter your token:')
    TOKEN = input()
    discord = Sender(token=TOKEN)
    
    while True:
        print("Enter message:")
        payload_message = input()
        discord.send_message(payload_message)
        