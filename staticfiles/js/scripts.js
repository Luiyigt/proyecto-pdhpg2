$(document).ready(function() { 
    // Añadir funcionalidad para colapsar el menú
    $('.toggle-btn').on('click', function() {
        $('.sidebar').toggleClass('active');  // Activa o desactiva la clase 'active' en la barra lateral
        $('.main-content').toggleClass('collapsed');  // Ajusta el contenido principal según el estado del menú
        
        // Asegura que los íconos mantengan su tamaño adecuado
        if ($('.sidebar').hasClass('active')) {
            $('.sidebar a i').css('font-size', '24px');  // Establece el tamaño de los íconos al colapsar
        } else {
            $('.sidebar a i').css('font-size', '18px');  // Restablece el tamaño de los íconos cuando se expande
        }
    });

    // Abrir modal de edición de perfil
    $('#editar-perfil').on('click', function() {
        $('#editarPerfilModal').modal('show');
    });

    // Búsqueda en tiempo real
    $('#search-input').on('input', function() {
        var query = $(this).val().trim();  // Elimina los espacios en blanco en los extremos del valor de búsqueda

        // Si el campo de búsqueda está vacío, recarga la lista completa
        if (!query) {
            resetTable();
            return;
        }

        // Realiza la búsqueda si el campo tiene contenido
        $.ajax({
            url: window.location.href,  // Usa la URL actual de la página
            data: {
                'q': query  // Envía el parámetro de búsqueda 'q' al servidor
            },
            success: function(data) {
                // Actualiza la tabla con los resultados obtenidos
                $('#resultados').html($(data).find('#resultados').html());

                // Verifica si no hay resultados en la tabla
                if ($('#resultados table tbody tr').length === 0) {
                    $('#resultados').html('<p>No se encontraron resultados para "' + query + '".</p>');  // Mensaje si no hay resultados
                }
            },
            error: function(xhr, status, error) {
                console.error("Error en la búsqueda: ", error);  // Manejo de errores
                $('#resultados').html('<p>Error en la búsqueda. Inténtalo de nuevo más tarde.</p>');  // Mensaje de error visible
            }
        });
    });

    // Función para restablecer la tabla de resultados a su estado inicial
    function resetTable() {
        $.ajax({
            url: window.location.href,  // Recargar la lista completa desde la URL actual
            success: function(data) {
                $('#resultados').html($(data).find('#resultados').html());  // Actualiza la tabla con la lista completa
            },
            error: function(xhr, status, error) {
                console.error("Error al restablecer: ", error);  // Manejo de errores
                $('#resultados').html('<p>Error al restablecer la lista. Inténtalo de nuevo más tarde.</p>');  // Mensaje de error visible
            }
        });
    }

    // Restablecer la búsqueda cuando se haga clic en el botón "Restablecer"
    $('#reset-btn').on('click', function() {
        $('#search-input').val('');  // Limpiar el campo de búsqueda
        resetTable();  // Recargar la lista completa
    });

    // Dropdown de usuario - Mostrar opciones de perfil y cerrar sesión
    $('.navbar-user .dropdown-toggle').on('click', function() {
        var $dropdownMenu = $(this).siblings('.dropdown-menu');
        if ($dropdownMenu.is(':visible')) {
            $dropdownMenu.slideUp();  // Cierra el dropdown si ya está abierto
        } else {
            $dropdownMenu.slideDown();  // Abre el dropdown si está cerrado
        }
    });

    // Cerrar dropdown cuando se hace clic fuera de él
    $(document).on('click', function(event) {
        if (!$(event.target).closest('.navbar-user').length) {
            $('.navbar-user .dropdown-menu').slideUp();  // Cierra el menú cuando se hace clic fuera
        }
    });

    // Funcionalidad para las etiquetas flotantes
    $('.form-group input, .form-group textarea, .form-group select').each(function() {
        if ($(this).val()) {
            $(this).siblings('label').addClass('float');  // Si el campo tiene valor, activa la clase 'float'
        }
    });

    $('.form-group input, .form-group textarea, .form-group select').on('focus', function() {
        $(this).siblings('label').addClass('float');  // Activa la clase 'float' al enfocar
    }).on('blur', function() {
        if (!$(this).val()) {
            $(this).siblings('label').removeClass('float');  // Remueve la clase 'float' si el campo está vacío al perder el foco
        }
    });

    // Agregar funcionalidad dinámica al login
    const btnSignIn = document.getElementById("sign-in"),
          btnSignUp = document.getElementById("sign-up"),
          containerFormRegister = document.querySelector(".register"),
          containerFormLogin = document.querySelector(".login");

    btnSignIn.addEventListener("click", e => {
        containerFormRegister.classList.add("hide");
        containerFormLogin.classList.remove("hide");
    });

    btnSignUp.addEventListener("click", e => {
        containerFormLogin.classList.add("hide");
        containerFormRegister.classList.remove("hide");
    });
});
