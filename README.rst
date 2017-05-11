wagtailmodelchoosers
====================

    A Wagtail app to pick generic models (rather than snippets or pages).

**This is alpha software, use at your own risk. Do not use in production (yet).**

Check out `Awesome Wagtail <https://github.com/springload/awesome-wagtail>`_ for more awesome packages and resources from the Wagtail community.

.. image:: https://cdn.rawgit.com/springload/wagtailmodelchoosers/b7b6202/.github/wagtailmodelchoosers-screenshot.png
   :width: 728 px

Installation
------------

Grab the package from pip with ``pip install wagtailmodelchoosers``, then add ``wagtailmodelchoosers`` in ``INSTALLED_APPS`` in your settings.

Usage
-----

``ModelChooserBlock`` takes the name of the chooser configuration as first positional argument. Use other block kwargs (e.g. `required`) as usual.

.. code:: python

    from wagtail.wagtailcore import blocks
    from wagtailmodelchoosers.blocks import ModelChooserBlock
    
    class CustomBlock(blocks.StructBlock):
        custom_model = ModelChooserBlock('custom_model')  # `chooser` can be a positional argument, the keyword is used here for clarity.
       
``ModelChooserPanel`` takes the name of the field as first positional argument (like a regular Panel) and the name of the chooser configuration as second positional argument. Use other panel kwargs as usual.

.. code:: python

    from django.db import models
    from wagtail.core.models import Page
    from wagtailmodelchoosers.edit_handlers import ModelChooserPanel
    
    class CustomPage(Page):
        custom_model = models.ForeignKey('myapp.CustomModel')
        
        panels = [
            ...
            ModelChooserPanel('custom_model', chooser='custom_model'),  # `chooser` can be a positional argument, the keyword is used here for clarity.
        ]

To select a model from a remote API, respectively use ``RemoteModelChooserBlock`` and ``RemoteModelChooserPanel`` instead.

If you have `WagtailDraftail <https://github.com/springload/wagtaildraftail>`_ installed, it will automatically register the ``ModelSource`` and ``RemoteModelSource`` to the JS. Refer to ``WagtailDraftail``'s `documentation <https://github.com/springload/wagtaildraftail#configuration>`_ to hook it up properly.

Configuration
~~~~~~~~~~~~~

It looks for a ``MODEL_CHOOSERS_OPTIONS`` dictionary in the settings where the key is the name of the chooser and the value, a dictionary of options.

The ModelChooser and RemoteModelChooser share a similar base configuration and only have a few specific fields.

.. code:: python

    MODEL_CHOOSERS_OPTIONS = {
        'navigation': {
            'label': 'Navigation',                                   # The label to use for buttons or modal title
            'display': 'name',                                       # The field to display when selecting an object
            'list_display': [                                        # The fields to display in the chooser
                {'label': 'Name', 'name': 'name'},
                {'label': 'Identity', 'name': 'identity'},
                {'label': 'Active', 'name': 'active'},
            ],
            'content_type': 'core.Navigation',                       # ONLY FOR MODEL: The django content type of the model
            'fields_to_save': ['id'] + RATE_CHOOSER_DISPLAY_FIELDS,  # ONLY FOR REMOTE: The remote objects fields to save to the DB. Leave empty to save the whole object.
            'remote_endpoint': 'http://...'                          # ONLY FOR REMOTE: The remote API endpoint.
            'pk_name': 'uuid',                                       # The primary key name of the model
        }
    }
    
In addition, you can customise the mapping of the key of the API, see the configuration key names being used for the `query <https://github.com/springload/wagtailmodelchoosers/blob/c36bb877eef4ac4af6b221f0d7ff7416354754c7/wagtailmodelchoosers/utils.py#L107-L112>`_ and the `response <https://github.com/springload/wagtailmodelchoosers/blob/c36bb877eef4ac4af6b221f0d7ff7416354754c7/wagtailmodelchoosers/utils.py#L115-L123>`_.


Development
-----------

Installation
~~~~~~~~~~~~

Requirements: ``virtualenv``, ``pyenv``, ``twine``

.. code:: sh

    git clone git@github.com:springload/wagtailmodelchoosers.git
    cd wagtailmodelchoosers/
    virtualenv .venv
    source ./.venv/bin/activate
    pip install -e .[testing,docs] -U
    nvm install
    npm install

Commands
~~~~~~~~

.. code:: sh

    make help            # See what commands are available.

TODO: Complete

Releases
~~~~~~~~

*  Make a new branch for the release of the new version.
*  Update the `CHANGELOG <https://github.com/springload/wagtailmodelchoosers/CHANGELOG.md>`_.
*  Update the version number in ``wagtailmodelchoosers/__init__.py`` and ``package.json``, following semver.
*  Make a PR and squash merge it.
*  Back on master with the PR merged, use ``make publish`` (confirm, and enter your password).
*  Finally, go to GitHub and create a release and a tag for the new version.
*  Done!

