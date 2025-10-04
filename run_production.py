#!/usr/bin/env python3
"""
Script para ejecutar la aplicación en modo producción con todas las optimizaciones.
"""

import os
import sys
from app import app
from utils.compression_utils import process_static_files

def setup_production():
    """Configura el entorno de producción."""
    # Configuración de producción
    app.config.from_object('config.ProductionConfig')
    
    # Deshabilitar debug
    app.debug = False
    
    # Procesar archivos estáticos si no están minificados
    static_folder = app.static_folder
    if static_folder and os.path.exists(static_folder):
        print("Verificando archivos minificados...")
        
        # Verificar si existen archivos minificados
        css_files = []
        js_files = []
        
        for root, dirs, files in os.walk(static_folder):
            for file in files:
                if file.endswith('.css') and not file.endswith('.min.css'):
                    min_file = file.replace('.css', '.min.css')
                    min_path = os.path.join(root, min_file)
                    if not os.path.exists(min_path):
                        css_files.append(os.path.join(root, file))
                elif file.endswith('.js') and not file.endswith('.min.js'):
                    min_file = file.replace('.js', '.min.js')
                    min_path = os.path.join(root, min_file)
                    if not os.path.exists(min_path):
                        js_files.append(os.path.join(root, file))
        
        if css_files or js_files:
            print("Minificando archivos faltantes...")
            process_static_files(static_folder)
        else:
            print("Archivos minificados encontrados.")

def main():
    """Función principal."""
    print("=== Iniciando aplicación en modo PRODUCCIÓN ===")
    
    # Configurar producción
    setup_production()
    
    # Configuración del servidor
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 2000))
    
    print(f"Servidor ejecutándose en: http://{host}:{port}")
    print("Modo: PRODUCCIÓN")
    print("Compresión: HABILITADA")
    print("Cache: HABILITADO")
    print("===================================")
    
    # Ejecutar aplicación
    try:
        app.run(
            host=host,
            port=port,
            debug=False,
            threaded=True,
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")
    except Exception as e:
        print(f"Error al ejecutar el servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()