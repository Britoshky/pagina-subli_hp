import os
from PIL import Image, ImageOps

def optimize_image(image_path, max_width=800, max_height=600, quality=85):
    """
    Optimiza una imagen redimensionándola y ajustando la calidad.
    """
    try:
        with Image.open(image_path) as img:
            # Corregir orientación basada en EXIF
            img = ImageOps.exif_transpose(img)
            
            # Convertir a RGB si es necesario
            if img.mode in ('RGBA', 'LA', 'P'):
                # Para imágenes con transparencia, usar fondo blanco
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Redimensionar manteniendo proporción
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Guardar optimizada
            img.save(image_path, format='JPEG', quality=quality, optimize=True)
            
        return True
    except Exception as e:
        print(f"Error optimizando imagen {image_path}: {e}")
        return False

def convert_to_webp(image_path, upload_folder, quality=80, max_width=800, max_height=600):
    """
    Convierte una imagen a formato WebP optimizado y la guarda en el directorio de subida.
    """
    filename = os.path.basename(image_path)
    webp_filename = os.path.splitext(filename)[0] + '.webp'
    webp_path = os.path.join(upload_folder, webp_filename)

    try:
        with Image.open(image_path) as img:
            # Corregir orientación basada en EXIF
            img = ImageOps.exif_transpose(img)
            
            # Redimensionar manteniendo proporción
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Guardar como WebP optimizado
            img.save(webp_path, format='WEBP', quality=quality, optimize=True)
        
        # Eliminar imagen original
        os.remove(image_path)
        
        # Mostrar información de compresión
        original_size = os.path.getsize(image_path) if os.path.exists(image_path) else 0
        webp_size = os.path.getsize(webp_path)
        if original_size > 0:
            compression_ratio = ((original_size - webp_size) / original_size) * 100
            print(f"Imagen convertida: {filename} -> {webp_filename} (Compresión: {compression_ratio:.1f}%)")
        
        return webp_filename
    except Exception as e:
        print(f"Error al convertir a WebP: {e}")
        return None

def create_thumbnail(image_path, thumbnail_path, size=(150, 150)):
    """
    Crea una miniatura de la imagen para vistas previas rápidas.
    """
    try:
        with Image.open(image_path) as img:
            # Corregir orientación
            img = ImageOps.exif_transpose(img)
            
            # Crear thumbnail
            img.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Guardar thumbnail
            if image_path.lower().endswith('.webp'):
                img.save(thumbnail_path, format='WEBP', quality=70, optimize=True)
            else:
                img.save(thumbnail_path, format='JPEG', quality=70, optimize=True)
                
        return True
    except Exception as e:
        print(f"Error creando thumbnail: {e}")
        return False
