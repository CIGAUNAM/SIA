/* Gráficas de los informes del SIA (ECharts), con el estilo del informe anual.
 *
 * Cada gráfica es una sola instancia de ECharts (título, paneles, total y pie incluidos), así que el PNG y el SVG
 * que se descargan son idénticos a lo que se ve. Los datos vienen del servidor en la forma común que describe
 * informes/indicadores.py.
 */
(function () {
  'use strict';

  const FONDO = '#F8F8F3', TARJETA = '#ECEBE6', OSCURO = '#2D3A2E', TEXTO = '#2F3A32', TENUE = '#6B736C',
    FUENTE = 'Poppins, "Segoe UI", sans-serif';

  // ------------------------------------------------------------------------------------------- utilidades
  function aclarar(hex, t) {
    const n = parseInt(hex.slice(1), 16);
    const c = [n >> 16, (n >> 8) & 255, n & 255].map(v => Math.round(v + (255 - v) * t));
    return '#' + c.map(v => v.toString(16).padStart(2, '0')).join('');
  }
  function partir(texto, max) {  // Parte un texto largo en renglones.
    const palabras = String(texto).split(' '), lineas = [];
    let actual = '';
    for (const p of palabras) {
      if ((actual + ' ' + p).trim().length > max && actual) { lineas.push(actual); actual = p; }
      else actual = (actual + ' ' + p).trim();
    }
    if (actual) lineas.push(actual);
    return lineas.join('\n');
  }
  const suma = a => a.reduce((x, y) => x + (Number(y) || 0), 0);
  const fmt = v => (typeof v === 'number' && !Number.isInteger(v)) ? v.toFixed(1) : String(v);

  function texto(x, y, contenido, estilo) {
    return {type: 'text', x: x, y: y, silent: true,
      style: Object.assign({text: contenido, fill: TEXTO, font: `400 14px ${FUENTE}`, textAlign: 'center',
        textVerticalAlign: 'top'}, estilo || {})};
  }
  function fuente(peso, tam) { return `${peso} ${tam}px ${FUENTE}`; }

  function base(g, W, H) {
    const titulo = [{text: g.titulo, left: 'center', top: 22,
      textStyle: {fontFamily: FUENTE, fontSize: 24, fontWeight: 700, color: OSCURO}}];
    if (g.subtitulo) titulo.push({text: g.subtitulo, left: 'center', top: 60,
      textStyle: {fontFamily: FUENTE, fontSize: 16, fontWeight: 400, color: TENUE}});
    return {
      backgroundColor: FONDO, animation: false, textStyle: {fontFamily: FUENTE, color: TEXTO},
      title: titulo, graphic: [texto(W / 2, H - 38, g.pie || '', {font: `italic 400 14px ${FUENTE}`, fill: TENUE})],
      grid: [], xAxis: [], yAxis: [], series: [], legend: []
    };
  }

  // Círculo con el total, arriba al centro. Devuelve la altura que ocupa.
  function circuloTotal(op, g, W, y) {
    const d = g.datos;
    if (!g.mostrar_total || d.total === undefined || d.total === null) return 0;
    const r = 58;
    op.graphic.push({type: 'circle', silent: true, shape: {cx: W / 2, cy: y + r, r: r},
      style: {fill: OSCURO, shadowBlur: 8, shadowColor: 'rgba(0,0,0,.18)', shadowOffsetY: 4}});
    op.graphic.push(texto(W / 2, y + r - 30, fmt(d.total), {fill: '#fff', font: fuente(700, 38)}));
    op.graphic.push(texto(W / 2, y + r + 14, partir(d.total_etiqueta || '', 18), {fill: '#fff', font: fuente(400, 12)}));
    return 2 * r + 24;
  }

  // Leyenda dibujada (no la de ECharts, que solo muestra nombres de series reales).
  function leyenda(op, nombres, colores, H, W) {
    W = W || 1200;
    const anchos = nombres.map(n => 40 + String(n).length * 8.2), hueco = 28;
    let x = (W - (suma(anchos) + hueco * (nombres.length - 1))) / 2;
    const y = H - 86;
    nombres.forEach((n, i) => {
      op.graphic.push({type: 'rect', silent: true, shape: {x: x, y: y, width: 26, height: 14, r: 7},
        style: {fill: colores[i % colores.length]}});
      op.graphic.push(texto(x + 34, y - 2, n, {textAlign: 'left', font: fuente(400, 14)}));
      x += anchos[i] + hueco;
    });
  }

  // Columnas o barras, un panel junto a otro (planta, publicaciones, cursos, tesis, PRIDE, SNII…).
  function barras(g, W, H, horizontal) {
    const op = base(g, W, H), d = g.datos, paneles = d.paneles, n = paneles.length;
    let y0 = g.subtitulo ? 100 : 76;
    y0 += circuloTotal(op, g, W, y0);
    const multi = paneles.some(p => p.series.length > 1);
    const nombres = multi ? paneles[0].series.map(s => s.nombre) : [];
    const margen = 40, hueco = 36, ancho = (W - 2 * margen - hueco * (n - 1)) / n;
    const maximo = Math.max(1, ...paneles.map(p => Math.max(0, ...p.categorias.map((_, i) =>
      g.apilado ? suma(p.series.map(s => s.valores[i])) : Math.max(...p.series.map(s => s.valores[i]))))));
    paneles.forEach((p, k) => {
      const x = margen + k * (ancho + hueco);
      let y = y0;
      if (n > 1 || p.titulo) {  // Tarjeta del panel con su título, total y reparto.
        op.graphic.push({type: 'rect', silent: true, z: -10, shape: {x: x, y: y, width: ancho, height: H - y - 100, r: 22},
          style: {fill: TARJETA}});
        op.graphic.push(texto(x + ancho / 2, y + 22, p.titulo || '', {font: fuente(600, 22),
          fill: n > 1 && !multi ? g.colores[k % g.colores.length] : OSCURO}));
        y += 58;
        if (p.total !== null && p.total !== undefined && g.mostrar_total) {
          op.graphic.push(texto(x + ancho / 2, y, fmt(p.total), {font: fuente(600, 17), fill: TENUE}));
          y += 34;
        }
        if (p.partes && p.partes.length) {  // Barra de reparto (F/M, internacional/nacional).
          // Con varias series, el reparto usa sus colores (internacional/nacional); si no, los de género.
          const w = ancho * 0.8, x1 = x + ancho * 0.1,
            colores = multi ? g.colores : ['#B87333', '#C4A85A', '#4A7C8C', '#949A90'];
          let acumulado = 0;
          p.partes.forEach((parte, j) => {
            const wj = w * parte.valor / 100;
            if (wj <= 0) return;
            op.graphic.push({type: 'rect', silent: true, shape: {x: x1 + acumulado, y: y, width: wj, height: 34, r: 17},
              style: {fill: colores[j % colores.length]}});
            op.graphic.push(texto(x1 + acumulado + wj / 2, y + 8, `${parte.nombre} ${parte.valor}%`,
              {font: fuente(600, 14), fill: j === 0 || multi ? '#fff' : OSCURO}));
            acumulado += wj;
          });
          y += 54;
        }
        y += 24;
      }
      const grid = {left: x + (horizontal ? Math.min(160, ancho * 0.32) : 18), width: ancho -
        (horizontal ? Math.min(160, ancho * 0.32) + 60 : 36), top: y + 26, bottom: n > 1 || p.titulo ? 150 : 120,
        containLabel: false};
      op.grid.push(grid);
      const cat = {type: 'category', data: p.categorias, gridIndex: k, axisTick: {show: false},
        axisLine: {lineStyle: {color: '#C9CBC3'}}, inverse: horizontal,
        axisLabel: {fontFamily: FUENTE, fontSize: 14, color: TENUE, interval: 0, fontWeight: horizontal ? 600 : 400,
          formatter: v => partir(v, horizontal ? 22 : 12)}};
      const val = {type: 'value', gridIndex: k, max: maximo * 1.12, show: false, splitLine: {show: false}};
      op.xAxis.push(horizontal ? val : cat);
      op.yAxis.push(horizontal ? cat : val);
      const unaSerie = p.series.length === 1;
      p.series.forEach((s, j) => {
        const color = unaSerie && n > 1 ? g.colores[k % g.colores.length] : g.colores[j % g.colores.length];
        const ultima = j === p.series.length - 1, primera = j === 0, r = 22;
        let radio = [r, r, r, r];
        if (g.apilado && !unaSerie) radio = horizontal ? [primera ? r : 0, ultima ? r : 0, ultima ? r : 0, primera ? r : 0]
          : [ultima ? r : 0, ultima ? r : 0, primera ? r : 0, primera ? r : 0];
        // Una sola serie en un solo panel: cada barra con su color (como en el informe).
        const datos = unaSerie && n === 1 ? s.valores.map((v, i) => ({value: v,
          itemStyle: {color: (d.colores_categorias || g.colores)[i % g.colores.length]}})) : s.valores;
        op.series.push({type: 'bar', name: s.nombre, xAxisIndex: k, yAxisIndex: k, data: datos,
          stack: g.apilado ? 'p' + k : null, barMaxWidth: horizontal ? 52 : 70, barCategoryGap: '38%',
          itemStyle: {color: color, borderRadius: radio, shadowBlur: 4, shadowColor: 'rgba(0,0,0,.12)', shadowOffsetX: 3},
          label: {show: g.mostrar_valores, position: unaSerie || !g.apilado ? (horizontal ? 'right' : 'top') : 'inside',
            formatter: o => o.value ? fmt(o.value) : '', fontFamily: FUENTE, fontWeight: 700,
            fontSize: unaSerie ? 20 : 14, color: unaSerie || !g.apilado ? OSCURO : '#fff'}});
      });
      if (g.apilado && !unaSerie && g.mostrar_valores) {  // Total encima de cada columna apilada.
        const totales = p.categorias.map((_, i) => suma(p.series.map(s => s.valores[i])));
        op.series.push({type: 'scatter', xAxisIndex: k, yAxisIndex: k, symbolSize: 0, silent: true,
          data: horizontal ? totales.map((t, i) => [t, i]) : totales.map((t, i) => [i, t]),
          label: {show: true, position: horizontal ? 'right' : 'top', formatter: o => fmt(horizontal ? o.value[0] : o.value[1]),
            fontFamily: FUENTE, fontWeight: 700, fontSize: 18, color: OSCURO}});
      }
    });
    if (multi) leyenda(op, nombres, g.colores, H, W);
    return op;
  }

  // Rango (mínimo–máximo) y promedio por categoría (antigüedad).
  function rango(g, W, H) {
    const op = base(g, W, H), paneles = g.datos.paneles, n = paneles.length;
    const y0 = g.subtitulo ? 110 : 86, margen = 70, hueco = 50, ancho = (W - 2 * margen - hueco * (n - 1)) / n;
    const maximo = Math.max(1, ...paneles.flatMap(p => p.series.find(s => s.nombre === 'Máximo').valores));
    paneles.forEach((p, k) => {
      const x = margen + k * (ancho + hueco), color = g.colores[k % g.colores.length];
      const serie = nombre => p.series.find(s => s.nombre === nombre).valores;
      const prom = serie('Promedio'), min = serie('Mínimo'), max = serie('Máximo');
      op.graphic.push(texto(x + ancho / 2, y0, p.titulo, {font: fuente(600, 22), fill: color}));
      op.grid.push({left: x, width: ancho, top: y0 + 60, bottom: 110});
      op.xAxis.push({type: 'category', gridIndex: k, data: p.categorias, axisTick: {show: false},
        axisLabel: {fontFamily: FUENTE, fontSize: 14, color: TEXTO, formatter: v => partir(v, 9)},
        axisLine: {lineStyle: {color: '#C9CBC3'}}});
      op.yAxis.push({type: 'value', gridIndex: k, max: Math.ceil(maximo / 5) * 5 + 2, min: 0,
        axisLabel: {show: k === 0, fontFamily: FUENTE, color: TENUE}, name: k === 0 ? 'Años' : '',
        splitLine: {lineStyle: {color: '#E3E4DD'}}});
      op.series.push({type: 'bar', xAxisIndex: k, yAxisIndex: k, stack: 'r' + k, data: min, silent: true,
        itemStyle: {color: 'transparent'}, barWidth: 44});
      op.series.push({type: 'bar', xAxisIndex: k, yAxisIndex: k, stack: 'r' + k, barWidth: 44, silent: true,
        data: max.map((m, i) => Math.max(m - min[i], 0.6)),
        itemStyle: {color: aclarar(color, 0.55), borderRadius: 22, opacity: 0.9}});
      op.series.push({type: 'scatter', xAxisIndex: k, yAxisIndex: k, data: prom, symbolSize: 18,
        itemStyle: {color: color, borderColor: '#fff', borderWidth: 3},
        label: {show: g.mostrar_valores, position: 'top', distance: 14, formatter: o => 'x̄ ' + fmt(o.value),
          fontFamily: FUENTE, fontWeight: 700, fontSize: 16, color: OSCURO}});
    });
    return op;
  }

  // Comparación por periodos: una columna por categoría y una pastilla por periodo (financiamiento).
  function pastillas(g, W, H) {
    const op = base(g, W, H), p = g.datos.paneles[0], n = p.categorias.length, periodos = p.series;
    const y0 = g.subtitulo ? 110 : 90, margen = 30, ancho = (W - 2 * margen) / n;
    const maximo = Math.max(1, ...periodos.flatMap(s => s.valores));
    p.categorias.forEach((c, k) => {
      const x = margen + k * ancho;
      op.graphic.push(texto(x + ancho / 2, y0, partir(c, 18), {font: fuente(700, 17), fill: OSCURO}));
      op.grid.push({left: x + 16, width: ancho - 32, top: y0 + 60, bottom: 190});
      op.xAxis.push({type: 'value', gridIndex: k, max: maximo, show: false});
      op.yAxis.push({type: 'category', gridIndex: k, inverse: true, show: false, data: periodos.map(s => s.nombre)});
      op.series.push({type: 'bar', xAxisIndex: k, yAxisIndex: k, barWidth: 44,
        data: periodos.map((s, j) => ({value: Math.max(s.valores[k], maximo * 0.13), real: s.valores[k],
          itemStyle: {color: g.colores[j % g.colores.length]}})),
        itemStyle: {borderRadius: 22, shadowBlur: 3, shadowColor: 'rgba(0,0,0,.15)', shadowOffsetX: 3},
        label: {show: true, position: 'inside', formatter: o => o.data.real, fontFamily: FUENTE, fontWeight: 700,
          fontSize: 17, color: '#fff'}});
      if (periodos.length > 1) {  // Cambio respecto al periodo anterior.
        const d = periodos[periodos.length - 1].valores[k] - periodos[periodos.length - 2].valores[k];
        const [etq, fondo, tinta] = d > 0 ? ['▲ +' + d, '#DDE5C6', '#4F6B2A'] : d < 0 ? ['▼ ' + d, '#F3DDCB', '#A35A26']
          : ['● Sin cambio', '#E6E6E1', '#555'];
        op.graphic.push({type: 'rect', silent: true, shape: {x: x + ancho / 2 - 70, y: H - 170, width: 140, height: 44, r: 22},
          style: {fill: fondo}});
        op.graphic.push(texto(x + ancho / 2, H - 158, etq, {font: fuente(700, 16), fill: tinta}));
      }
    });
    leyenda(op, periodos.map(s => s.nombre), g.colores, H, W);
    return op;
  }

  // Dona con una sola serie (cuartiles, prioridades…).
  function dona(g, W, H) {
    const op = base(g, W, H), p = g.datos.paneles[0], unidad = (g.datos.extra || {}).unidad === '%' ? '%' : '';
    const datos = p.categorias.map((c, i) => ({name: c, value: p.series[0].valores[i],
      itemStyle: {color: (g.datos.colores_categorias || g.colores)[i % g.colores.length]}}));
    op.series.push({type: 'pie', radius: ['36%', '66%'], center: ['50%', '54%'], data: datos,
      itemStyle: {borderColor: FONDO, borderWidth: 4},
      label: {show: g.mostrar_valores, formatter: o => `{n|${o.name}}\n{v|${fmt(o.value)}${unidad}}`,
        rich: {n: {fontFamily: FUENTE, fontSize: 15, color: TEXTO, lineHeight: 22},
          v: {fontFamily: FUENTE, fontSize: 18, fontWeight: 700, color: OSCURO, lineHeight: 26}}}});
    if (g.mostrar_total && g.datos.total != null) {
      op.graphic.push(texto(W / 2, H * 0.54 - 30, fmt(g.datos.total), {font: fuente(700, 40), fill: OSCURO}));
      op.graphic.push(texto(W / 2, H * 0.54 + 16, g.datos.total_etiqueta || '', {font: fuente(400, 14), fill: TENUE}));
    }
    return op;
  }

  // Anillos jerárquicos (tipos de proyectos; cuartil y factor de impacto).
  function anillos(g, W, H) {
    const op = base(g, W, H), d = g.datos, total = d.total || suma(d.jerarquia.map(j => j.valor));
    const grises = {'Con temática de género': '#5B655C', 'Sin temática de género': '#949A90', 'NA': '#FFFFFF',
      'FI <1.0': '#EFEFEC', 'FI 1.0–3.0': '#DADAD5', 'FI 3.1–5.0': '#C3C4BE', 'FI >5.0': '#A3A59F'};
    const nodo = (j, nivel, color) => ({name: j.nombre, value: j.valor,
      // Los rangos de factor de impacto y la temática de género van en grises, con el borde del color de su grupo.
      itemStyle: {color: nivel === 1 ? color : grises[j.nombre] || (nivel === 2 ? aclarar(color, 0.35) : '#949A90'),
        borderColor: nivel > 1 && grises[j.nombre] ? color : FONDO},
      children: (j.hijos || []).map(h => nodo(h, nivel + 1, color))});
    const datos = d.jerarquia.map((j, i) => nodo(j, 1, g.colores[i % g.colores.length]));
    op.series.push({type: 'sunburst', data: datos, radius: [0, '68%'], center: ['50%', '53%'], sort: null,
      nodeClick: false, itemStyle: {borderWidth: 4, borderColor: FONDO},
      levels: [{}, {r0: '6%', r: '34%', label: {rotate: 0, minAngle: 22, fontFamily: FUENTE, fontWeight: 700, fontSize: 15, color: '#fff',
        formatter: o => `${o.name}\n${o.value} (${Math.round(100 * o.value / total)}%)`}},
        {r0: '36%', r: '54%', label: {rotate: 0, fontFamily: FUENTE, fontWeight: 600, fontSize: 13, color: OSCURO,
          minAngle: 10}},
        {r0: '56%', r: '68%', label: {show: d.jerarquia.some(j => (j.hijos || []).some(h => (h.hijos || []).some(x =>
          /^(FI|NA)/.test(x.nombre)))), rotate: 'tangential', fontFamily: FUENTE, fontSize: 11, color: OSCURO, minAngle: 10}}]});
    op.graphic.push(texto(W / 2, g.subtitulo ? 92 : 70, `n = ${total} ${d.total_etiqueta || ''}`,
      {font: `italic 400 16px ${FUENTE}`, fill: TENUE}));
    leyenda(op, d.jerarquia.map(j => j.nombre), g.colores, H, W);
    return op;
  }

  // Rosa polar con un color por categoría (ODS).
  function rosa(g, W, H) {
    const op = base(g, W, H), p = g.datos.paneles[0], colores = g.datos.colores_categorias || g.colores;
    op.polar = {radius: ['17%', '62%'], center: ['50%', '55%']};
    op.angleAxis = {type: 'category', data: p.categorias, startAngle: 95, axisLine: {show: false}, axisTick: {show: false},
      splitLine: {show: false}, axisLabel: {fontFamily: FUENTE, fontSize: 13, color: TEXTO, margin: 26,
        formatter: v => partir(v, 18)}};
    op.radiusAxis = {show: false, max: Math.max(1, ...p.series[0].valores) * 1.05};
    op.series.push({type: 'bar', coordinateSystem: 'polar', barCategoryGap: '18%',
      data: p.series[0].valores.map((v, i) => ({value: v, itemStyle: {color: colores[i % colores.length]}})),
      label: {show: g.mostrar_valores, position: 'end', fontFamily: FUENTE, fontWeight: 700, fontSize: 18, color: OSCURO,
        formatter: o => o.value}});
    const r = Math.min(W, H) * 0.17 * 0.52;
    op.graphic.push({type: 'circle', silent: true, shape: {cx: W / 2, cy: H * 0.55, r: r}, style: {fill: OSCURO}});
    op.graphic.push(texto(W / 2, H * 0.55 - 20, (g.datos.extra || {}).centro || '', {font: fuente(700, 34), fill: '#fff'}));
    return op;
  }

  // Semicírculo por grupos con su desglose (vinculación académica).
  function semicirculo(g, W, H) {
    const op = base(g, W, H), d = g.datos;
    const datos = d.grupos.map((gr, i) => {
      const color = g.colores[i % g.colores.length], total = suma(gr.items.map(x => x.valor));
      const detalle = gr.items.length > 1 ? '\n' + gr.items.map(x => `{d|${x.nombre} — }{b|${x.valor}}`).join('\n') : '';
      // Todos los grupos con el mismo ángulo (como en el informe); la cifra va en la etiqueta.
      return {name: gr.nombre, value: 1, itemStyle: {color: color},
        label: {formatter: `{t|${total} acciones}\n{g|${gr.nombre}}${detalle}`,
          rich: {t: {fontFamily: FUENTE, fontWeight: 700, fontSize: 17, color: color, lineHeight: 26},
            g: {fontFamily: FUENTE, fontWeight: 600, fontSize: 13, color: TENUE, lineHeight: 20},
            d: {fontFamily: FUENTE, fontSize: 13, color: TEXTO, lineHeight: 20},
            b: {fontFamily: FUENTE, fontSize: 13, fontWeight: 700, color: OSCURO, lineHeight: 20}}}};
    });
    op.series.push({type: 'pie', startAngle: 180, endAngle: 360, radius: ['40%', '56%'], center: ['50%', '72%'],
      data: datos, itemStyle: {borderColor: FONDO, borderWidth: 3, borderRadius: 12},
      label: {show: true, position: 'outside', alignTo: 'labelLine', bleedMargin: 10},
      labelLine: {length: 18, length2: 26, lineStyle: {width: 2}}, labelLayout: {hideOverlap: false}});
    if (g.mostrar_total) {
      const r = Math.min(W, H) * 0.14;
      op.graphic.push({type: 'circle', silent: true, shape: {cx: W / 2, cy: H * 0.72, r: r}, style: {fill: OSCURO}});
      op.graphic.push(texto(W / 2, H * 0.72 - r * 0.6, fmt(d.total), {font: fuente(700, Math.round(r * 0.55)), fill: '#fff'}));
      op.graphic.push(texto(W / 2, H * 0.72 + r * 0.05, partir(d.total_etiqueta || '', 20),
        {font: fuente(600, 16), fill: '#fff'}));
    }
    return op;
  }

  const TIPOS = {columnas: (g, W, H) => barras(g, W, H, false), barras: (g, W, H) => barras(g, W, H, true),
    rango: rango, pastillas: pastillas, dona: dona, anillos: anillos, rosa: rosa, semicirculo: semicirculo};

  function alto(g) {
    const d = g.datos;
    if (g.tipo === 'barras') {
      const filas = Math.max(...(d.paneles || [{categorias: []}]).map(p => p.categorias.length));
      return Math.max(560, 300 + filas * 78 + (d.paneles && d.paneles.length > 1 ? 120 : 0));
    }
    return {semicirculo: 900, anillos: 920, rosa: 900, pastillas: 720, rango: 760}[g.tipo] ||
      ((d.total != null && g.mostrar_total) ? 980 : 820);
  }

  // ------------------------------------------------------------------------------------------- tabla (HTML)
  function tabla(g) {
    const d = g.datos, t = document.createElement('table');
    t.className = 'tabla-informe';
    const fila = (celdas, th) => {
      const tr = t.insertRow();
      celdas.forEach(c => { const el = document.createElement(th ? 'th' : 'td'); el.textContent = c ?? ''; tr.appendChild(el); });
    };
    (d.paneles || []).forEach(p => {
      if (p.titulo) fila([p.titulo + (p.total != null ? ` (${p.total})` : '')], true);
      fila(['', ...p.series.map(s => s.nombre)], true);
      p.categorias.forEach((c, i) => fila([c, ...p.series.map(s => fmt(s.valores[i]))]));
    });
    return t;
  }

  // ------------------------------------------------------------------------------------------- API
  const instancias = {};

  function opciones(g, W) {
    const H = alto(g);
    return {op: TIPOS[g.tipo](g, W, H), H: H};
  }

  function dibujar(contenedor, g) {
    contenedor.innerHTML = '';
    if (g.datos.error) {
      contenedor.innerHTML = `<p class="error">${g.datos.error}</p>`;
      return;
    }
    if (g.tipo === 'tabla' || !TIPOS[g.tipo]) {
      contenedor.appendChild(tabla(g));
      return;
    }
    const W = 1200, {op, H} = opciones(g, W);
    const lienzo = document.createElement('div');
    lienzo.style.width = W + 'px';
    lienzo.style.height = H + 'px';
    contenedor.appendChild(lienzo);
    const grafica = echarts.init(lienzo, null, {width: W, height: H});
    grafica.setOption(op);
    instancias[g.id] = {grafica: grafica, g: g, W: W, H: H};
    escalar(contenedor, W, H);
  }

  function escalar(contenedor, W, H) {  // La gráfica se dibuja a 1200 px y se ajusta al ancho disponible.
    const lienzo = contenedor.firstChild, f = Math.min(1, contenedor.clientWidth / W);
    lienzo.style.transform = `scale(${f})`;
    lienzo.style.transformOrigin = 'top left';
    contenedor.style.height = (H * f) + 'px';
  }

  function png(id, escala) {
    const i = instancias[id];
    return i ? i.grafica.getDataURL({type: 'png', pixelRatio: escala || 3, backgroundColor: FONDO}) : null;
  }

  function svg(id) {
    const i = instancias[id];
    if (!i) return null;
    const div = document.createElement('div');
    const tmp = echarts.init(div, null, {renderer: 'svg', width: i.W, height: i.H});
    tmp.setOption(opciones(i.g, i.W).op);
    const texto_ = tmp.renderToSVGString();
    tmp.dispose();
    return texto_;
  }

  function reescalar() {
    Object.values(instancias).forEach(i => escalar(i.grafica.getDom().parentNode, i.W, i.H));
  }

  window.GraficasSIA = {dibujar: dibujar, png: png, svg: svg, reescalar: reescalar, instancias: instancias};
})();
