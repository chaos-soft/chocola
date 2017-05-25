from django.conf.urls import url

from .views import test1, test4_2

urlpatterns = [
    url(r'^test1$', test1, name='tasks_test1'),
    url(r'^test4_2$', test4_2, name='tasks_test4_2'),
]
