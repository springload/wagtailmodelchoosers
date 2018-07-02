from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page

from wagtailmodelchoosers.edit_handlers import ModelChooserPanel

__all__ = ['SimplePage']


class SimplePage(Page):
    required_simple_model = models.ForeignKey(
        'core.SimpleModel',
        related_name='+',
        on_delete=models.PROTECT,
    )
    optional_simple_model = models.ForeignKey(
        'core.SimpleModel',
        related_name='+',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    content_panels = [
        FieldPanel('title', classname="full title"),
        ModelChooserPanel('required_simple_model', chooser='simple_model'),
        ModelChooserPanel('optional_simple_model', chooser='simple_model'),
    ]


class SimpleModel(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name
