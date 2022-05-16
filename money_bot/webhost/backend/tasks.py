from celery import Celery, shared_task

# celery = Celery('tasks', broker='redis://redis:6379/0')

@shared_task
def start_collect(id):
    print(f"Started collect for bot {id}")
    