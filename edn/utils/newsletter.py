"""Utils for newsletter"""
# import re

from bs4 import BeautifulSoup
from django.core.urlresolvers import reverse
from edn.models import Link


def track_links(content, context):
    """
    Convert all links in the template for the user to track his navigation
    """
    if not context.get('uidb36'):
        return content

    soup = BeautifulSoup(content)
    for link_markup in soup('a'):
        if link_markup.get('href') and 'no-track' not in link_markup.get('rel', ''):
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

    return soup.prettify()
