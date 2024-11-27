function filterItems(category) {
    const searchInput = document.getElementById("search-input").value;

    fetch(`/${category}/?search=${encodeURIComponent(searchInput)}`)
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
