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

def convert_to_webp(image_path, upload_folder, quality=75, max_width=600, max_height=450):
    """
    Convierte una imagen a formato WebP optimizado y la guarda en el directorio de subida.
    Aplica optimización automática con configuración agresiva para web.
    """
    filename = os.path.basename(image_path)
    webp_filename = os.path.splitext(filename)[0] + '.webp'
    webp_path = os.path.join(upload_folder, webp_filename)

    try:
        # Obtener tamaño original para estadísticas
        original_size = os.path.getsize(image_path)
        
        with Image.open(image_path) as img:
            # Corregir orientación basada en EXIF
            img = ImageOps.exif_transpose(img)
            
            # Convertir a RGB si es necesario para WebP
            if img.mode in ('RGBA', 'LA', 'P'):
                # Crear fondo blanco para transparencias
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[-1])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Redimensionar automáticamente para web (más agresivo)
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Guardar como WebP con optimización máxima
            img.save(webp_path, format='WEBP', quality=quality, optimize=True, method=6)
        
        # Eliminar imagen original
        if os.path.exists(image_path):
            os.remove(image_path)
        
        # Mostrar información de compresión
        webp_size = os.path.getsize(webp_path)
        compression_ratio = ((original_size - webp_size) / original_size) * 100
        
        print(f"✅ Imagen optimizada automáticamente:")
        print(f"   📁 {filename} -> {webp_filename}")
        print(f"   📊 {original_size//1024}KB -> {webp_size//1024}KB ({compression_ratio:.1f}% reducción)")
        
        return webp_filename
    except Exception as e:
        print(f"❌ Error al convertir a WebP: {e}")
        # Si falla la conversión, devolver el nombre original
        return os.path.basename(image_path)

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

def optimize_uploaded_image(image_file, upload_folder, max_width=600, max_height=450, quality=75):
    """
    Optimiza una imagen recién subida automáticamente.
    Combina guardado + conversión + optimización en un solo paso.
    """
    try:
        # Generar nombre único para evitar conflictos
        import time
        timestamp = int(time.time())
        original_filename = image_file.filename
        name_without_ext = os.path.splitext(original_filename)[0]
        webp_filename = f"{name_without_ext}_{timestamp}.webp" if not original_filename.lower().endswith('.webp') else original_filename
        
        # Asegurar que el directorio existe
        os.makedirs(upload_folder, exist_ok=True)
        webp_path = os.path.join(upload_folder, webp_filename)
        
        # Procesar imagen directamente desde el objeto file
        img = Image.open(image_file.stream)
        
        # Obtener información original
        original_format = img.format
        original_size = len(image_file.read())
        image_file.seek(0)  # Reset stream
        
        # Corregir orientación EXIF
        img = ImageOps.exif_transpose(img)
        
        # Convertir a RGB si es necesario
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            if img.mode == 'RGBA':
                background.paste(img, mask=img.split()[-1])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Redimensionar automáticamente
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # Guardar optimizado como WebP
        img.save(webp_path, format='WEBP', quality=quality, optimize=True, method=6)
        
        # Obtener nuevo tamaño
        webp_size = os.path.getsize(webp_path)
        compression_ratio = ((original_size - webp_size) / original_size) * 100
        
        print(f"🚀 OPTIMIZACIÓN AUTOMÁTICA:")
        print(f"   📸 {original_filename} -> {webp_filename}")
        print(f"   📉 {original_size//1024}KB -> {webp_size//1024}KB ({compression_ratio:.1f}% reducción)")
        print(f"   🎯 Dimensiones ajustadas automáticamente")
        
        return webp_filename
        
    except Exception as e:
        print(f"❌ Error en optimización automática: {e}")
        # Fallback: guardar archivo original
        try:
            fallback_path = os.path.join(upload_folder, image_file.filename)
            image_file.save(fallback_path)
            return image_file.filename
        except Exception as fallback_error:
            print(f"❌ Error en fallback: {fallback_error}")
            return None
