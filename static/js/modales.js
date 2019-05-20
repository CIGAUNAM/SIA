agregar_dependencia_dialog = null
$(function () {
    $(".ui-dialog-buttonset").removeClass()

    $("#boton-detalle-proyectoinvestigacion").on("click", function (e) {
        if ($("#id_proyecto").val() == null) {
            e.stopPropagation();
        } else {
            var win = window.open('/investigacion/proyectos/' + $("#id_proyecto").val().toString() + '/', '_blank');
            win.focus();
        }
    });

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
        if ($("#id_carrera").val() == null) {
            e.stopPropagation();
        } else {

            detalle_programalicenciatura_dialog = $("#detalle-programalicenciatura").dialog({
                autoOpen: false,
                height: 500,
                width: 900,
                modal: true,
                buttons: {
                    actualizar: {
                        text: "Actualizar programa de licenciatura",
                        click: function () {
                            $("#modal_form_programalicenciatura_detalle").submit()
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
                    $('#detalle-programalicenciatura-modal-body').load(('/nucleo/programas-licenciatura/' + $("#id_carrera").val().toString()) + "/", function () {
                        console.log("detalle start")
                        $("#id_programalicenciatura_areaconocimiento").djangoSelect2({dropdownParent: $("#agregar-programalicenciatura")});

                    });
                    e.stopPropagation();
                }
            });
            detalle_programalicenciatura_dialog.dialog("open");
        }
    });


    /***** *****  *****/


    $("#boton-agregar-programamaestria").on("click", function (e) {
        console.log("boton agregar programa maestria")
        agregar_programamaestria_dialog = $("#agregar-programamaestria").dialog({
            autoOpen: false,
            height: 500,
            width: 900,
            modal: true,
            class: 'ui-button-left',
            buttons: {
                agregar: {
                    text: "Agregar programa de maestria",
                    click: function () {
                        $("#modal_form_programamaestria_agregar").submit()
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
                $('#agregar-programamaestria-modal-body').load('/nucleo/programas-maestria/agregar/', function () {
                    $("#id_programamaestria_areaconocimiento").djangoSelect2({dropdownParent: $("#agregar-programamaestria")});
                });
            }
        });
        agregar_programamaestria_dialog.dialog("open");
    });

    $("#boton-detalle-programamaestria").on("click", function (e) {
        if ($("#id_programa").val() == null) {
            e.stopPropagation();
        } else {

            detalle_programamaestria_dialog = $("#detalle-programamaestria").dialog({
                autoOpen: false,
                height: 500,
                width: 900,
                modal: true,
                buttons: {
                    actualizar: {
                        text: "Actualizar programa de maestria",
                        click: function () {
                            $("#modal_form_programamaestria_detalle").submit()
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
                    $('#detalle-programamaestria-modal-body').load(('/nucleo/programas-maestria/' + $("#id_programa").val().toString()) + "/", function () {
                        console.log("detalle start")
                        $("#id_programamaestria_areaconocimiento").djangoSelect2({dropdownParent: $("#agregar-programamaestria")});

                    });
                    e.stopPropagation();
                }
            });
            detalle_programamaestria_dialog.dialog("open");
        }
    });


    $("#boton-agregar-programadoctorado").on("click", function (e) {
        console.log("boton agregar programa doctorado")
        agregar_programadoctorado_dialog = $("#agregar-programadoctorado").dialog({
            autoOpen: false,
            height: 500,
            width: 900,
            modal: true,
            class: 'ui-button-left',
            buttons: {
                agregar: {
                    text: "Agregar programa de doctorado",
                    click: function () {
                        $("#modal_form_programadoctorado_agregar").submit()
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
                $('#agregar-programadoctorado-modal-body').load('/nucleo/programas-doctorado/agregar/', function () {
                    $("#id_programadoctorado_areaconocimiento").djangoSelect2({dropdownParent: $("#agregar-programadoctorado")});
                });
            }
        });
        agregar_programadoctorado_dialog.dialog("open");
    });

    $("#boton-detalle-programadoctorado").on("click", function (e) {
        if ($("#id_programa").val() == null) {
            e.stopPropagation();
        } else {

            detalle_programadoctorado_dialog = $("#detalle-programadoctorado").dialog({
                autoOpen: false,
                height: 500,
                width: 900,
                modal: true,
                buttons: {
                    actualizar: {
                        text: "Actualizar programa de doctorado",
                        click: function () {
                            $("#modal_form_programadoctorado_detalle").submit()
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
                    $('#detalle-programadoctorado-modal-body').load(('/nucleo/programas-doctorado/' + $("#id_programa").val().toString()) + "/", function () {
                        console.log("detalle start")
                        $("#id_programadoctorado_areaconocimiento").djangoSelect2({dropdownParent: $("#agregar-programadoctorado")});

                    });
                    e.stopPropagation();
                }
            });
            detalle_programadoctorado_dialog.dialog("open");
        }
    });

    /* * * * */

    $("#boton-agregar-revista").on("click", function (e) {
        console.log("boton agregar revista")
        agregar_revista_dialog = $("#agregar-revista").dialog({
            autoOpen: false,
            height: 700,
            width: 900,
            modal: true,
            class: 'ui-button-left',
            buttons: {
                agregar: {
                    text: "Agregar revista",
                    click: function () {
                        $("#modal_form_revista_agregar").submit()
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
                $('#agregar-revista-modal-body').load('/nucleo/revistas/agregar/', function () {
                    $("#id_revista_indices").djangoSelect2({dropdownParent: $("#agregar-revista")});
                    $("#id_revista_pais").djangoSelect2({dropdownParent: $("#agregar-revista")});
                });
            }
        });
        agregar_revista_dialog.dialog("open");
    });

    $("#boton-detalle-revista").on("click", function (e) {
        if ($("#id_revista").val() == null) {
            e.stopPropagation();
        } else {

            detalle_revista_dialog = $("#detalle-revista").dialog({
                autoOpen: false,
                height: 700,
                width: 900,
                modal: true,
                buttons: {
                    actualizar: {
                        text: "Actualizar revista",
                        click: function () {
                            $("#modal_form_revista_detalle").submit()
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
                    $('#detalle-revista-modal-body').load(('/nucleo/revistas/' + $("#id_revista").val().toString()) + "/", function () {
                        console.log("detalle start")
                        $("#id_revista_indices").djangoSelect2({dropdownParent: $("#agregar-revista")});
                        $("#id_revista_pais").djangoSelect2({dropdownParent: $("#agregar-revista")});
                    });
                    e.stopPropagation();
                }
            });
            detalle_revista_dialog.dialog("open");
        }
    });

    /* ------- */


    $("#boton-agregar-eventodifusion").on("click", function (e) {
        console.log("boton agregar eventodifusion")
        agregar_eventodifusion_dialog = $("#agregar-eventodifusion").dialog({
            autoOpen: false,
            height: 500,
            width: 900,
            modal: true,
            class: 'ui-button-left',
            buttons: {
                agregar: {
                    text: "Agregar eventodifusion",
                    click: function () {
                        $("#modal_form_eventodifusion_agregar").submit()
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
                $('#agregar-eventodifusion-modal-body').load('/difusion-cientifica/eventos-difusion/agregar/', function () {
                    $("#id_eventodifusion_tipo").djangoSelect2({dropdownParent: $("#agregar-eventodifusion")});
                    $("#id_eventodifusion_pais").djangoSelect2({dropdownParent: $("#agregar-eventodifusion")});
                    $("#id_eventodifusion_ambito").djangoSelect2({dropdownParent: $("#agregar-eventodifusion")});
                    $('#id_eventodifusion_fecha_inicio').datepicker({format: 'yyyy-mm-dd'});
                    $('#id_eventodifusion_fecha_fin').datepicker({format: 'yyyy-mm-dd'});
                });
            }
        });
        agregar_eventodifusion_dialog.dialog("open");
    });

    $("#boton-detalle-eventodifusion").on("click", function (e) {
        console.log("Clic");
        if ($("#id_evento").val() == null) {
            e.stopPropagation();
        } else {

            detalle_eventodifusion_dialog = $("#detalle-eventodifusion").dialog({
                autoOpen: false,
                height: 500,
                width: 900,
                modal: true,
                buttons: {
                    actualizar: {
                        text: "Actualizar eventodifusion",
                        click: function () {
                            $("#modal_form_eventodifusion_detalle").submit()
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
                    $('#detalle-eventodifusion-modal-body').load(('/difusion-cientifica/eventos-difusion/' + $("#id_evento").val().toString()) + "/", function () {
                        console.log("detalle start")
                        $("#id_eventodifusion_tipo").djangoSelect2({dropdownParent: $("#agregar-eventodifusion")});
                        $("#id_eventodifusion_pais").djangoSelect2({dropdownParent: $("#agregar-eventodifusion")});
                        $("#id_eventodifusion_ambito").djangoSelect2({dropdownParent: $("#agregar-eventodifusion")});
                        $('#id_eventodifusion_fecha_inicio').datepicker({format: 'yyyy-mm-dd'});
                        $('#id_eventodifusion_fecha_fin').datepicker({format: 'yyyy-mm-dd'});
                    });
                    e.stopPropagation();
                }
            });
            detalle_eventodifusion_dialog.dialog("open");
        }
    });









    $("#boton-agregar-eventodivulgacion").on("click", function (e) {
        console.log("boton agregar eventodivulgacion")
        agregar_eventodivulgacion_dialog = $("#agregar-eventodivulgacion").dialog({
            autoOpen: false,
            height: 500,
            width: 900,
            modal: true,
            class: 'ui-button-left',
            buttons: {
                agregar: {
                    text: "Agregar eventodivulgacion",
                    click: function () {
                        $("#modal_form_eventodivulgacion_agregar").submit()
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
                $('#agregar-eventodivulgacion-modal-body').load('/divulgacion-cientifica/eventos-divulgacion/agregar/', function () {
                    $("#id_eventodivulgacion_tipo").djangoSelect2({dropdownParent: $("#agregar-eventodivulgacion")});
                    $("#id_eventodivulgacion_pais").djangoSelect2({dropdownParent: $("#agregar-eventodivulgacion")});
                    $("#id_eventodivulgacion_ambito").djangoSelect2({dropdownParent: $("#agregar-eventodivulgacion")});
                    $('#id_eventodivulgacion_fecha_inicio').datepicker({format: 'yyyy-mm-dd'});
                    $('#id_eventodivulgacion_fecha_fin').datepicker({format: 'yyyy-mm-dd'});
                });
            }
        });
        agregar_eventodivulgacion_dialog.dialog("open");
    });

    $("#boton-detalle-eventodivulgacion").on("click", function (e) {
        console.log("Clic");
        if ($("#id_evento").val() == null) {
            e.stopPropagation();
        } else {

            detalle_eventodivulgacion_dialog = $("#detalle-eventodivulgacion").dialog({
                autoOpen: false,
                height: 500,
                width: 900,
                modal: true,
                buttons: {
                    actualizar: {
                        text: "Actualizar eventodivulgacion",
                        click: function () {
                            $("#modal_form_eventodivulgacion_detalle").submit()
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
                    $('#detalle-eventodivulgacion-modal-body').load(('/divulgacion-cientifica/eventos-divulgacion/' + $("#id_evento").val().toString()) + "/", function () {
                        console.log("detalle start")
                        $("#id_eventodivulgacion_tipo").djangoSelect2({dropdownParent: $("#agregar-eventodivulgacion")});
                        $("#id_eventodivulgacion_pais").djangoSelect2({dropdownParent: $("#agregar-eventodivulgacion")});
                        $("#id_eventodivulgacion_ambito").djangoSelect2({dropdownParent: $("#agregar-eventodivulgacion")});
                        $('#id_eventodivulgacion_fecha_inicio').datepicker({format: 'yyyy-mm-dd'});
                        $('#id_eventodivulgacion_fecha_fin').datepicker({format: 'yyyy-mm-dd'});
                    });
                    e.stopPropagation();
                }
            });
            detalle_eventodivulgacion_dialog.dialog("open");
        }
    });




});