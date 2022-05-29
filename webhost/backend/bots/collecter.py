#
# Author: Andrew Kulishov <support@andrewkulishov.com>
# Copyright (C) 2022 Andrew Kulishov - All Rights Reserved
# 
# Created on Sun May 29 2022
# 
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# 
# If there are any issues contact me on the email above.
#


import random
import logging
from time import sleep
from utils.discord import DiscordAndSearch
from utils.parsers import Extractor
from backend.settings import (
    WORK_CHANNEL_ID,
    UNBELIEVABOAT_BOT_ID
)
from django.core.cache import cache
from datetime import datetime
from backend.models import MoneyLog, ErrorLog

logger = logging.getLogger(__name__)


class BotTools(DiscordAndSearch, Extractor):

    def __init__(self, bot=None):
        self.bot = bot
        self.token = bot.token

    def collect_work(self):
        success, error_body = self.send_message(WORK_CHANNEL_ID, ",work")
        self.save_result(success, error_body, "work")
        
    def collect_crime(self):
        success, error_body = self.send_message(WORK_CHANNEL_ID, ",crime")
        self.save_result(success, error_body, "crime")

    def collect_collect_daily(self):
        success_coll, error_body_coll = self.send_message(WORK_CHANNEL_ID, ",collect")
        success_bal, error_body_bal = self.send_message(WORK_CHANNEL_ID, ",bal")
        if success_coll and success_bal:
            self.save_result(True, error_body_bal, "collect")
        else:
            error_body = error_body_coll + error_body_bal
            error = ErrorLog(
                owner=self.bot,
                comment=f"Error while collecting daily",
                body=error_body
            )
            error.save()   
                         
    def save_result(self, success, error_body, operation):
        if success:
            logger.info(f"Successfully collected {operation}")
            sleep(3)
            message = self.get_latest_money_bot_message(
                WORK_CHANNEL_ID,
                UNBELIEVABOAT_BOT_ID,
                self.bot.name
            )
            if message:
                
                if operation == "work":
                    value = self.extract_work_money_value(message)
                    if value:
                        MoneyLog.save_work(self.bot, value)
                elif operation == "crime":
                    crime_sucess, value = self.extract_crime_money_value(message)
                    if value:
                        MoneyLog.save_crime(self.bot, crime_sucess, value)
                elif operation == "collect":
                    cash, bank = self.extract_collect_money_value(message)
                    if cash and bank:
                        MoneyLog.save_collect(self.bot, cash, bank)
                else:
                    logger.info(f"No money found in message: {message}")
                    error = ErrorLog(
                        owner=self.bot,
                        comment=f"No money found in message, operation: {operation}",
                        body=message
                    )
                    error.save()
            else:
                logger.info(f"No message found")
                error = ErrorLog(
                    owner=self.bot,
                    comment="No message found"
                )
                error.save()
        else:
            error = ErrorLog(
                owner=self.bot,
                comment=f"Error while completing {operation}",
                body=error_body
            )
            error.save()


class BotCacheManager():

    CACHE_TEMPLATE = {
        "bot_id": None,
        "bot_name": None,
        "reserve_chat": {
            "reserved": False,
            "reason": None,
            "time": datetime.now(),
        }
    }

    def __init__(self, bot):
        self.bot = bot
        self.cache_key = f"CACHE_{self.bot.id}"

        self.cache = cache.get(self.cache_key)
        if self.cache is None:
            self.cache = self.CACHE_TEMPLATE
            self.cache["bot_id"] = self.bot.id
            self.cache["bot_name"] = self.bot.name
            cache.set(self.cache_key, self.cache)
            logger.info(f"Cache created: {self.cache}")
        else:
            logger.info(f"Cache found: {self.cache}")

    def reserve(self, reason):
        logger.info("Reserving chat")
        self.cache = cache.get(self.cache_key)
        
        self.cache["reserve_chat"]["reserved"] = True
        self.cache["reserve_chat"]["reason"] = reason
        self.cache["reserve_chat"]["time"] = datetime.now()
        
        cache.set(self.cache_key, self.cache)
        
    def release(self):
        logger.info("Releasing chat")
        self.cache = cache.get(self.cache_key)
        
        self.cache["reserve_chat"]["reserved"] = False
        self.cache["reserve_chat"]["reason"] = None
        self.cache["reserve_chat"]["time"] = datetime.now()
        
        cache.set(self.cache_key, self.cache)
        
    @property
    def is_reserved(self):
        self.cache = cache.get(self.cache_key)
        return self.cache["reserve_chat"]["reserved"]
    
    def refresh_cache(self):
        self.cache = cache.get(self.cache_key)
        logger.info(f"Cache refreshed: {self.cache}")

    def delete_cache(self):
        cache.delete(self.cache_key)
        logger.info(f"Cache deleted: {self.cache_key}")

    def log_cache(self):
        self.cache = cache.get(self.cache_key)
        logger.info(f"Cache: {self.cache}")
