from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import SimpleModel


class SimpleModelModelAdmin(ModelAdmin):
    model = SimpleModel


modeladmin_register(SimpleModelModelAdmin)
