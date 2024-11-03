from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:khongrotmon@localhost:3306/sns_fake_face"
    db.init_app(app)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
