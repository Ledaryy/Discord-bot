from celery import shared_task
from .models import Bot
from time import sleep

@shared_task
def start_collect(bot_id, delay):
    print(f"Will start collect for bot {bot_id} in {delay} minutes")

    sleep(delay * 60)
    bot = Bot.objects.get(id=bot_id)
    bot.is_active = True
    bot.save()
    print(f"Started collect for bot {bot_id}")

@shared_task   
def stop_collect(bot_id, delay):
    print(f"Will stop collect for bot {bot_id} in {delay} minutes")
    
    sleep(delay * 60)
    bot = Bot.objects.get(id=bot_id)
    bot.is_active = False
    bot.save()
    print(f"Stopped collect for bot {bot_id}")