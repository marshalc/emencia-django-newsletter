"""Forms for edn"""
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db.utils import ProgrammingError

from edn.models import Contact, MailingList, SubscriberVerification


class MailingListSubscriptionForm(forms.ModelForm):
    """
    Form for subscribing to a mailing list
    """
    # Notes : This form will not check the uniqueness of the 'email' field, by defining it explicitly and setting
    # it the Meta.exclude list, for allowing registration to a mailing list even if the contact already exists.
    # Then the contact is always added to the subscribers field of the mailing list because it will be cleaned with no
    # double.
    error_css_class = 'error'
    required_css_class = 'required'

    email = forms.EmailField(label=_('Email'), max_length=75)

    def save(self, mailing_list):
        data = self.cleaned_data
        contact, created = Contact.objects.get_or_create(
            email=data['email'],
            defaults={
                'full_name': data['full_name'],
            }
        )

        mailing_list.subscribers.add(contact)
        mailing_list.unsubscribers.remove(contact)

    class Meta:
        model = Contact
        fields = ('full_name',)
        exclude = ('email',)


class AllMailingListSubscriptionForm(MailingListSubscriptionForm):
    """
    Form for subscribing to all mailing lists
    """
    try:
        mailing_lists = forms.ModelMultipleChoiceField(
            queryset=MailingList.objects.all(),
            initial=[
                obj.id for obj in MailingList.objects.all()
            ],
            label=_('Mailing lists'),
            widget=forms.CheckboxSelectMultiple()
        )
    except ProgrammingError:
        mailing_lists = None

    def save(self, mailing_list):
        data = self.cleaned_data
        contact, created = Contact.objects.get_or_create(
            email=data['email'],
            defaults={'full_name': data['full_name']}
        )

        for mailing_list in data['mailing_lists']:
            mailing_list.subscribers.add(contact)
            mailing_list.unsubscribers.remove(contact)


class VerificationMailingListSubscriptionForm(forms.Form):
    """
    Form for subscribing to all mailing lists after verification
    """
    try:
        mailing_lists = forms.ModelMultipleChoiceField(
            queryset=MailingList.objects.all(),
            initial=[
                obj.id for obj in MailingList.objects.all()
            ],
            label=_('Mailing lists'),
            widget=forms.CheckboxSelectMultiple(),
        )
    except ProgrammingError:
        mailing_lists = None

    def save(self, contact_id):
        mailing_list = None
        data = self.cleaned_data

        for mailing_list in data['mailing_lists']:
            mailing_list.subscribers.add(Contact.objects.get(id=contact_id))
            mailing_list.unsubscribers.remove(Contact.objects.get(id=contact_id))


class SubscriberVerificationForm(forms.ModelForm):
    """
    Form for verifying a contact
    """
    class Meta:
        model = Contact
        exclude = ('verified', 'tester')
