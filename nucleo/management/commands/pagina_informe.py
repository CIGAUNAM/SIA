"""Página HTML con las gráficas del informe calculadas desde el SIA, junto a las hechas a mano para compararlas."""

import base64
import html
import io
import json
from pathlib import Path

from django.core.management.base import BaseCommand

from nucleo.cifras_informe import FIGURAS, REFERENCIA_2025_2026, Periodo

#: Imagen original de cada figura (prefijo del nombre de archivo en la carpeta de gráficas).
IMAGENES = {'6.': '6.E2.1', '7.': '7.E2.1', '8.': '8_Movimientos', '11.': '11.E2.2', '12.': '12.E2.2', '13.': '13.E2.2',
            '14.': '14.E2.2', '15.': '15.E2.2', '20.': '20.E2.2', '21.': '21.E2.2', '22.': '22.E2.2', '24.': '24.E2.3',
            '26.': '26.E3.1', '28.': '28.E3.1'}

PLANTILLA = """<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Informe {periodo} · SIA</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
:root {{ --fondo:#f7f7f2; --tarjeta:#fff; --texto:#1f2a24; --tenue:#5b6660; --sia:#4a7c8c; --informe:#c4a35a;
         --igual:#5f8a3a; --distinto:#b5562f; --borde:#e2e2da; }}
@media (prefers-color-scheme: dark) {{ :root {{ --fondo:#151a17; --tarjeta:#1f2622; --texto:#e8ece9; --tenue:#a3ada7;
         --borde:#2e3832; }} }}
body {{ margin:0; background:var(--fondo); color:var(--texto); font:15px/1.5 system-ui, sans-serif; }}
main {{ max-width:1200px; margin:0 auto; padding:24px 16px 64px; }}
h1 {{ margin:0 0 4px; font-size:1.6rem; }} .tenue {{ color:var(--tenue); }}
.resumen {{ display:flex; gap:12px; flex-wrap:wrap; margin:16px 0 28px; }}
.cifra {{ background:var(--tarjeta); border:1px solid var(--borde); border-radius:12px; padding:12px 18px; }}
.cifra b {{ display:block; font-size:1.6rem; }}
section {{ background:var(--tarjeta); border:1px solid var(--borde); border-radius:14px; padding:18px; margin:0 0 20px; }}
section h2 {{ margin:0 0 4px; font-size:1.15rem; }}
.fila {{ display:grid; grid-template-columns: minmax(0,1.3fr) minmax(0,1fr); gap:18px; align-items:start; margin-top:12px; }}
@media (max-width:820px) {{ .fila {{ grid-template-columns: 1fr; }} }}
img {{ width:100%; border-radius:10px; border:1px solid var(--borde); }}
table {{ width:100%; border-collapse:collapse; font-size:.9rem; margin-top:12px; }}
td, th {{ padding:4px 6px; border-bottom:1px solid var(--borde); text-align:right; }} td:first-child, th:first-child {{ text-align:left; }}
.ok {{ color:var(--igual); }} .no {{ color:var(--distinto); font-weight:600; }}
.lienzo {{ position:relative; height:var(--alto); }}
</style></head><body><main>
<h1>Informe anual {periodo}: gráficas calculadas por el SIA</h1>
<div class="tenue">Del {inicio} al {fin}. Azul: SIA · Ocre: gráfica del informe hecha a mano.</div>
<div class="resumen"><div class="cifra"><b>{iguales}</b>cifras iguales</div><div class="cifra"><b>{distintas}</b>cifras distintas</div>
<div class="cifra"><b>{figuras}</b>figuras</div></div>
{secciones}
</main>
<script>
const color = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
for (const g of {datos}) {{
  new Chart(document.getElementById(g.id), {{ type:'bar', data:{{ labels:g.etiquetas, datasets:[
      {{ label:'SIA', data:g.sia, backgroundColor:color('--sia') }},
      ...(g.informe.some(v => v !== null) ? [{{ label:'Informe', data:g.informe, backgroundColor:color('--informe') }}] : [])] }},
    options:{{ indexAxis:'y', maintainAspectRatio:false, plugins:{{ legend:{{ labels:{{ color:color('--texto') }} }} }},
      scales:{{ x:{{ ticks:{{ color:color('--tenue') }}, grid:{{ color:color('--borde') }} }},
               y:{{ ticks:{{ color:color('--texto'), autoSkip:false }}, grid:{{ display:false }} }} }} }} }});
}}
</script></body></html>"""


def miniatura(ruta, ancho=900):
    from PIL import Image

    Image.MAX_IMAGE_PIXELS = None
    imagen = Image.open(ruta).convert('RGB')
    imagen.thumbnail((ancho, ancho))
    salida = io.BytesIO()
    imagen.save(salida, 'JPEG', quality=72)
    return 'data:image/jpeg;base64,' + base64.b64encode(salida.getvalue()).decode()


class Command(BaseCommand):
    help = 'Genera una página HTML con las gráficas del informe calculadas desde el SIA y la comparación con las originales.'

    def add_arguments(self, parser):
        parser.add_argument('salida', help='Archivo .html a escribir.')
        parser.add_argument('--periodo', default='2025-2026')
        parser.add_argument('--graficas', help='Carpeta con las imágenes originales del informe (opcional).')

    def handle(self, salida, periodo, graficas=None, **options):
        p = Periodo.de(periodo)
        referencia = REFERENCIA_2025_2026 if p.nombre == '2025-2026' else {}
        carpeta = Path(graficas) if graficas else None
        secciones, datos, iguales, distintas = [], [], 0, 0
        for n, (figura, funcion) in enumerate(FIGURAS.items()):
            calculado, esperado = funcion(p), referencia.get(figura, {})
            claves = list(dict.fromkeys([*esperado, *calculado]))
            filas = []
            for clave in claves:
                c, e = calculado.get(clave, 0), esperado.get(clave)
                if e is not None:
                    iguales, distintas = iguales + (c == e), distintas + (c != e)
                estado = '' if e is None else ('<span class="ok">=</span>' if c == e else '<span class="no">≠</span>')
                filas.append(f'<tr><td>{html.escape(str(clave))}</td><td>{c}</td>'
                             f'<td>{"" if e is None else e}</td><td>{estado}</td></tr>')
            graficables = [k for k in claves if k != 'total' and not k.endswith('· horas')]  # Las horas van en la tabla.
            datos.append({'id': f'g{n}', 'etiquetas': graficables, 'sia': [calculado.get(k, 0) for k in graficables],
                          'informe': [esperado.get(k) for k in graficables]})
            imagen = ''
            prefijo = IMAGENES.get(figura.split()[0])
            if carpeta and prefijo:
                ruta = next(iter(sorted(carpeta.glob(f'{prefijo}*'))), None)
                if ruta:
                    imagen = f'<img alt="Gráfica original: {html.escape(figura)}" src="{miniatura(ruta)}">'
            alto = max(160, 26 * len(graficables) + 60)
            secciones.append(
                f'<section><h2>{html.escape(figura)}</h2><div class="fila"><div>'
                f'<div class="lienzo" style="--alto:{alto}px"><canvas id="g{n}"></canvas></div>'
                f'<table><tr><th></th><th>SIA</th><th>Informe</th><th></th></tr>{"".join(filas)}</table></div>'
                f'<div>{imagen}</div></div></section>')
        Path(salida).write_text(PLANTILLA.format(
            periodo=p.nombre, inicio=p.inicio.strftime('%d/%m/%Y'), fin=p.fin.strftime('%d/%m/%Y'), iguales=iguales,
            distintas=distintas, figuras=len(FIGURAS), secciones='\n'.join(secciones), datos=json.dumps(datos)),
            encoding='utf-8')
        self.stdout.write(self.style.SUCCESS(f'Página escrita en {salida} ({iguales} iguales, {distintas} distintas).'))
