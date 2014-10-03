import os
from django.conf import settings
from django.utils.importlib import import_module


def get_app_template_dir(app_name, dir):
    app = import_module(app_name)
    return os.path.join(os.path.dirname(app.__file__), dir)


def get_templates():
    try:
        return (
            (i, i) for i in os.walk(
                os.path.join(settings.TEMPLATE_DIRS[0], 'mailouts')
            ).next()[1] if i[0] not in '.'
        )
    except (IndexError, StopIteration):
        return (
            (i, i) for i in os.walk(
                os.path.join(get_app_template_dir('edn', 'templates'), 'mailouts')
            ).next()[1] if i[0] not in '.'
        )
