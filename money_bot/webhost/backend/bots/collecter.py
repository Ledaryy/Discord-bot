import random
import logging
from time import sleep
from utils.discord import Discord
from webhost.settings import (
    WORK_CHANNEL_ID
)

logger = logging.getLogger(__name__)



class BotCollecter(Discord):

    def __init__(self, delay=False, bot=None):
        self.delay = delay
        self.bot = bot
        self.token = bot.token

    def collect(self):
        logger.info(f"Collect started")

        self.send_message(WORK_CHANNEL_ID, ",work")

        crime = random.choice([True, False])
        if crime:
            logger.info("Crime function triggered")
            sleep(random.randint(5, 10))
            self.send_message(WORK_CHANNEL_ID, ",crime")

        sleep(random.randint(5, 10))
        self.send_message(WORK_CHANNEL_ID, ",collect")

        logger.info(f"Collect finished")

