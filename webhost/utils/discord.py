import logging
import requests
import json

logger = logging.getLogger(__name__)


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

class DiscordAndSearch(Discord):
    
    def get_latest_money_bot_message(
        self, 
        channel_id,
        author_id,
        bot_name
    ):
        
        response_json = self.get_latest_messages(channel_id, limit=20)
        if response_json:
            bot_messages = self.search_for_author(response_json, author_id)
        else:
            return None
        
        if bot_messages:
            mentioned_by_bot_messages = self.search_mentioned_in_embeds(bot_messages, bot_name)
        else:
            return None
        
        if mentioned_by_bot_messages:
            sorted_by_newest = self.sort_by_newest(mentioned_by_bot_messages)
            return sorted_by_newest[0]        
        else:
            return None
    
    def search_for_author(self, response_json, author_id):
        
        if len(response_json) < 2:
            return response_json
        
        messages = []
        
        for message in response_json:
            if "author" in message:
                if message["author"]["id"] == author_id:
                    messages.append(message)

        return messages
    
    def search_mentioned_in_embeds(self, response_json, bot_name):
        
        if len(response_json) < 2:
            return response_json
        
        messages = []
        
        for message in response_json:
            if "embeds" in message:
                if message["embeds"] != []:
                    if "author" in message['embeds'][0]:
                        if message['embeds'][0]['author']['name'] == bot_name:
                            messages.append(message)
        
        return messages
    
    def sort_by_newest(self, response_json):
        
        if len(response_json) < 2:
            return response_json
        
        # Buble sort by timestamp in descending order
        for i in range(len(response_json) - 1):
            for j in range(len(response_json) - i - 1):
                if response_json[j]["timestamp"] < response_json[j + 1]["timestamp"]:
                    response_json[j], response_json[j + 1] = response_json[j + 1], response_json[j]
        
        return response_json
