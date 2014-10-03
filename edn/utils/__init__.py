"""Utils for edn"""
from django.template import Context, Template
import re
from html2text import html2text as html2text_orig
from StringIO import StringIO

def render_string(template_string, context={}):
    """Shortcut for render a template string with a context"""
    t = Template(template_string)
    c = Context(context)
    return t.render(c)

LINK_RE = re.compile(r"https?://([^ \n]+\n)+[^ \n]+", re.MULTILINE)

def html2text(html):
    """
    Use html2text but repair newlines cutting urls.
    Need to use this hack until https://github.com/aaronsw/html2text/issues/#issue/7 is not fixed
    """
    txt = html2text_orig(html)
    links = list(LINK_RE.finditer(txt))
    out = StringIO()
    pos = 0
    for l in links:
        out.write(txt[pos:l.start()])
        out.write(l.group().replace('\n', ''))
        pos = l.end()
    out.write(txt[pos:])
    return out.getvalue()

