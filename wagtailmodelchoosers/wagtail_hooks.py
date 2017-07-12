from django.conf.urls import url
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html

from wagtail.wagtailcore import hooks

from wagtailmodelchoosers.views import ModelView, RemoteResourceView


@hooks.register('insert_editor_css')
def wagtailmodelchoosers_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('wagtailmodelchoosers/wagtailmodelchoosers.css')
    )


@hooks.register('insert_editor_js')
def wagtailmodelchoosers_admin_js():
    js_html = format_html(
        '<script src="{}"></script>',
        static('wagtailmodelchoosers/wagtailmodelchoosers.js')
    ) + format_html(
        '<script src="{}"></script>',
        static('wagtailmodelchoosers/polyfills.js')
    )
    return js_html


@hooks.register('register_admin_urls')
def wagtailmodelchoosers_admin_urls():
    return [
        url(
            r'^modelchoosers/api/v1/model/(?P<app_name>[\w-]+).(?P<model_name>\w+)',
            ModelView.as_view({'get': 'list'}),
            name='wagtailmodelchoosers_api_model'
        ),
        url(
            r'^modelchoosers/api/v1/remote_model/(?P<chooser>[\w-]+)',
            RemoteResourceView.as_view({'get': 'list'}),
            name='wagtailmodelchoosers_api_remote_model'
        )
    ]
