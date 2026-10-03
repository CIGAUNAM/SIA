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
        self.assertEqual(self.plantilla.graficas.count(), 14)
        for g in self.plantilla.graficas.all():
            self.assertIn(g.tipo, INDICADORES[g.indicador].tipos)

    def test_todos_los_indicadores_calculan_sin_datos(self):
        from nucleo.models import ConfiguracionEntidad

        datos = datos_informe(self.plantilla, ConfiguracionEntidad.objects.first())
        self.assertEqual(len(datos['graficas']), 14)
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
        self.assertEqual(nuevo.graficas.count(), 14)
        self.assertEqual(nuevo.basado_en, self.plantilla)
        self.assertEqual(self.plantilla.graficas.count(), 14)  # La plantilla no cambia.

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
