import os
import sys

# Añadir el directorio raíz al path para poder importar la app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.services.scheduler import process_scheduled_tasks

if __name__ == "__main__":
    print("Ejecutando revisión manual de tareas programadas...")
    app = create_app()
    process_scheduled_tasks(app)
    print("Proceso manual finalizado.")
