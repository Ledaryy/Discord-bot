import random
import logging
from time import sleep
from utils.discord import Discord
from webhost.settings import (
    WORK_CHANNEL_ID
)
from django.core.cache import cache
from datetime import datetime

logger = logging.getLogger(__name__)


class BotCollecter(Discord):

    def __init__(self, bot=None):
        self.bot = bot
        self.token = bot.token

    def send_collect(self):
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


class BotCollecterCacheManager():

    CACHE_TEMPLATE = {
        "bot_name": None,
        "bot_id": None,
        "started_at": datetime.now(),
        "collecter": {
            "active": False,
            "next_task_id": None,
            "next_task_eta": None,
            "next_task_eta_seconds": None,
        }
    }

    def __init__(self, bot):
        self.bot = bot
        self.cache_key = f"bot_{self.bot.id}_collecter"

        self.cache = cache.get(self.cache_key)
        if self.cache is None:
            self.cache = self.CACHE_TEMPLATE
            self.cache["bot_name"] = self.bot.name
            self.cache["bot_id"] = self.bot.id
            cache.set(self.cache_key, self.cache)
            logger.info(f"Cache created: {self.cache}")
        else:
            logger.info(f"Cache found: {self.cache}")


    def start_collecter(self):
        self.cache = cache.get(self.cache_key)
        self.cache["collecter"]["active"] = True
        cache.set(self.cache_key, self.cache)
        
    @property
    def collecter_active(self):
        self.cache = cache.get(self.cache_key)
        return self.cache["collecter"]["active"]
    
    def set_next_collect_task(self, task_id, task_eta, delay):
        self.cache = cache.get(self.cache_key)
        self.cache["collecter"]["next_task_id"] = task_id
        self.cache["collecter"]["next_task_eta"] = task_eta
        self.cache["collecter"]["next_task_eta_seconds"] = delay
        cache.set(self.cache_key, self.cache)

    def get_next_collect_task(self):
        self.cache = cache.get(self.cache_key)
        return self.cache["collecter"]["next_task_id"]

    def delete_cache(self):
        cache.delete(self.cache_key)
        logger.info(f"Cache deleted: {self.cache_key}")

    def log_cache(self):
        self.cache = cache.get(self.cache_key)
        logger.info(f"Cache: {self.cache}")
