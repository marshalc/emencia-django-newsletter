"""
Models for edn
"""
import logging
from datetime import datetime
from random import sample
from smtplib import SMTPRecipientsRefused
from urllib2 import urlopen

from autoslug import AutoSlugField
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import Context, Template
from django.utils.encoding import smart_str, smart_unicode
from django.utils.translation import ugettext_lazy as _
from premailer import Premailer, transform
from uuidfield import UUIDField

from django.template.loader import render_to_string
from django.template.loader import get_template


from edn.managers import ContactManager
from edn.settings import TRACKING_LINKS, TRACKING_IMAGE_FORMAT, UNIQUE_KEY_LENGTH, UNIQUE_KEY_CHAR_SET
from edn.utils import html2text
from edn.utils.template import get_templates


logger = logging.getLogger(__name__)


class Contact(models.Model):
    """Contact for emailing"""

    # Contact's email address and name
    email = models.EmailField(_('email'), unique=True)
    full_name = models.CharField(_('full name'), max_length=255, null=True, blank=True)

    # Has contact validated their email via
    verified = models.BooleanField('verified', default=False)
    verified_on = models.DateTimeField('verified on', blank=True, null=True)

    # Use this contact for a test mail out
    tester = models.BooleanField(_('contact tester'), default=False)

    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)

    objects = ContactManager()

    def subscriptions(self):
        """Return the user subscriptions"""
        return MailingList.objects.filter(subscribers=self)

    def unsubscriptions(self):
        """Return the user unsubscriptions"""
        return MailingList.objects.filter(unsubscribers=self)

    # def vcard_format(self):
    #     return vcard_contact_export(self)

    def mail_format(self):
        if self.full_name:
            return smart_unicode('"%s" <%s>' % (
                self.full_name,
                self.email
            ))
        return self.email
    mail_format.short_description = _('mail format')

    def get_absolute_url(self):
        urlname = 'admin:%s_contact_change' % self._meta.app_label
        return reverse(urlname, args=[self.pk])

    def __unicode__(self):
        if self.full_name:
            contact_name = self.full_name
        else:
            contact_name = self.email
        return smart_unicode(contact_name)

    class Meta:
        ordering = ('creation_date',)
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')


class ContactMailingStatus(models.Model):
    """Status of the reception"""
    SENT_TEST = -1
    SENT = 0
    ERROR = 1
    INVALID = 2
    OPENED = 4
    OPENED_ON_SITE = 5
    LINK_OPENED = 6
    UNSUBSCRIPTION = 7

    STATUS_CHOICES = (
        (SENT_TEST, _('sent in test')),
        (SENT, _('sent')),
        (ERROR, _('error')),
        (INVALID, _('invalid email')),
        (OPENED, _('opened')),
        (OPENED_ON_SITE, _('opened on site')),
        (LINK_OPENED, _('link opened')),
        (UNSUBSCRIPTION, _('unsubscription')),
    )

    newsletter = models.ForeignKey('Newsletter', verbose_name=_('newsletter'))
    contact = models.ForeignKey('Contact', verbose_name=_('contact'))
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES)
    link = models.ForeignKey('Link', verbose_name=_('link'), blank=True, null=True)

    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)

    def __unicode__(self):
        return '%s : %s : %s' % (self.newsletter.__unicode__(), self.contact.__unicode__(), self.get_status_display())

    class Meta:
        ordering = ('-creation_date',)
        verbose_name = _('contact mailing status')
        verbose_name_plural = _('contact mailing statuses')


class MailingList(models.Model):
    """Mailing list"""
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    subscribers = models.ManyToManyField(
        Contact, verbose_name=_('subscribers'),
        related_name='mailinglist_subscriber', null=True, blank=True
    )
    unsubscribers = models.ManyToManyField(
        Contact, verbose_name=_('unsubscribers'),
        related_name='mailinglist_unsubscriber', null=True, blank=True
    )

    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)

    def subscribers_count(self):
        return self.subscribers.all().count()
    subscribers_count.short_description = _('subscribers')

    def unsubscribers_count(self):
        return self.unsubscribers.all().count()
    unsubscribers_count.short_description = _('unsubscribers')

    def expedition_set(self):
        return self.subscribers.verified_subscribers()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('-creation_date',)
        verbose_name = _('mailing list')
        verbose_name_plural = _('mailing lists')


class Newsletter(models.Model):
    """Newsletter to be sended to contacts"""
    DRAFT = 0
    WAITING = 1
    SENDING = 2
    SENT = 4
    CANCELED = 5

    STATUS_CHOICES = (
        (DRAFT, _('draft')),
        (WAITING, _('waiting sending')),
        (SENDING, _('sending')),
        (SENT, _('sent')),
        (CANCELED, _('canceled')),
    )

    title = models.CharField(
        _('title'),
        max_length=255,
        help_text=_('')
    )
    content = models.TextField(
        _('content'), help_text=_(''), default=_('<!-- Edit your newsletter here -->')
    )

    template = models.CharField(verbose_name=_('template'), max_length=200, choices=get_templates())
    base_url = models.CharField(verbose_name=_('base URL'), max_length=200, null=True, blank=True)

    mailing_list = models.ForeignKey(MailingList, verbose_name=_('mailing list'), null=True)
    test_contacts = models.ManyToManyField(Contact, verbose_name=_('test contacts'), blank=True, null=True)

    header_sender = models.CharField(_('sender'), max_length=255)
    header_reply = models.CharField(_('reply to'), max_length=255)

    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=DRAFT)
    sending_date = models.DateTimeField(_('sending date'), default=datetime.now)

    slug = AutoSlugField(help_text=_('Used for displaying the newsletter on the site.'),
                         populate_from="title", unique=True)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)

    def status_str(self):
        for (code, string) in self.STATUS_CHOICES:
            if code == self.status:
                return string

    def mails_sent(self):
        return self.contactmailingstatus_set.filter(status=ContactMailingStatus.SENT).count()

    @models.permalink
    def get_absolute_url(self):
        return 'newsletter_newsletter_public', (self.slug,)

    @models.permalink
    def get_historic_url(self):
        return 'newsletter_newsletter_historic', (self.slug,)

    @models.permalink
    def get_statistics_url(self):
        return 'newsletter_newsletter_statistics', (self.slug,)

    def __unicode__(self):
        return self.title

    def __init__(self, *args, **kwargs):
        self._attachments_done = False
        self._attachments = []
        super(Newsletter, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self._attachments_done = False
        if self.content.startswith('http://'):
            self.content = transform(urlopen(self.content.strip()).read())
        super(Newsletter, self).save(*args, **kwargs)

    @property
    def can_send(self):
        """Check if the newsletter should be sent out"""
        try:
            if settings.USE_TZ:
                from django.utils.timezone import utc
                now = datetime.utcnow().replace(tzinfo=utc)
            else:
                now = datetime.now()
        except:
            now = datetime.now()

        if self.sending_date <= now and (self.status == Newsletter.WAITING or self.status == Newsletter.SENDING):
            return True

        return False

    # @property
    # def attachments(self):
    #     if not self._attachments_done:
    #         self._attachments = []
    #         for attachment in self.attachment_set.all():
    #             ctype, encoding = mimetypes.guess_type(attachment.file_attachment.path)
    #
    #             if ctype is None or encoding is not None:
    #                 ctype = 'application/octet-stream'
    #
    #             maintype, subtype = ctype.split('/', 1)
    #
    #             fd = open(attachment.file_attachment.path, 'rb')
    #             if maintype == 'text':
    #                 message_attachment = MIMEText(fd.read(), _subtype=subtype)
    #             elif maintype == 'message':
    #                 message_attachment = message_from_file(fd)
    #             elif maintype == 'image':
    #                 message_attachment = MIMEImage(fd.read(), _subtype=subtype)
    #             elif maintype == 'audio':
    #                 message_attachment = MIMEAudio(fd.read(), _subtype=subtype)
    #             else:
    #                 message_attachment = MIMEBase(maintype, subtype)
    #                 message_attachment.set_payload(fd.read())
    #                 encode_base64(message_attachment)
    #             fd.close()
    #
    #             message_attachment.add_header('Content-Disposition', 'attachment', filename=attachment.title)
    #             self._attachments.append(message_attachment)
    #
    #     return self._attachments

    def update_newsletter_status(self):
        if self.status == Newsletter.WAITING:
            self.status = Newsletter.SENDING
        if self.status == Newsletter.SENDING and self.mails_sent() >= self.mailing_list.expedition_set().count():
            self.status = Newsletter.SENT
        self.save()

    def prepare_message(self, contact):

        from edn.utils.tokens import tokenize
        # from edn.utils.newsletter import fix_tinymce_links

        uidb36, token = tokenize(contact)

        base_url = self.base_url

        context = Context({
            'contact': contact,
            'base_url': base_url,
            'newsletter': self,
            'tracking_image_format': TRACKING_IMAGE_FORMAT,
            'uidb36': uidb36,
            'token': token,
            'UNIQUE_KEY': ''.join(sample(UNIQUE_KEY_CHAR_SET, UNIQUE_KEY_LENGTH))
        })

        message = EmailMultiAlternatives()
        message.from_email = smart_str(self.header_sender)
        message.extra_headers = {'Reply-to': smart_str(self.header_reply)}
        message.to = [contact.mail_format()]

        # Render only the message provided by the user with the WYSIWYG editor
        message_template = Template(self.content)
        message_content = message_template.render(context)

        context.update({'message': message_content})

        # link_site_exist = False
        link_site = render_to_string('views/newsletter_link_site.html', context)
        context.update({'link_site': link_site})

        unsubscription = render_to_string('views/newsletter_link_unsubscribe.html', context)
        context.update({'unsubscription': unsubscription})

        image_tracking = render_to_string('views/newsletter_image_tracking.html', context)
        context.update({'image_tracking': image_tracking})

        content_template = get_template('mailouts/{0}/{1}'.format(self.template, 'index.html'))
        content = content_template.render(context)

        if TRACKING_LINKS:
            from edn.utils.newsletter import track_links
            content = track_links(content, context)

        content = smart_unicode(content)

        p = Premailer(content, base_url=base_url, preserve_internal_links=True)
        content = p.transform()

        message.body = html2text(content)
        message.attach_alternative(smart_str(content), "text/html")

        title_template = Template(self.title)
        title = title_template.render(context)
        message.subject = title

        return message

    def update_contact_status(self, contact, state):
        if state == ContactMailingStatus.INVALID:
            contact.valid = False
            contact.save()

        ContactMailingStatus.objects.get_or_create(newsletter=self, contact=contact, defaults={'status': state})

    @property
    def recipients(self):
        already_sent = ContactMailingStatus.objects.filter(
            status=ContactMailingStatus.SENT, newsletter=self
        ).values_list('contact__id', flat=True)
        expedition_list = self.mailing_list.expedition_set().exclude(id__in=already_sent)
        return expedition_list

    def send(self, recipients, force_now=False):
        if not self.can_send and not force_now:
            return

        number_of_recipients = len(recipients)

        logger.debug('%i emails will be sent' % number_of_recipients)

        i = 1
        for contact in recipients:
            if not contact.verified:
                logger.warn('- E-mail address not verified, not sending: {0}'.format(contact.email))
                continue

            logger.debug('- Processing %s/%s (%s)', i, number_of_recipients, contact.pk)

            try:
                message = self.prepare_message(contact)
                message.send()
                self.update_contact_status(contact, ContactMailingStatus.SENT)
            except SMTPRecipientsRefused:
                self.update_contact_status(contact, ContactMailingStatus.INVALID)

            i += 1

        self.update_newsletter_status()

    class Meta:
        ordering = ('-creation_date',)
        verbose_name = _('newsletter')
        verbose_name_plural = _('newsletters')
        permissions = (('can_change_status', 'Can change status'),)


class Link(models.Model):
    """Link sent in a newsletter"""
    title = models.CharField(_('title'), max_length=255)
    url = models.CharField(_('url'), max_length=255)

    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)

    def get_absolute_url(self):
        return self.url

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-creation_date',)
        verbose_name = _('link')
        verbose_name_plural = _('links')


# class Attachment(models.Model):
#     """Attachment file in a newsletter"""
#
#     def get_newsletter_storage_path(self, filename):
#         filename = force_unicode(filename)
#         return '/'.join([BASE_PATH, self.newsletter.slug, filename])
#
#     newsletter = models.ForeignKey(Newsletter, verbose_name=_('newsletter'))
#     title = models.CharField(_('title'), max_length=255)
#     file_attachment = models.FileField(_('file to attach'), max_length=255, upload_to=get_newsletter_storage_path)
#
#     class Meta:
#         verbose_name = _('attachment')
#         verbose_name_plural = _('attachments')
#
#     def __unicode__(self):
#         return self.title
#
#     def get_absolute_url(self):
#         return self.file_attachment.url


class SubscriberVerification(models.Model):
    link_id = UUIDField(name=_('link_id'), auto=True)
    contact = models.ForeignKey(Contact)

    def __unicode__(self):
        return unicode(self.id)
