jQuery(document).ready(function ($jquery) {
    $jquery("#tabla_json").dataTable({
        "iDisplayLength": 15,
        "ajax": {
            "processing": true,
            "url": "/distinciones/capacidades/json/",
            "dataSrc": ""
        },
        "columns": [
            {
                "data": "fields.competencia",
                "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                    $(nTd).html("<a href='/distinciones/capacidades/" + oData.pk + "'>" + oData.fields.competencia + "</a>");
                }
            },
            {"data": "fields.fecha_inicio"},
        ]
    });
});