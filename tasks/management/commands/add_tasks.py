from django.core.management.base import BaseCommand

from tasks.common import add_tasks


class Command(BaseCommand):

    def handle(self, *args, **options):
        add_tasks()
