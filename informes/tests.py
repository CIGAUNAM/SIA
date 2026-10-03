import json

from django.urls import reverse

from nucleo.tests import Datos

from .admin import datos_informe
from .indicadores import INDICADORES
from .models import Grafica, Informe


class InformesTests(Datos):
    def setUp(self):
        super().setUp()
        self.plantilla = Informe.objects.get(es_plantilla=True)  # La crea la migración con las 14 gráficas.

    def test_la_plantilla_trae_las_graficas_del_informe_anual(self):
        self.assertEqual(self.plantilla.graficas.count(), 15)
        for g in self.plantilla.graficas.all():
            self.assertIn(g.tipo, INDICADORES[g.indicador].tipos)

    def test_todos_los_indicadores_calculan_sin_datos(self):
        from nucleo.models import ConfiguracionEntidad

        datos = datos_informe(self.plantilla, ConfiguracionEntidad.objects.first())
        self.assertEqual(len(datos["graficas"]), 15)
        for g in datos['graficas']:
            self.assertNotIn('error', g['datos'], g['indicador'])
            self.assertTrue(g['datos'].get('paneles'), g['indicador'])

    def test_administracion_ve_edita_y_duplica(self):
        self.client.force_login(self.administrativa)
        self.assertEqual(self.client.get(reverse('admin:informes_ver', args=[self.plantilla.pk])).status_code, 200)
        respuesta = self.client.post(reverse('admin:informes_nuevo_desde', args=[self.plantilla.pk]),
                                     {'nombre': 'Informe anual', 'periodo': '2026-2027'})
        nuevo = Informe.objects.get(nombre='Informe anual', periodo='2026-2027')
        self.assertRedirects(respuesta, reverse('admin:informes_informe_change', args=[nuevo.pk]))
        self.assertEqual(nuevo.graficas.count(), 15)
        self.assertEqual(nuevo.basado_en, self.plantilla)
        self.assertEqual(self.plantilla.graficas.count(), 15)  # La plantilla no cambia.

    def test_los_academicos_no_entran_a_los_informes(self):
        self.client.force_login(self.ana)
        self.assertNotEqual(self.client.get(reverse('admin:informes_ver', args=[self.plantilla.pk])).status_code, 200)
        self.assertNotEqual(self.client.get(reverse('admin:informes_informe_changelist')).status_code, 200)

    def test_excel_y_word(self):
        self.client.force_login(self.administrativa)
        excel = self.client.get(reverse('admin:informes_excel', args=[self.plantilla.pk]))
        self.assertEqual(excel.status_code, 200)
        self.assertIn('spreadsheetml', excel['Content-Type'])
        word = self.client.post(reverse('admin:informes_documento', args=[self.plantilla.pk]),
                                json.dumps({'formato': 'docx', 'imagenes': {}}), content_type='application/json')
        self.assertEqual(word.status_code, 200)
        self.assertIn('wordprocessingml', word['Content-Type'])

    def test_tipo_de_grafica_incompatible_con_el_indicador(self):
        from django.core.exceptions import ValidationError

        g = Grafica(informe=self.plantilla, indicador='planta', tipo='rosa', titulo='x')
        with self.assertRaises(ValidationError):
            g.full_clean()


class EmisionTests(Datos):
    def setUp(self):
        super().setUp()
        plantilla = Informe.objects.get(es_plantilla=True)
        self.informe = plantilla.duplicar(self.administrativa, nombre='Informe anual', periodo='2025-2026')
        self.client.force_login(self.administrativa)

    def emitir(self, motivo=''):
        return self.client.post(reverse('admin:informes_emitir', args=[self.informe.pk]), {'motivo': motivo})

    def test_emitir_congela_las_cifras(self):
        from nucleo.models import Nombramiento, SituacionAcademica

        self.emitir()
        emision = self.informe.emisiones.get()
        self.assertEqual(emision.version, 1)
        planta = next(g for g in emision.datos['graficas'] if g['indicador'] == 'planta')
        self.assertEqual(planta['datos']['total'], 0)
        # Después de emitir llega un académico al periodo: la versión emitida no cambia, pero se avisa.
        nombramiento, _ = Nombramiento.objects.get_or_create(
            nombre='Investigador Titular A, Tiempo Completo', defaults={'clave': 'PRUEBA-ITA'})
        SituacionAcademica.objects.create(usuario=self.ana, anio=2026, nombramiento=nombramiento)
        respuesta = self.client.get(reverse('admin:informes_ver', args=[self.informe.pk]))
        planta = next(g for g in respuesta.context['datos']['graficas'] if g['indicador'] == 'planta')
        self.assertEqual(planta['datos']['total'], 0)
        self.assertGreater(respuesta.context['diferencias'], 0)
        vivo = self.client.get(reverse('admin:informes_ver', args=[self.informe.pk]) + '?vivo=1')
        planta = next(g for g in vivo.context['datos']['graficas'] if g['indicador'] == 'planta')
        self.assertEqual(planta['datos']['total'], 1)
        cambios = self.client.get(reverse('admin:informes_cambios', args=[self.informe.pk]))
        self.assertEqual(cambios.status_code, 200)
        self.assertTrue(cambios.context['diferencias'])

    def test_la_segunda_version_pide_motivo(self):
        self.emitir()
        self.assertEqual(self.emitir().status_code, 200)  # Sin motivo: vuelve al formulario.
        self.assertEqual(self.informe.emisiones.count(), 1)
        self.emitir('Se agregaron dos tesis que faltaban')
        self.assertEqual(list(self.informe.emisiones.values_list('version', flat=True)), [2, 1])

    def test_una_plantilla_no_se_emite(self):
        plantilla = Informe.objects.get(es_plantilla=True)
        self.client.post(reverse('admin:informes_emitir', args=[plantilla.pk]), {'motivo': ''})
        self.assertFalse(plantilla.emisiones.exists())


class CifrasHistoricasTests(Datos):
    def test_anios_anteriores_de_las_cifras_historicas_y_el_del_informe_calculado(self):
        from nucleo.cifras_informe import Periodo

        from .indicadores import snii
        from .models import CifraHistorica

        CifraHistorica.objects.create(indicador='snii', anio=2025, categoria='Nivel I', valor=13)
        CifraHistorica.objects.create(indicador='snii', anio=2026, categoria='Nivel I', valor=99)  # Se ignora.
        datos = snii(Periodo.de('2025-2026'), 2)['paneles'][0]
        self.assertEqual(datos['categorias'], ['2024-2025', '2025-2026'])
        nivel_i = next(s for s in datos['series'] if s['nombre'] == 'Nivel I')
        self.assertEqual(nivel_i['valores'], [13, 0])  # 2026 se calcula: aún no hay académicos con SNII.


class IndicadoresPersonalizadosTests(Datos):
    def test_contar_filtrar_y_agrupar(self):
        from nucleo.cifras_informe import Periodo

        from .models import FiltroIndicador, IndicadorPersonalizado
        from .personalizados import calcular

        self.articulo('Uno', self.ana.persona)
        self.articulo('Dos', self.beto.persona)
        indicador = IndicadorPersonalizado.objects.create(
            nombre='Artículos por país', modelo='investigacion.ArticuloCientifico', campo_fecha='fecha_publicado',
            agrupar_por='revista__pais')
        indicador.full_clean()
        datos = calcular(indicador, Periodo.de('2017-2018'))['paneles'][0]
        self.assertEqual(datos['categorias'], ['México'])
        self.assertEqual(datos['series'][0]['valores'], [2])
        FiltroIndicador.objects.create(indicador=indicador, campo='titulo', operador='es', valor='Uno')
        self.assertEqual(calcular(indicador, Periodo.de('2017-2018'))['paneles'][0]['series'][0]['valores'], [1])
        self.assertEqual(calcular(indicador, Periodo.de('2019-2020'))['paneles'][0]['categorias'], [])

    def test_campo_ajeno_no_valida(self):
        from django.core.exceptions import ValidationError

        from .models import IndicadorPersonalizado

        indicador = IndicadorPersonalizado(nombre='x', modelo='investigacion.ArticuloCientifico',
                                           agrupar_por='usuario__password')
        with self.assertRaises(ValidationError):
            indicador.full_clean()

    def test_formulario_y_grafica(self):
        from .models import IndicadorPersonalizado

        indicador = IndicadorPersonalizado.objects.create(
            nombre='Artículos por año', modelo='investigacion.ArticuloCientifico', agrupar_por='fecha_publicado')
        self.client.force_login(self.administrativa)
        url = reverse('admin:informes_indicadorpersonalizado_change', args=[indicador.pk])
        self.assertContains(self.client.get(url), 'resultado en el periodo actual')
        informe = Informe.objects.get(es_plantilla=True)
        Grafica.objects.create(informe=informe, indicador='personalizado', personalizado=indicador, tipo='columnas',
                               titulo='Artículos por año', orden=99)
        self.assertEqual(self.client.get(reverse('admin:informes_ver', args=[informe.pk])).status_code, 200)
