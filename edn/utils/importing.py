"""Utils for importation of contacts"""
import csv
import xlrd
import vobject

from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _

from emencia.models import Contact
from emencia.models import MailingList


COLUMNS = ['email', 'full_name']
csv.register_dialect('edn', delimiter=';')


def create_contact(contact_dict):
    """Create a contact and validate the mail"""
    contact_dict['email'] = contact_dict['email'].strip()
    try:
        validate_email(contact_dict['email'])
        contact_dict['valid'] = True
    except ValidationError:
        contact_dict['valid'] = False

    contact, created = Contact.objects.get_or_create(
        email=contact_dict['email'],
        defaults=contact_dict)

    return contact, created


def create_contacts(contact_dicts, importer_name, mailing_list=None, segment=None):
    """Create all the contacts to import and associated them in a mailing list"""
    inserted = 0
    when = str(datetime.now()).split('.')[0]

    if not mailing_list:
        mailing_list = MailingList(
            name=_('Mailing list imported at %s') % when,
            description=_('Contacts imported by %s.') % importer_name)
        mailing_list.save()

    for contact_dict in contact_dicts:
        contact, created = create_contact(contact_dict)
        mailing_list.subscribers.add(contact)
        if segment:
            segment.subscribers.add(contact)
        inserted += int(created)

    return inserted


def vcard_contacts_import(stream, mailing_list=None, segment=None):
    """Import contacts from a VCard file"""
    contacts = []
    vcards = vobject.readComponents(stream)

    for vcard in vcards:
        contact = {'email': vcard.email.value,
                   'full_name': "%s %s" % (vcard.n.value.given, vcard.n.value.family)}
        contacts.append(contact)

    return create_contacts(contacts, 'vcard', mailing_list, segment)


def text_contacts_import(stream, mailing_list=None, segment=None):
    """Import contact from a plaintext file, like CSV"""
    contacts = []
    contact_reader = csv.reader(stream, dialect='edn')

    for contact_row in contact_reader:
        contact = {}
        for i in range(len(contact_row)):
            contact[COLUMNS[i]] = contact_row[i]
        contacts.append(contact)

    return create_contacts(contacts, 'text', mailing_list, segment)


def excel_contacts_import(stream, mailing_list=None, segment=None):
    """Import contacts from an Excel file"""
    contacts = []
    wb = xlrd.open_workbook(file_contents=stream.read())
    sh = wb.sheet_by_index(0)

    for row in range(sh.nrows):
        contact = {}
        for i in range(len(COLUMNS)):
            try:
                value = sh.cell(row, i).value
                contact[COLUMNS[i]] = value
            except IndexError:
                break
        contacts.append(contact)

    return create_contacts(contacts, 'excel', mailing_list, segment)


def import_dispatcher(source, type_, mailing_list, segment):
    """Select importer and import contacts"""
    if type_ == 'vcard':
        return vcard_contacts_import(source, mailing_list, segment)
    elif type_ == 'text':
        return text_contacts_import(source, mailing_list, segment)
    elif type_ == 'excel':
        return excel_contacts_import(source, mailing_list, segment)
    return 0
