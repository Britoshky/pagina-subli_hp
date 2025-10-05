/* Funcionalidad para agregar cantidades rápidas */
document.addEventListener('DOMContentLoaded', function() {
    // Manejar envío de formularios de cantidad rápida
    const quickQuantityForms = document.querySelectorAll('.quick-quantity-form');
    
    quickQuantityForms.forEach(form => {
        const input = form.querySelector('.quick-quantity-input');
        const btn = form.querySelector('.quick-quantity-btn');
        
        // Enviar con Enter
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                if (validateAndSubmit(form, input)) {
                    form.submit();
                }
            }
        });
        
        // Enviar con botón
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            if (validateAndSubmit(form, input)) {
                form.submit();
            }
        });
        
        // Seleccionar texto al hacer foco
        input.addEventListener('focus', function() {
            this.select();
        });
    });
    
    function validateAndSubmit(form, input) {
        const quantity = parseInt(input.value);
        
        // Validar que sea un número válido
        if (isNaN(quantity) || quantity <= 0) {
            alert('Por favor ingresa una cantidad válida (mayor a 0)');
            input.focus();
            return false;
        }
        
        // Confirmación para cantidades grandes
        if (quantity > 100) {
            if (!confirm(`¿Estás seguro de agregar ${quantity} unidades?`)) {
                return false;
            }
        }
        
        // Mostrar feedback visual
        const btn = form.querySelector('.quick-quantity-btn');
        const originalText = btn.textContent;
        btn.textContent = '...';
        btn.disabled = true;
        
        // Restaurar después de un momento (en caso de error)
        setTimeout(() => {
            btn.textContent = originalText;
            btn.disabled = false;
        }, 3000);
        
        return true;
    }
    
    // Auto-focus en el primer input visible al cargar la página
    const firstInput = document.querySelector('.quick-quantity-input');
    if (firstInput) {
        // Pequeño delay para asegurar que la página esté completamente cargada
        setTimeout(() => {
            firstInput.focus();
        }, 100);
    }
});

/* Atajo de teclado para foco rápido */
document.addEventListener('keydown', function(e) {
    // Ctrl + Q para enfocar el primer input de cantidad
    if (e.ctrlKey && e.key === 'q') {
        e.preventDefault();
        const firstInput = document.querySelector('.quick-quantity-input');
        if (firstInput) {
            firstInput.focus();
            firstInput.select();
        }
    }
});