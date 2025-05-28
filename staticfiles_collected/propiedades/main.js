document.addEventListener('DOMContentLoaded', function() {
    const propertyListDiv = document.getElementById('property-list');
    const loadingMessage = document.getElementById('loading-message');
    const errorMessage = document.getElementById('error-message');
    const noPropertiesMessage = document.getElementById('no-properties-message');

    function fetchProperties() {
        loadingMessage.style.display = 'block'; // Muestra el mensaje de carga
        errorMessage.style.display = 'none'; // Oculta el mensaje de error
        noPropertiesMessage.style.display = 'none'; // Oculta el mensaje de no propiedades
        propertyListDiv.innerHTML = ''; // Limpia cualquier contenido previo

        fetch('/propiedades/api/propiedades/')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(properties => {
                loadingMessage.style.display = 'none'; // Oculta el mensaje de carga
                if (properties.length === 0) {
                    noPropertiesMessage.style.display = 'block'; // Muestra el mensaje de no propiedades
                } else {
                    properties.forEach(property => {
                        const propertyCard = document.createElement('div');
                        propertyCard.className = 'property-card';

                        // Construye la URL de la imagen. Si no hay imagen, usa una por defecto.
                        // Asegúrate de tener una imagen 'default_property.jpg' en static/propiedades/
                        // o cambia la ruta a tu imagen por defecto.
                        const imageUrl = property.imagen || '{% static "propiedades/default_property.jpg" %}';

                        propertyCard.innerHTML = `
                            <a href="/propiedades/${property.id}/">
                                <div class="property-card-image">
                                    <img src="${imageUrl}" alt="${property.titulo}">
                                </div>
                            </a>
                            <div class="property-card-content">
                                <h3 class="property-card-title">${property.titulo}</h3>
                                <p class="property-card-location">
                                    <i class="fas fa-map-marker-alt"></i> ${property.ciudad}, ${property.pais}
                                </p>
                                <p class="property-card-price">$${parseFloat(property.precio).toLocaleString('en-US')}</p>
                                <div class="property-card-features">
                                    <div class="feature-item">
                                        <i class="fas fa-bed"></i> ${property.habitaciones || '-'}
                                    </div>
                                    <div class="feature-item">
                                        <i class="fas fa-bath"></i> ${property.banios || '-'}
                                    </div>
                                    <div class="feature-item">
                                        <i class="fas fa-ruler-combined"></i> ${property.metros_cuadrados || '-'} m²
                                    </div>
                                </div>
                                <div class="property-card-actions">
                                    <a href="/propiedades/${property.id}/" class="btn-details">Ver Detalles</a>
                                </div>
                            </div>
                        `;
                        propertyListDiv.appendChild(propertyCard);
                    });
                }
            })
            .catch(error => {
                loadingMessage.style.display = 'none'; // Oculta el mensaje de carga
                errorMessage.style.display = 'block'; // Muestra el mensaje de error
                console.error('Error fetching properties:', error);
            });
    }

    fetchProperties(); // Llama a la función para cargar las propiedades al inicio
});