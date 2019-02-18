agregar_dependencia_dialog = null
$(function () {

    $("#boton-agregar-dependencia").on("click", function () {
        agregar_dependencia_dialog.dialog("open");
    });

    $("#boton-agregar-institucion").on("click", function () {
        //alert("instituciosdkfhbdjksfb")
        agregar_institucion_dialog.dialog("open");
    });

    $("#boton-detalle-institucion").on("click", function (e) {
        console.log("clic detalle")
                if ($("#id_dependencia").val() === null) {
            e.stopPropagation();
        } else {
            console.log($("#id_dependencia").val())
            detalle_institucion_dialog.dialog("open");
        }

    });

    agregar_institucion_dialog = $("#agregar-institucion").dialog({
        autoOpen: false,
        height: 700,
        width: 900,
        modal: true,
        buttons: {
            agregar: {
                text: "Agregar institución",
                click: function () {
                    $("#modal_form_institucion_agregar").submit()
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
            $('#agregar-institucion-modal-body').load('/nucleo/instituciones/agregar/', function () {
                $("#id_institucion_pais").djangoSelect2({dropdownParent: $("#agregar-institucion")});
                $("#id_institucion_clasificacion").djangoSelect2({dropdownParent: $("#agregar-institucion")});
                $("#id_institucion_subsistemaunam").djangoSelect2({dropdownParent: $("#agregar-institucion")});
            });
        }
    });

    detalle_institucion_dialog = $("#agregar-institucion").dialog({
        autoOpen: false,
        height: 700,
        width: 900,
        modal: true,
        buttons: {
            agregar: {
                text: "Agregar institución",
                click: function () {
                    $("#modal_form_institucion_agregar").submit()
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
            $('#detalle-institucion-modal-body').load(('/nucleo/dependencias/' + $("#id_dependencia").val().toString()) + "/", function () {
                $("#id_institucion_pais").djangoSelect2({dropdownParent: $("#agregar-institucion")});
                $("#id_institucion_clasificacion").djangoSelect2({dropdownParent: $("#agregar-institucion")});
                $("#id_institucion_subsistemaunam").djangoSelect2({dropdownParent: $("#agregar-institucion")});
            });
        }
    });

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