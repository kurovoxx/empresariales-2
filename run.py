from app import create_app
import os
import logging
from werkzeug.serving import WSGIRequestHandler

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'

    # 🔥 Desactivar logs informativos de Flask
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    print("\n" + "="*50)
    print("🚀 ¡EmailFlow está iniciando con éxito!")
    print(f"🔗 Accede a la aplicación aquí: http://localhost:{port}")
    print("="*50 + "\n")

    app.run(host=host, port=port, debug=False)