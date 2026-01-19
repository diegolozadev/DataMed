// Ocultar alertas después de 5 segundo
setTimeout(() => {document.querySelectorAll('.alert').forEach(alert => {
            alert.classList.remove('show');
            alert.classList.add('fade');
        });
    }, 5000);

// Enfocar el campo de búsqueda al cargar la página
document.addEventListener('DOMContentLoaded', function() {
        const searchInput = document.querySelector('.search-input');
        searchInput.focus();
    });
