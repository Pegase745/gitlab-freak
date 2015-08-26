from flask import Flask
from g2t.models import db

app = Flask(__name__)
app.config.from_envvar('G2T_SETTINGS')
db.init_app(app)

with app.app_context():
    db.create_all()
