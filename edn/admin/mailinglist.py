"""
ModelAdmin for MailingList
"""
from datetime import datetime

from django.conf.urls import url
from django.conf.urls import patterns
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_str
from django.utils.translation import ugettext_lazy as _

from edn.models import Contact, MailingList

class MailingListAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    list_display = ('name', 'creation_date', 'description', 'subscribers_count', 'unsubscribers_count')
    list_filter = ('creation_date', 'modification_date')
    search_fields = ('name', 'description',)
    filter_horizontal = ['subscribers', 'unsubscribers']
    fieldsets = (
        (None, {'fields': ('name', 'description',)}),
        (None, {'fields': ('subscribers',)}),
        (None, {'fields': ('unsubscribers',)}),
    )
    actions = ['merge_mailinglist']
    actions_on_top = False
    actions_on_bottom = True

    def get_queryset(self, request):
        queryset = super(MailingListAdmin, self).get_queryset(request)
        return queryset

    def save_model(self, request, mailinglist, form, change):
        mailinglist.save()

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # if 'subscribers' in db_field.name and not request.user.is_superuser and USE_WORKGROUPS:
        #     contacts_pk = request_workgroups_contacts_pk(request)
        #     kwargs['queryset'] = Contact.objects.filter(pk__in=contacts_pk)
        return super(MailingListAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs)

    def merge_mailinglist(self, request, queryset):
        """Merge multiple mailing list"""
        if queryset.count() == 1:
            self.message_user(request, _('Please select at least 2 mailing lists.'))
            return None

        subscribers = {}
        unsubscribers = {}
        for ml in queryset:
            for contact in ml.subscribers.all():
                subscribers[contact] = ''
            for contact in ml.unsubscribers.all():
                unsubscribers[contact] = ''

        when = str(datetime.now()).split('.')[0]
        new_mailing = MailingList(name=_('Merging list at %s') % when,
                                  description=_('Mailing list created by merging at %s') % when)
        new_mailing.save()
        new_mailing.subscribers = subscribers.keys()
        new_mailing.unsubscribers = unsubscribers.keys()

        self.message_user(request, _('%s successfully created by merging.') % new_mailing)
        urlname = 'admin:%s_mailinglist_change' % self.opts.app_label
        return HttpResponseRedirect(reverse(urlname, args=[new_mailing.pk]))
    merge_mailinglist.short_description = _('Merge selected mailinglists')

    # def export_links(self, mailinglist):
    #     """Display links for export"""
    #     return u'<a href="%s">%s</a> / <a href="%s">%s</a>' % (
    #         reverse('admin:%s_mailinglist_export_excel' % self.opts.app_label,
    #                 args=[mailinglist.pk]), _('Excel'),
    #         reverse('admin:%s_mailinglist_export_vcard' % self.opts.app_label,
    #                 args=[mailinglist.pk]), _('VCard'))
    # export_links.allow_tags = True
    # export_links.short_description = _('Export')

    # def exportion_vcard(self, request, mailinglist_id):
    #     """Export subscribers in the mailing in VCard"""
    #     mailinglist = get_object_or_404(MailingList, pk=mailinglist_id)
    #     name = 'contacts_%s' % smart_str(mailinglist.name)
    #     return vcard_contacts_export_response(mailinglist.subscribers.all(), name)

    # def exportion_excel(self, request, mailinglist_id):
    #     """Export subscribers in the mailing in Excel"""
    #     mailinglist = get_object_or_404(MailingList, pk=mailinglist_id)
    #     name = 'contacts_%s' % smart_str(mailinglist.name)
    #     return ExcelResponse(mailinglist.subscribers.all(), name)

    def get_urls(self):
        urls = super(MailingListAdmin, self).get_urls()
        my_urls = patterns(
            '',
            # url(r'^export/vcard/(?P<mailinglist_id>\d+)/$',
            #     self.admin_site.admin_view(self.exportion_vcard),
            #     name='%s_mailinglist_export_vcard' % self.opts.app_label),
            # url(r'^export/excel/(?P<mailinglist_id>\d+)/$',
            #     self.admin_site.admin_view(self.exportion_excel),
            #     name='%s_mailinglist_export_excel' % self.opts.app_label),
        )
        return my_urls + urls


class SubscriberVerificationAdmin(admin.ModelAdmin):
    readonly_fields = ("link_id",)
    fields = ['link_id', 'contact']
