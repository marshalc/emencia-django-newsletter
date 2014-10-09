"""
Views for edn Mailing List and Subscriber Verification
"""
import re
from StringIO import StringIO

from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, RequestContext
from django.template.loader import render_to_string
from django.utils.encoding import smart_str

from edn.signals import contact_unsubscribed
from edn.models import Newsletter, MailingList, ContactMailingStatus, SubscriberVerification
from edn.settings import DEFAULT_HEADER_REPLY, UNSUBSCRIBE_ALL
from edn.utils.tokens import untokenize
from edn.utils import html2text


def view_mailinglist_unsubscribe(request, slug, uidb36, token):
    """
    Unsubscribe a contact to one or all mailing lists
    """
    newsletter = get_object_or_404(Newsletter, slug=slug)
    contact = untokenize(uidb36, token)
    if UNSUBSCRIBE_ALL:
        mailing_lists = MailingList.objects.all()
        contact.subscriber = False
        contact.save()
    else:
        mailing_lists = [newsletter.mailing_list]

    unsubscribed = 0
    already_unsubscribed = False

    if request.POST.get('email'):
        for mailing_list in mailing_lists:
            mailing_list.unsubscribers.add(contact)
            mailing_list.subscribers.remove(contact)
            contact_unsubscribed.send(sender=contact, mailing_list=mailing_list)
            unsubscribed += 1

    if unsubscribed > 0:
        already_unsubscribed = True
        ContactMailingStatus.objects.create(
            newsletter=newsletter,
            contact=contact,
            status=ContactMailingStatus.UNSUBSCRIPTION
        )

    return render_to_response(
        'edn/views/mailing_list_unsubscribe.html',
        {'email': contact.email, 'unsubscribed_count':unsubscribed, 'already_unsubscribed': already_unsubscribed},
        context_instance=RequestContext(request)
    )


def view_mailinglist_subscribe(request, form_class, mailing_list_id=None, link_id=None):
    """
    A simple view that shows a form for subscription for a mailing list(s).
    """
    subscribed = False
    mailing_list = None
    if mailing_list_id:
        mailing_list = get_object_or_404(MailingList, id=mailing_list_id)

    if request.POST and not subscribed:
        form = form_class(request.POST)
        if form.is_valid():
            form.save(mailing_list)
            subscribed = True
    else:
        form = form_class()

    return render_to_response(
        'edn/views/mailing_list_subscribe.html',
        {'subscribed': subscribed, 'mailing_list': mailing_list, 'form': form},
        context_instance=RequestContext(request)
    )


def _view_subscriber_verification_context(request, form_class):

    """
    A simple view that shows a form for subscription for the newsletter.
    """
    context = {}

    if request.POST:
        context['form'] = form_class(request.POST)
        if context['form'].is_valid():
            subscription = SubscriberVerification()
            contact = context['form'].save()                
            subscription.contact = context['form'].instance
            subscription.save()

            link_id = str(subscription.link_id)

            mail_context = Context({
                'base_url': "%s://%s" % ("https" if request.is_secure() else "http", request.get_host()),
                'link_id': link_id,
            })

            content_html = render_to_string('edn/views/newsletter_mail_verification.html', mail_context)

            content_text = html2text(content_html)

            message = EmailMultiAlternatives()
            message.from_email = smart_str(DEFAULT_HEADER_REPLY)
            message.extra_headers = {'Reply-to': smart_str(DEFAULT_HEADER_REPLY)}
            message.to = [smart_str(context['form'].instance.email)]
            
            message.subject = render_to_string('edn/views/newsletter_mail_verification_subject.html', context)

            message.body = smart_str(content_text)
            message.attach_alternative(smart_str(content_html), "text/html")       

            try:
                message.send()
            except Exception, e:
                print e

            context['send'] = True

    else:
        context['form'] = form_class()

    return context


def view_subscriber_verification(request, form_class):

    context = _view_subscriber_verification_context(request, form_class)
    
    return render_to_response(
        'edn/views/subscriber_verification.html',
        context,
        context_instance=RequestContext(request)
    )


def _view_uuid_verification_context(request, link_id, form_class=None):
    context = {}
    context['mailinglists'] = mailinglists = MailingList.objects.filter(public=True)
    context['mailing_list_count'] = mailinglists.count()
    context['link_id'] = link_id

    try:
        subscription = {}
        subscription['object'] = SubscriberVerification.objects.get(link_id=link_id)
        context['uuid_exist'] = True
        subscription['contact'] = subscription['object'].contact
        ready = True

        # # If there is only one mailing list, subscribe the (now)
        # # verified user to it
        # if AUTO_SUBSCRIBE_TO_ONLY_LIST:
        #     if context['mailing_list_count'] == 1:
        #         mailing_list = mailinglists.get()
        #         mailing_list.subscribers.add(subscription['contact'].id)
        #         mailing_list.unsubscribers.remove(subscription['contact'].id)
        #
        # if AUTO_SUBSCRIBE_LIST_NAME is not None:
        #     if isinstance(AUTO_SUBSCRIBE_LIST_NAME, basestring):
        #         lists = [AUTO_SUBSCRIBE_LIST_NAME]
        #     else:
        #         lists = AUTO_SUBSCRIBE_LIST_NAME
        #
        #     mls = mailinglists.filter(name__in=lists)
        #     for ml in mls:
        #         ml.subscribers.add(subscription['contact'].id)
        #         ml.unsubscribers.remove(subscription['contact'].id)

        if request.POST:
            form = form_class(request.POST)
            if form.is_valid():
                form.save(subscription['contact'].id)
                context['send'] = True
            else:
                ready = False
        else:
            context['form'] = form_class()

        if ready:
            subscription['contact'].verified = True
            subscription['contact'].save()
            subscription['object'].delete()

    except SubscriberVerification.DoesNotExist:
        context['uuid_exist'] = False

    return context


def view_uuid_verification(request, link_id, form_class=None):
    """
    A simple view that shows if verification is true or false.
    """

    context = _view_uuid_verification_context(request, link_id, form_class)

    return render_to_response(
        'edn/views/uuid_verification.html',
        context,
        context_instance=RequestContext(request)
    )
