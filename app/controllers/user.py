from app import lm
from flask import render_template
from app.models.tables import User

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
