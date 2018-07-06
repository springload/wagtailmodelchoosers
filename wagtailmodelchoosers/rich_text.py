import re

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html, format_html_join
from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineEntityElementHandler
from wagtail.admin.rich_text.editors.draftail import features as draftail_features

from .utils import get_chooser_options


def normalize_entity_name(name):
    """
    Lower and replace non-alphanumeric characters with underscores.
    """

    return re.sub(r'[^\w]', '_', name.lower())


def get_chooser_generic_to_database_format(feature_name):
    entity_name = normalize_entity_name(feature_name)
    attrname = 'data-{}'.format(entity_name.replace('_', '-'))

    def entity_decorator(props):
        return DOM.create_element(
            'span',
            {attrname: props['value']},
            props['children'],
        )
    entity_decorator.__name__ = '{}_entity_decorator'.format(feature_name)

    return entity_decorator


def get_chooser_generic_from_database_format(feature_name):
    entity_name = normalize_entity_name(feature_name)
    attrname = 'data-{}'.format(entity_name.replace('_', '-'))
    klassname = '{}EntityElementHandler'.format(entity_name.title().replace('_', ''))

    class BaseEntityElementHandler(InlineEntityElementHandler):
        mutability = 'IMMUTABLE'

        def get_attribute_data(self, attrs):
            return {
                'value': attrs[attrname],
            }

    return type(klassname, (BaseEntityElementHandler,), {})


def get_chooser_feature(
    chooser,
    feature_name,
    feature_type,
    icon=None,
    label=None,
    description=None,
    from_database_format=None,
    to_database_format=None,
    js_source='window.wagtailModelChoosers.ModelSource',
    js_decorator='window.wagtailModelChoosers.GenericModelDecorator',
):

    # Base control options
    chooser_options = get_chooser_options('simple_model')
    control = dict(chooser_options, **{
        'type': feature_type,
    })

    # Add overwrites if any
    if icon:
        control['icon'] = icon
    if label:
        control['label'] = label
    if description:
        control['description'] = description

    # Get converters
    from_database_format = from_database_format or get_chooser_generic_from_database_format(feature_name)
    to_database_format = to_database_format or get_chooser_generic_to_database_format(feature_name)

    # Create register feature function
    def register_feature(features):
        # Register the feature
        features.register_editor_plugin(
            'draftail',
            feature_name,
            draftail_features.EntityFeature(control),
        )

        # Register the converter rules
        features.register_converter_rule(
            'contentstate',
            feature_name,
            {
                'from_database_format': {'span[data-stock]': from_database_format(feature_type)},  # TODO: Replace stock
                'to_database_format': {'entity_decorators': {feature_type: to_database_format}},
            }
        )

    # Create register plugin scripts
    js_dependencies = (
        'wagtailadmin/js/draftail.js',
        'wagtailmodelchoosers/wagtailmodelchoosers.js',
        'wagtailmodelchoosers/polyfills.js',
    )
    js_includes = format_html_join(
        '\n',
        '<script src="{}"></script>',
        ((static(filename),) for filename in js_dependencies)
    )

    js_script = format_html(
        "<script>window.draftail.registerPlugin({{type: '{0}', source: {1}, decorator: {2},}});</script>",
        feature_type,
        js_source,
        js_decorator,
    )

    register_plugin = js_includes + js_script

    return register_feature, register_plugin
