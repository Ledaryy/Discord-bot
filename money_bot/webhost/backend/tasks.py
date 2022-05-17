import logging

from celery import shared_task
from .models import Bot
from .models.bots import Bot, BotRoles

from time import sleep
from datetime import datetime, timedelta
# from webhost.utils.discord import Discord

from .bots.collecter import BotCollecter

logger = logging.getLogger(__name__)


@shared_task
def start_bot(bot_id, delay):
    logger.info(
        f"Started background bot {bot_id}, delay: {delay}")
    try:

        eta = datetime.now() + timedelta(minutes=delay)

        _start_bot.apply_async(
            eta=eta,
            kwargs={
                "bot_id": bot_id,
            },
        )

    except Exception as e:
        logger.error(
            f"Error {e} while starting bot {bot_id}")
    logger.info(f"Finished background start bot task for {bot_id}")


@shared_task()
def _start_bot(bot_id: int):
    logger.info(f"Started background collect task for bot {bot_id}")

    bot = Bot.objects.get(id=bot_id)
    bot.is_active = True
    bot.save()

    if bot.role == BotRoles.disabled:
        logger.info(f"This bot is disabled: {bot}")
    if bot.role == BotRoles.collecter:
        start_send_collect_money(bot_id)

    logger.info(f"Finished background collect task for bot {bot_id}")


@shared_task()
def start_send_collect_money(bot_id: int):
    logger.info(f"Started background collect task for bot {bot_id}")

    bot = Bot.objects.get(id=bot_id)
    
    BotCollecter(
        bot=bot
    ).collect()

    if bot.is_active:
        reshedule_send_task(bot)
    else:
        logger.info(f"Finished collect task for bot {bot}")

    logger.info(f"Finished background collect task for bot {bot_id}")


def reshedule_send_task(bot: Bot):
    logger.info(f"Started reshedule background collect task for bot {bot}")

    delay = bot.get_collecter_delay_in_seconds()
    eta = datetime.now() + timedelta(seconds=delay)
    start_send_collect_money.apply_async(
        eta=eta,
        kwargs={
            "bot_id": bot.id,
        },
    )

    logger.info(f"Finished reshedule background collect task for bot {bot}")


@shared_task
def stop_bot(bot_id, delay):
    logger.info(
        f"Started initial background stop task for bot {bot_id}, delay: {delay}")

    eta = datetime.now() + timedelta(minutes=delay)
    _stop_bot.apply_async(
        eta=eta,
        kwargs={
            "bot_id": bot_id,
        },
    )

    logger.info(f"Finished initial background stop task for bot {bot_id}")


@shared_task
def _stop_bot(bot_id):
    logger.info(f"Started background stop task for bot {bot_id}")
    
    bot = Bot.objects.get(id=bot_id)
    bot.is_active = False
    bot.save()

    logger.info(f"Finished background stop task for bot {bot_id}")