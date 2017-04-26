from django.apps import AppConfig


class FilesConfig(AppConfig):
    name = 'files'
    verbose_name = 'Files'

    def ready(self):
        from . import signals
