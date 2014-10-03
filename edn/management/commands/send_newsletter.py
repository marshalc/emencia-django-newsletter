"""Command for sending the newsletter"""

from django.conf import settings
from django.utils.translation import activate
from django.core.management.base import NoArgsCommand

from edn.models import Newsletter

import logging

logger = logging.getLogger(__name__)

class Command(NoArgsCommand):
    """Send the newsletter in queue"""
    help = 'Send the newsletter in queue'

    def handle_noargs(self, **options):
        logger.debug('Starting sending newsletters...')

        activate(settings.LANGUAGE_CODE)

        for newsletter in Newsletter.objects.exclude(status=Newsletter.DRAFT).exclude(status=Newsletter.SENT):
            if newsletter.can_send:
                logger.debug('Start emailing %s', newsletter.title.encode("utf-8"))
                newsletter.send(newsletter.recipients)

        logger.debug('End session sending')
