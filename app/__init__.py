from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-key-123')

    # Registro de Blueprints
    from app.routes.main import main_bp
    from app.routes.groups import groups_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(groups_bp, url_prefix='/groups')

    return app
