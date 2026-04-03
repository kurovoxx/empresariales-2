from flask import Flask
from dotenv import load_dotenv
import os
import threading
import time

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-key-123')

    # Registro de Blueprints
    from app.routes.main import main_bp
    from app.routes.groups import groups_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(groups_bp, url_prefix='/groups')

    # Iniciar el planificador en segundo plano
    from app.services.scheduler import process_scheduled_tasks
    
    def run_scheduler():
        # Evitar que se ejecute dos veces cuando Flask está en modo debug/reload
        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or not app.debug:
            print("Iniciando hilo del planificador...")
            while True:
                try:
                    # Pasamos la app al procesador para manejar el contexto
                    process_scheduled_tasks(app)
                except Exception as e:
                    print(f"Error en el planificador: {e}")
                time.sleep(30) # Revisar cada 30 segundos

    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    return app
