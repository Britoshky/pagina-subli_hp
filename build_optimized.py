#!/usr/bin/env python3
"""
Script de construcción para optimizar archivos estáticos.
Ejecutar antes de desplegar en producción.
"""

import os
import sys
from utils.compression_utils import process_static_files

def main():
    """Función principal del script de construcción."""
    print("=== Iniciando proceso de optimización ===")
    
    # Ruta de la carpeta static
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_folder = os.path.join(current_dir, 'static')
    
    if not os.path.exists(static_folder):
        print(f"Error: No se encontró la carpeta static en {static_folder}")
        sys.exit(1)
    
    print(f"Procesando archivos en: {static_folder}")
    
    try:
        # Procesar archivos CSS y JS
        process_static_files(static_folder)
        
        print("\n=== Optimización completada ===")
        print("Archivos minificados y comprimidos correctamente.")
        print("Tu aplicación ahora cargará más rápido!")
        
    except Exception as e:
        print(f"Error durante la optimización: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()