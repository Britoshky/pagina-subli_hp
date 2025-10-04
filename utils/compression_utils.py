import os
import gzip
import shutil
from csscompressor import compress as css_compress
from jsmin import jsmin
import hashlib
from datetime import datetime

def minify_css_file(css_file_path, output_path=None):
    """
    Minifica un archivo CSS y opcionalmente lo guarda en una nueva ubicación.
    """
    if not output_path:
        output_path = css_file_path.replace('.css', '.min.css')
    
    try:
        with open(css_file_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Minificar CSS
        minified_css = css_compress(css_content)
        
        # Guardar archivo minificado
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(minified_css)
        
        print(f"CSS minificado: {css_file_path} -> {output_path}")
        return output_path
    except Exception as e:
        print(f"Error minificando CSS {css_file_path}: {e}")
        return css_file_path

def minify_js_file(js_file_path, output_path=None):
    """
    Minifica un archivo JavaScript y opcionalmente lo guarda en una nueva ubicación.
    """
    if not output_path:
        output_path = js_file_path.replace('.js', '.min.js')
    
    try:
        with open(js_file_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Minificar JavaScript
        minified_js = jsmin(js_content)
        
        # Guardar archivo minificado
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(minified_js)
        
        print(f"JS minificado: {js_file_path} -> {output_path}")
        return output_path
    except Exception as e:
        print(f"Error minificando JS {js_file_path}: {e}")
        return js_file_path

def compress_file_gzip(file_path):
    """
    Comprime un archivo usando gzip.
    """
    try:
        with open(file_path, 'rb') as f_in:
            with gzip.open(f"{file_path}.gz", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        print(f"Archivo comprimido: {file_path}.gz")
        return f"{file_path}.gz"
    except Exception as e:
        print(f"Error comprimiendo {file_path}: {e}")
        return None

def get_file_hash(file_path):
    """
    Genera un hash MD5 del contenido del archivo para cache busting.
    """
    try:
        with open(file_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()[:8]
        return file_hash
    except Exception as e:
        print(f"Error generando hash para {file_path}: {e}")
        return str(int(datetime.now().timestamp()))

def process_static_files(static_folder):
    """
    Procesa todos los archivos CSS y JS en la carpeta static para minificarlos y comprimirlos.
    """
    css_files = []
    js_files = []
    
    # Buscar archivos CSS y JS
    for root, dirs, files in os.walk(static_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.css') and not file.endswith('.min.css'):
                css_files.append(file_path)
            elif file.endswith('.js') and not file.endswith('.min.js'):
                js_files.append(file_path)
    
    # Procesar archivos CSS
    for css_file in css_files:
        minified_path = minify_css_file(css_file)
        if minified_path:
            compress_file_gzip(minified_path)
    
    # Procesar archivos JS
    for js_file in js_files:
        minified_path = minify_js_file(js_file)
        if minified_path:
            compress_file_gzip(minified_path)
    
    print(f"Procesamiento completado: {len(css_files)} CSS, {len(js_files)} JS")

def get_versioned_url(file_path, static_folder):
    """
    Genera una URL con versión basada en el hash del archivo para cache busting.
    """
    try:
        full_path = os.path.join(static_folder, file_path.lstrip('/static/'))
        if os.path.exists(full_path):
            file_hash = get_file_hash(full_path)
            return f"{file_path}?v={file_hash}"
        return file_path
    except Exception as e:
        print(f"Error generando URL versionada para {file_path}: {e}")
        return file_path