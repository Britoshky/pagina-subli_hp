import os
from PIL import Image

def convert_to_webp(image_path, upload_folder):
    """
    Convierte una imagen a formato WebP y la guarda en el directorio de subida.
    """
    filename = os.path.basename(image_path)
    webp_filename = os.path.splitext(filename)[0] + '.webp'
    webp_path = os.path.join(upload_folder, webp_filename)

    try:
        with Image.open(image_path) as img:
            img.save(webp_path, format='WEBP', quality=80)
        os.remove(image_path)
        return webp_filename
    except Exception as e:
        print(f"Error al convertir a WebP: {e}")
        return None
