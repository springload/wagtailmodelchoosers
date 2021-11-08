from wagtail.admin.edit_handlers import BaseChooserPanel
from wagtail.utils.decorators import cached_classmethod

from wagtailmodelchoosers.utils import flatten, get_chooser_options
from wagtailmodelchoosers.widgets import ModelChooserWidget, RemoteModelChooserWidget


class BaseModelChooserPanel(BaseChooserPanel):
    object_type_name = "model"

    @cached_classmethod
    def target_model(cls):
        return cls.model._meta.get_field(cls.field_name).remote_field.model

    @classmethod
    def get_required(cls):
        null = cls.model._meta.get_field(cls.field_name).null
        return not null

    @classmethod
    def widget_overrides(cls):
        return {
            cls.field_name: ModelChooserWidget(
                cls.target_model(),
                required=cls.get_required(),
                label=cls.label,
                display=cls.display,
                list_display=cls.list_display,
                filters=cls.filters,
                page_size_param=cls.page_size_param,
                page_size=cls.page_size,
                pk_name=cls.pk_name,
                translations=cls.translations,
            )
        }


class ModelChooserPanel(object):
    def __init__(self, field_name, chooser, **kwargs):
        options = get_chooser_options(chooser)
        options.update(kwargs)

        self.field_name = field_name
        self.chooser = chooser
        self.label = options.pop("label", chooser)
        self.display = options.pop("display", "title")
        self.list_display = options.pop("list_display", list(flatten([self.display])))
        self.filters = options.pop("filters", [])
        self.page_size_param = options.pop("page_size_param", None)
        self.page_size = options.pop("page_size", None)
        self.pk_name = options.pop("pk_name", "uuid")
        self.translations = options.pop("translations", [])

    def bind_to_model(self, model):
        return type(
            str("_ModelChooserPanel"),
            (BaseModelChooserPanel,),
            {
                "model": model,
                "field_name": self.field_name,
                "label": self.label,
                "display": self.display,
                "list_display": self.list_display,
                "filters": self.filters,
                "page_size_param": self.page_size_param,
                "page_size": self.page_size,
                "pk_name": self.pk_name,
                "translations": self.translations,
            },
        )(field_name=self.field_name)


class BaseRemoteModelChooserPanel(BaseChooserPanel):
    object_type_name = "remote_model"

    @classmethod
    def get_required(cls):
        blank = cls.model._meta.get_field(cls.field_name).blank
        return not blank

    @classmethod
    def widget_overrides(cls):
        return {
            cls.field_name: RemoteModelChooserWidget(
                cls.chooser,
                required=cls.get_required(),
                label=cls.label,
                display=cls.display,
                list_display=cls.list_display,
                filters=cls.filters,
                page_size_param=cls.page_size_param,
                page_size=cls.page_size,
                fields_to_save=cls.fields_to_save,
                pk_name=cls.pk_name,
                translations=cls.translations,
            )
        }


class RemoteModelChooserPanel(object):
    def __init__(self, field_name, chooser, **kwargs):
        options = get_chooser_options(chooser)
        options.update(kwargs)

        self.field_name = field_name
        self.chooser = chooser
        self.label = options.pop("label", chooser)
        self.display = options.pop("display", "title")
        self.list_display = options.pop("list_display", list(flatten([self.display])))
        self.filters = options.pop("filters", [])
        self.page_size_param = options.pop("page_size_param", None)
        self.page_size = options.pop("page_size", None)
        self.fields_to_save = options.pop("fields_to_save", None)
        self.pk_name = options.pop("pk_name", "uuid")
        self.translations = options.pop("translations", [])

    def bind_to_model(self, model):
        return type(
            str("_RemoteModelChooserPanel"),
            (BaseRemoteModelChooserPanel,),
            {
                "model": model,
                "field_name": self.field_name,
                "chooser": self.chooser,
                "label": self.label,
                "display": self.display,
                "list_display": self.list_display,
                "filters": self.filters,
                "page_size_param": self.page_size_param,
                "page_size": self.page_size,
                "fields_to_save": self.fields_to_save,
                "pk_name": self.pk_name,
                "translations": self.translations,
            },
        )(field_name=self.field_name)
