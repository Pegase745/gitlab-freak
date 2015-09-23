"""Gitlab Freak database models."""
import datetime
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ProjectHasBoard(db.Model):

    """Describe the link between a Gitlab project and a Trello board."""

    __tablename__ = 'project_board'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Unicode(50), nullable=False)
    board_id = db.Column(db.Unicode(50), nullable=False)
    closing_column = db.Column(db.Unicode(50), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def by_project(cls, project):
        """Get a link for a given project."""
        return db.session.query(cls)\
            .filter_by(project_id=project)\
            .one()

    @classmethod
    def by_board(cls, board):
        """Get a link for a given board."""
        return db.session.query(cls)\
            .filter_by(board_id=board)\
            .one()


class IssueHasCard(db.Model):

    """Describe the link between a Gitlab issue and a Trello card."""

    __tablename__ = 'issue_card'

    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Unicode(50), nullable=False)
    card_id = db.Column(db.Unicode(50), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def by_issue(cls, issue):
        """Get a link for a given issue."""
        return db.session.query(cls)\
            .filter_by(issue_id=issue)\
            .one()

    @classmethod
    def by_card(cls, card):
        """Get a link for a given card."""
        return db.session.query(cls)\
            .filter_by(card_id=card)\
            .one()
