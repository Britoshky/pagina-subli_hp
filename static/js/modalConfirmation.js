// Esperar a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", () => {
    // Seleccionar elementos del DOM
    const openModalBtn = document.getElementById("open-modal-btn");
    const modal = document.getElementById("confirmation-modal");
    const cancelModalBtn = document.getElementById("cancel-modal-btn");
    const confirmResetBtn = document.getElementById("confirm-reset-btn");

    if (!openModalBtn || !modal || !cancelModalBtn || !confirmResetBtn) {
        console.error("Error: No se encontraron todos los elementos del modal.");
        return;
    }

    // Obtener la categoría desde el atributo data-category
    const category = openModalBtn.dataset.category;

    // Abrir el modal
    openModalBtn.addEventListener("click", () => {
        modal.classList.remove("hidden");
    });

    // Cerrar el modal
    cancelModalBtn.addEventListener("click", () => {
        modal.classList.add("hidden");
    });

    // Confirmar la acción y reiniciar el stock
    confirmResetBtn.addEventListener("click", () => {
        if (!category) {
            console.error("Error: No se pudo obtener la categoría.");
            return;
        }

        // Construir la URL correcta
        const url = `/${category}/reset_stock`;

        fetch(url, { method: "POST" })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error en la solicitud: ${response.statusText}`);
                }
                // Recargar la página después de reiniciar el stock
                window.location.reload();
            })
            .catch(error => {
                console.error("Error al reiniciar el stock:", error);
            });
    });
});
