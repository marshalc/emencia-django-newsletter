"""Managers for edn"""
from django.db import models


class ContactManager(models.Manager):
    """Manager for the contacts"""

    def subscribers(self):
        """Return all subscribers"""
        return self.get_query_set().filter(subscriber=True)

    def unsubscribers(self):
        """Return all unsubscribers"""
        return self.get_query_set().filter(subscriber=False)

    def verified_subscribers(self):
        """Return only verified contacts"""
        return self.subscribers().filter(verified=True)
