"""Settings for emencia"""
import string
from django.conf import settings

# Tracking related settings
BASE64_IMAGES = {
    'gif': 'AJEAAAAAAP///////wAAACH5BAEHAAIALAAAAAABAAEAAAICVAEAOw==',
    'png': 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAABBJREFUeNpi+P//PwNAgAEACPwC/tuiTRYAAAAASUVORK5CYII=',
    'jpg': '/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAYEBAQFBAYFBQYJBgUGCQsIBgYICwwKCgsKCgwQDAwMDAwMEAwODxAPDgwTExQUExMcGxsbHCAgICAgICAgICD/2wBDAQcHBw0MDRgQEBgaFREVGiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICD/wAARCAABAAEDAREAAhEBAxEB/8QAFAABAAAAAAAAAAAAAAAAAAAACP/EABQQAQAAAAAAAAAAAAAAAAAAAAD/xAAUAQEAAAAAAAAAAAAAAAAAAAAA/8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAwDAQACEQMRAD8AVIP/2Q=='
}
TRACKING_LINKS = getattr(settings, 'NEWSLETTER_TRACKING_LINKS', True)
TRACKING_IMAGE_FORMAT = getattr(settings, 'NEWSLETTER_TRACKING_IMAGE_FORMAT', 'gif')
TRACKING_IMAGE = getattr(settings, 'NEWSLETTER_TRACKING_IMAGE', BASE64_IMAGES[TRACKING_IMAGE_FORMAT])
UNIQUE_KEY_LENGTH = getattr(settings, 'NEWSLETTER_UNIQUE_KEY_LENGTH', 8)
UNIQUE_KEY_CHAR_SET = getattr(settings, 'NEWSLETTER_UNIQUE_KEY_CHAR_SET', string.ascii_uppercase + string.digits)
USE_UTM_TAGS = getattr(settings, 'NEWSLETTER_USE_UTM_TAGS', True)

# Email header defaults
DEFAULT_HEADER_SENDER = getattr(settings, 'NEWSLETTER_DEFAULT_HEADER_SENDER', 'Emencia Newsletter<noreply@example.com>')
DEFAULT_HEADER_REPLY = getattr(settings, 'NEWSLETTER_DEFAULT_HEADER_REPLY', DEFAULT_HEADER_SENDER)

# Still not sure what this does... TODO: Investigate this function!
USE_WORKGROUPS = getattr(settings, 'NEWSLETTER_USE_WORKGROUPS', False)

# Settings used by utils/newsletter/
USE_PRETTIFY = getattr(settings, 'NEWSLETTER_USE_PRETTIFY', True)
TRACKING_IGNORE_ANCHOR = getattr(settings, 'NEWSLETTER_TRACKING_IGNORE_ANCHOR', False)

# Allow subscribers to get an unsubscribe link in their newsletters
INCLUDE_UNSUBSCRIPTION = getattr(settings, 'NEWSLETTER_INCLUDE_UNSUBSCRIPTION', True)

# Allow the unsubscribe form to unsubscribe from all newsletters
UNSUBSCRIBE_ALL = getattr(settings, 'NEWSLETTER_UNSUBSCRIBE_ALL', False)

# Base location for newsletter attachments to be stored
BASE_PATH = getattr(settings, 'NEWSLETTER_BASE_PATH', 'uploads/newsletter')

# Settings related to optional WYSIWYG components
USE_CKEDITOR = getattr(settings, 'NEWSLETTER_USE_CKEDITOR', 'ckeditor' in settings.INSTALLED_APPS)
USE_TINYMCE = getattr(settings, 'NEWSLETTER_USE_TINYMCE', 'tinymce' in settings.INSTALLED_APPS)
TINYMCE_WIDGET_ATTRS = getattr(settings, 'TINYMCE_WIDGET_ATTRS', {'cols': 150, 'rows': 80})
NEWSLETTER_TINYMCE_TEMPLATE_DIR = getattr(settings, 'NEWSLETTER_TINYMCE_TEMPLATE_DIR', 'upload/tinymce/templates/')

# Should a user be automatically subscribed to a mailing list if it's
# the only list in system?
AUTO_SUBSCRIBE_TO_ONLY_LIST = getattr(settings, 'NEWSLETTER_AUTO_SUBSCRIBE_TO_ONLY_LIST', True)

# To which mailing list(s) should a new user be automatically subscribed?
AUTO_SUBSCRIBE_LIST_NAME = getattr(settings, 'NEWSLETTER_AUTO_SUBSCRIBE_LIST_NAME', None)
