"""Gitlab Freak views."""
from __future__ import absolute_import, unicode_literals
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, render_template, redirect

import gitlab
from trello import TrelloApi

from gitlab_freak.models import db, ProjectHasBoard, IssueHasCard
from gitlab_freak.helpers import get_or_create

app = Flask(__name__)
app.config.from_envvar('GITLAB_FREAK_SETTINGS')
db.init_app(app)

trello = TrelloApi(app.config['TRELLO_APPKEY'], app.config['TRELLO_TOKEN'])
git = gitlab.Gitlab(app.config['GITLAB_ENDPOINT'], app.config['GITLAB_TOKEN'])


# Views
@app.route('/', methods=['GET', 'POST'])
def home():
    """Homepage for linking a Gitlab project to a Trello board."""
    if request.method == 'POST':
        project_id = request.form['project-id']
        board_id = request.form['board-id']

        # check if project is already linked with a board
        try:
            project = ProjectHasBoard.by_project(project_id)
            project.update({'board_id': board_id})
        except Exception:
            app.logger.info('Linking project %s with board %s'
                            % (project_id, board_id))
            link, created = get_or_create(
                db.session, ProjectHasBoard, project_id=project_id,
                board_id=board_id)
            if not created:
                app.logger.info('Already linked')
        db.session.commit()

    # Check for Trello App Token
    if app.config['TRELLO_TOKEN'] in (None, ''):
        token_url = trello.get_token_url(
            'Gitlab To Trello', expires='never', write_access=True)
        return redirect(token_url)

    # Get all gitlab projects
    projects = git.getprojects()

    # Get all Trello boards
    token_username = trello.tokens.get_member(
        app.config['TRELLO_TOKEN']).get('username')
    boards = trello.members.get_board(token_username)

    return render_template('index.html', projects=projects, boards=boards)


@app.route('/dispatch', methods=['POST'])
def dispatcher():
    """Dispatcher for Gitlab webhook triggering."""
    data = request.json
    kind = data.get('object_kind')
    content = data.get('object_attributes')

    if (kind in 'issue') and (content.get('action') in 'open'):
        # when opening an issue, create a Trello card and comment on Gitlab
        try:
            link = ProjectHasBoard.by_project(content.get('project_id'))
        except Exception, e:
            # in case of orm_exc.NoResultFound
            app.logger.error(e)

        opening_list = trello.boards.get_list(link.board_id)[0]
        app.logger.info('Creating a card for issue #%s on %s list.' %
                        (content.get('iid'), opening_list.get('name')))
        card = trello.cards.new(
            '#%s %s' % (
                content.get('iid'), content.get('title')),
            opening_list.get('id'),
            content.get('description'))

        # create link between a card and an issue
        ilink, created = get_or_create(
            db.session, IssueHasCard,
            issue_id=content.get('iid'), card_id=card.get('id'))

        if created:
            # create a comment in gitlab with card's shortUrl
            git.createissuewallnote(
                content.get('project_id'), content.get('iid'),
                'Created Trello card -> %s' % card.get('shortUrl'))
    elif (kind in 'issue') and (content.get('action') in 'close'):
        # when closing an issue, move a Trello card to the closing column
        pass
    else:
        app.logger.warn('Kind %s with action %s not yet taken care of'
                        % (kind, content.get('action')))
    return "OK"  # or other thing

if __name__ == "__main__":
    handler = RotatingFileHandler(
        app.config['LOGGING_FILE'], maxBytes=10000,  backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run('0.0.0.0', port=app.config['PORT'], debug=app.config['DEBUG'])
