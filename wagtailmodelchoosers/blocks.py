import json

from django import forms
from django.apps import apps
from django.utils.functional import cached_property

from wagtail.core.blocks import ChooserBlock

from wagtailmodelchoosers.utils import first_non_empty, flatten, get_chooser_options
from wagtailmodelchoosers.widgets import ModelChooserWidget, RemoteModelChooserWidget


class ModelChooserBlock(ChooserBlock):
    def __init__(self, chooser, **kwargs):
        options = get_chooser_options(chooser)
        options.update(kwargs)

        self.chooser = chooser
        self.content_type = options.pop('content_type')
        self.label = options.pop('label', chooser)
        self.display = options.pop('display', 'title')
        self.list_display = options.pop('list_display', list(flatten([self.display])))
        self.filters = options.pop('filters', [])
        self.page_size_param = options.pop('page_size_param', None)
        self.page_size = options.pop('page_size', None)
        self.pk_name = options.pop('pk_name', 'uuid')
        self.translations = options.pop('translations', [])

        super(ModelChooserBlock, self).__init__(**kwargs)

    @cached_property
    def target_model(self):
        return apps.get_model(self.content_type)

    @cached_property
    def widget(self):
        return ModelChooserWidget(
            self.target_model,
            required=self._required,
            label=self.label,
            display=self.display,
            list_display=self.list_display,
            filters=self.filters,
            page_size_param=self.page_size_param,
            page_size=self.page_size,
            pk_name=self.pk_name,
            translations=self.translations,
        )

    def get_prep_value(self, value):
        # The native value (a model instance or None) should serialise to a PK or None
        if not value:
            return None

        elif isinstance(value, (int, str)):
            return value

        else:
            return value.pk

    def to_python(self, value):
        if not value:
            return None

        try:
            return self.target_model.objects.get(pk=value)
        except self.target_model.DoesNotExist:
            return None

    def bulk_to_python(self, values):
        return [self.to_python(value) for value in values]

    def value_from_form(self, value):
        if not value:
            return None

        elif isinstance(value, self.target_model):
            return value

        else:
            try:
                return self.target_model.objects.get(pk=value)
            except self.target_model.DoesNotExist:
                return None

    def render_basic(self, value, context=None):
        return first_non_empty(value, self.display, default='')

    class Meta:
        icon = "snippet"


class RemoteModelChooserBlock(ChooserBlock):
    def __init__(self, chooser, **kwargs):
        options = get_chooser_options(chooser)
        options.update(kwargs)

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

        super(RemoteModelChooserBlock, self).__init__(**options)

    @cached_property
    def field(self):
        return forms.CharField(
            widget=self.widget,
            required=self._required,
            help_text=self._help_text
        )

    @cached_property
    def widget(self):
        return RemoteModelChooserWidget(
            self.chooser,
            required=self._required,
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

    def get_prep_value(self, value):
        return value

    def to_python(self, value):
        if not value:
            return {}

        elif isinstance(value, dict):
            return value

        else:
            return json.loads(value)

    def bulk_to_python(self, values):
        return [self.to_python(value) for value in values]

    def value_for_form(self, value):
        return value

    def value_from_form(self, value):
        if not value:
            return None

        try:
            # Ensure we have a serialisable JSON object.
            return json.dumps(json.loads(value))
        except ValueError:
            return None

    def render_basic(self, value, context=None):

        # When previewing a page, the form field value (a string) will not be converted with `to_python`
        # and will be passed to this method directly.
        if isinstance(value, str):
            value = self.to_python(value)

        return first_non_empty(value, self.display, default='')

    def clean(self, value):
        return value

    class Meta:
        icon = 'snippet'
        default = {}
