import os

# Bots settings
WORK_CHANNEL_ID = os.environ.get("WORK_CHANNEL_ID")
BUMP_CHANNEL_ID = os.environ.get("BUMP_CHANNEL_ID")
ANIHOUSE_BOT_ID = os.environ.get("ANIHOUSE_BOT_ID")
UNBELIEVABOAT_BOT_ID = os.environ.get("UNBELIEVABOAT_BOT_ID")
BOT_NAME_TAG = os.environ.get("BOT_NAME_TAG")

BUMP_NAMES = {"UP": "S.up", "BUMP": "Bump", "LIKE": "Like"}

BUMP_COMMANDS = {"UP": "!up", "BUMP": "!bump", "LIKE": "!like"}

COMMANDS_ENABLED = ["LIKE"]
