/* Lazy loading mejorado para imágenes */
document.addEventListener('DOMContentLoaded', function() {
    // Detectar conexión lenta
    const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    const isSlowConnection = connection && (connection.effectiveType === 'slow-2g' || connection.effectiveType === '2g');
    
    // Configuración adaptativa
    const rootMargin = isSlowConnection ? '20px 0px' : '100px 0px';
    const threshold = isSlowConnection ? 0.1 : 0.01;
    
    // Intersection Observer para lazy loading
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                loadImage(img);
                observer.unobserve(img);
            }
        });
    }, {
        rootMargin: rootMargin,
        threshold: threshold
    });

    // Función para cargar imágenes con manejo de errores
    function loadImage(img) {
        const src = img.dataset.src;
        if (!src) return;
        
        // Mostrar placeholder de carga
        img.classList.add('loading');
        
        // Crear nueva imagen para precargar
        const newImg = new Image();
        
        newImg.onload = function() {
            img.src = src;
            img.classList.remove('lazy', 'loading');
            img.classList.add('loaded');
            
            // Fade in suave
            img.style.opacity = '0';
            img.style.transition = 'opacity 0.3s ease';
            setTimeout(() => {
                img.style.opacity = '1';
            }, 10);
        };
        
        newImg.onerror = function() {
            img.classList.remove('loading');
            img.classList.add('error');
            console.warn('Error cargando imagen:', src);
        };
        
        newImg.src = src;
    }

    // Aplicar lazy loading a todas las imágenes de la tabla
    const tableImages = document.querySelectorAll('.item-list img');
    tableImages.forEach(img => {
        if (img.src && !img.dataset.src) {
            // Convertir imágenes existentes a lazy loading
            img.dataset.src = img.src;
            img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjBmMGYwIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9IjAuM2VtIj5DYXJnYW5kby4uLjwvdGV4dD48L3N2Zz4=';
            img.classList.add('lazy');
        }
        
        if (img.classList.contains('lazy')) {
            imageObserver.observe(img);
        }
    });

    // Precargar solo la primera imagen visible
    const firstVisibleImg = document.querySelector('.item-list img.lazy');
    if (firstVisibleImg) {
        loadImage(firstVisibleImg);
        imageObserver.unobserve(firstVisibleImg);
    }
});

/* Optimización de rendimiento para formularios */
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func(...args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func(...args);
    };
}

/* Mejorar rendimiento de búsqueda */
if (document.getElementById('search-input')) {
    const searchInput = document.getElementById('search-input');
    const debouncedSearch = debounce(function(e) {
        // La búsqueda se realizará después de 300ms sin escribir
        console.log('Búsqueda:', e.target.value);
    }, 300);
    
    searchInput.addEventListener('input', debouncedSearch);
}