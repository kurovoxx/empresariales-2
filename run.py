from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Configuración de puerto y host para Docker
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    
    print("\n" + "="*50)
    print("🚀 ¡EmailFlow está iniciando con éxito!")
    print(f"🔗 Accede a la aplicación aquí: http://localhost:{port}")
    print("="*50 + "\n")
    
    # Ejecutar la aplicación
    app.run(host=host, port=port, debug=False)
