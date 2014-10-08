"""Managers for edn"""
from django.db import models


class ContactManager(models.Manager):
    """Manager for the contacts"""

    def unverified_subscribers(self):
        """Return all subscribers"""
        return self.get_queryset().filter(verified=False)

    def verified_subscribers(self):
        """Return only verified contacts"""
        return self.get_queryset().filter(verified=True)
