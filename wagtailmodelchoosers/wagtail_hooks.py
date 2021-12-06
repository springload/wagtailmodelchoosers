from django.urls import re_path
from django.templatetags.static import static
from django.utils.html import format_html, format_html_join
from wagtail.core import hooks
from .register_entity import register_entity

from wagtailmodelchoosers.views import ModelView, RemoteResourceView

from .utils import get_all_chooser_options


@hooks.register("insert_editor_css")
def wagtailmodelchoosers_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("wagtailmodelchoosers/wagtailmodelchoosers.css"),
    )


@hooks.register("insert_editor_js")
def wagtailmodelchoosers_admin_js():
    js_files = (
        "wagtailmodelchoosers/wagtailmodelchoosers.js",
        "wagtailmodelchoosers/polyfills.js",
    )
    js_includes = format_html_join(
        "\n",
        '<script src="{}"></script>',
        ((static(filename),) for filename in js_files),
    )
    return js_includes


@hooks.register("register_admin_urls")
def wagtailmodelchoosers_admin_urls():
    return [
        re_path(
            r"^modelchoosers/api/v1/model/(?P<app_name>[\w-]+).(?P<model_name>\w+)",
            ModelView.as_view({"get": "list"}),
            name="wagtailmodelchoosers_api_model",
        ),
        re_path(
            r"^modelchoosers/api/v1/remote_model/(?P<chooser>[\w-]+)",
            RemoteResourceView.as_view({"get": "list"}),
            name="wagtailmodelchoosers_api_remote_model",
        ),
    ]


@hooks.register("register_rich_text_features")
def register_rich_text_features(features):
    choosers = get_all_chooser_options()
    for name, chooser in choosers.items():
        draftail_type = chooser.get("draftail_type", None)
        if not draftail_type:
            continue

        # If there's no content_type then it's a remote chooser, and
        # content_type means the name of the chooser instead of the model.
        if "content_type" not in chooser:
            chooser["content_type"] = name

        chooser["type"] = draftail_type
        register_entity(features, chooser, name, draftail_type, "model_chooser_")
