"""Urls for the demo of emencia.django.newsletter"""
from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls import patterns

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^$', 'django.views.generic.simple.redirect_to',{'url': '/admin/'}),
    url(r'^newsletters/', include('emencia.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', include(admin.site.urls)),
)
