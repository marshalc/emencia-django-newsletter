"""Utils for newsletter"""
import re

from bs4 import BeautifulSoup

from django.core.urlresolvers import reverse

from emencia.settings import TRACKING_IGNORE_ANCHOR
from emencia.settings import USE_PRETTIFY
from emencia.models import Link

###  Moot since all emails are now template based?
# def body_insertion(content, insertion, end=False):
#     """Insert an HTML content into the body HTML node"""
#     if not content.startswith('<body'):
#         content = '<body>%s</body>' % content
#     soup = BeautifulSoup(content)
#     insertion = BeautifulSoup(insertion)
#
#     if end:
#         soup.body.append(insertion)
#     else:
#         soup.body.insert(0, insertion)
#
#     if USE_PRETTIFY:
#         return soup.prettify()
#     else:
#         return soup.renderContents()


def track_links(content, context):
    """
    Convert all links in the template for the user to track his navigation
    """
    if not context.get('uidb36'):
        return content

    soup = BeautifulSoup(content)
    for link_markup in soup('a'):
        if link_markup.get('href') and 'no-track' not in link_markup.get('rel', ''):
            if TRACKING_IGNORE_ANCHOR:
                if '#' in link_markup.get('href')[0]:
                    continue
            link_href = link_markup['href']

            if link_href.startswith("http"):
                link_title = link_markup.get('title', link_href)
                link, created = Link.objects.get_or_create(url=link_href, defaults={'title': link_title})
                link_markup['href'] = '%s%s' % (
                    context['base_url'], 
                    reverse(
                        'newsletter_newsletter_tracking_link', 
                        args=[context['newsletter'].slug, context['uidb36'], context['token'], link.pk]
                    )
                )

    if USE_PRETTIFY:
        return soup.prettify()
    else:
        return soup.renderContents()


def fix_tinymce_links(content):
    """ Clean the src attribute of images in content edited with TinyMCE and django-filebrowser"""
    return re.sub(r'(\.\.\/)+', '/', content)
