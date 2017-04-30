from collections import OrderedDict

from django.test import TestCase

from wagtailmodelchoosers.templatetags.html_attributes import html_attributes


class HTMLAttributesTestCase(TestCase):

    def test_html_attributes_with_no_attributes(self):
        self.assertEqual(html_attributes({}), '')

    def test_html_attributes_with_text_attributes(self):
        # Use an OrderedDict to guarantee the order output for the test purposes.
        attrs = OrderedDict([('id', 'name'), ('placeholder', 'Arthur Dent')])
        expected_output = 'id="name" placeholder="Arthur Dent"'

        self.assertEqual(html_attributes(attrs), expected_output)

    def test_html_attributes_with_truthy_boolean_attribute(self):
        attrs = {'checked': True}
        expected_output = 'checked'

        self.assertEqual(html_attributes(attrs), expected_output)

    def test_html_attributes_with_falsy_boolean_attribute(self):
        attrs = {'checked': False}
        expected_output = ''

        self.assertEqual(html_attributes(attrs), expected_output)

    def test_html_attributes_with_mixed_attributes(self):
        # Use an OrderedDict to guarantee the order output for the test purposes.
        attrs = OrderedDict([('id', 'name'), ('placeholder', 'Arthur Dent'), ('checked', False), ('disabled', True)])
        expected_output = 'id="name" placeholder="Arthur Dent" disabled'

        self.assertEqual(html_attributes(attrs), expected_output)

    def test_html_attributes_excludes_excluded_fields(self):
        attrs = {'id': 'name', 'placeholder': 'Arthur Dent'}
        exclude = ['placeholder']
        expected_output = 'id="name"'

        self.assertEqual(html_attributes(attrs, exclude), expected_output)

    def test_html_attributes_excludes_excluded_fields_regardless_of_case_or_surrounding_spaces(self):
        attrs = {'id': 'name', 'placeholder': 'Arthur Dent'}
        exclude = ['ID', '   placeholder   ']
        expected_output = ''

        self.assertEqual(html_attributes(attrs, exclude), expected_output)

    def test_html_attributes_excludes_as_comma_separated_string(self):
        attrs = {'id': 'name', 'placeholder': 'Arthur Dent'}
        exclude = 'placeholder,id'
        expected_output = ''

        self.assertEqual(html_attributes(attrs, exclude), expected_output)

    def test_html_attributes_strip_tags_for_keys(self):
        attrs = {'<span>hello</span>': 'name'}
        expected_output = 'hello="name"'

        self.assertEqual(html_attributes(attrs), expected_output)

    def test_html_attributes_escapes_values(self):
        attrs = {'value': '<>&\'"'}
        expected_output = 'value="&lt;&gt;&amp;&#39;&quot;"'

        self.assertEqual(html_attributes(attrs), expected_output)
