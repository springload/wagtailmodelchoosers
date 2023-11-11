import re

from html import unescape
from django.conf import settings
from django.utils.module_loading import import_string
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from draftjs_exporter.dom import DOM
from wagtail.core.rich_text import LinkHandler
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineEntityElementHandler
from wagtail.core.rich_text.rewriters import extract_attrs


"""
This basically revives the old way of registering draftail extensions where you don't have to
think about from_database or to_database matching rules.  Also it wraps old style decorators
into a link rewriter in a hacky way.
"""


ENTITY_TAG_NAME = "entity"
ENTITY_ID_ATTR_NAME = ENTITY_TAG_NAME + "_id"
ENTITY_TYPE_ATTR_NAME = ENTITY_TAG_NAME + "_type"


class FromDBHandler(InlineEntityElementHandler):
    mutability = "IMMUTABLE"

    # Populate 'id' but leave original attrs alone
    def get_attribute_data(self, attrs):
        self.attrs = attrs
        extra = {}
        if ENTITY_ID_ATTR_NAME in attrs:
            extra = {"id": attrs[ENTITY_ID_ATTR_NAME]}
        return dict(attrs, **extra)


def default_expand_attrs(attrs):
    tag = DOM.create_element(ENTITY_TAG_NAME, attrs)
    return str(DOM.render(tag))


class EntityLinkRewriter:
    """Everything is entity and entity_type now.  also, this comment should say something better"""
    A_TAG_AND_CHILDREN = re.compile(r"<entity(\b[^>]*)>(.+?)</entity>")

    def __init__(self):
        self.expanders = {}

    def add_type(self, t, expander):
        self.expanders[t] = expander

    def replace_tag(self, match):
        attrs = extract_attrs(match.group(1))
        attrs["children"] = match.group(2)

        entity_type = attrs.get(ENTITY_TYPE_ATTR_NAME, None)
        if not entity_type:
            return match.string
        expander = self.expanders.get(entity_type, None)
        if not expander:
            return match.string
        return DOM.render(expander(attrs))

    def __call__(self, html):
        decorated_html = self.A_TAG_AND_CHILDREN.sub(self.replace_tag, html)

        # Can't get draftjs_exporter to disable escaping and there's another layer
        # of escaping further up the stack, so need to unescape here.
        return unescape(decorated_html)


entity_rewriter = EntityLinkRewriter()


def to_database_format(t):
    def inner(props):
        children = props.pop("children", "")

        props[ENTITY_TYPE_ATTR_NAME] = t
        if "id" in props:
            props[ENTITY_ID_ATTR_NAME] = str(props["id"])

        return DOM.create_element(ENTITY_TAG_NAME, props, children)
    return inner


def register_entity(features, chooser, name, draftail_type, prefix):
    feature = draftail_features.EntityFeature(chooser)
    features.register_editor_plugin("draftail", name, feature)

    # This has to be lower because html attr names get lowered and
    # the DOM selector has to match.  The type in the actual handler
    # doesn't get lowered because it's the real type draftail is expecting.
    t = prefix + draftail_type.lower()

    rule = {
        "from_database_format": {"{}[{}={}]".format(ENTITY_TAG_NAME, ENTITY_TYPE_ATTR_NAME, t): FromDBHandler(draftail_type)},
        "to_database_format": {"entity_decorators": {draftail_type: to_database_format(t)}},
    }

    features.register_converter_rule("contentstate", name, rule)

    expander_path = getattr(settings, "DRAFT_EXPORTER_ENTITY_DECORATORS", {}).get(draftail_type, None)
    expander = default_expand_attrs
    if expander_path:
        expander = import_string(expander_path)

    entity_rewriter.add_type(t, expander)
