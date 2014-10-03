"""
Admin for emencia
"""
from django.contrib import admin
from django.conf import settings

from emencia.models import Contact
from emencia.models import Newsletter
from emencia.models import MailingList
from emencia.models import SubscriberVerification

from emencia.settings import USE_WORKGROUPS

from emencia.admin.contact import ContactAdmin
from emencia.admin.newsletter import NewsletterAdmin
from emencia.admin.mailinglist import MailingListAdmin
from emencia.admin.mailinglist import SubscriberVerificationAdmin

admin.site.register(Contact, ContactAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(MailingList, MailingListAdmin)
admin.site.register(SubscriberVerification, SubscriberVerificationAdmin)

if USE_WORKGROUPS:
    from emencia.models import WorkGroup
    from emencia.admin.workgroup import WorkGroupAdmin

    admin.site.register(WorkGroup, WorkGroupAdmin)

if settings.DEBUG:
    from emencia.models import Link
    from emencia.models import ContactMailingStatus

    class LinkAdmin(admin.ModelAdmin):
        list_display = ('title', 'url', 'creation_date')

    admin.site.register(Link, LinkAdmin)
    admin.site.register(ContactMailingStatus)
