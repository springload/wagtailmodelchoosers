from django.apps import AppConfig


class Config(AppConfig):
    name = "wagtailmodelchoosers"

    def ready(self):
        from wagtail.core import rich_text
        rich_text.expand_db_html("")

        from .register_entity import entity_rewriter
        rich_text.FRONTEND_REWRITER.rewriters.append(entity_rewriter)
