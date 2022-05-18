import logging
import requests
import json

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

class Discord():

    def __init__(self, token=None):
        self.token = token

    def send_message(self, channel_id, message):

        headers = {
            "authorization": f"{self.token}"
        }

        endpoint = f"https://discord.com/api/v9/channels/{channel_id}/messages"

        payload = {
            "content": f"{message}"
        }

        request_body = {
            "url": endpoint,
            "data": payload,
            "headers": headers
        }

        r = requests.post(**request_body)

        if r.status_code != 200:
            print(f"Request wasnt sent: [{message}], response: [{r.status_code}]")
        print(f"Message sent: [{message}], response: [{r.status_code}]")
        
        
    def get_latest_messages(self, channel_id, limit=50):
        
        headers = {
            "authorization": f"{self.token}"
        }

        endpoint = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit={limit}"

        

        request_body = {
            "url": endpoint,
            "headers": headers
        }

        r = requests.get(**request_body)
        print(f"Request sent: limit: [{limit}], response: [{r.status_code}]")
        
        if r:
            return json.loads(r.text)
        else:
            raise Exception("No response")
