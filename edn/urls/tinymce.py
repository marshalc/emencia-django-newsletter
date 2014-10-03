from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'edn.views.tinymce_utils',
    url(r'^templates/$', 'view_tinymce_templates', name='tinymce_templates_list'),
)
