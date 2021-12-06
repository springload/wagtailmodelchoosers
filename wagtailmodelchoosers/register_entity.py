from django.conf import settings
from django.utils.module_loading import import_string
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from draftjs_exporter.dom import DOM
from wagtail.core.rich_text import LinkHandler
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineEntityElementHandler


"""
This basically revives the old way of registering draftail extensions where you don't have to
think about from_database or to_database matching rules.  Also it wraps old style decorators
into a link rewriter in a hacky way.
"""

ID_ATTR_NAME = "modelchooser_id"


class FromDBHandler(InlineEntityElementHandler):
    mutability = "IMMUTABLE"

    def get_attribute_data(self, attrs):
        self.attrs = attrs
        extra = {}
        if ID_ATTR_NAME in attrs:
            extra = {"id": attrs[ID_ATTR_NAME]}
        return dict(attrs, **extra)

    # This is a hack that allows us to store <a> tags without children
    # If it has broken due to upgrade, you have to refactor how modelchoosers
    # stores stuff and possibly do a data migration.  My prayers are with you.
    def handle_endtag(self, name, state, contentstate):
        label = self.attrs.get("label", None)
        if label:
            state.current_block.text = label
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
            elt = DOM.render(expander(attrs))
            tag_spl = elt.rsplit("><", 1)
            opening_tag = tag_spl[0]
            if len(tag_spl) > 1:
                opening_tag += ">"
            return opening_tag

    return ModelLinkHandler


def to_database_format(t):
    def inner(props):
        children = props.pop("children")

        props["linktype"] = t
        if "id" in props:
            props[ID_ATTR_NAME] = str(props["id"])

        if "label" in props:
            children = []

        return DOM.create_element("a", props, children)
    return inner


def register_entity(features, chooser, name, draftail_type, prefix):
        feature = draftail_features.EntityFeature(chooser)
        features.register_editor_plugin("draftail", name, feature)

        # This has to be lower because html attr names get lowered and
        # the DOM selector has to match.  The type in the actual handler
        # doesn't get lowered because it's the real type draftail is expecting.
        t = prefix + draftail_type.lower()

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
