import os
from dotenv import load_dotenv

load_dotenv()

#TOKEN = os.environ['TOKEN']
WORK_CHANNEL_ID = os.environ['WORK_CHANNEL_ID']
BUMP_CHANNEL_ID = os.environ['BUMP_CHANNEL_ID']
ANIHOUSE_BOT_ID = os.environ['ANIHOUSE_BOT_ID']
BOT_NAME_TAG = os.environ['BOT_NAME_TAG']

BUMP_NAMES = {
    "UP": "S.up", 
    "BUMP": "Bump", 
    "LIKE": "Like"
    }