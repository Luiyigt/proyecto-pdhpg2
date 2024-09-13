$(document).ready(function() {
    // Funcionalidad para colapsar el menú
    $('.toggle-btn').on('click', function() {
        $('body').toggleClass('collapsed');
    });

    // Abrir modal de edición de perfil
    $('#editar-perfil').on('click', function() {
        $('#editarPerfilModal').modal('show');
    });

    // Búsqueda en tiempo real
    $('#search-input').on('input', function() {
        var query = $(this).val();
        $.ajax({
            url: '',
            data: {
                'q': query
            },
            success: function(data) {
                $('#resultados').html($(data).find('#resultados').html());
            }
        });
    });

    // Restablecer la búsqueda
    $('#reset-btn').on('click', function() {
        $('#search-input').val('');
        $.ajax({
            url: '',
            success: function(data) {
                $('#resultados').html($(data).find('#resultados').html());
            }
        });
    });
});
