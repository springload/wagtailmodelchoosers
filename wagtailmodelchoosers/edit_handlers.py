from wagtail.admin.edit_handlers import BaseChooserPanel

from wagtailmodelchoosers.utils import flatten, get_chooser_options
from wagtailmodelchoosers.widgets import ModelChooserWidget, RemoteModelChooserWidget


class ModelChooserPanel(BaseChooserPanel):
    object_type_name = 'model'

    def __init__(self, field_name, chooser, **kwargs):
        options = get_chooser_options(chooser)
        options.update(kwargs)

        self.field_name = field_name
        self.chooser = chooser
        self.label = options.pop('label', chooser)
        self.display = options.pop('display', 'title')
        self.list_display = options.pop('list_display', list(flatten([self.display])))
        self.filters = options.pop('filters', [])
        self.page_size_param = options.pop('page_size_param', None)
        self.page_size = options.pop('page_size', None)
        self.pk_name = options.pop('pk_name', 'uuid')
        self.translations = options.pop('translations', [])

        # The `ModelChooserBlock` required the `content_type` option
        # which the pannel does not need, poping it out.
        options.pop('content_type', None)

        super().__init__(field_name, **options)

    def target_model(self):
        return self.model._meta.get_field(self.field_name).related_model

    def get_required(self):
        null = self.model._meta.get_field(self.field_name).null
        return not null

    def widget_overrides(self):
        return {
            self.field_name: ModelChooserWidget(
                self.target_model(),
                required=self.get_required(),
                label=self.label,
                display=self.display,
                list_display=self.list_display,
                filters=self.filters,
                page_size_param=self.page_size_param,
                page_size=self.page_size,
                pk_name=self.pk_name,
                translations=self.translations,
            )
        }

    def clone(self):
        return self.__class__(
            field_name=self.field_name,
            widget=self.widget if hasattr(self, 'widget') else None,
            heading=self.heading,
            classname=self.classname,
            help_text=self.help_text,
            chooser=self.chooser,
        )


class RemoteModelChooserPanel(BaseChooserPanel):
    object_type_name = 'remote_model'

    def __init__(self, field_name, chooser, **kwargs):
        options = get_chooser_options(chooser)
        options.update(kwargs)

        self.field_name = field_name
        self.chooser = chooser
        self.label = options.pop('label', chooser)
        self.display = options.pop('display', 'title')
        self.list_display = options.pop('list_display', list(flatten([self.display])))
        self.filters = options.pop('filters', [])
        self.page_size_param = options.pop('page_size_param', None)
        self.page_size = options.pop('page_size', None)
        self.fields_to_save = options.pop('fields_to_save', None)
        self.pk_name = options.pop('pk_name', 'uuid')
        self.translations = options.pop('translations', [])

        super().__init__(field_name, **options)

    def get_required(self):
        blank = self.model._meta.get_field(self.field_name).blank
        return not blank

    def widget_overrides(self):
        return {
            self.field_name: RemoteModelChooserWidget(
                self.chooser,
                required=self.get_required(),
                label=self.label,
                display=self.display,
                list_display=self.list_display,
                filters=self.filters,
                page_size_param=self.page_size_param,
                page_size=self.page_size,
                fields_to_save=self.fields_to_save,
                pk_name=self.pk_name,
                translations=self.translations,
            )
        }
