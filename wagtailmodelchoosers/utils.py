import collections
import copy

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def is_list(obj):
    return isinstance(obj, collections.Sequence) and not isinstance(obj, (str, bytes))


def flatten(list_):
    """
    Flatten irregular list of lists
    """
    for element in list_:
        if is_list(element):
            for sub in flatten(element):
                yield sub
        else:
            yield element


def get_chooser_options(chooser):
    """
    :type chooser: str
    :param chooser: the chooser name
    :rtype: dict
    :return: the chooser options
    :raise: django.core.exceptions.ImproperlyConfigured if the chooser definition is missing \
            or if it lack some required keys.
    """
    choosers_options = getattr(settings, 'MODEL_CHOOSERS_OPTIONS', {})

    chooser_options = choosers_options.get(chooser)
    if not chooser_options:
        raise ImproperlyConfigured(
            'Missing options definition for chooser `{}` in `MODEL_CHOOSERS_OPTIONS`'.format(chooser))

    if not ('content_type' in chooser_options or 'remote_endpoint' in chooser_options):
        raise ImproperlyConfigured((
            'The `{}` chooser definition should define either '
            '`content_type` (for models) or `remote_endpoint` (for remote models)'
        ).format(chooser))

    fields_to_save = chooser_options.get('fields_to_save')
    if fields_to_save:
        display = chooser_options.get('display', 'title')
        display = list(flatten([display]))
        missing_fields = [field for field in display if field not in fields_to_save]

        if missing_fields:
            missing_fields = ', '.join(map(lambda f: '`{}`'.format(f), missing_fields))
            raise ImproperlyConfigured((
                'Invalid `fields_to_save` definition for chooser `{}`, '
                'it should contain at least all the fields from `display` and is currently missing: {}'
            ).format(chooser, missing_fields))

    return copy.deepcopy(chooser_options)


def first_non_empty(data_or_instance, field_or_fields, default=None):
    """
    Return the first non-empty attribute of `instance` or `default`

    :type data_or_instance: object or dict
    :param data_or_instance: the instance or the resource
    :type field_or_fields: str or tuple or list
    :param field_or_fields: the field or fields to look for on the resource
    :type default: anything
    :param default: the default value to return if no non-empty field was found, default to None
    :return: the first non-empty field of `instance` or `default`
    """

    # Convert `data_or_instance` to an object-like structure
    # so attributes can be fetched with `getattr` regardless of the initial type.
    if isinstance(data_or_instance, dict):
        class ObjectView(object):
            def __init__(self, d):
                self.__dict__ = d

        obj = ObjectView(data_or_instance)

    else:
        obj = data_or_instance

    # Find the first non-empty.
    if isinstance(field_or_fields, str):
        return getattr(obj, field_or_fields, default)

    elif isinstance(field_or_fields, (tuple, list)):
        for field in field_or_fields:
            val = getattr(obj, field, None)
            if val:
                return val

    return default


def get_query_keys_map(resource_options):
    return {
        'page_size': resource_options.get('remote_query_page_size_key', 'page_size'),
        'page': resource_options.get('remote_query_page_key', 'page'),
        'search': resource_options.get('remote_query_search_key', 'search'),
    }


def get_response_keys_map(resource_options):
    return {
        'results': resource_options.get('remote_response_data_key', 'results'),
        'page': resource_options.get('remote_response_page_key', 'page'),
        'num_pages': resource_options.get('remote_response_pages_count_key', 'num_pages'),
        'next': resource_options.get('remote_response_next_page_key', 'next'),
        'previous': resource_options.get('remote_response_previous_page_key', 'previous'),
        'count': resource_options.get('remote_response_items_count_key', 'count'),
    }
