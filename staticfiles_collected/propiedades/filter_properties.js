// propiedades/static/propiedades/filter_properties.js

document.addEventListener('DOMContentLoaded', function() {
    // Selecciona los elementos del DOM usando sus IDs
    const filterForm = document.getElementById('filterForm');
    const propertyGrid = document.getElementById('propertyGrid');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const applyFiltersBtn = filterForm ? filterForm.querySelector('.btn-filter') : null; // Asegúrate de que filterForm no sea null
    const clearFiltersBtn = document.getElementById('clearFiltersBtn');

    // Función para mostrar el indicador de carga (spinner)
    function showLoading() {
        // Mantener la altura del contenedor de propiedades para evitar "saltos" en el layout
        // Esto solo aplica si propertyGrid ya tiene una altura, si no, se usará 'auto'
        if (propertyGrid) { // Asegúrate de que propertyGrid existe
            if (propertyGrid.clientHeight > 0) {
                propertyGrid.style.minHeight = propertyGrid.clientHeight + 'px';
            } else {
                // Si el grid está vacío inicialmente, puedes establecer una altura mínima por defecto
                propertyGrid.style.minHeight = '150px'; // Ajusta esto según necesites
            }
        }
        if (loadingOverlay) { // Asegúrate de que loadingOverlay existe
            loadingOverlay.classList.add('visible'); // Agrega la clase 'visible' para mostrar el overlay
        }
    }

    // Función para ocultar el indicador de carga (spinner)
    function hideLoading() {
        if (loadingOverlay) { // Asegúrate de que loadingOverlay existe
            loadingOverlay.classList.remove('visible'); // Remueve la clase 'visible' para ocultar el overlay
        }
        if (propertyGrid) { // Asegúrate de que propertyGrid existe
            propertyGrid.style.minHeight = ''; // Restablece la altura mínima
        }
    }

    // Función asíncrona para aplicar los filtros mediante una petición AJAX
    async function applyFilters() {
        showLoading(); // Muestra el spinner al inicio de la operación

        const formData = new FormData(filterForm); // Obtiene los datos del formulario
        const params = new URLSearchParams(); // Crea un objeto para construir la URL de la petición

        // Itera sobre los datos del formulario y agrega solo los campos con valor a los parámetros de la URL
        for (const [name, value] of formData.entries()) {
            // Se filtra por null, undefined, y cadenas vacías para no añadir parámetros innecesarios
            // Además, se filtra el valor "None" que Django puede enviar para opciones no seleccionadas o vacías
            // Y ahora también filtra "Todas las ciudades" o "Todos los tipos" si esos son los valores por defecto
            if (value !== null && value !== undefined && value !== '' && value !== 'None' &&
                value !== 'Todas las ciudades' && value !== 'Todos los tipos' && value !== 'Cualquiera') { // Añadido para opciones de selección
                params.append(name, value);
            }
        }

        // Construye la URL completa para la petición AJAX
        // *** CORRECCIÓN CRÍTICA: La URL debe ser `/lista/ajax/` sin doble barra, como ya lo tienes. ***
        const ajaxUrl = `/lista/ajax/?${params.toString()}`;

        // Deshabilita el botón de aplicar filtros y cambia su texto durante la carga
        if (applyFiltersBtn) { // Asegúrate de que el botón existe antes de manipularlo
            applyFiltersBtn.disabled = true;
            applyFiltersBtn.textContent = 'Cargando...';
        }


        try {
            // Realiza la petición Fetch a la URL AJAX
            const response = await fetch(ajaxUrl);
            if (!response.ok) {
                // Si la respuesta no es exitosa (ej. 404, 500), lanza un error
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const html = await response.text(); // Obtiene la respuesta HTML como texto
            if (propertyGrid) { // Asegúrate de que propertyGrid existe
                propertyGrid.innerHTML = html; // Reemplaza el contenido del contenedor de propiedades con el HTML recibido
            }
        } catch (error) {
            // Captura y maneja cualquier error durante la petición
            console.error('Error al cargar propiedades:', error);
            if (propertyGrid) { // Asegúrate de que propertyGrid existe
                propertyGrid.innerHTML = '<p class="no-properties-found-message">Error al cargar las propiedades. Por favor, inténtalo de nuevo más tarde.</p>'; // Usar la clase del mensaje de no encontrado
            }
        } finally {
            // Siempre se ejecuta, independientemente de si hubo éxito o error
            hideLoading(); // Oculta el spinner
            if (applyFiltersBtn) { // Asegúrate de que el botón existe
                applyFiltersBtn.disabled = false; // Habilita el botón de nuevo
                applyFiltersBtn.textContent = 'Aplicar Filtros'; // Restablece el texto del botón
            }
        }
    }

    // Event listener para el evento 'submit' del formulario de filtros
    if (filterForm) { // Asegúrate de que el formulario existe
        filterForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Previene el envío por defecto del formulario (que causaría una recarga de página)
            applyFilters(); // Llama a la función para aplicar los filtros vía AJAX
        });
    }


    // Event listeners para la búsqueda instantánea en los campos de filtro
    // Es CRÍTICO que los IDs de los elementos HTML aquí coincidan exactamente con los IDs en tu lista_propiedades.html
    const instantFilterInputs = [
        document.getElementById('id_buscar'),
        document.getElementById('id_ciudad'),
        document.getElementById('id_tipo_propiedad'),
        document.getElementById('id_habitaciones'),
        document.getElementById('id_banos'),
        document.getElementById('id_metros_cuadrados_min'),
        document.getElementById('id_metros_cuadrados_max'),
        document.getElementById('id_tiene_garaje'),
        document.getElementById('id_caracteristicas'),
        document.getElementById('id_precio_min'),
        document.getElementById('id_precio_max')
    ];

    instantFilterInputs.forEach(input => {
        if (input) { // Asegura que el elemento HTML existe antes de añadir el listener
            if (input.tagName === 'SELECT') {
                // Para elementos <select>, el evento 'change' es el adecuado
                input.addEventListener('change', applyFilters);
            } else {
                // Para inputs de texto o número, usa un temporizador para evitar llamadas excesivas al escribir
                let timeout = null;
                input.addEventListener('input', function() {
                    clearTimeout(timeout); // Limpia cualquier temporizador anterior
                    timeout = setTimeout(applyFilters, 500); // Establece un nuevo temporizador de 500ms
                });
            }
        }
    });

    // Event listener para el botón "Limpiar Filtros"
    if (clearFiltersBtn) { // Asegura que el botón exista
        clearFiltersBtn.addEventListener('click', function(event) {
            event.preventDefault(); // Previene el comportamiento por defecto del botón (si fuera un submit)
            filterForm.reset(); // Resetea todos los campos del formulario a sus valores iniciales

            // También resetea los selects a la primera opción ("Todas las ciudades", "Todos los tipos", "Cualquiera")
            instantFilterInputs.forEach(input => {
                if (input && input.tagName === 'SELECT') {
                    input.selectedIndex = 0;
                }
                // Si tienes checkboxes o radios que necesiten ser desmarcados al limpiar, agrégalos aquí.
                // Por ejemplo, para un checkbox 'tiene_garaje', podrías tener:
                // if (input && input.type === 'checkbox') {
                //     input.checked = false;
                // }
            });
            applyFilters(); // Vuelve a aplicar los filtros para mostrar todas las propiedades
        });
    }

    // Opcional: Cargar propiedades al cargar la página inicialmente
    // Si la página se carga con parámetros de URL (ej. desde un bookmark o un enlace directo con filtros)
    // O si simplemente quieres que la lista se cargue al inicio sin que el usuario haga clic en "Aplicar Filtros"
    // Descomenta la siguiente línea si quieres que se ejecute applyFilters() al cargar la página.
    // Esto es útil si esperas que la lista de propiedades se muestre automáticamente al visitar /lista/
    applyFilters();
});