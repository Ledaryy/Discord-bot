import random
import logging
from datetime import datetime, timedelta
from time import sleep
from utils.discord import Discord
from webhost.settings import (
    WORK_CHANNEL_ID,
    LOGGER_FORMAT
)

logger = logging.getLogger(__name__)



class BotCollecter(Discord):

    def __init__(self, delay=False, bot=None):
        self.delay = delay
        self.bot = bot
        self.collecter_time = datetime.now()
        # self.init_arg_parser()

    def collect(self):
        logger.info(f"Collect loop started")

        # self.send_message(WORK_CHANNEL_ID, ",work")

        # crime = random.choice([True, False])
        # if crime:
        #     logging.debug("Crime function triggered")
        #     sleep(random.randint(10, 30))
        #     self.send_message(WORK_CHANNEL_ID, ",crime")

        # sleep(random.randint(10, 30))
        # self.send_message(WORK_CHANNEL_ID, ",collect")

    def initial_delay(self):
        if self.delay:
            initial_delay_seconds = 60 * 60 * \
                round(random.uniform(0, 3), 5)  # 0-3 hours, 5 decimals places
            logging.info(
                f"Initial delay started: {initial_delay_seconds} seconds")
            sleep(initial_delay_seconds)
        else:
            logging.info("Initial delay skipped")

    def get_collecter_delay(self):
        # 0-30 minutes, 5 decimal places
        delay_minutes = round(random.uniform(0, 30), 5)
        return timedelta(hours=4, minutes=delay_minutes)

    def start_collection_loop(self):
        logging.info("Collection loop started")

        self.initial_delay()
        self.collect()

        delay = self.get_collecter_delay()

        while True:
            if (datetime.now() - self.collecter_time) > delay:
                self.collect()
                self.collecter_time = datetime.now()
                delay = self.get_collecter_delay()
            else:
                logging.info(
                    f"Waiting... {(datetime.now() - self.collecter_time)} passed")
                sleep(30)


if __name__ == '__main__':

    bot_collecter = BotCollecter()
    bot_collecter.start_collection_loop()
