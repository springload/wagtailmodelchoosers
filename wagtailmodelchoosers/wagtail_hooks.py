import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from django.conf import settings
from django.conf.urls import url
from django.templatetags.static import static
from django.utils.html import format_html, format_html_join
from wagtail.core import hooks

from wagtailmodelchoosers.views import ModelView, RemoteResourceView


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
        url(
            r"^modelchoosers/api/v1/model/(?P<app_name>[\w-]+).(?P<model_name>\w+)",
            ModelView.as_view({"get": "list"}),
            name="wagtailmodelchoosers_api_model",
        ),
        url(
            r"^modelchoosers/api/v1/remote_model/(?P<chooser>[\w-]+)",
            RemoteResourceView.as_view({"get": "list"}),
            name="wagtailmodelchoosers_api_remote_model",
        ),
    ]


@hooks.register("register_rich_text_features")
def register_rich_text_features(features):
    entity_types = getattr(settings, "MODEL_CHOOSER_DRAFTAIL_ENTITY_TYPES", {})
    for entity_type in entity_types:
        type_ = entity_type.get("type", None)
        if not type_:
            continue

        features.default_features.append(type_)
        feature = draftail_features.EntityFeature(entity_type)
        features.register_editor_plugin("draftail", type_, feature)
