agregar_dependencia_dialog = null
$(function () {

    /*
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
    */

    $("#boton-agregar-institucion").on("click", function (e) {
        $('#d_subsunam').hide();

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

        $("#id_institucion_perteneceunam").on('change', function () {
            console.log($("#id_institucion_perteneceunam").is(':checked'));
            if ($("#id_institucion_perteneceunam").is(':checked')) {
                $('#d_subsunam').show('slow');
                $('#id_institucion_subsistemaunam').attr("required", "true");
            } else {
                console.log("esconder cambio")
                $('#d_subsunam').hide('slow');
                $('#id_institucion_subsistemaunam').val(null).trigger('change');
                $('#id_institucion_subsistemaunam').attr("required", null);
            }
        });



        agregar_institucion_dialog.dialog("open");
    });

    $("#boton-detalle-institucion").on("click", function (e) {
        console.log("clic detalle")
        console.log($("#id_institucion").val())
        if ($("#id_institucion").val() == '') {
            e.stopPropagation();
            console.log("no item")
        } else {
            console.log($("#id_dependencia").val())
            detalle_institucion_dialog = $("#detalle-institucion").dialog({
                autoOpen: false,
                height: 700,
                width: 900,
                modal: true,
                buttons: {
                    agregar: {
                        text: "Agregar institución",
                        click: function () {
                            $("#modal_form_institucion_detalle").submit()
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
                    //$('#agregar-institucion-modal-body').load('/nucleo/instituciones/agregar/', function () {

                    $('#detalle-institucion-modal-body').load(('/nucleo/instituciones/' + $("#id_institucion").val().toString()) + "/", function () {
                        console.log("detalle start")
                        $("#id_institucion_pais").djangoSelect2({dropdownParent: $("#agregar-institucion")});
                        $("#id_institucion_clasificacion").djangoSelect2({dropdownParent: $("#agregar-institucion")});
                        $("#id_institucion_subsistemaunam").djangoSelect2({dropdownParent: $("#agregar-institucion")});

                    });
                    e.stopPropagation();

                }
            });
            console.log("aqui")
            detalle_institucion_dialog.dialog("open");
        }

    });


})