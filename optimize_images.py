import os
import sys
from PIL import Image, ImageOps
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def optimize_all_images(upload_folder, max_width=600, max_height=450, quality=75):
    """
    Optimiza todas las imágenes en una carpeta específica.
    """
    optimized_count = 0
    total_size_before = 0
    total_size_after = 0
    
    logger.info(f"Optimizando imágenes en: {upload_folder}")
    
    # Buscar todas las imágenes
    for root, dirs, files in os.walk(upload_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
                file_path = os.path.join(root, file)
                
                # Obtener tamaño original
                original_size = os.path.getsize(file_path)
                total_size_before += original_size
                
                try:
                    # Optimizar imagen
                    if optimize_single_image(file_path, max_width, max_height, quality):
                        optimized_count += 1
                        
                        # Obtener nuevo tamaño
                        new_size = os.path.getsize(file_path)
                        total_size_after += new_size
                        
                        # Calcular reducción
                        reduction = ((original_size - new_size) / original_size) * 100
                        if reduction > 0:
                            logger.info(f"✅ {file}: {original_size//1024}KB → {new_size//1024}KB ({reduction:.1f}% reducción)")
                        else:
                            total_size_after = total_size_after - new_size + original_size  # Revertir si no hubo mejora
                    else:
                        total_size_after += original_size
                        
                except Exception as e:
                    logger.error(f"❌ Error optimizando {file}: {e}")
                    total_size_after += original_size
    
    # Mostrar resumen
    total_reduction = ((total_size_before - total_size_after) / total_size_before) * 100 if total_size_before > 0 else 0
    logger.info(f"\n📊 RESUMEN DE OPTIMIZACIÓN:")
    logger.info(f"Imágenes procesadas: {optimized_count}")
    logger.info(f"Tamaño total antes: {total_size_before / (1024*1024):.2f} MB")
    logger.info(f"Tamaño total después: {total_size_after / (1024*1024):.2f} MB")
    logger.info(f"Reducción total: {total_reduction:.1f}%")
    
    return optimized_count

def optimize_single_image(image_path, max_width=600, max_height=450, quality=75):
    """
    Optimiza una sola imagen.
    """
    try:
        with Image.open(image_path) as img:
            # Obtener información original
            original_size = os.path.getsize(image_path)
            original_width, original_height = img.size
            
            # Si la imagen ya es pequeña, no hacer nada
            if original_size < 100 * 1024 and original_width <= max_width and original_height <= max_height:
                return False
            
            # Corregir orientación EXIF
            img = ImageOps.exif_transpose(img)
            
            # Convertir a RGB si es necesario
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
            
            # Redimensionar si es necesario
            if img.width > max_width or img.height > max_height:
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Determinar formato de salida
            if image_path.lower().endswith('.webp'):
                # Guardar como WebP optimizado
                img.save(image_path, format='WEBP', quality=quality, optimize=True, method=6)
            else:
                # Convertir a WebP
                webp_path = os.path.splitext(image_path)[0] + '.webp'
                img.save(webp_path, format='WEBP', quality=quality, optimize=True, method=6)
                
                # Eliminar archivo original si se creó WebP
                if webp_path != image_path:
                    os.remove(image_path)
                    # Actualizar referencias en JSON si es necesario
                    update_json_references(image_path, webp_path)
            
            return True
            
    except Exception as e:
        logger.error(f"Error procesando {image_path}: {e}")
        return False

def update_json_references(old_path, new_path):
    """
    Actualiza las referencias en archivos JSON cuando se cambia el nombre de una imagen.
    """
    import json
    
    old_filename = os.path.basename(old_path)
    new_filename = os.path.basename(new_path)
    
    # Lista de archivos JSON a actualizar
    json_files = [
        'data/books.json',
        'data/stickers.json', 
        'data/cojines.json'
    ]
    
    for json_file in json_files:
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Actualizar referencias
                updated = False
                for item in data:
                    if item.get('image_filename') == old_filename:
                        item['image_filename'] = new_filename
                        updated = True
                
                # Guardar si hubo cambios
                if updated:
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
                    logger.info(f"📝 Actualizado {json_file}")
                    
            except Exception as e:
                logger.error(f"Error actualizando {json_file}: {e}")

def main():
    """Función principal del optimizador."""
    print("🖼️  OPTIMIZADOR DE IMÁGENES AGRESIVO")
    print("="*50)
    
    # Carpetas a optimizar
    upload_folders = [
        'static/uploads/books',
        'static/uploads/stickers', 
        'static/uploads/cojines'
    ]
    
    total_optimized = 0
    
    for folder in upload_folders:
        if os.path.exists(folder):
            print(f"\n📁 Procesando: {folder}")
            count = optimize_all_images(folder, max_width=600, max_height=450, quality=75)
            total_optimized += count
        else:
            logger.warning(f"❌ Carpeta no encontrada: {folder}")
    
    print(f"\n🎉 OPTIMIZACIÓN COMPLETADA")
    print(f"Total de imágenes optimizadas: {total_optimized}")
    print("Las imágenes ahora cargarán mucho más rápido!")

if __name__ == "__main__":
    main()