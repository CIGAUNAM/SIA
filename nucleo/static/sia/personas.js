// Colorea a las personas en los selectores de los formularios según su adscripción a la entidad:
// adscritas en negro, ex adscritas casi negro y externas en gris (el servidor manda `adscripcion` en cada
// resultado del buscador y `data-adscripcion` en la opción ya elegida). Otros catálogos no se tocan.
document.addEventListener('DOMContentLoaded', function () {
  const $ = window.django && window.django.jQuery;
  if (!$ || !$.fn.select2) return;
  const dibujar = function (datos) {
    const nivel = datos.adscripcion || (datos.element && datos.element.dataset.adscripcion);
    if (!nivel || !datos.id) return datos.text;
    return $('<span>').addClass('sia-persona sia-persona--' + nivel).text(datos.text);
  };
  $.fn.select2.defaults.set('templateResult', dibujar);
  $.fn.select2.defaults.set('templateSelection', dibujar);
});
