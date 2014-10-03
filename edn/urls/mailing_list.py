"""
Urls for the edn Mailing List
"""
from django.conf.urls import patterns
from django.conf.urls import url

from edn.forms import AllMailingListSubscriptionForm
from edn.forms import MailingListSubscriptionForm
from edn.forms import SubscriberVerificationForm
from edn.forms import VerificationMailingListSubscriptionForm

urlpatterns = patterns(
    'edn.views.mailing_list',
    url(
        r'^unsubscribe/(?P<slug>[-\w]+)/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'view_mailinglist_unsubscribe',
        name='newsletter_mailinglist_unsubscribe'
    ),
    url(
        r'^subscribe/(?P<mailing_list_id>\d+)/',
        'view_mailinglist_subscribe',
        {'form_class': MailingListSubscriptionForm},
        name='newsletter_mailinglist_subscribe'
    ),
    url(
        r'^subscribe/',
        'view_mailinglist_subscribe',
        {'form_class': AllMailingListSubscriptionForm},
        name='newsletter_mailinglist_subscribe_all'
    ),
    url(
        r'^$',
        'view_subscriber_verification',
        {'form_class': SubscriberVerificationForm},
        name='newsletter_subscriber_verification',
    ),
    url(
        r'^(?P<link_id>[\w-]+)/$',
        'view_uuid_verification',
        {'form_class': VerificationMailingListSubscriptionForm},
        name='newsletter_subscriber_verification',
    ),
)
