function previewImage(event) {
    const file = event.target.files[0]; // Obtén el archivo seleccionado
    const preview = document.getElementById('image-preview'); // Elemento <img> para vista previa
    const container = document.getElementById('preview-container'); // Contenedor de la vista previa

    // Validar si existe un archivo seleccionado
    if (file) {
        // Validar si el archivo es una imagen
        const validImageTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
        if (!validImageTypes.includes(file.type)) {
            alert('Por favor, selecciona un archivo de imagen válido (JPEG, PNG, WEBP, GIF).');
            event.target.value = ''; // Limpia el input
            preview.src = ''; // Limpia la vista previa
            preview.style.display = 'none'; // Oculta la vista previa
            return;
        }

        // Leer el archivo como una URL base64 y asignarlo al elemento <img>
        const reader = new FileReader();

        reader.onload = function (e) {
            preview.src = e.target.result; // Asigna la imagen al atributo src del elemento <img>
            preview.style.display = 'block'; // Muestra la imagen
        };

        reader.onerror = function () {
            alert('Error al cargar la imagen. Inténtalo de nuevo.');
            event.target.value = ''; // Limpia el input
            preview.src = ''; // Limpia la vista previa
            preview.style.display = 'none'; // Oculta la vista previa
        };

        reader.readAsDataURL(file); // Lee el archivo como una URL base64
    } else {
        // Si no hay archivo seleccionado, limpia la vista previa
        preview.src = '';
        preview.style.display = 'none';
    }
}
