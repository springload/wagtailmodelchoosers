import uuid

from django.test import TestCase
from wagtail.core.models import Page
from wagtail.tests.utils.form_data import rich_text

from core.models import SimpleModel, SimplePage
from wagtailmodelchoosers import widgets


class TestModelChooserWidget(TestCase):
    def setUp(self):
        self.root_page = Page.objects.get(id=2)

        # Add test model
        self.simple_model = SimpleModel.objects.create(name='Choubidou')

        # Add child page
        self.child_page = SimplePage(
            title='foobarbaz',
            rich_text=rich_text('hello'),
            required_simple_model=self.simple_model,
        )
        self.root_page.add_child(instance=self.child_page)

    def get_widget_options(self):
        return {
            'display': 'title',
            'list_display': [{'name': 'title', 'label': 'Title'}],
            'pk_name': 'id',
        }

    def test_get_target_model_string(self):
        widget = widgets.ModelChooserWidget('wagtailcore.Page', **self.get_widget_options())
        model = widget.target_model()
        self.assertEqual(model.__class__, Page)

    def test_get_target_model_class(self):
        widget = widgets.ModelChooserWidget(Page, **self.get_widget_options())
        model = widget.target_model()
        self.assertEqual(model.__class__, Page)

    def test_get_instance_none_value(self):
        widget = widgets.ModelChooserWidget(Page, **self.get_widget_options())
        self.assertFalse(widget.get_instance(''))

    def test_get_instance_page_value(self):
        widget = widgets.ModelChooserWidget(Page, **self.get_widget_options())
        self.assertEqual(widget.get_instance(2), self.root_page)

    def test_get_instance_no_page_value_is_none(self):
        widget = widgets.ModelChooserWidget(Page, **self.get_widget_options())
        self.assertEqual(widget.get_instance(999), None)

    def test_url_builder(self):
        widget = widgets.ModelChooserWidget(Page, **self.get_widget_options())
        url = widget.get_endpoint()
        self.assertEqual(url, '/admin/modelchoosers/api/v1/model/wagtailcore.Page')

    def test_get_internal_value(self):
        id_ = uuid.uuid4()

        class Stub:
            pk = None

        stub = Stub()
        stub.pk = id_
        widget = widgets.ModelChooserWidget(Page, **self.get_widget_options())
        value = widget.get_internal_value(stub)
        self.assertEqual(value, str(id_))

    def test_get_js_init_data(self):
        widget = widgets.ModelChooserWidget(Page, **self.get_widget_options())
        data = widget.get_js_init_data('field-1', None, self.root_page)
        expected_data = {
            'label': 'Page',
            'required': True,
            'initial_display_value': 'Welcome to your new Wagtail site!',
            'display': 'title',
            'list_display': [{'name': 'title', 'label': 'Title'}],
            'endpoint': '/admin/modelchoosers/api/v1/model/wagtailcore.Page',
            'pk_name': 'id',
        }

        self.assertEqual(data, expected_data)

    def test_render_js_init(self):
        widget = widgets.ModelChooserWidget(Page, **self.get_widget_options())
        js_init = widget.render_js_init('field-1', None, self.root_page)

        expected_pattern = (
            r'^'                                        # Start of line
            r'wagtailModelChoosers.initModelChooser\('  # Function name
            r'".+"'                                     # First argument, the field id (a string)
            r', '                                       # Comma and space between arguments
            r'.+'                                       # Second argument, the data (an object)
            r'\)'                                       # End of function
            r'$'                                        # End of line
        )

        self.assertRegex(js_init, expected_pattern)

    def test_render_html(self):
        widget = widgets.ModelChooserWidget(Page, **self.get_widget_options())
        html = widget.render_html('test', None, {})
        self.assertIn('<input type="hidden" value="" name="test" >', html)

    def test_render_html_with_value(self):
        widget = widgets.ModelChooserWidget(Page, **self.get_widget_options())
        html = widget.render_html('test', self.root_page, {})
        self.assertIn('<input type="hidden" value="2" name="test" >', html)
