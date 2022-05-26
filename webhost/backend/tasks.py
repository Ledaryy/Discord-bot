import uuid
import logging
import celery

from celery import shared_task
from .models import Bot
from .models.bots import Bot, BotRoles

from datetime import datetime, timedelta, timezone

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
        bot.schedule.start_all()
        

    logger.info(f"Finished background start bot task for bot: {bot_id}")


@shared_task()
def execute_tasks(bot_id: int, tasks_list: list):
    logger.info(f"Started background execute task for bot: {bot_id}, tasks: {tasks_list}")

    bot = Bot.objects.get(id=bot_id)

    if bot.is_active:
        bot_collecter = BotCollecter(bot)
        
        if "work" in tasks_list:
            bot_collecter.collect_work()
            
        if "collect" in tasks_list:
            bot_collecter.collect_collect_daily()
            
        if "crime" in tasks_list:
            bot_collecter.collect_crime()
        

    else:
        logger.info(f"Bot is not active, task execution skipped: {bot}")

    logger.info(f"Finished background execute task for bot: {bot_id}")

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
    logger.info(f"Started background stop task for bot: {bot_id}")

    bot = Bot.objects.get(id=bot_id)
    bot.is_active = False
    bot.save()

    logger.info(f"Finished background stop task for bot: {bot_id}")

@shared_task
def schedule_tasks():
    logger.info("Started background schedule tasks")
    
    bots = Bot.objects.all()
    
    for bot in bots:

        if bot.is_active:
            
            if bot.role == BotRoles.collecter:
                
                diff = bot.schedule.next_work_task - datetime.now(timezone.utc)                
                if diff < timedelta(minutes=2):
                    celery.current_app.send_task(
                        name="backend.tasks.execute_tasks",
                        kwargs={
                            "bot_id": bot.id,
                            "tasks_list": ["work"],
                        },
                        eta=bot.schedule.next_work_task,
                    )
                    bot.schedule.reschedule_work()
                    
                diff = bot.schedule.next_crime_task - datetime.now(timezone.utc)                
                if diff < timedelta(minutes=2):
                    celery.current_app.send_task(
                        name="backend.tasks.execute_tasks",
                        kwargs={
                            "bot_id": bot.id,
                            "tasks_list": ["crime"],
                        },
                        eta=bot.schedule.next_crime_task,
                    )
                    bot.schedule.reschedule_crime()
                    
                diff = bot.schedule.next_collect_task - datetime.now(timezone.utc)                
                if diff < timedelta(minutes=2):
                    celery.current_app.send_task(
                        name="backend.tasks.execute_tasks",
                        kwargs={
                            "bot_id": bot.id,
                            "tasks_list": ["collect"],
                        },
                        eta=bot.schedule.next_collect_task,
                    )
                    bot.schedule.rechedule_collect()
                                            
                    
    logger.info("Finished background schedule tasks")
    