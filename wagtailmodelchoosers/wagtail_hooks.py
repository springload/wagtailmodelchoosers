import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from django.conf import settings
from django.conf.urls import url
from django.templatetags.static import static
from django.utils.html import format_html, format_html_join
from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters import html_to_contentstate
from wagtail.admin.rich_text.editors.draftail import (
    DraftailRichTextArea,
#    DraftailRichTextAreaAdapter,
)
from wagtail.core import hooks
#from wagtail.core.rich_text import LinkHandler

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


# Handlers for converting to and from wagtail database format
def make_handlers(name, draftail_type):
    class Handler(html_to_contentstate.InlineEntityElementHandler):
        mutability = "IMMUTABLE"

        def get_attribute_data(self, attrs):
            return {"id": attrs[f"data-{name}"]}

    def decorator(props):
        return DOM.create_element(
            "span", {f"data-{name}": props["id"]}, props["children"]
        )

    return Handler(draftail_type), decorator


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
        feature = draftail_features.EntityFeature(chooser)
        features.register_editor_plugin("draftail", name, feature)

        _from, _to = make_handlers(name, draftail_type)

        features.register_converter_rule(
            "contentstate",
            name,
            {
                "from_database_format": {f"span[data-{name}]": _from},
                "to_database_format": {"entity_decorators": {draftail_type: _to}},
            },
        )


#class ModelChooserDraftailRichTextAreaAdapter(DraftailRichTextAreaAdapter):
#    js_constructor = "modelChooserDraftailInit"

#    class Media:
#        js = ["wagtailmodelchoosers/draftailmodelchoosers.js"]

#    def js_args(self, *args, **kwargs):
#        js_args = super().js_args(*args, **kwargs)

        # Give it all draftail types to register
#        f = "draftail_type"
#        js_args.append([c[f] for c in get_all_chooser_options().values() if f in c])

        # Upstream's JS constructor to call with options
#        js_args.append(super().js_constructor)

#        return js_args


#telepath.register(ModelChooserDraftailRichTextAreaAdapter(), DraftailRichTextArea)
