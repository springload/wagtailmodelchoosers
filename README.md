[![Travis](https://travis-ci.org/springload/wagtailmodelchoosers.svg?branch=master)](https://travis-ci.org/springload/wagtailmodelchoosers)
[![PyPi](https://img.shields.io/pypi/v/wagtailmodelchoosers.svg)](https://pypi.python.org/pypi/wagtailmodelchoosers)

# Wagtail Model Choosers

> A Wagtail app to pick generic models (rather than snippets or pages).

**This is alpha software, use at your own risk. Do not use in production (yet).**

Check out [Awesome Wagtail](https://github.com/springload/awesome-wagtail) for more awesome packages and resources from the Wagtail community.

[![screenshot](https://cdn.rawgit.com/springload/wagtailmodelchoosers/b7b6202/.github/wagtailmodelchoosers-screenshot.png)]

## Installation

1. Grab the package from pip with `pip install wagtailmodelchoosers`.
1. Add `wagtailmodelchoosers` in `INSTALLED_APPS` in your settings.

## Usage

### Blocks & Fields

`ModelChooserBlock` takes the name of the chooser configuration as first positional argument. Use other block kwargs (e.g. `required`) as usual.

```python
from wagtail.wagtailcore import blocks
from wagtailmodelchoosers.blocks import ModelChooserBlock

class CustomBlock(blocks.StructBlock):
    custom_model = ModelChooserBlock(chooser='custom_model')
```

`ModelChooserPanel` takes the name of the field as first positional argument (like a regular Panel) and the name of the chooser configuration as second positional argument. Use other panel kwargs as usual.

```python
from django.db import models
from wagtail.core.models import Page
from wagtailmodelchoosers.edit_handlers import ModelChooserPanel

class CustomPage(Page):
    custom_model = models.ForeignKey('myapp.CustomModel')

    panels = [
        ModelChooserPanel('custom_model', chooser='custom_model'),
    ]
```

To select a model from a remote API, respectively use `RemoteModelChooserBlock` and `RemoteModelChooserPanel` instead.

### Draftail

**Important**: Whether you use [WagtailDraftail](https://github.com/springload/wagtaildraftail) or use `Wagtail 2.x` built-in `Draftail` editor, the underlying version of `Draftail` needs to be at least `v0.17.0`.

If you have `WagtailDraftail` installed, it will automatically register the `ModelSource` and `RemoteModelSource` to the JS. Refer to `WagtailDraftail`'s [documentation](https://github.com/springload/wagtaildraftail#configuration) to hook it up properly.

If you use `Draftail` from `Wagtail 2.x`, do the following in you app's `wagtail_hooks.py` file:

```python
from wagtailmodelchoosers.rich_text import get_chooser_feature


register_custom_model_chooser_feature, register_custom_model_chooser_plugin = get_chooser_feature(
    # Required.
    chooser='custom_model',       # Same as what was used for the block and/or panel.
    feature_name='custom_model',  # RichText's feature name (e.g. `RichTextField(features=['bold', 'custom_model'])`).
    feature_type='CUSTOM_MODEL',  # Draftail's *unique* and *never changing* feature ID.

    # Optional but recommended for nice UI display.
    icon='icon icon-snippet',
    label='Custom Model',
    description='Insert a Custom Model inline',

    # Optional if you need to customise the generic behaviour.
    # Note that it requires good knowlegde of Draftail source/decorators and Wagtail features converters.
    from_database_format=None,    # Wagtail from database converter
    to_database_format=None,      # Wagtail to database converter
    js_source='',                 # Draftail Source
    js_decorator='',              # Draftail Decorator
)


@hooks.register('register_rich_text_features')
def register_chooser_feature(features):
    register_custom_model_chooser_feature(features)


@hooks.register('insert_editor_js')
def insert_chooser_js():
    return register_custom_model_chooser_plugin
```

### Configuration

It looks for a `MODEL_CHOOSERS_OPTIONS` dictionary in the settings where the key is the name of the chooser and the value, a dictionary of options.

The ModelChooser and RemoteModelChooser share a similar base configuration and only have a few specific fields.

```python
NAVIGATION_DISPLAY = 'name'
MODEL_CHOOSERS_OPTIONS = {
    'navigation': {
        'label': 'Navigation',                                   # The label to use for buttons or modal title
        'display': NAVIGATION_DISPLAY,                           # The field to display when selecting an object
        'list_display': [                                        # The fields to display in the chooser
            {'label': 'Name', 'name': 'name'},
            {'label': 'Identity', 'name': 'identity'},
            {'label': 'Active', 'name': 'active'},
        ],
        'pk_name': 'uuid',                                       # The primary key name of the model

        # ONLY FOR MODEL:
        'content_type': 'core.Navigation',                       # The django content type of the model

        # ONLY FOR REMOTE:
        'fields_to_save': ['id', NAVIGATION_DISPLAY],            # The remote objects fields to save to the DB (it should contain the `display` field). Leave empty to save the whole object.
        'remote_endpoint': 'https://...'                         # The remote API endpoint.
    }
}
```

In addition, you can customise the mapping of the key of the API, see the configuration key names being used for the [query](https://github.com/springload/wagtailmodelchoosers/blob/c36bb877eef4ac4af6b221f0d7ff7416354754c7/wagtailmodelchoosers/utils.py#L107-L112) and the [response](https://github.com/springload/wagtailmodelchoosers/blob/c36bb877eef4ac4af6b221f0d7ff7416354754c7/wagtailmodelchoosers/utils.py#L115-L123).


## Development

### Installation

Requirements: `virtualenv`, `pyenv`, `twine`

```sh
git clone git@github.com:springload/wagtailmodelchoosers.git
cd wagtailmodelchoosers/
virtualenv .venv
source ./.venv/bin/activate
pip install -e .[testing,docs] -U
nvm install
npm install
```

### Commands

```sh
make help            # See what commands are available.

# TODO: Complete commands
```

### Releases

1. Make a new branch for the release of the new version.
1. Update the [CHANGELOG](https://github.com/springload/wagtailmodelchoosers/blob/master/CHANGELOG.md).
1. Update the version number in `wagtailmodelchoosers/__init__.py` and `package.json`, following semver.
1. Make a PR and squash merge it.
1. Back on master with the PR merged, use `make publish` (confirm, and enter your password).
1. Finally, go to GitHub and create a release and a tag for the new version.
1. Done!
