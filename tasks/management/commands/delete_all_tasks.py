from django.core.management.base import BaseCommand

from tasks.common import delete_all_tasks


class Command(BaseCommand):

    def handle(self, *args, **options):
        delete_all_tasks()
