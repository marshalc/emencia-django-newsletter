"""
Urls for the emencia Newsletter
"""
from django.conf.urls import url
from django.conf.urls import patterns

urlpatterns = patterns(
    'emencia.views.newsletter',
    url(r'^preview/(?P<slug>[-\w]+)/$', 'view_newsletter_preview', name='newsletter_newsletter_preview'),
    url(r'^public/(?P<slug>[-\w]+)/$', 'view_newsletter_public', name='newsletter_newsletter_public'),
    url(
        r'^(?P<slug>[-\w]+)/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'view_newsletter_contact',
        name='newsletter_newsletter_contact'
    ),
)
