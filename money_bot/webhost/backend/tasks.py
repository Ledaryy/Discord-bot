import uuid
import logging
import celery

from celery import shared_task
from .models import Bot
from .models.bots import Bot, BotRoles

from time import sleep
from django.core.cache import cache
from datetime import datetime, timedelta
# from webhost.utils.discord import Discord

from .bots.collecter import BotCollecter

logger = logging.getLogger(__name__)


@shared_task
def start_bot(bot_id, delay):
    logger.info(
        f"Started background task, init start bot {bot_id}, delay: {delay}")
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
    logger.info(f"Finished background init start bot for {bot_id}")


@shared_task()
def _start_bot(bot_id: int):
    
    logger.info(f"Started background start bot task {bot_id}")

    bot = Bot.objects.get(id=bot_id)
    bot.is_active = True
    bot.save()
    
    CACHE_TEMPLATE = {
        "bot_name": bot.name,
        "bot_id": bot.id,
        "started_at": datetime.now(),
        "collecter": {
            "active": False,
            "next_task_id": None,
            "next_task_eta": None,
            "next_task_eta_seconds": None,
        }
    }
    
    cache.set(f"bot_{bot.id}", CACHE_TEMPLATE)
    

    if bot.role == BotRoles.disabled:
        logger.info(f"This bot is disabled: {bot}")
    if bot.role == BotRoles.collecter:
        send_and_reschedule_collect(bot_id)
        
    logger.info(f"Finished background start bot task {bot_id}")


@shared_task()
def send_and_reschedule_collect(bot_id: int):
    logger.info(f"Started background collect task for bot {bot_id}")

    bot = Bot.objects.get(id=bot_id)
    
    if bot.is_active:
        BotCollecter(
            bot=bot
        ).collect()

        bot_cache = cache.get(f"bot_{bot.id}")
        bot_cache['collecter']['active'] = True
        cache.set(f"bot_{bot.id}", bot_cache)
        
        reschedule_collect_task(bot)
    else:
        logger.info(f"Finished collect task for bot {bot}")

    logger.info(f"Finished background collect task for bot {bot_id}")


def reschedule_collect_task(bot: Bot):
    logger.info(f"Started reshedule background collect task for bot {bot}")

    delay = bot.get_collecter_delay_in_seconds()
    eta = datetime.now() + timedelta(seconds=delay)
    task_uniq_id = uuid.uuid4()
    task_uniq_id = str(task_uniq_id)
    
    bot_cache = cache.get(f"bot_{bot.id}")
    
    bot_cache["collecter"]["next_task_id"] = task_uniq_id
    bot_cache["collecter"]["next_task_eta"] = eta
    bot_cache["collecter"]["next_task_eta_seconds"] = delay
    
    cache.set(f"bot_{bot.id}", bot_cache)
    
    logger.info(f"Cache resh task: {bot_cache}")
    
    celery.current_app.send_task(
        name="backend.tasks.send_and_reschedule_collect",
        kwargs={
            "bot_id": bot.id,
        },
        task_id=task_uniq_id,
        eta=eta,
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
    from webhost.celery import app
    logger.info(f"Started background stop task for bot {bot_id}")
    
    bot = Bot.objects.get(id=bot_id)
    bot.is_active = False
    bot.save()
    
    bot_cache = cache.get(f"bot_{bot.id}")
    
    if bot_cache['collecter']['active']:
        app.control.revoke(bot_cache['collecter']['next_task_id'])
        logger.info(f"Task revoked: {bot_cache['collecter']['next_task_id']}")
    
    logger.info(f"Cache: {bot_cache}")
    
    cache.delete(f"bot_{bot.id}")

    logger.info(f"Finished background stop task for bot {bot_id}")