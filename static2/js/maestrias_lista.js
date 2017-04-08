jQuery(document).ready(function ($jquery) {
    $jquery("#tabla_json").dataTable({
        "iDisplayLength": 15,
        "ajax": {
            "processing": true,
            "url": "/formacion/maestrias/json/",
            "dataSrc": ""
        },
        "columns": [
            {
                "data": "fields.programa",
                "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                    $(nTd).html("<a href='/formacion/maestrias/json/" + oData.pk + "'>" + oData.fields.programa + "</a>");
                }
            },
            {"data": "fields.titulo_tesis"},
            {"data": "fields.fecha_grado"},
            {"data": "fields.dependencia"},
        ]
    });
});
