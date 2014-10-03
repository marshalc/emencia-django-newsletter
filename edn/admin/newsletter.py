"""
ModelAdmin for Newsletter
"""
from HTMLParser import HTMLParseError

from django import forms
from django.db.models import Q
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from tinymce.widgets import TinyMCE

from edn.models import Contact, Newsletter
from edn.settings import DEFAULT_HEADER_SENDER, DEFAULT_HEADER_REPLY, TINYMCE_WIDGET_ATTRS


class BaseNewsletterAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    list_display = ('title', 'mailing_list', 'status', 'sending_date', 'creation_date', 'modification_date',
                    'historic_link', 'statistics_link')
    list_filter = ('status', 'sending_date', 'creation_date', 'modification_date')
    search_fields = ('title', 'content', 'header_sender', 'header_reply')
    filter_horizontal = ['test_contacts']
    fieldsets = (
        (None, {'fields': ('title', 'template', 'content',)}),
        (_('Receivers'), {'fields': ('mailing_list', 'test_contacts',)}),
        (_('Sending'), {'fields': ('sending_date', 'status',)}),
        (_('Miscellaneous'), {'fields': ('header_sender', 'header_reply', 'base_url'), 'classes': ('collapse',)}),
    )
    # inlines = (AttachmentAdminInline,)
    actions = ['send_mail_test', 'make_ready_to_send', 'make_cancel_sending', 'duplicate']
    actions_on_top = False
    actions_on_bottom = True

    def get_actions(self, request):
        actions = super(BaseNewsletterAdmin, self).get_actions(request)
        if not request.user.has_perm('edn.can_change_status'):
            del actions['make_ready_to_send']
            del actions['make_cancel_sending']
        return actions

    def get_queryset(self, request):
        queryset = super(BaseNewsletterAdmin, self).queryset(request)
        return queryset

    def formfield_for_dbfield(self, field, **kwargs):
        if field.name == 'header_sender':
            kwargs['initial'] = DEFAULT_HEADER_SENDER
        if field.name == 'header_reply':
            kwargs['initial'] = DEFAULT_HEADER_REPLY
        if field.name == 'base_url':
            kwargs['initial'] = "%s://%s" % ('https' if kwargs['request'].is_secure() else 'http', kwargs['request'].get_host())
        return super(BaseNewsletterAdmin, self).formfield_for_dbfield(field, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # if db_field.name == 'mailing_list' and not request.user.is_superuser and USE_WORKGROUPS:
        #     mailinglists_pk = request_workgroups_mailinglists_pk(request)
        #     kwargs['queryset'] = MailingList.objects.filter(pk__in=mailinglists_pk)
        #     return db_field.formfield(**kwargs)
        return super(BaseNewsletterAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'status' and not request.user.has_perm('edn.can_change_status'):
            kwargs['choices'] = ((Newsletter.DRAFT, _('Default')),)
            return db_field.formfield(**kwargs)
        return super(BaseNewsletterAdmin, self).formfield_for_choice_field(
            db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'test_contacts':
            queryset = Contact.objects.filter(tester=True)
            kwargs['queryset'] = queryset
        return super(BaseNewsletterAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs)

    def save_model(self, request, newsletter, form, change):
        workgroups = []
        if not request.user.has_perm('edn.can_change_status'):
            newsletter.status = form.initial.get('status', Newsletter.DRAFT)

        try:
            newsletter.save()
        except:
            self.message_user(request, _('Unable to download HTML, due to errors within.'))

    def historic_link(self, newsletter):
        """Display link for historic"""
        if newsletter.contactmailingstatus_set.count():
            return u'<a href="%s">%s</a>' % (newsletter.get_historic_url(), _('View historic'))
        return _('Not available')
    historic_link.allow_tags = True
    historic_link.short_description = _('Historic')

    def statistics_link(self, newsletter):
        """Display link for statistics"""
        if newsletter.status == Newsletter.SENDING or newsletter.status == Newsletter.SENT:
            return u'<a href="%s">%s</a>' % (newsletter.get_statistics_url(), _('View statistics'))
        return _('Not available')
    statistics_link.allow_tags = True
    statistics_link.short_description = _('Statistics')

    def send_mail_test(self, request, queryset):
        """Send newsletter in test"""
        for newsletter in queryset:
            try:
                newsletter.send(newsletter.test_contacts.all(), force_now=True)
            except HTMLParseError:
                self.message_user(request, _('Unable send newsletter, due to errors within HTML.'))
                continue
            self.message_user(request, _('%s successfully sent.') % newsletter)
    send_mail_test.short_description = _('Send test email')

    def make_ready_to_send(self, request, queryset):
        """Make newsletter ready to send"""
        from django.contrib import messages
        queryset.filter(status=Newsletter.DRAFT).update(status=Newsletter.WAITING)
        messages.success(request, _('%s newsletters are ready to send') % queryset.count())
        # self.message_user(request, message)
    make_ready_to_send.short_description = _('Make ready to send')

    def make_cancel_sending(self, request, queryset):
        """Cancel the sending of newsletters"""
        queryset = queryset.filter(Q(status=Newsletter.WAITING) | Q(status=Newsletter.SENDING)).update(status=Newsletter.CANCELED)
        self.message_user(request, _('%s newsletters are cancelled') % queryset.count())
    make_cancel_sending.short_description = _('Cancel the sending')

    def duplicate(self, request, queryset):
        """Duplicate selected newsletters"""
        for newsletter in queryset:
            attachments = newsletter.attachment_set.all()
            newsletter.pk = None
            i = 1
            while Newsletter.objects.filter(title=u'%s [%s]' % (newsletter.title, i)).count() > 0:
                i += 1
            newsletter.title = u'%s [%s]' % (newsletter.title, i)
            newsletter.save()
            for att in attachments:
                att.pk = None
                att.newsletter = newsletter
                att.save()


class NewsletterTinyMCEForm(forms.ModelForm):
    content = forms.CharField(label=_('content'),
                              widget=TinyMCE(attrs=TINYMCE_WIDGET_ATTRS))

    class Meta:
        model = Newsletter

class NewsletterAdmin(BaseNewsletterAdmin):
    form = NewsletterTinyMCEForm
