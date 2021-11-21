import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from django.conf import settings
from django.conf.urls import url
from django.templatetags.static import static
from django.utils.html import format_html, format_html_join
from django.utils.module_loading import import_string
from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineEntityElementHandler
from wagtail.core import hooks

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


def default_decorator(props):
    children = props.pop("children")
    return DOM.create_element("span", props, children)


def wrap_dec(dec, matcher):
    def inner(props):
        el = dec(props)
        el.attr.update({matcher: str(props["id"])})
        DOM.append_child(el, props["children"])
        return el
    return inner


def wrap_hand(matcher):

    class Handler(InlineEntityElementHandler):
        mutability = "IMMUTABLE"

        def get_attribute_data(self, attrs):
            return { "id": attrs[matcher] }

    return Handler

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

        decorator_path = getattr(settings, "DRAFT_EXPORTER_ENTITY_DECORATORS", {}).get(draftail_type, None)
        decorator = None
        if decorator_path:
            decorator = import_string(decorator_path)
        else:
            decorator = default_decorator

        matcher = "modelchooser_choice_{}".format(draftail_type.lower())

        features.register_converter_rule(
            "contentstate",
            name,
            {
                "from_database_format": {"span[{}]".format(matcher): wrap_hand(matcher)(draftail_type)},
                "to_database_format": {"entity_decorators": {draftail_type: wrap_dec(decorator, matcher)}},
            },
        )
