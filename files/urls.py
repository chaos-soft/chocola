from django.conf.urls import include, url
from rest_framework import routers

from .views import LinkViewSet, DownloadView, IndexView

router = routers.DefaultRouter()
router.register(r'', LinkViewSet, base_name='files')

urlpatterns = [
    url(r'^files/', include(router.urls)),
    url(r'^files/(?P<pk>\d+)/download/(?P<name>.+)$', DownloadView.as_view(),
        name='download'),
    url(r'^$', IndexView.as_view(), name='index'),
]
