wagtailmodelchoosers
====================

    A Wagtail app to pick generic models (rather than snippets or pages).

**This is alpha software, use at your own risk. Do not use in production (yet).**

Check out `Awesome Wagtail <https://github.com/springload/awesome-wagtail>`_ for more awesome packages and resources from the Wagtail community.

Installation
------------

Grab the package from pip with ``pip install wagtailmodelchoosers``, then add ``wagtailmodelchoosers`` in ``INSTALLED_APPS`` in your settings.

Usage
-----

TODO

Configuration
~~~~~~~~~~~~~

TODO

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

