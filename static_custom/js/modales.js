agregar_dependencia_dialog = null
$(function () {
    $(".ui-dialog-buttonset").removeClass()

    $("#boton-agregar-institucion").on("click", function (e) {
        agregar_institucion_dialog = $("#agregar-institucion").dialog({
            autoOpen: false,
            height: 700,
            width: 900,
            modal: true,
            class: 'ui-button-left',
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
                    $('#d_subsunam').hide();

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
                });
            }
        });
        agregar_institucion_dialog.dialog("open");
    });

    $("#boton-detalle-institucion").on("click", function (e) {
        if ($("#id_institucion").val() == '') {
            e.stopPropagation();
        } else {
            detalle_institucion_dialog = $("#detalle-institucion").dialog({
                autoOpen: false,
                height: 700,
                width: 900,
                modal: true,
                buttons: {
                    actualizar: {
                        text: "Actualizar institución",
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
                    $('#detalle-institucion-modal-body').load(('/nucleo/instituciones/' + $("#id_institucion").val().toString()) + "/", function () {
                        console.log("detalle start")
                        $("#id_institucion_pais").djangoSelect2({dropdownParent: $("#agregar-institucion")});
                        $("#id_institucion_clasificacion").djangoSelect2({dropdownParent: $("#agregar-institucion")});
                        $("#id_institucion_subsistemaunam").djangoSelect2({dropdownParent: $("#agregar-institucion")});

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

                    });
                    e.stopPropagation();

                }
            });
            detalle_institucion_dialog.dialog("open");
        }
    });

    /* ***** */

    $("#boton-agregar-programalicenciatura").on("click", function (e) {
        console.log("boton agregar programa licenciatura")
        agregar_programalicenciatura_dialog = $("#agregar-programalicenciatura").dialog({
            autoOpen: false,
            height: 500,
            width: 900,
            modal: true,
            class: 'ui-button-left',
            buttons: {
                agregar: {
                    text: "Agregar programa de licenciatura",
                    click: function () {
                        $("#modal_form_programalicenciatura_agregar").submit()
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
                $('#agregar-programalicenciatura-modal-body').load('/nucleo/programas-licenciatura/agregar/', function () {
                    $("#id_programalicenciatura_areaconocimiento").djangoSelect2({dropdownParent: $("#agregar-programalicenciatura")});
                });
            }
        });
        agregar_programalicenciatura_dialog.dialog("open");
    });

    $("#boton-detalle-programalicenciatura").on("click", function (e) {
        if ($("#id_institucion").val() == '') {
            e.stopPropagation();
        } else {
            detalle_institucion_dialog = $("#detalle-institucion").dialog({
                autoOpen: false,
                height: 700,
                width: 900,
                modal: true,
                buttons: {
                    actualizar: {
                        text: "Actualizar institución",
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
                    $('#detalle-institucion-modal-body').load(('/nucleo/instituciones/' + $("#id_institucion").val().toString()) + "/", function () {
                        console.log("detalle start")
                        $("#id_institucion_pais").djangoSelect2({dropdownParent: $("#agregar-institucion")});
                        $("#id_institucion_clasificacion").djangoSelect2({dropdownParent: $("#agregar-institucion")});
                        $("#id_institucion_subsistemaunam").djangoSelect2({dropdownParent: $("#agregar-institucion")});

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

                    });
                    e.stopPropagation();

                }
            });
            detalle_institucion_dialog.dialog("open");
        }
    });


})