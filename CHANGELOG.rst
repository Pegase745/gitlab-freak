.. :changelog:

Changelog
---------

1.0.0-alpha.1 (2X-09-2015)
++++++++++++++++++++++++++

* Rename gitlab-to-trello into gitlab-freak.

* Choose a Gitlab project (Node.js only) for which dependencies update monitoring is wanted.
* Get dependencies from `package.json`.
* Fetch twice a day for dependencies new versions on npm registry (the official one or your own mirror).
* List dependencies versions status on a webpage.


1.0.0-alpha (26-08-2015)
++++++++++++++++++++++++

* Link a Gitlab project to a Trello Board.
* Listen to Gitlab issue creation webhook.
* Create a Trello card in the first column of the linked board, when an issue is created in a project.
