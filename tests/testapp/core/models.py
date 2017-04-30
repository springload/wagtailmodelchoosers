from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.models import Page

__all__ = ['SimplePage']


class SimplePage(Page):
    content = models.TextField()

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('content'),
    ]
