import requests

from settings import (
    #TOKEN,
    CHANNEL_ID
)


class Sender():

    def __init__(self, token):
        self.token = token

    def send_message(self, message):

        headers = {
            "authorization": f"{self.token}"
        }

        endpoint = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"

        payload = {
            "content": f"{message}"
        }

        request_body = {
            "url": endpoint,
            "data": payload,
            "headers": headers
        }

        r = requests.post(**request_body)
        print(f"Message sent: '{message}', response: '{r}'")
