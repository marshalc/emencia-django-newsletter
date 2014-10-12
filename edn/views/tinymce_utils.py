# views.py
import os

from django.conf import settings
from django.http import HttpResponse

from edn.settings import NEWSLETTER_TINYMCE_TEMPLATE_DIR

try:
    from filebrowser.base import FileObject
except ImportError:
    pass


def view_tinymce_templates(request):
    full_path = os.path.join(settings.MEDIA_ROOT, NEWSLETTER_TINYMCE_TEMPLATE_DIR)
    tmpl_dir = os.listdir(full_path)
    templates = []
    for tmpl in tmpl_dir:
        fileobject = FileObject(os.path.join(NEWSLETTER_TINYMCE_TEMPLATE_DIR, tmpl))
        templates.append('["%s", "%s"]' % (fileobject.filename, fileobject._url_full()))
    
    page = """
    var tinyMCETemplateList = [
            // Name, URL, Description
            %s,
    ];
    """ % ",".join(templates)
    return HttpResponse(page, content_type='text/javascript; charset=utf8')
