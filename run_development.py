#!/usr/bin/env python3
"""
Script para ejecutar la aplicación en modo desarrollo.
"""

import os
import sys
from app import app

def setup_development():
    """Configura el entorno de desarrollo."""
    # Configuración de desarrollo
    app.config.from_object('config.DevelopmentConfig')
    
    # Habilitar debug
    app.debug = True

def main():
    """Función principal."""
    print("=== Iniciando aplicación en modo DESARROLLO ===")
    
    # Configurar desarrollo
    setup_development()
    
    # Configuración del servidor
    host = '0.0.0.0'
    port = 2000
    
    print(f"Servidor ejecutándose en: http://{host}:{port}")
    print("Modo: DESARROLLO")
    print("Debug: HABILITADO")
    print("Hot Reload: HABILITADO")
    print("=====================================")
    
    # Ejecutar aplicación
    try:
        app.run(
            host=host,
            port=port,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")
    except Exception as e:
        print(f"Error al ejecutar el servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()