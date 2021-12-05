import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from django.conf import settings
from django.urls import re_path
from django.templatetags.static import static
from django.utils.html import format_html, format_html_join
from django.utils.module_loading import import_string
from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineEntityElementHandler
from wagtail.core.rich_text import LinkHandler
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


class FromDBHandler(InlineEntityElementHandler):
    mutability = "IMMUTABLE"

    def get_attribute_data(self, attrs):
        self.attrs = attrs
        return dict(attrs, **{"id": attrs["modelchooser_id"]})

    # This is a hack that allows us to store <a> tags without children
    # If it has broken due to upgrade, you have to refactor how modelchoosers
    # stores stuff and possibly do a data migration.  My prayers are with you.
    def handle_endtag(self, name, state, contentstate):
        state.current_block.text = self.attrs["label"]
        return super().handle_endtag(name, state, contentstate)


def default_expand_attrs(attrs):
    href = attrs.pop("url")
    attrs.pop("linktype")
    tag = DOM.create_element("a", dict(attrs, **{"href": href}))
    return str(DOM.render(tag))


def make_rewriter(t, expander):
    class ModelLinkHandler(LinkHandler):
        identifier = t

        @classmethod
        def expand_db_attributes(cls, attrs):
            return str(DOM.render(expander(attrs)))

    return ModelLinkHandler


def to_database_format(t):
    def inner(props):
        children = props.pop("children")

        props["linktype"] = t
        props["modelchooser_id"] = str(props["id"])

        return DOM.create_element("a", props)
    return inner


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

        t = "model_chooser_" + draftail_type.lower()

        rule = {
            "from_database_format": {"a[linktype={}]".format(t): FromDBHandler(draftail_type)},
            "to_database_format": {"entity_decorators": {draftail_type: to_database_format(t)}},
        }

        features.register_converter_rule("contentstate", name, rule)

        expander_path = getattr(settings, "DRAFT_EXPORTER_ENTITY_DECORATORS", {}).get(draftail_type, None)
        expander = default_expand_attrs
        if expander_path:
            expander = import_string(expander_path)

        features.register_link_type(make_rewriter(t, expander))
