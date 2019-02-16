agregar_dependencia_dialog = null
$(function () {
    $("#boton-agregar-dependencia").on("click", function () {
        $("#agregar-dependencia").dialog("open");
    });

    function agregar_dependencia() {
        alert("Agregar dependencia")
    }

    agregar_dependencia_dialog = $("#agregar-dependencia").dialog({
        autoOpen: false,
        height: 700,
        width: 900,
        modal: true,
        buttons: {
            agregar: {
                text: "Agregar dependencia",
                click: function () {
                    $("#modal_form_dependencia_agregar").submit()
                },
                class: 'btn btn-success ui-button-left'
            },
            cancelar: {
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