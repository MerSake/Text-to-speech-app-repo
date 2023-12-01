from flask import Flask
from flask_login import LoginManager
from passwordgenerator import pwgenerator
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = pwgenerator.generate()

    # Database connection
    env_path = os.path.join(os.path.dirname(__file__), "..")
    dotenv_path = os.path.join(env_path, ".env")
    load_dotenv(dotenv_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+mysqlconnector://"
        + "T2Sapplication_db_user"
        + ":"
        + os.getenv("T2Sapplication_db_user_pass")
        + "@localhost/t2s-app-db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .models import User

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
