function filterItems(category) {
    const searchInput = document.getElementById("search-input").value;

    // Recuperar el número de página actual de la URL
    const urlParams = new URLSearchParams(window.location.search);
    const currentPage = urlParams.get("page") || 1; // Si no existe 'page', se asume la página 1

    fetch(`/${category}/?search=${encodeURIComponent(searchInput)}&page=${currentPage}`)
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, "text/html");
            const newTable = doc.querySelector(".item-list");
            const newPagination = doc.querySelector(".pagination");

            if (newTable) {
                document.querySelector(".item-list").innerHTML = newTable.innerHTML;
            } else {
                console.error("No se encontró el elemento .item-list en la respuesta.");
            }

            if (newPagination) {
                document.querySelector(".pagination").innerHTML = newPagination.innerHTML;
            } else {
                console.warn("No se encontró la paginación en la respuesta.");
            }
        })
        .catch(error => console.error("Error al realizar la búsqueda:", error));
}


function applyFilter(category) {
    const filter = document.getElementById("filter-select").value;
    const searchQuery = document.getElementById("search-input").value;

    // Recuperar el número de página actual de la URL
    const urlParams = new URLSearchParams(window.location.search);
    const currentPage = urlParams.get("page") || 1;

    const url = new URL(window.location.href);
    url.searchParams.set("filter", filter); // Agregar el filtro a los parámetros de la URL
    url.searchParams.set("search", searchQuery); // Mantener la búsqueda activa si existe
    url.searchParams.set("page", currentPage); // Mantener la página actual

    window.location.href = url.toString(); // Redirigir a la URL actualizada
}
