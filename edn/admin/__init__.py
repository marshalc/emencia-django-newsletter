"""
Admin for edn
"""
from django.contrib import admin
from django.conf import settings

from edn.models import Contact, Newsletter, MailingList, SubscriberVerification

from edn.admin.contact import ContactAdmin
from edn.admin.newsletter import NewsletterAdmin
from edn.admin.mailinglist import MailingListAdmin
from edn.admin.mailinglist import SubscriberVerificationAdmin

admin.site.register(Contact, ContactAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(MailingList, MailingListAdmin)
admin.site.register(SubscriberVerification, SubscriberVerificationAdmin)

if settings.DEBUG:
    from edn.models import Link
    from edn.models import ContactMailingStatus

    class LinkAdmin(admin.ModelAdmin):
        list_display = ('title', 'url', 'creation_date')

    admin.site.register(Link, LinkAdmin)
    admin.site.register(ContactMailingStatus)
