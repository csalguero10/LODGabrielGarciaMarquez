$(document).ready(function() {
    console.log("Carousel script iniciado.");

    const $viewport = $('.carousel-viewport');
    const $track = $('.carousel-track');
    const $slides = $('.carousel-slide');
    const $prevButton = $('.carousel-prev');
    const $nextButton = $('.carousel-next');

    console.log("Viewport encontrado:", $viewport);
    console.log("Track encontrado:", $track);
    console.log("Número de slides encontrados:", $slides.length);

    const numSlides = $slides.length;

    if (numSlides === 0) {
        console.warn("No se encontraron slides. El carrusel no se activará.");
        $prevButton.hide();
        $nextButton.hide();
        return;
    }

    const slideHeight = $viewport.height();
    console.log("Altura calculada del slide/viewport:", slideHeight);

    if (slideHeight === 0 || !slideHeight) {
        console.error("¡ERROR CRÍTICO! La altura del viewport es 0 o indefinida. El carrusel no funcionará. Revisa el CSS de .carousel-viewport.");
        // Podrías querer detener la ejecución aquí o mostrar un mensaje al usuario.
        // Por ahora, dejaremos que intente continuar para ver si hay más errores.
    }

    let currentIndex = 0;

    function updateButtons() {
        console.log("Actualizando botones. Índice actual:", currentIndex, "de", numSlides -1);
        $prevButton.prop('disabled', currentIndex === 0);
        $nextButton.prop('disabled', currentIndex >= numSlides - 1); // Usar >= por seguridad
        console.log("Botón Prev deshabilitado:", $prevButton.prop('disabled'));
        console.log("Botón Next deshabilitado:", $nextButton.prop('disabled'));
    }

    function goToSlide(index) {
        console.log("goToSlide llamado con índice:", index);

        if (slideHeight === 0 || !slideHeight) {
            console.error("goToSlide: No se puede mover porque slideHeight es 0 o inválido.");
            return;
        }

        if (index < 0 || index >= numSlides) {
            console.warn("Intento de ir a un slide fuera de rango:", index);
            // No mover si está fuera de rango, pero asegurarse de que los botones reflejen el estado actual válido
            updateButtons(); // Actualiza los botones al estado actual antes de salir
            return;
        }

        const newTransformValue = -index * slideHeight;
        console.log("Aplicando transformación CSS: translateY(" + newTransformValue + "px) al track:", $track);
        
        $track.css('transform', 'translateY(' + newTransformValue + 'px)');
        
        currentIndex = index;
        updateButtons();
        console.log("Slide cambiado a índice:", currentIndex);
    }

$prevButton.on('click', function() {
        console.log("Botón Prev presionado.");
        if ($(this).prop('disabled')) {
            console.log("Botón Prev está deshabilitado, no se hace nada.");
            return;
        }
        goToSlide(currentIndex - 1);
    });

    $nextButton.on('click', function() {
        console.log("Botón Next presionado.");
        if ($(this).prop('disabled')) {
            console.log("Botón Next está deshabilitado, no se hace nada.");
            return;
        }
        goToSlide(currentIndex + 1);
    });

    console.log("Inicializando carrusel al slide 0.");
    // Llama a goToSlide para establecer la posición inicial y el estado de los botones
    goToSlide(0); 
});