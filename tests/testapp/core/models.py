from __future__ import absolute_import, unicode_literals

from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page
from wagtailmodelchoosers.edit_handlers import ModelChooserPanel

__all__ = ['SimplePage']


class OtherPage(Page):
    content = models.TextField()


class SimplePage(Page):
    content = models.TextField()
    other_page = models.ForeignKey(
            OtherPage,
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name="+",
        )

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('content'),
        ModelChooserPanel('other_page', chooser='other_page'),
    ]
