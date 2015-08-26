================
gitlab-to-trello
================

-----
Usage
-----

Install dependencies
====================

.. code-block:: bash

    $ mkvirtualenv g2t
    $ workon g2t
    (g2t)$ pip install -r requirements.txt
    (g2t)$ pyhon setup.py develop

Initialize database model
=========================

.. code-block:: bash

    (g2t)$ g2t-init-db.py

Prepare config file
===================

You need to copy `config-sample.cfg` somewhere on your server, and fill it with your desired configuration. Then export its path into an environment variable `G2T_SETTINGS`.

**GITLAB_TOKEN**: find it on Gitlab, under your profile settings, Account section (private token).
**TRELLO_APPKEY**: it'll be generated when visiting this page https://trello.com/app-key under the `Key` section.
**TRELLO_TOKEN**: you'll be given it when launching for the first time g2t server and visiting the homepage. You'll need to restart the server after setting it.

Run dev server
==============

.. code-block:: bash

    (g2t)$ g2t-run-dev.py

Authorize the application
=========================

Visit for the first time the homepage and authorize g2t to access your Trello account. When done, put the generated token in g2t config file, and restart the server.

Set a webhook in Gitlab
=======================

In your project's setting, put the dispatch url of g2t (http://your-g2t-endpoint/dispatch) on issue trigger.
