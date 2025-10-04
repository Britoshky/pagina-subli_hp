from flask import Flask, send_file, request, abort
import os
from PIL import Image
import io
from utils.image_utils import optimize_image

def setup_image_optimization(app):
    """
    Configura el middleware para optimización de imágenes on-the-fly.
    """
    
    @app.route('/static/uploads/<path:category>/<path:filename>')
    def optimized_image(category, filename):
        """
        Sirve imágenes optimizadas según el dispositivo y conexión del usuario.
        """
        # Ruta completa del archivo
        file_path = os.path.join(app.static_folder, 'uploads', category, filename)
        
        if not os.path.exists(file_path):
            abort(404)
        
        # Verificar si el navegador soporta WebP
        accept_header = request.headers.get('Accept', '').lower()
        supports_webp = 'image/webp' in accept_header
        
        # Verificar si es una conexión lenta (simplified)
        connection_header = request.headers.get('Save-Data', '').lower()
        slow_connection = connection_header == 'on'
        
        # Parámetros de optimización
        quality = 60 if slow_connection else 85
        max_width = 400 if slow_connection else 800
        max_height = 300 if slow_connection else 600
        
        # Si ya es WebP y el navegador lo soporta, enviarlo directamente
        if filename.lower().endswith('.webp') and supports_webp:
            return send_file(file_path)
        
        # Generar versión optimizada
        try:
            optimized_path = generate_optimized_image(
                file_path, supports_webp, quality, max_width, max_height
            )
            return send_file(optimized_path)
        except Exception as e:
            app.logger.error(f"Error optimizando imagen {filename}: {e}")
            return send_file(file_path)  # Fallback a imagen original

def generate_optimized_image(file_path, supports_webp, quality, max_width, max_height):
    """
    Genera una versión optimizada de la imagen.
    """
    # Generar nombre de archivo optimizado
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    ext = '.webp' if supports_webp else '.jpg'
    cache_name = f"{base_name}_q{quality}_w{max_width}_h{max_height}{ext}"
    cache_dir = os.path.join(os.path.dirname(file_path), '.cache')
    cache_path = os.path.join(cache_dir, cache_name)
    
    # Crear directorio de caché si no existe
    os.makedirs(cache_dir, exist_ok=True)
    
    # Si la versión optimizada ya existe, usarla
    if os.path.exists(cache_path):
        return cache_path
    
    # Crear versión optimizada
    with Image.open(file_path) as img:
        # Redimensionar manteniendo proporción
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # Convertir a RGB si es necesario
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Guardar optimizada
        if supports_webp:
            img.save(cache_path, format='WEBP', quality=quality, optimize=True)
        else:
            img.save(cache_path, format='JPEG', quality=quality, optimize=True)
    
    return cache_path