from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

from .base import urlpatterns

urlpatterns += [url(r'^admin/', admin.site.urls),
                url(r'^__debug__/', include(debug_toolbar.urls))] + \
               static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
