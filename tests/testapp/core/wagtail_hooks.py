from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.core import hooks
from wagtailmodelchoosers.rich_text import get_chooser_feature

from .models import SimpleModel

register_simple_model_chooser_feature, register_simple_model_chooser_plugin = get_chooser_feature(
    chooser='simple_model', feature_name='simple_model', feature_type='SIMPLE_MODEL')


@hooks.register('register_rich_text_features')
def register_chooser_feature(features):
    register_simple_model_chooser_feature(features)


@hooks.register('insert_editor_js')
def insert_chooser_js():
    return register_simple_model_chooser_plugin


@modeladmin_register
class SimpleModelModelAdmin(ModelAdmin):
    model = SimpleModel
