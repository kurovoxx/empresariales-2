from app import create_app
from app.models.database import init_db
import os

app = create_app()

if __name__ == "__main__":
    # Asegurar que las carpetas de datos existan al arrancar
    os.makedirs('data/samples', exist_ok=True)
    os.makedirs('data/temp', exist_ok=True)
    
    # Inicializar base de datos en Turso
    print("Iniciando base de datos en Turso...")
    try:
        init_db()
        print("✓ Base de datos lista.")
    except Exception as e:
        print(f"⚠ Error al conectar con Turso: {e}")
    
    # Iniciar la aplicación
    app.run(debug=True, port=5001)
