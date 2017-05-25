import logging

from django.http import HttpResponse, HttpResponseBadRequest
from django.db import transaction
from django.utils import timezone

from .models import Task
from .common import is_chance


def test1(request):
    Task.objects.create(task='a' * 5)

    try:
        with transaction.atomic():
            Task.objects.create(task='b' * 5)

            if is_chance(20):
                raise Exception('is_chance(20)')
    except Exception as e:
        logger = logging.getLogger('django')
        logger.error(e, exc_info=True)

        return HttpResponseBadRequest('<body>error</body>')

    return HttpResponse('<body>ok</body>')


def test4_2(request):
    if not request.user.is_authenticated:
        return HttpResponse('<body>401 Unauthorized</body>', status=401)

    a = Task.objects.filter(date_created=timezone.now(), is_completed=True)
    b = Task.objects.filter(date_created=timezone.now(), is_completed=True).count()
    c = Task.objects.filter(is_completed=True, user=request.user). \
        select_related('user').only('task', 'date_created', 'user__username')
    d = Task.objects.filter(date_created=timezone.now(), is_completed=False,
                            user=request.user). \
        select_related('user').only('task', 'date_created', 'user__username')

    print(a)
    print(b)
    print(c)
    print(d)

    return HttpResponse('<body>ok</body>')
