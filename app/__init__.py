
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from flask_login import LoginManager

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("db", MigrateCommand)

manager.add_command("runserverproduction", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0'))

lm = LoginManager()
lm.init_app(app)

from app.models import book,borrow,collection, user, sale
from app.controllers import user_controller, book_controller, collection_controller, index, sale_controller
