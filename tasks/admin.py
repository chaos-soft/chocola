from django.contrib import admin
from django.utils import timezone

from .models import Task
from .common import add_tasks, delete_all_tasks


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'date_created', 'user', 'is_completed')
    list_per_page = 100
    list_display_links = ('task',)
    actions = ('complete_tasks', add_tasks, delete_all_tasks)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user'). \
            only('task', 'date_created', 'user__username', 'is_completed')

    def complete_tasks(self, request, queryset):
        ids = sorted(map(int, request.POST.getlist('_selected_action')))
        id_ = min(ids)
        # Все запросы выполняются от текущего пользователя и за сегодня.
        data = dict(user=request.user, date_created=timezone.now())

        task = Task.objects.filter(id__lt=id_, **data).only('is_completed').\
            order_by('-id').first()

        # Если номера в ids идут не по порядку.
        if ids != list(range(id_, len(ids) + id_)):
            ids = (id_,)

        # Если это первая задача либо предыдущая завершена.
        if not task or task.is_completed:
            Task.objects.filter(id__in=ids, **data).update(is_completed=True)


admin.site.register(Task, TaskAdmin)
