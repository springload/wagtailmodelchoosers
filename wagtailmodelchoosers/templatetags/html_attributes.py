from django import template
from django.utils.html import conditional_escape, strip_tags
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def html_attributes(attrs, exclude=None):
    """
    Convert a mapping of html attributes to a safe string (with boolean support).

    :type attrs: dict
    :param attrs: the html attributes key/values
    :type exclude: str or list or tuple
    :param exclude: a comma separated string or a list of attributes to exclude
    :rtype: str
    :return: a safe string of html attributes
    """

    # Ensure `exclude` is a list of lowercase keys.
    if exclude is None:
        exclude = []
    elif isinstance(exclude, str):
        exclude = exclude.split(',')
    exclude = list(map(lambda e: e.strip().lower(), exclude))

    html_attrs = []
    for key, val in attrs.items():
        if key.lower() in exclude:
            continue

        # Only include boolean values if `True`, and only add the attribute name (no value) as per HTML specs.
        if isinstance(val, bool):
            if val:
                html_attrs.append(strip_tags(key))

        # Other attributes, display normally.
        else:
            html_attrs.append('{key}="{val}"'.format(key=strip_tags(key), val=conditional_escape(val)))

    return mark_safe(' '.join(html_attrs))
