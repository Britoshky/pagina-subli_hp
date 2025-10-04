/* Lazy loading para imágenes */
document.addEventListener('DOMContentLoaded', function() {
    // Intersection Observer para lazy loading
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    }, {
        rootMargin: '50px 0px',
        threshold: 0.01
    });

    // Observar todas las imágenes con clase lazy
    document.querySelectorAll('img[data-src]').forEach(img => {
        img.classList.add('lazy');
        imageObserver.observe(img);
    });

    // Precargar imágenes críticas
    const criticalImages = document.querySelectorAll('img[data-critical]');
    criticalImages.forEach(img => {
        if (img.dataset.src) {
            img.src = img.dataset.src;
            img.classList.add('loaded');
        }
    });
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