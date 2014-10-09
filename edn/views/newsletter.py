"""
Views for edn Newsletter
"""
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, RequestContext, Template

from django.template.loader import render_to_string

from edn.models import ContactMailingStatus, Newsletter
from edn.utils.newsletter import track_links
from edn.utils.tokens import untokenize


def render_newsletter(request, slug, context):
    """Return a newsletter in HTML format"""
    newsletter = get_object_or_404(Newsletter, slug=slug)
    context = Context(context)
    context.update({
        'newsletter': newsletter,
        'title': newsletter.title,
        'base_url': newsletter.base_url,
    })

    # Render only the message provided by the user with the WYSIWYG editor
    message_template = Template(newsletter.content)
    message = message_template.render(context)
    message = track_links(message, context)
    context.update({'message': message})

    unsubscription = render_to_string('edn/views/newsletter_link_unsubscribe.html', context)
    context.update({'unsubscription': unsubscription})

    return render_to_response(
        'edn/email_templates/{0}/{1}'.format(newsletter.template, 'index.html'),
        dictionary=context,
        # context_instance=RequestContext(request)
    )


@staff_member_required
def view_newsletter_preview(request, slug):
    """View of the newsletter preview"""
    context = {'contact': request.user}
    return render_newsletter(request, slug, context)


def view_newsletter_public(request, slug):
    # newsletter = Newsletter.objects.get(slug=slug)
    
    return render_newsletter(request, slug, {})
    # return render_to_response('edn/views/newsletter_forbidden.html')


def view_newsletter_contact(request, slug, uidb36, token):
    """Visualization of a newsletter by an user"""
    newsletter = get_object_or_404(Newsletter, slug=slug)
    contact = untokenize(uidb36, token)
    ContactMailingStatus.objects.create(
        newsletter=newsletter, contact=contact, status=ContactMailingStatus.OPENED_ON_SITE
    )
    context = {'contact': contact, 'uidb36': uidb36, 'token': token}

    return render_newsletter(request, slug, context)
