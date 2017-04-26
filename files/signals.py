import os

from django.db import models

from .models import File, Link


def file_post_delete(sender, instance, **kwargs):
    if os.path.isfile(instance.file.path):
        os.remove(instance.file.path)


def link_post_delete(sender, instance, **kwargs):
    total = Link.objects.filter(file_id=instance.file_id).count()
    if not total:
        File.objects.only('file').get(id=instance.file_id).delete()


models.signals.post_delete.connect(file_post_delete, sender=File)
models.signals.post_delete.connect(link_post_delete, sender=Link)
