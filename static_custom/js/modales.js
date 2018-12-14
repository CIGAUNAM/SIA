$(function () {

    if ($("#id_institucion_dependencia").val() != 1) {
        $('#d_subsunam').hide();
    }

    $("#boton-agregar-dependencia").on("click", function () {
        $("#agregar-dependencia").dialog("open");
    });

    function agregar_dependencia() {
        alert("ygjgjhg")
    }

    agregar_dependencia_dialog = $("#agregar-dependencia").dialog({
        autoOpen: false,
        height: 730,
        width: 900,
        modal: true,
        buttons: {
            agregar: {
                text: "Agregar dependencia",
                click: agregar_dependencia,
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

    $("#id_institucion_dependencia").on('change', function () {
        if ($("#id_institucion_dependencia").val() == 1) {
            $('#d_subsunam').show('slow');
        } else {
            $('#d_subsunam').hide('slow');
            $('#id_subsistema_unam_dependencia').val(null).trigger('change');
        }
    });

    $("#modal_form_dependencia_agregar").submit(function (event) {
        console.log("Handler for .submit() called.");
        var datos = {
            nombre_dependencia: $("#id_nombre_dependencia").val(),
            institucion_dependencia: parseInt($("#id_institucion_dependencia").val()),
            ciudad_text_dependencia: $("#id_ciudad_text_dependencia").val(),
        };
        if ($("#id_subsistema_unam_dependencia").val() != "") {
            datos.subsistema_unam_dependencia = $("#id_subsistema_unam_dependencia").val();
        }
        $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
        $.ajax({
            type: "POST",
            url: "/nucleo/rest/dependencias/",
            dataType: 'json',
            data: datos,
            headers: {"X-CSRFToken": $crf_token},
            error: function (xhr, ajaxOptions, thrownError) {
                //console.log(xhr.responseJSON.non_field_errors[0])
                alert(xhr.responseJSON.non_field_errors[0])

                $('#id_subsistema_unam_dependencia').val(null).trigger('change');
                $('#id_institucion_dependencia').val(null).trigger('change');
                $('#id_institucion_dependencia').children('option').remove();
                $('#d_subsunam').hide('slow');
                $('#modal_form_dependencia_agregar').trigger('reset');
            },
            success: function (data) {
                console.log("success")
                $('#id_subsistema_unam_dependencia').val(null).trigger('change');
                $('#id_institucion_dependencia').val(null).trigger('change');
                $('#id_institucion_dependencia').children('option').remove();
                $('#d_subsunam').hide('slow');
                $('#modal_form_dependencia_agregar').trigger('reset');

                //$('#id_dependencia').focus('change');
                var nueva_dependencia_institucion = ""
                console.log(nueva_dependencia_institucion)
                var insturl = "/nucleo/rest/instituciones/" + data.institucion_dependencia.toString() + "/"
                $.ajax({
                    url: insturl,
                    success: function (dataf) {
                        console.log(dataf.nombre_institucion);
                        nueva_dependencia_institucion = dataf.nombre_institucion.toString();
                        console.log(nueva_dependencia_institucion)
                        var nueva_dependencia = new Option(data.nombre_dependencia + " :: " + nueva_dependencia_institucion, data.id, true, true);
                        $('#id_dependencia').append(nueva_dependencia).trigger('change');


                        $('#dependencia-modal-body').empty();

                    }
                });
            }
        });
        event.preventDefault();
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