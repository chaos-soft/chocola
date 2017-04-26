from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class File(models.Model):
    UPLOAD_TO = 'files/%Y/%m'
    md5 = models.CharField(max_length=32)
    file = models.FileField(upload_to=UPLOAD_TO, max_length=255)
    size = models.BigIntegerField()

    class Meta:
        index_together = ('md5', 'size')

    def __str__(self):
        return self.md5


class Link(models.Model):
    name = models.CharField(max_length=100)
    file = models.ForeignKey(File, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.name

    def url(self):
        return reverse('download', kwargs={'pk': self.id, 'name': self.name})
