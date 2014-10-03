from django.dispatch import Signal

contact_unsubscribed = Signal(providing_args=["mailing_list"])
