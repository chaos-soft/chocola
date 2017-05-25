import random
import logging

from django.contrib.auth.models import User

from .models import Task


def add_tasks(*args):
    """Добавляет три задачи для каждого пользователя в системе."""
    tasks = []

    for user in User.objects.all():
        tasks += [Task(task=task * 5, user=user) for task in 'xyz']

    Task.objects.bulk_create(tasks) if tasks else None


def delete_all_tasks(*args):
    Task.objects.all().delete()


def is_chance(percentage=0):
    """Возвращает True с процентной вероятностью либо False."""
    try:
        return not random.randrange(100 // percentage)
    except Exception as e:
        logger = logging.getLogger('django')
        logger.info(e, exc_info=True)
        return False
