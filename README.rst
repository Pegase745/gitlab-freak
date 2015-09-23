============
gitlab-freak
============

-----
Usage
-----

Install dependencies
====================

.. code-block:: bash

    $ mkvirtualenv gitlab_freak
    $ workon gitlab_freak
    (gitlab_freak)$ pip install -r requirements.txt
    (gitlab_freak)$ pyhon setup.py dgitlab_freakevelop

Initialize database model
=========================

.. code-block:: bash

    (gitlab_freak)$ gitlab-freak-init-db.py

Prepare config file
===================

You need to copy `config-sample.cfg` somewhere on your server, and fill it with your desired configuration. Then export its path into an environment variable `GITLAB_FREAK_SETTINGS`.

**GITLAB_TOKEN**: find it on Gitlab, under your profile settings, Account section (private token).
**TRELLO_APPKEY**: it'll be generated when visiting this page https://trello.com/app-key under the `Key` section.
**TRELLO_TOKEN**: you'll be given it when launching for the first time gitlab-freak server and visiting the homepage. You'll need to restart the server after setting it.

Run dev server
==============

.. code-block:: bash

    (gitlab_freak)$ gitlab-freak-run-dev.py

Authorize the application
=========================

Visit for the first time the homepage and authorize gitlab-freak to access your Trello account. When done, put the generated token in gitlab-freak config file, and restart the server.

Set a webhook in Gitlab
=======================

In your project's setting, put the dispatch url of gitlab-freak (http://your-gitlab-freak-endpoint/dispatch) on issue trigger.
