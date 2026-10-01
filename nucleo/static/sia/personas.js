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

// Ayuda del catálogo elegido (comisión, cargo, beca, distinción): se muestra bajo el campo al capturar y no sale en
// los reportes. Llega en `ayuda` de cada resultado del buscador y en `data-ayuda` de la opción ya elegida.
document.addEventListener('DOMContentLoaded', function () {
  const $ = window.django && window.django.jQuery;
  if (!$) return;
  const mostrar = function (select, texto) {
    const contenedor = $(select).closest('.related-widget-wrapper, .flex-grow, div').first();
    let nota = contenedor.siblings('.sia-ayuda');
    if (!nota.length) nota = $('<div class="sia-ayuda">').insertAfter(contenedor);
    nota.text(texto || '').toggle(Boolean(texto));
  };
  $('select').each(function () {
    const elegida = this.options[this.selectedIndex];
    if (elegida && elegida.dataset.ayuda) mostrar(this, elegida.dataset.ayuda);
  });
  $(document).on('select2:select', 'select', function (e) {
    mostrar(this, e.params.data.ayuda || (e.params.data.element && e.params.data.element.dataset.ayuda));
  });
  $(document).on('select2:clear', 'select', function () { mostrar(this, ''); });
});
