from flask import Flask
from gitlab_freak.models import db

app = Flask(__name__)
app.config.from_envvar('GITLAB_FREAK_SETTINGS')
db.init_app(app)

with app.app_context():
    db.create_all()
