import uuid
import logging
import celery

from celery import shared_task
from .models import Bot
from .models.bots import Bot, BotRoles

from datetime import datetime, timedelta

from .bots.collecter import BotCollecter, BotCollecterCacheManager

logger = logging.getLogger(__name__)


@shared_task
def start_bot(bot_id, delay):
    logger.info(
        f"Started background task, init start bot: {bot_id}, delay: {delay}")
    try:

        eta = datetime.now() + timedelta(minutes=delay)

        celery.current_app.send_task(
            name="backend.tasks._start_bot",
            kwargs={
                "bot_id": bot_id,
            },
            eta=eta,
        )

    except Exception as e:
        logger.error(
            f"Error {e} while starting bot {bot_id}")
    logger.info(f"Finished background init start bot for bot: {bot_id}")


@shared_task()
def _start_bot(bot_id: int):

    logger.info(f"Started background start bot for bot: {bot_id}")

    bot = Bot.objects.get(id=bot_id)
    bot.is_active = True
    bot.save()


    if bot.role == BotRoles.disabled:
        logger.info(f"This bot is disabled: {bot}")
    if bot.role == BotRoles.collecter:
        cache = BotCollecterCacheManager(bot)
        cache.start_collecter()
        send_and_reschedule_collect(bot_id)

    logger.info(f"Finished background start bot task for bot: {bot_id}")


@shared_task()
def send_and_reschedule_collect(bot_id: int):
    logger.info(f"Started background collect task for bot: {bot_id}")

    bot = Bot.objects.get(id=bot_id)

    if bot.is_active:
        bot_collecter = BotCollecter(bot)
        bot_collecter.collect()

        reschedule_collect_task(bot)
    else:
        logger.info(f"Finished collect task for bot: {bot}")

    logger.info(f"Finished background collect task for bot: {bot_id}")


def reschedule_collect_task(bot: Bot):
    logger.info(f"Started background reshedule task for bot: {bot}")

    delay = bot.get_collecter_delay_in_seconds()
    eta = datetime.now() + timedelta(seconds=delay)
    task_uniq_id = uuid.uuid4()
    task_uniq_id = str(task_uniq_id)

    cache = BotCollecterCacheManager(bot)
    cache.set_next_collect_task(task_uniq_id, eta, delay)
    cache.log_cache()

    celery.current_app.send_task(
        name="backend.tasks.send_and_reschedule_collect",
        kwargs={
            "bot_id": bot.id,
        },
        task_id=task_uniq_id,
        eta=eta,
    )

    logger.info(f"Finished background reshedule task for bot: {bot}")


@shared_task
def stop_bot(bot_id, delay):
    logger.info(
        f"Started initial background stop task for bot: {bot_id}, delay: {delay}")

    eta = datetime.now() + timedelta(minutes=delay)

    celery.current_app.send_task(
        name="backend.tasks._stop_bot",
        kwargs={
            "bot_id": bot_id,
        },
        eta=eta,
    )

    logger.info(f"Finished initial background stop task for bot: {bot_id}")


@shared_task
def _stop_bot(bot_id):
    from webhost.celery import app
    logger.info(f"Started background stop task for bot: {bot_id}")

    bot = Bot.objects.get(id=bot_id)
    bot.is_active = False
    bot.save()
    
    if bot.role == BotRoles.collecter:
        cache = BotCollecterCacheManager(bot)

        if cache.collecter_active:
            task_id = cache.get_next_collect_task()
            app.control.revoke(task_id, terminate=True)
            logger.info(f"Revoked task {task_id}")
            
        cache.delete_cache()


    logger.info(f"Finished background stop task for bot: {bot_id}")
