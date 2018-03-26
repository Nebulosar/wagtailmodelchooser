import wagtail.wagtailcore.urls
import wagtail.wagtailadmin.urls
from django.conf.urls import include, url

urlpatterns = [
    url(r'^admin/', include(wagtail.wagtailadmin.urls)),
    url(r'', include(wagtail.wagtailcore.urls)),
]
