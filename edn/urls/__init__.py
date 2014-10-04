"""
Default urls for the edn
"""
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns(
    '',
    url(r'^mailing/', include('edn.urls.mailing_list')),
    url(r'^tracking/', include('edn.urls.tracking')),
    url(r'^statistics/', include('edn.urls.statistics')),
    url(r'^', include('edn.urls.newsletter')),
)
