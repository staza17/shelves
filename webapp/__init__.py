from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from webapp.user.forms import LoginForm
from webapp.db import db
from webapp.admin.views import blueprint as admin_blueprint
from webapp.boards.views import blueprint as board_blueprint
from webapp.cards.views import blueprint as card_blueprint
from webapp.col.views import blueprint as col_blueprint
from webapp.home.views import blueprint as home_blueprint
from webapp.user.views import blueprint as user_blueprint
from webapp.user.models import User


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(board_blueprint)
    app.register_blueprint(card_blueprint)
    app.register_blueprint(col_blueprint)
    app.register_blueprint(home_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
