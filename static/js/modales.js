$(function () {

    $("#boton-agregar-dependencia").on("click", function () {
        $("#agregar-dependencia").dialog("open");
    });

    function addUser() {
        alert("ygjgjhg")

        return valid;
    }

    agregar_dependencia_dialog = $("#agregar-dependencia").dialog({
        autoOpen: false,
        height: 730,
        width: 900,
        modal: true,
        buttons: {
            create: {
                text: "createetrert",
                click: addUser,
                class: 'btn btn-success ui-button-left'
            },
            cancel: {
                text: "Cancelar",
                click: function () {
                    $(this).dialog("close")
                },
                class: 'btn btn-primary ui-button-left'
            }
        },
        open: function (event, ui) {
            $('#agregar-dependencia-modal-body').load('/nucleo/dependencias/agregar/', function () {
                $("#id_institucion_dependencia").djangoSelect2({dropdownParent: $("#agregar-dependencia")});
                $("#id_subsistema_unam_dependencia").djangoSelect2({dropdownParent: $("#agregar-dependencia")});
            });
        }
    });

    $('#boton-ver-dependencia').on('click', function (e) {
        if ($("#id_dependencia").val() === null) {
            e.stopPropagation();
        } else {
            console.log($("#id_dependencia").val())
            $("#detalle-dependencia").modal()
            $("#detalle-dependencia").removeData()
            $('#detalle-dependencia-modal-body').html('');
            $('#detalle-dependencia-modal-body').load(('/nucleo/dependencias/' + $("#id_dependencia").val().toString()) + "/", function () {
                $("#id_institucion_dependencia").djangoSelect2({dropdownParent: $("#detalle-dependencia")});
            })
        }
    })
})