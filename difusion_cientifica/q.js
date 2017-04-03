jQuery(document).ready(function ($jquery) {
    $jquery("#tabla_json").dataTable({
        "iDisplayLength": 15,
        "ajax": {
            "processing": true,
            "url": "/difusion-cientifica/organizacion-eventos-academicos/json/",
            "dataSrc": ""
        },
        "columns": [
            {
                "data": "fields.evento",
                "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                    $(nTd).html("<a href='/difusion-cientifica/organizacion-eventos-academicos/" + oData.pk + "'>" + oData.fields.evento + "</a>");
                }
            },
            {"data": "fields.responsabilidad"},
            {"data": "fields.ambito"},
        ]
    });
});