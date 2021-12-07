from __future__ import absolute_import, unicode_literals

from core.models import SimplePage
from django.test import TestCase, override_settings
from wagtail.admin.edit_handlers import BaseChooserPanel
from wagtail.core.models import Page

from wagtailmodelchoosers import blocks, widgets, edit_handlers

TEST_MODEL_CHOOSERS_OPTIONS = {
    'core_page': {
        'content_type': 'wagtailcore.Page',
    },
    'other_page': {
        'content_type': 'wagtailcore.Page',
    }
}


@override_settings(MODEL_CHOOSERS_OPTIONS=TEST_MODEL_CHOOSERS_OPTIONS)
class TestModelChooserPanel(TestCase):
    def setUp(self):
        self.root_page = Page.objects.get(id=2)

        # Add child page
        self.child_page = SimplePage(
            title="foobarbaz",
            content="hello",
        )
        self.root_page.add_child(instance=self.child_page)

    def test_serialize(self):
        """The value of a ModelChooserBlock (a Page object) should serialize to an ID"""
        panel = edit_handlers.ModelChooserPanel('other_page', chooser='other_page')
        # None should serialize to None
        self.assertIsInstance(panel, BaseChooserPanel)
