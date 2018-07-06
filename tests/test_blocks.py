from django.test import TestCase, override_settings
from wagtail.core.models import Page
from wagtail.tests.utils.form_data import rich_text

from core.models import SimpleModel, SimplePage
from wagtailmodelchoosers import blocks, widgets

TEST_MODEL_CHOOSERS_OPTIONS = {
    'core_page': {
        'content_type': 'wagtailcore.Page',
    }
}


@override_settings(MODEL_CHOOSERS_OPTIONS=TEST_MODEL_CHOOSERS_OPTIONS)
class TestModelChooserBlock(TestCase):
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

    def test_serialize(self):
        """The value of a ModelChooserBlock (a Page object) should serialize to an ID"""
        block = blocks.ModelChooserBlock('core_page')
        self.assertEqual(block.get_prep_value(self.child_page), self.child_page.id)

        # None should serialize to None
        self.assertEqual(block.get_prep_value(None), None)

    def test_deserialize(self):
        """The serialized value of a ModelChooserBlock (an ID) should deserialize to a Page object"""
        block = blocks.ModelChooserBlock('core_page')
        self.assertEqual(isinstance(block.to_python(self.child_page.id), Page), isinstance(self.child_page, Page))

        # None should deserialize to None
        self.assertEqual(block.to_python(None), None)

    def test_form_render(self):
        block = blocks.ModelChooserBlock('core_page', help_text="pick a page, any page")

        empty_form_html = block.render_form(None, 'page')
        self.assertIn('<input type="hidden" value="" name="page"', empty_form_html)
        self.assertIn('initModelChooser(', empty_form_html)

        test_page = self.child_page
        test_form_html = block.render_form(test_page, 'page')
        expected_html = '<input type="hidden" value="%d" name="page" ' % test_page.id
        self.assertIn(expected_html, test_form_html)
        self.assertIn("pick a page, any page", test_form_html)

    def test_to_python(self):
        block = blocks.ModelChooserBlock('core_page')
        test_page = self.child_page

        value = block.to_python(test_page.pk)
        self.assertEqual(isinstance(value, Page), isinstance(test_page, Page))
        self.assertEqual(block.to_python(None), None)

    def test_get_prep_value(self):
        block = blocks.ModelChooserBlock('core_page')
        test_page = self.child_page

        self.assertEqual(block.get_prep_value(test_page.pk), test_page.pk)
        self.assertEqual(block.get_prep_value(test_page), test_page.pk)
        self.assertEqual(block.get_prep_value(None), None)

    def test_target_model(self):
        block = blocks.ModelChooserBlock('core_page')
        self.assertEqual(block.target_model, Page)

    def test_widget(self):
        block = blocks.ModelChooserBlock('core_page')
        self.assertTrue(isinstance(block.widget, widgets.ModelChooserWidget))
