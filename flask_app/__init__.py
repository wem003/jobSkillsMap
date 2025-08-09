from flask import Flask
from .config import Config
from .routes.dashboard import bp as ui_bp

def create_app():
    app = Flask(__name__)  # <-- no template_folder arg
    app.config.from_object(Config)
    Config.validate()
    app.register_blueprint(ui_bp)
    return app
