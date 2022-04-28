import os
import crontab
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['TOKEN']

payload = {
    "content": "hi"
}

headers = {
    "authorization": f"{TOKEN}"
}


r = requests.post(
    "https://discord.com/api/v9/channels/969301454437355620/messages",
    data=payload,
    headers=headers
    )

print(r)