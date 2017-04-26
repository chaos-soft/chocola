from django.contrib import admin

from .models import File, Link
from .forms import FileForm


class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'md5', 'file', 'size')
    list_per_page = 100
    list_display_links = ('md5',)
    form = FileForm


class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'file', 'user')
    list_per_page = 100
    list_display_links = ('name',)


admin.site.register(File, FileAdmin)
admin.site.register(Link, LinkAdmin)
