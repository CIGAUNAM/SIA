import io
import json
import tempfile
from datetime import date
from pathlib import Path
from unittest import mock

from cities_light.models import City, Country, Region
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from formatos.models import PagoViaticos
from investigacion.models import ArticuloCientifico, ArticuloCientificoAutor
from nucleo.admin_base import es_administrador
from nucleo.models import ConfiguracionEntidad, Evento, Institucion, Persona, Revista, TipoEvento, User
from nucleo.externos import ErrorServicio
from nucleo.nombres import formato_cita, partes_cita
from nucleo.permisos import GRUPO_ACADEMICOS, GRUPO_ADMINISTRACION
from SIA.tablero import construir_tablero


SIN_EVIDENCIAS = {'nucleo-evidencia-content_type-object_id-TOTAL_FORMS': 0,
                  'nucleo-evidencia-content_type-object_id-INITIAL_FORMS': 0}


def datos_de_formulario(formulario):
    """Lo que el navegador enviaría con el formulario tal como se muestra (para probar un POST de cambio)."""
    from django.forms import MultiWidget

    datos = {}
    for campo in formulario:
        valor, widget = campo.value(), campo.field.widget
        if valor is None or valor is False or campo.name in ('password', 'avatar'):
            continue
        if isinstance(widget, MultiWidget):
            for i, (sub, parte) in enumerate(zip(widget.widgets, widget.decompress(valor))):
                datos[f'{campo.html_name}_{i}'] = sub.format_value(parte) or ''
        elif isinstance(valor, (list, tuple)):
            datos[campo.html_name] = [getattr(v, 'pk', v) for v in valor]
        elif valor is True:
            datos[campo.html_name] = 'on'
        else:
            datos[campo.html_name] = widget.format_value(getattr(valor, 'pk', valor)) or ''
    return datos


def datos_de_pagina(respuesta):
    """POST equivalente a guardar sin cambios una página de alta o edición del admin (formulario e inlines)."""
    datos = datos_de_formulario(respuesta.context['adminform'].form)
    for inline in respuesta.context['inline_admin_formsets']:
        formset = inline.formset
        datos.update(datos_de_formulario(formset.management_form))
        for formulario in formset.initial_forms:
            datos.update(datos_de_formulario(formulario))
    return datos


class Datos(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.mexico = Country.objects.get(code2='MX')  # Cargado por la migración desde el fixture de países.
        cls.institucion = Institucion.objects.create(nombre='UNAM', pais=cls.mexico)
        cls.revista = Revista.objects.create(nombre='Investigaciones Geográficas', pais=cls.mexico)
        grupo = Group.objects.get(name=GRUPO_ACADEMICOS)
        cls.ana = User.objects.create_user('ana@ciga.unam.mx', password='x', first_name='Ana', last_name='López Pérez',
                                           is_staff=True, tipo=User.Tipo.INVESTIGADOR)
        cls.beto = User.objects.create_user('beto@ciga.unam.mx', password='x', first_name='Beto', last_name='Ruiz',
                                            is_staff=True, tipo=User.Tipo.INVESTIGADOR)
        cls.ana.groups.add(grupo)
        cls.beto.groups.add(grupo)
        cls.admin = User.objects.create_superuser('admin@ciga.unam.mx', password='x')
        cls.administrativa = User.objects.create_user('eva@ciga.unam.mx', password='x', first_name='Eva',
                                                      last_name='Admin', is_staff=True,
                                                      tipo=User.Tipo.ADMINISTRATIVO)
        cls.administrativa.groups.add(Group.objects.get(name=GRUPO_ADMINISTRACION))
        cls.externo = Persona.objects.create(nombre='Externa, C.')
        ConfiguracionEntidad.objects.update(pais_sede=cls.mexico, titular='Dra. Titular Prueba')

    def setUp(self):
        cache.clear()  # La configuración de la entidad se guarda en caché; la BD se revierte en cada prueba.
        # Sin red en las pruebas: las que consultan ORCID o Crossref simulan la respuesta.
        sin_red = mock.patch('nucleo.externos.obtener_json', side_effect=ErrorServicio('sin red'))
        sin_red.start()
        self.addCleanup(sin_red.stop)

    def articulo(self, titulo, *personas, **extra):
        articulo = ArticuloCientifico.objects.create(
            titulo=titulo, revista=self.revista, status='PUBLICADO', fecha_publicado=date(2018, 5, 1), **extra)
        for orden, persona in enumerate(personas, start=1):
            ArticuloCientificoAutor.objects.create(articulo=articulo, persona=persona, orden=orden)
        return articulo


class PersonaTests(Datos):
    def test_cada_cuenta_nace_con_su_persona(self):
        self.assertEqual(self.ana.persona.nombre, 'López Pérez, A.')
        self.ana.last_name = 'López'
        self.ana.save()
        self.ana.persona.refresh_from_db()
        self.assertEqual(self.ana.persona.nombre, 'López Pérez, A.')  # El nombre para mostrar es independiente.

    def test_formato_cita(self):
        self.assertEqual(formato_cita('Juan Carlos', 'Pérez García'), 'Pérez García, J. C.')
        self.assertEqual(formato_cita('Jean-Pierre', 'Dubois'), 'Dubois, J.-P.')
        self.assertEqual(formato_cita('María de los Ángeles', 'Ruiz'), 'Ruiz, M. Á.')
        self.assertEqual(formato_cita('Hans Th.A.', 'Bressers'), 'Bressers, H. T. A.')
        self.assertEqual(formato_cita('E.J', 'Aguayo'), 'Aguayo, E. J.')
        self.assertEqual(formato_cita('adminn', ''), 'adminn')
        self.assertEqual(partes_cita('Bocco (mal), G.'), ('Bocco (mal)', 'G.'))

    def test_grupo_investigadores_incluye_modelos_de_inlines(self):
        permisos = set(Group.objects.get(name=GRUPO_ACADEMICOS).permissions.values_list('codename', flat=True))
        self.assertIn('add_articulocientificoautor', permisos)
        self.assertIn('view_country', permisos)  # Para elegir países en los campos de autocompletado.
        self.assertNotIn('change_pais', permisos)
        self.assertNotIn('add_user', permisos)
        self.assertFalse(es_administrador(self.ana))


class PropietarioAdminTests(Datos):
    def test_lista_solo_registros_propios(self):
        propio = self.articulo('Propio', self.ana.persona, self.externo)
        ajeno = self.articulo('Ajeno', self.beto.persona)
        self.client.force_login(self.ana)
        respuesta = self.client.get(reverse('admin:investigacion_articulocientifico_changelist'))
        self.assertEqual(list(respuesta.context['cl'].result_list), [propio])
        respuesta = self.client.get(reverse('admin:investigacion_articulocientifico_change', args=[ajeno.pk]))
        self.assertEqual(respuesta.status_code, 302)  # El admin redirige cuando el objeto no está en su queryset.

    def test_administrador_ve_todo(self):
        self.articulo('Uno', self.ana.persona)
        self.articulo('Dos', self.beto.persona)
        self.client.force_login(self.admin)
        respuesta = self.client.get(reverse('admin:investigacion_articulocientifico_changelist'))
        self.assertEqual(respuesta.context['cl'].result_count, 2)

    def test_usuario_se_asigna_y_no_se_puede_suplantar(self):
        self.client.force_login(self.ana)
        respuesta = self.client.post(reverse('admin:experiencia_profesional_capacidadpotencialidad_add'), {
            'nombre': 'Percepción remota', 'fecha_inicio': '2018-01-01', 'usuario': self.beto.pk, **SIN_EVIDENCIAS})
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(self.ana.capacidades.get().nombre, 'Percepción remota')
        self.assertFalse(self.beto.capacidades.exists())

    def test_se_agrega_como_autor_si_no_figura(self):
        self.client.force_login(self.ana)
        prefijo = 'articulocientificoautor_set'
        respuesta = self.client.post(reverse('admin:investigacion_articulocientifico_add'), {
            'titulo': 'Sin mí', 'revista': self.revista.pk, 'status': 'ENVIADO', 'fecha_enviado': '2020-01-01',
            f'{prefijo}-TOTAL_FORMS': 1, f'{prefijo}-INITIAL_FORMS': 0,
            f'{prefijo}-0-persona': self.externo.pk, f'{prefijo}-0-orden': '', **SIN_EVIDENCIAS,
        })
        self.assertEqual(respuesta.status_code, 302)
        articulo = ArticuloCientifico.objects.get(titulo='Sin mí')
        autores = list(articulo.articulocientificoautor_set.values_list('persona', 'orden'))
        self.assertEqual(autores, [(self.externo.pk, 1), (self.ana.persona.pk, 2)])

    def test_orden_de_autores_se_renumera(self):
        self.client.force_login(self.ana)
        prefijo = 'articulocientificoautor_set'
        self.client.post(reverse('admin:investigacion_articulocientifico_add'), {
            'titulo': 'Orden', 'revista': self.revista.pk, 'status': 'ENVIADO', 'fecha_enviado': '2020-01-01',
            f'{prefijo}-TOTAL_FORMS': 2, f'{prefijo}-INITIAL_FORMS': 0,
            f'{prefijo}-0-persona': self.externo.pk, f'{prefijo}-0-orden': '5',
            f'{prefijo}-1-persona': self.ana.persona.pk, f'{prefijo}-1-orden': '2', **SIN_EVIDENCIAS,
        })
        articulo = ArticuloCientifico.objects.get(titulo='Orden')
        autores = list(articulo.articulocientificoautor_set.values_list('persona', 'orden'))
        self.assertEqual(autores, [(self.ana.persona.pk, 1), (self.externo.pk, 2)])

    def test_autocomplete_de_proyectos_es_compartido(self):
        from investigacion.models import ProyectoInvestigacion, ProyectoResponsable
        proyecto = ProyectoInvestigacion.objects.create(
            nombre='Proyecto de Beto', fecha_inicio=date(2018, 1, 1), status='EN_PROCESO', clasificacion='BASICO',
            organizacion='INDIVIDUAL', modalidad='DISCIPLINARIO')
        ProyectoResponsable.objects.create(proyecto=proyecto, persona=self.beto.persona)
        self.client.force_login(self.ana)
        respuesta = self.client.get(reverse('admin:autocomplete'), {
            'app_label': 'investigacion', 'model_name': 'articulocientifico', 'field_name': 'proyecto', 'term': ''})
        self.assertEqual([r['text'] for r in respuesta.json()['results']], ['Proyecto de Beto'])


class CatalogoCompartidoTests(Datos):
    """Un catálogo lo edita cualquiera si nadie lo usa, solo su usuario si lo usa una cuenta, y solo la
    administración si lo usan varias."""

    def editar_revista(self, usuario):
        self.client.force_login(usuario)
        url = reverse('admin:nucleo_revista_change', args=[self.revista.pk])
        datos = datos_de_pagina(self.client.get(url))
        datos['nombre'] = f'Revista de {usuario.first_name}'
        return self.client.post(url, datos)

    def test_huerfano_lo_edita_cualquiera_y_solo_quien_lo_creo_lo_borra(self):
        self.client.force_login(self.ana)
        self.client.post(reverse('admin:nucleo_institucion_add'), {
            'nombre': 'Instituto Nuevo', 'pais': self.mexico.pk, 'ciudad': 'Morelia'})
        nueva = Institucion.objects.get(nombre='Instituto Nuevo')
        self.assertEqual(nueva.creado_por, self.ana)
        url = reverse('admin:nucleo_institucion_change', args=[nueva.pk])
        self.client.force_login(self.beto)
        self.assertEqual(self.client.post(url, {'nombre': 'Instituto Renombrado', 'pais': self.mexico.pk,
                                                'ciudad': 'Morelia'}).status_code, 302)
        borrar = reverse('admin:nucleo_institucion_delete', args=[nueva.pk])
        self.assertEqual(self.client.post(borrar, {'post': 'yes'}).status_code, 403)
        self.client.force_login(self.ana)
        self.client.post(borrar, {'post': 'yes'})
        self.assertFalse(Institucion.objects.filter(pk=nueva.pk).exists())

    def test_usado_por_una_cuenta_solo_lo_edita_esa_cuenta(self):
        self.articulo('Uno', self.ana.persona)
        self.articulo('Dos', self.ana.persona)  # Dos registros, pero de la misma cuenta.
        self.assertEqual(self.editar_revista(self.beto).status_code, 403)
        self.assertEqual(self.editar_revista(self.ana).status_code, 302)

    def test_usado_por_varias_cuentas_queda_de_solo_lectura(self):
        self.articulo('De Ana', self.ana.persona)
        self.articulo('De Beto', self.beto.persona)
        self.assertEqual(self.editar_revista(self.ana).status_code, 403)
        self.client.force_login(self.ana)
        pagina = self.client.get(reverse('admin:nucleo_revista_change', args=[self.revista.pk]))
        self.assertContains(pagina, 'Solo lectura')
        self.client.force_login(self.administrativa)
        pagina = self.client.get(reverse('admin:nucleo_revista_change', args=[self.revista.pk]))
        self.assertContains(pagina, 'se reflejará en todos los registros vinculados')
        self.assertEqual(self.editar_revista(self.administrativa).status_code, 302)

    def test_libro_con_autores_de_varias_cuentas(self):
        from nucleo.models import Libro, LibroParticipante
        libro = Libro.objects.create(titulo='Atlas', tipo='INVESTIGACION', pais=self.mexico, status='PUBLICADO',
                                     fecha_publicado=date(2018, 1, 1))
        LibroParticipante.objects.create(libro=libro, persona=self.ana.persona, orden=1)
        url = reverse('admin:nucleo_libro_change', args=[libro.pk])
        self.client.force_login(self.ana)
        self.assertTrue(self.client.get(url).context['has_change_permission'])
        self.client.force_login(self.beto)
        self.assertFalse(self.client.get(url).context['has_change_permission'])
        LibroParticipante.objects.create(libro=libro, persona=self.beto.persona, orden=2)
        self.client.force_login(self.ana)
        self.assertFalse(self.client.get(url).context['has_change_permission'])


class PerfilTests(Datos):
    def test_investigador_solo_edita_su_perfil(self):
        self.client.force_login(self.ana)
        self.assertEqual(self.client.get(reverse('admin:nucleo_user_change', args=[self.ana.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse('admin:nucleo_user_change', args=[self.beto.pk])).status_code, 302)
        self.assertEqual(self.client.get(reverse('admin:nucleo_user_add')).status_code, 403)

    def test_cuenta_nueva_entra_como_investigador(self):
        self.client.force_login(self.admin)
        self.client.post(reverse('admin:nucleo_user_add'), {
            'email': 'Nueva@CIGA.unam.mx', 'password1': 'Clave-de-prueba-9', 'password2': 'Clave-de-prueba-9',
            'usable_password': 'true', 'first_name': 'Nueva', 'last_name': 'Cuenta Prueba'})
        nueva = User.objects.get(email='nueva@ciga.unam.mx')  # Se guarda en minúsculas.
        self.assertTrue(nueva.is_staff)
        self.assertTrue(nueva.groups.filter(name=GRUPO_ACADEMICOS).exists())
        self.assertEqual((nueva.persona.nombre, nueva.persona.email), ('Cuenta Prueba, N.', 'nueva@ciga.unam.mx'))

    def alta(self, **datos):
        self.client.force_login(self.admin)
        return self.client.post(reverse('admin:nucleo_user_add'), {
            'email': 'nuevo@ciga.unam.mx', 'password1': 'Clave-de-prueba-9', 'password2': 'Clave-de-prueba-9',
            'usable_password': 'true', **datos})

    def test_alta_toma_el_nombre_de_orcid(self):
        orcid = {'name': {'given-names': {'value': 'Juan Carlos'}, 'family-name': {'value': 'Pérez García'}}}
        with mock.patch('nucleo.externos.obtener_json', return_value=orcid):
            self.alta(orcid='https://orcid.org/0000-0002-1825-0097')
        persona = User.objects.get(email='nuevo@ciga.unam.mx').persona
        self.assertEqual((persona.nombre, persona.orcid), ('Pérez García, J. C.', '0000-0002-1825-0097'))

    def test_alta_pregunta_si_es_un_coautor_parecido(self):
        respuesta = self.alta(first_name='Carla', last_name='Externa')
        self.assertContains(respuesta, 'Ya hay personas parecidas')
        self.assertContains(respuesta, 'Externa, C. — sin registros')
        self.assertFalse(User.objects.filter(email='nuevo@ciga.unam.mx').exists())
        self.alta(first_name='Carla', last_name='Externa', es_persona=self.externo.pk)
        self.assertEqual(User.objects.get(email='nuevo@ciga.unam.mx').persona, self.externo)

    def test_alta_solo_pregunta_si_hay_parecidas(self):
        self.client.force_login(self.admin)
        self.assertNotContains(self.client.get(reverse('admin:nucleo_user_add')), '¿Es alguna de estas personas?')
        self.assertNotContains(self.alta(first_name='Zoe', last_name='Única', password2='otra'),
                               '¿Es alguna de estas personas?')

    def test_alta_puede_crear_persona_nueva_aunque_haya_parecidas(self):
        self.alta(first_name='Carla', last_name='Externa', es_persona='nueva')
        persona = User.objects.get(email='nuevo@ciga.unam.mx').persona
        self.assertNotEqual(persona, self.externo)
        self.assertEqual(persona.nombre, 'Externa, C.')

    def test_alta_liga_por_orcid_y_no_reutiliza_persona_con_cuenta(self):
        Persona.objects.filter(pk=self.externo.pk).update(orcid='0000-0002-1825-0097')
        Persona.objects.filter(pk=self.beto.persona_id).update(orcid='0000-0001-5109-3700')
        respuesta = self.alta(orcid='0000-0001-5109-3700')
        self.assertContains(respuesta, 'que ya tiene cuenta')
        self.alta(orcid='https://orcid.org/0000-0002-1825-0097')
        self.assertEqual(User.objects.get(email='nuevo@ciga.unam.mx').persona, self.externo)

    def test_alta_encuentra_el_orcid_por_correo(self):
        busqueda = {'num-found': 1, 'expanded-result': [
            {'orcid-id': '0000-0002-1825-0097', 'given-names': 'Juan Carlos', 'family-names': 'Pérez García'}]}
        with mock.patch('nucleo.externos.obtener_json', return_value=busqueda):
            self.alta()
        persona = User.objects.get(email='nuevo@ciga.unam.mx').persona
        self.assertEqual((persona.orcid, persona.nombre), ('0000-0002-1825-0097', 'Pérez García, J. C.'))

    def test_orcid_de_coautor_en_perfil_une_su_produccion(self):
        coautor = Persona.objects.create(nombre='López, A.', orcid='0000-0002-1825-0097')
        self.articulo('Del coautor', coautor)
        url = reverse('admin:nucleo_user_change', args=[self.ana.pk])
        for usuario, esperado in ((self.ana, 'Pide a un administrador'), (self.admin, None)):
            self.client.force_login(usuario)
            datos = datos_de_formulario(self.client.get(url).context['adminform'].form)
            datos['orcid'] = '0000-0002-1825-0097'
            respuesta = self.client.post(url, datos)
            if esperado:
                self.assertContains(respuesta, esperado)
        self.assertEqual(respuesta.status_code, 302, respuesta.context and respuesta.context['adminform'].form.errors)
        self.ana.refresh_from_db()
        self.assertEqual(self.ana.persona.orcid, '0000-0002-1825-0097')
        self.assertFalse(Persona.objects.filter(pk=coautor.pk).exists())
        self.assertEqual(list(ArticuloCientifico.objects.get(titulo='Del coautor').autores.all()), [self.ana.persona])

    def test_buscador_de_persona_para_cuenta_omite_personas_con_cuenta(self):
        self.client.force_login(self.admin)
        respuesta = self.client.get(reverse('admin:autocomplete'), {
            'app_label': 'nucleo', 'model_name': 'user', 'field_name': 'persona', 'term': ''})
        ids = {int(r['id']) for r in respuesta.json()['results']}
        self.assertIn(self.externo.pk, ids)
        self.assertNotIn(self.beto.persona_id, ids)

    def test_buscar_orcid_cuentas(self):
        User.objects.filter(pk=self.ana.pk).update(email='ana@ciga.unam.mx')
        coautor = Persona.objects.create(nombre='López P., Ana', orcid='0000-0002-1825-0097')
        self.articulo('Del coautor', coautor)

        def respuesta(url):
            if 'ana%40ciga' in url:
                return {'num-found': 1, 'expanded-result': [
                    {'orcid-id': '0000-0002-1825-0097', 'given-names': 'Ana', 'family-names': 'López Pérez'}]}
            return {'num-found': 0, 'expanded-result': None}

        with mock.patch('nucleo.externos.obtener_json', side_effect=respuesta):
            call_command('buscar_orcid_cuentas', stdout=io.StringIO())
            self.assertEqual(Persona.objects.get(pk=self.ana.persona_id).orcid, '')  # Sin --aplicar no cambia.
            call_command('buscar_orcid_cuentas', '--aplicar', stdout=io.StringIO())
        self.ana.refresh_from_db()
        self.assertEqual(self.ana.persona.orcid, '0000-0002-1825-0097')
        self.assertFalse(Persona.objects.filter(pk=coautor.pk).exists())
        self.assertEqual(list(ArticuloCientifico.objects.get(titulo='Del coautor').autores.all()), [self.ana.persona])

    def test_coincidencia_de_nombres_con_orcid(self):
        from nucleo.sugerencias_orcid import coincidencia
        perfil = lambda nombres, apellidos: {'nombres': nombres, 'apellidos': apellidos}
        self.assertEqual(coincidencia('Cinthia', 'Ruiz López', perfil('RUIZ-LÓPEZ', 'CINTHIA')), 'exacta')
        self.assertEqual(coincidencia('Gustavo Martín', 'Morales', perfil('Gustavo', 'Martín Morales')), 'exacta')
        self.assertEqual(coincidencia('Adi Estela', 'Lazos Ruíz', perfil('Adi E.', 'Lazos Ruíz')), 'probable')
        self.assertEqual(coincidencia('Alina', 'Alvarez Larrain', perfil('Alina', 'Alvarez')), 'probable')
        self.assertIsNone(coincidencia('Alina', 'Alvarez Larrain', perfil('Alina', 'Alvarez León')))
        self.assertIsNone(coincidencia('Beatriz', 'de la Tejera', perfil('Beatriz', 'de Abreu de Carvalho')))
        self.assertIsNone(coincidencia('Juan', 'Pérez', perfil('José', 'Pérez')))

    def test_sugerir_orcid(self):
        from nucleo.sugerencias_orcid import sugerencias
        User.objects.filter(pk=self.beto.pk).update(is_active=False)
        perfiles = {'ana': [{'orcid': '0000-0002-1825-0097', 'nombres': 'Ana', 'apellidos': 'López Pérez',
                             'nombre': 'López Pérez, A.', 'instituciones': ['Universidad Nacional Autónoma de México']},
                            {'orcid': '0000-0001-5109-3700', 'nombres': 'Ana', 'apellidos': 'López',
                             'nombre': 'López, A.', 'instituciones': []}]}
        with mock.patch('nucleo.sugerencias_orcid.perfiles_por_nombre',
                        side_effect=lambda n, a: perfiles.get(n.lower(), [])), \
                mock.patch('nucleo.sugerencias_orcid.perfiles_por_afiliacion', return_value=[]):
            ConfiguracionEntidad.objects.update(institucion_madre='Universidad Nacional Autónoma de México')
            filas = sugerencias()
            self.assertEqual([(c, [p['orcid'] for p, *_ in x]) for c, x in filas],
                             [(self.ana, ['0000-0002-1825-0097', '0000-0001-5109-3700'])])
            self.client.force_login(self.admin)
            url = reverse('admin:nucleo_user_sugerir_orcid')
            respuesta = self.client.get(url)
            self.assertContains(respuesta, 'value="0000-0002-1825-0097" class="mt-1" checked')
            self.client.post(url, {f'cuenta_{self.ana.pk}': '0000-0002-1825-0097'})
        self.ana.refresh_from_db()
        self.assertEqual(self.ana.persona.orcid, '0000-0002-1825-0097')
        self.client.force_login(self.ana)
        self.assertEqual(self.client.get(reverse('admin:nucleo_user_sugerir_orcid')).status_code, 403)

    def test_invalidar_contrasenas_antiguas(self):
        from django.contrib.auth.hashers import make_password
        User.objects.filter(pk=self.ana.pk).update(password=make_password('vieja', hasher='pbkdf2_sha256').replace(
            'pbkdf2_sha256$1500000$', 'pbkdf2_sha256$100000$'))
        self.beto.set_password('nueva-clave-9')
        self.beto.save()
        call_command('invalidar_contrasenas_antiguas', stdout=io.StringIO())
        self.assertTrue(User.objects.get(pk=self.ana.pk).has_usable_password())  # Sin --aplicar no cambia.
        call_command('invalidar_contrasenas_antiguas', '--aplicar', stdout=io.StringIO())
        self.assertFalse(User.objects.get(pk=self.ana.pk).has_usable_password())
        self.assertTrue(User.objects.get(pk=self.beto.pk).check_password('nueva-clave-9'))

    def test_completar_orcid(self):
        Persona.objects.filter(pk=self.externo.pk).update(orcid='0000-0002-1825-0097')
        orcid = {'name': {'given-names': {'value': 'Carla María'}, 'family-name': {'value': 'Externa Ruiz'}}}
        salida = io.StringIO()
        with mock.patch('nucleo.externos.obtener_json', return_value=orcid):
            call_command('completar_orcid', stdout=salida)
            self.externo.refresh_from_db()
            self.assertEqual(self.externo.nombre, 'Externa, C.')  # Sin --aplicar no cambia nada.
            call_command('completar_orcid', '--aplicar', stdout=salida)
        self.externo.refresh_from_db()
        self.assertEqual(self.externo.nombre, 'Externa Ruiz, C. M.')

    def test_investigador_ajusta_su_nombre_pero_no_su_persona_ni_su_orcid(self):
        Persona.objects.filter(pk=self.ana.persona_id).update(orcid='0000-0002-1825-0097')
        self.client.force_login(self.ana)
        url = reverse('admin:nucleo_user_change', args=[self.ana.pk])
        formulario = self.client.get(url).context['adminform'].form
        self.assertNotIn('persona', formulario.fields)
        self.assertTrue(formulario.fields['orcid'].disabled)
        self.assertNotIn('tipo', formulario.fields)  # Solo lo cambia un administrador.
        datos = {k: v for k, v in formulario.initial.items() if v is not None and k not in ('password', 'avatar')}
        datos.update(nombre_persona='López-Pérez, Ana', orcid='0000-0001-0000-0000', persona=self.beto.persona_id,
                     tipo=User.Tipo.ADMINISTRATIVO)
        respuesta = self.client.post(url, datos)
        self.assertEqual(respuesta.status_code, 302, respuesta.context and respuesta.context['adminform'].form.errors)
        self.ana.refresh_from_db()
        self.assertEqual(self.ana.persona.nombre, 'López-Pérez, Ana')
        self.assertEqual(self.ana.persona.orcid, '0000-0002-1825-0097')
        self.assertNotEqual(self.ana.persona, self.beto.persona)
        self.assertEqual(self.ana.tipo, User.Tipo.INVESTIGADOR)  # Se ignora el tipo que mande el académico.


    def test_perfil_ofrece_copiar_domicilio_de_la_entidad(self):
        ConfiguracionEntidad.objects.update(direccion='Antigua carretera a Pátzcuaro 8701')
        cache.clear()
        self.client.force_login(self.ana)
        respuesta = self.client.get(reverse('admin:nucleo_user_change', args=[self.ana.pk]))
        self.assertContains(respuesta, 'data-domicilio="Antigua carretera a Pátzcuaro 8701"')
        self.assertNotContains(respuesta, 'name="celular"')

    def test_entra_con_correo_sin_distinguir_mayusculas(self):
        self.assertTrue(self.client.login(username='ANA@ciga.unam.mx', password='x'))
        respuesta = self.client.post(reverse('admin:login'), {'username': 'Beto@Ciga.unam.mx', 'password': 'x'})
        self.assertEqual(respuesta.status_code, 302)


class DocumentosTests(Datos):
    def test_cv_en_html_escapa_y_formatea(self):
        self.articulo('Suelos & agua <al 100%>', self.ana.persona, self.externo)
        self.client.force_login(self.ana)
        respuesta = self.client.get(reverse('admin:cv'), {'generar': 1, 'formato': 'html'})
        self.assertContains(respuesta, '<strong>Suelos &amp; agua &lt;al 100%&gt;</strong>', html=False)
        self.assertContains(respuesta, 'López Pérez, A., Externa, C. (2018)')

    def test_cv_filtra_por_periodo_y_seccion(self):
        self.articulo('Artículo 2018', self.ana.persona)
        self.client.force_login(self.ana)
        fuera = self.client.get(reverse('admin:cv'), {'generar': 1, 'formato': 'html', 'desde': 2019})
        self.assertNotContains(fuera, 'Artículo 2018')
        otra_seccion = self.client.get(reverse('admin:cv'), {'generar': 1, 'formato': 'html', 'secciones': 'docencia'})
        self.assertNotContains(otra_seccion, 'Artículo 2018')

    def test_cv_en_pdf_y_word(self):
        self.articulo('Artículo', self.ana.persona)
        self.client.force_login(self.ana)
        pdf = self.client.get(reverse('admin:cv'), {'generar': 1, 'formato': 'pdf'})
        self.assertEqual(pdf['Content-Type'], 'application/pdf')
        self.assertTrue(pdf.content.startswith(b'%PDF'))
        docx = self.client.get(reverse('admin:cv'), {'generar': 1, 'formato': 'docx'})
        self.assertTrue(docx.content.startswith(b'PK'))

    def test_pagina_de_opciones_del_cv(self):
        self.client.force_login(self.ana)
        respuesta = self.client.get(reverse('admin:cv'))
        self.assertContains(respuesta, 'Generar currículum')
        self.assertNotIn('usuario', respuesta.context['form'].fields)

    def test_cv_de_otro_usuario_requiere_ser_administrador(self):
        self.client.force_login(self.ana)
        self.assertEqual(self.client.get(reverse('admin:cv_usuario', args=[self.beto.pk])).status_code, 403)

    def test_formato_solo_para_su_dueno(self):
        evento = Evento.objects.create(nombre='Congreso', tipo=TipoEvento.objects.create(nombre='Congreso'),
                                       fecha_inicio=date(2026, 5, 1), fecha_fin=date(2026, 5, 3), pais=self.mexico)
        formato = PagoViaticos.objects.create(
            usuario=self.ana, evento=evento, fecha_salida=date(2026, 5, 1), fecha_regreso=date(2026, 5, 3),
            actividades='Ponencia', importe='1500.00', beneficiario='Ana López', cargo_papiit=True)
        url = reverse('admin:formatos_pagoviaticos_descargar_pdf', args=[formato.pk])
        self.client.force_login(self.ana)
        self.assertContains(self.client.get(url, {'formato': 'html'}), '☒ PAPIIT')
        self.assertTrue(self.client.get(url).content.startswith(b'%PDF'))
        self.client.force_login(self.beto)
        self.assertEqual(self.client.get(url).status_code, 403)


class NavegacionTests(Datos):
    def titulos_menu(self, usuario):
        from django.test import RequestFactory

        from SIA.navegacion import menu
        request = RequestFactory().get('/admin/')
        request.user = usuario
        return {item['title'] for grupo in menu(request) for item in grupo['items']}

    def test_investigador_no_ve_catalogos_de_solo_consulta(self):
        titulos = self.titulos_menu(self.ana)
        self.assertIn('Artículos científicos', titulos)
        self.assertIn('Personas', titulos)
        self.assertNotIn('Países', titulos)
        self.assertNotIn('Grupos', titulos)

    def test_administrador_ve_todo_el_menu(self):
        titulos = self.titulos_menu(self.admin)
        self.assertNotIn('Países', titulos)  # Catálogo fijo: solo se elige en los campos.
        self.assertIn('Grupos', titulos)


class TableroTests(Datos):
    def test_cuenta_articulos_con_coautores_externos(self):
        self.articulo('Con externo', self.ana.persona, self.externo)
        self.articulo('Solo Beto', self.beto.persona)
        tablero = construir_tablero(self.ana, hasta=2018, ver_total=True)
        articulos = tablero['series'][0]
        self.assertEqual(articulos['anios'][-1], 2018)
        self.assertEqual(articulos['mios'][-1], 1)
        self.assertEqual(articulos['maximo'][-1], 1)
        self.assertEqual(articulos['total'][-1], 2)

    def test_inicio_del_admin(self):
        self.client.force_login(self.ana)
        respuesta = self.client.get(reverse('admin:index'))
        self.assertContains(respuesta, 'Artículos científicos publicados')


class ConvertirLegacyTests(TestCase):
    LEGACY = [
        {'model': 'nucleo.pais', 'pk': 1, 'fields': {'pais_nombre': 'México', 'pais_nombre_extendido': 'Estados Unidos '
                                                     'Mexicanos', 'pais_codigo': 'mx', 'pais_zona': 'AMERICA_NORTE'}},
        {'model': 'nucleo.user', 'pk': 10, 'fields': {
            'password': 'pbkdf2_sha256$1$a$b', 'last_login': '2019-01-01T00:00:00Z', 'is_superuser': False,
            'username': 'ana', 'first_name': 'Ana', 'last_name': 'López', 'email': '', 'is_staff': False,
            'is_active': True, 'date_joined': '2018-01-01', 'grado': None, 'descripcion': '', 'tipo': 'INVESTIGADOR',
            'fecha_nacimiento': None, 'genero': None, 'pais_origen': 1, 'rfc': '', 'curp': '', 'direccion': '',
            'direccion_continuacion': '', 'pais': 1, 'ciudad': 1, 'telefono': '', 'celular': '', 'url': None,
            'sni': 1, 'pride': '-', 'ingreso_unam': None, 'ingreso_entidad': None, 'egreso_entidad': None,
            'ultimo_contrato': None, 'avatar': '', 'sic': False, 'groups': [], 'user_permissions': []}},
        {'model': 'nucleo.user', 'pk': 11, 'fields': {
            'password': '123', 'last_login': None, 'is_superuser': False, 'username': 'externo', 'first_name': 'Eva',
            'last_name': 'Externa', 'email': '', 'is_staff': False, 'is_active': True, 'date_joined': '2018-01-01',
            'tipo': 'OTRO'}},
        {'model': 'nucleo.revista', 'pk': 5, 'fields': {
            'revista_nombre': 'Revista', 'revista_nombreabreviadowos': None, 'revista_pais': 1, 'revista_indices': [],
            'revista_issn_impreso': None, 'revista_issn_online': None, 'revista_regverificado': True,
            'revista_regfechacreado': '2018-01-01', 'revista_regfechaactualizado': None, 'revista_regusuario': 10}},
        {'model': 'investigacion.articulocientifico', 'pk': 7, 'fields': {
            'titulo': 'Artículo', 'revista': 5, 'volumen': None, 'numero': None, 'fecha_enviado': None,
            'fecha_aceptado': None, 'fecha_enprensa': None, 'fecha_publicado': '2018-03-01', 'status': 'PUBLICADO',
            'solo_electronico': False, 'autores': [11, 10], 'autores_todos': 'Externa, E., López, A.', 'alumnos': [],
            'agradecimientos': [], 'factor_impacto': '1.500', 'url': '', 'pagina_inicio': 1, 'pagina_fin': 9,
            'id_doi': None, 'proyecto': None}},
    ]

    def test_conversion_y_carga(self):
        with tempfile.TemporaryDirectory() as directorio:
            entrada = Path(directorio) / 'legacy.json'
            salida = Path(directorio) / 'fixture.json'
            entrada.write_text(json.dumps(self.LEGACY), encoding='utf-8')
            call_command('convertir_legacy', str(entrada), str(salida), stdout=io.StringIO())
            call_command('loaddata', str(salida), verbosity=0)

        ana = User.objects.get(pk=10)
        self.assertTrue(ana.groups.filter(name=GRUPO_ACADEMICOS).exists())
        self.assertEqual((ana.sni, ana.genero), ('I', ''))
        self.assertEqual(ana.email, 'ana@sin-correo.invalid')  # No tenía correo: recibe uno provisional.
        self.assertEqual(ana.persona.nombre, 'López, A.')
        self.assertFalse(User.objects.filter(pk=11).exists())
        self.assertEqual(str(Persona.objects.get(pk=11)), 'Externa, E.')
        articulo = ArticuloCientifico.objects.get(pk=7)
        autores = [a.persona_id for a in articulo.articulocientificoautor_set.all()]
        self.assertEqual(autores, [11, 10])
        self.assertEqual(Revista.objects.get(pk=5).pais.code2, 'MX')  # El país legacy 'mx' pasa al catálogo.


class GruposTests(Datos):
    def test_permisos_de_administracion(self):
        permisos = set(Group.objects.get(name=GRUPO_ADMINISTRACION).permissions.values_list('codename', flat=True))
        self.assertTrue({'ver_todo', 'change_articulocientifico', 'delete_revista', 'change_user',
                         'change_periodoinforme', 'change_configuracionentidad'} <= permisos)
        self.assertFalse({'delete_articulocientifico', 'delete_user', 'change_group', 'change_permission'} & permisos)

    def test_editar_produccion_ajena_pide_motivo_y_queda_en_historial(self):
        articulo = self.articulo('De Ana', self.ana.persona)
        url = reverse('admin:investigacion_articulocientifico_change', args=[articulo.pk])
        self.client.force_login(self.administrativa)
        datos = datos_de_pagina(self.client.get(url))
        datos['titulo'] = 'De Ana (corregido)'
        respuesta = self.client.post(url, datos)
        self.assertContains(respuesta, 'Motivo del cambio')
        datos['motivo_cambio'] = 'Título corregido según la constancia'
        self.assertEqual(self.client.post(url, datos).status_code, 302)
        ultimo = articulo.history.first()
        self.assertEqual((ultimo.titulo, ultimo.history_user, ultimo.history_change_reason),
                         ('De Ana (corregido)', self.administrativa, 'Título corregido según la constancia'))

    def test_administracion_no_borra_produccion_ajena(self):
        articulo = self.articulo('De Ana', self.ana.persona)
        self.client.force_login(self.administrativa)
        url = reverse('admin:investigacion_articulocientifico_delete', args=[articulo.pk])
        self.assertEqual(self.client.post(url, {'post': 'yes'}).status_code, 403)
        self.assertTrue(ArticuloCientifico.objects.filter(pk=articulo.pk).exists())

    def test_administracion_no_toca_superusuarios_ni_permisos(self):
        self.client.force_login(self.administrativa)
        cambio = lambda u: reverse('admin:nucleo_user_change', args=[u.pk])
        formulario = self.client.get(cambio(self.ana)).context['adminform'].form
        self.assertNotIn('is_superuser', formulario.fields)
        self.assertNotIn('groups', formulario.fields)
        pagina_admin = self.client.get(cambio(self.admin))
        self.assertNotContains(pagina_admin, 'name="password1"')
        self.assertEqual(self.client.get(reverse('admin:auth_user_password_change', args=[self.admin.pk]))
                         .status_code, 403)
        self.assertEqual(self.client.get(reverse('admin:auth_group_changelist')).status_code, 403)

    def test_superusuario_edita_sin_motivo(self):
        articulo = self.articulo('De Ana', self.ana.persona)
        url = reverse('admin:investigacion_articulocientifico_change', args=[articulo.pk])
        self.client.force_login(self.admin)
        datos = datos_de_pagina(self.client.get(url))
        datos['titulo'] = 'Otro título'
        respuesta = self.client.post(url, datos)
        self.assertEqual(respuesta.status_code, 302, respuesta.context and [
            respuesta.context['adminform'].form.errors, [(f.formset.prefix, f.formset.errors, f.formset.non_form_errors()) for f in respuesta.context['inline_admin_formsets']]])


class MiPerfilTests(Datos):
    def test_mi_perfil_sin_controles_administrativos_y_con_trayectoria(self):
        from formacion_academica.models import Grado
        Grado.objects.create(usuario=self.ana, nivel='DOCTORADO', titulo_obtenido='Doctora en Geografía',
                             institucion=self.institucion, fecha_grado=date(2015, 6, 1))
        for usuario in (self.ana, self.administrativa, self.admin):
            self.client.force_login(usuario)
            respuesta = self.client.get(reverse('admin:perfil'), follow=True)
            self.assertEqual(respuesta.redirect_chain[-1][0], reverse('admin:nucleo_user_change', args=[usuario.pk]))
            formulario = respuesta.context['adminform'].form
            self.assertNotIn('groups', formulario.fields)
            self.assertNotIn('is_superuser', formulario.fields)
            self.assertIn('nombre_persona', formulario.fields)
            self.assertContains(respuesta, 'Formación académica')
        self.client.force_login(self.ana)
        self.assertContains(self.client.get(reverse('admin:perfil'), follow=True), 'Doctora en Geografía')
        self.client.force_login(self.admin)
        self.assertContains(self.client.get(reverse('admin:nucleo_user_change', args=[self.admin.pk]) + '?completo=1'),
                            'name="is_superuser"')

    def test_guardar_desde_el_perfil_regresa_al_perfil(self):
        from experiencia_profesional.models import LineaInvestigacion
        self.client.force_login(self.ana)
        perfil = reverse('admin:nucleo_user_change', args=[self.ana.pk])
        respuesta = self.client.get(perfil)
        agregar = next(m['agregar'] for s in respuesta.context['trayectoria'] for m in s['modelos']
                       if 'nea' in m['titulo'])
        respuesta = self.client.post(agregar, {'nombre': 'Geografía ambiental', 'fecha_inicio': '2015-01-01',
                                               **SIN_EVIDENCIAS})
        self.assertRedirects(respuesta, perfil, fetch_redirect_response=False)
        self.assertTrue(LineaInvestigacion.objects.filter(usuario=self.ana, nombre='Geografía ambiental').exists())
        self.assertContains(self.client.get(perfil), 'Geografía ambiental')

    def test_menu_de_academicos_sin_formacion_ni_experiencia(self):
        from django.test import RequestFactory
        from SIA.navegacion import menu
        solicitud = RequestFactory().get('/')
        for usuario, esperado in ((self.ana, False), (self.admin, True)):
            solicitud.user = usuario
            grupos = menu(solicitud)
            titulos = [str(g.get('title')) for g in grupos]
            self.assertNotIn('Formación académica', titulos)
            self.assertEqual('Trayectoria' in titulos, esperado, titulos)
            if esperado:
                self.assertEqual(titulos[-1], 'Trayectoria')
            self.assertIn('Mi perfil', [str(i['title']) for i in menu(solicitud)[0]['items']])


class PaisesTests(Datos):
    def test_catalogo_cargado_en_espanol_y_con_los_del_sia_anterior(self):
        self.assertEqual(Country.objects.count(), 264)
        self.assertEqual(str(self.mexico), 'México')
        self.assertTrue(Country.objects.filter(name='Desconocido', code2=None).exists())
        self.assertFalse(Country.objects.filter(name__in=['Inglaterra', 'Gales']).exists())  # Unidas a Reino Unido.
        self.assertIn('Inglaterra', Country.objects.get(code2='GB').alternate_names)

    def test_equivalencia_de_paises_anteriores(self):
        from nucleo.paises import del_fixture, equivalencia
        paises = del_fixture()
        pk = {codigo: p for p, codigo, _ in paises if codigo}
        resultado = equivalencia([(1, 'mx', 'México'), (2, 'EU', 'Estados Unidos'), (3, '99', 'Desconocido'),
                                  (4, '23', 'Inglaterra')], paises)
        desconocido = next(p for p, codigo, nombre in paises if nombre == 'Desconocido')
        self.assertEqual(resultado, {1: pk['MX'], 2: pk['US'], 3: desconocido, 4: pk['GB']})
        with self.assertRaises(ValueError):
            equivalencia([(4, 'ZZ', 'Atlántida')], paises)

    def test_paises_solo_se_seleccionan(self):
        from django.contrib import admin
        self.assertFalse(admin.site.is_registered(Region) or admin.site.is_registered(City))
        self.client.force_login(self.ana)
        busqueda = self.client.get(reverse('admin:autocomplete'), {
            'app_label': 'nucleo', 'model_name': 'institucion', 'field_name': 'pais', 'term': 'Méxi'})
        self.assertIn(str(self.mexico.pk), [r['id'] for r in busqueda.json()['results']])
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse('admin:cities_light_country_add')).status_code, 403)
        self.assertEqual(self.client.post(reverse('admin:cities_light_country_change', args=[self.mexico.pk]),
                                          {'name': 'Otro'}).status_code, 403)
        self.assertNotContains(self.client.get(reverse('admin:index')), '/admin/cities_light/')


class IdentificadoresTests(Datos):
    PERSONA_ORCID = {'name': {'given-names': {'value': 'Juan Carlos'}, 'family-name': {'value': 'Pérez García'}},
                     'emails': {'email': [{'email': 'JCPEREZ@ejemplo.org'}]}}

    def test_rfc_curp_y_telefono(self):
        from django.core.exceptions import ValidationError
        from nucleo.identificadores import normalizar_telefono, validar_curp, validar_rfc, validar_telefono
        for valido in ('GODE561231GR8', 'gode561231gr8'):
            validar_rfc(valido)
        for invalido in ('GODE561231GR9', 'GODE561331GR8', 'DgFdm'):
            with self.assertRaises(ValidationError):
                validar_rfc(invalido)
        validar_curp('HEGG560427MVZRRL04')
        for invalido in ('HEGG560427MVZRRL05', 'HEGG561327MVZRRL04', 'HEGG560427MXXRRL04'):
            with self.assertRaises(ValidationError):
                validar_curp(invalido)
        validar_telefono('(443) 322-3854')
        validar_telefono('+1 650 253 0000')
        with self.assertRaises(ValidationError):
            validar_telefono('12345')
        self.assertEqual(normalizar_telefono('(443) 322-3854 ext. 12'), '+52 443 322 3854 ext. 12')

    def test_perfil_normaliza_y_revisa_la_fecha_de_la_curp(self):
        from django.core.exceptions import ValidationError
        self.ana.rfc, self.ana.curp, self.ana.telefono = 'gode561231gr8', 'hegg560427mvzrrl04', '443 322 3854'
        self.ana.fecha_nacimiento = date(1956, 4, 27)
        self.ana.full_clean()
        self.assertEqual((self.ana.rfc, self.ana.curp, self.ana.telefono),
                         ('GODE561231GR8', 'HEGG560427MVZRRL04', '+52 443 322 3854'))
        self.ana.fecha_nacimiento = date(1960, 1, 1)
        with self.assertRaises(ValidationError) as error:
            self.ana.full_clean()
        self.assertIn('curp', error.exception.message_dict)

    def test_persona_toma_nombre_y_correo_de_orcid_al_guardar(self):
        self.client.force_login(self.admin)
        with mock.patch('nucleo.externos.obtener_json', return_value=self.PERSONA_ORCID):
            respuesta = self.client.post(reverse('admin:nucleo_persona_add'),
                                         {'orcid': '0000-0002-1825-0097', 'nombre': '', 'email': ''})
        self.assertEqual(respuesta.status_code, 302)
        persona = Persona.objects.get(orcid='0000-0002-1825-0097')
        self.assertEqual((persona.nombre, persona.email), ('Pérez García, J. C.', 'jcperez@ejemplo.org'))

    def test_boton_buscar_en_orcid(self):
        self.client.force_login(self.ana)
        url = reverse('admin:orcid')
        with mock.patch('nucleo.externos.obtener_json', return_value=self.PERSONA_ORCID):
            datos = self.client.get(url, {'orcid': 'https://orcid.org/0000-0002-1825-0097'}).json()
        self.assertEqual(datos, {'orcid': '0000-0002-1825-0097', 'nombre': 'Pérez García, J. C.',
                                 'email': 'jcperez@ejemplo.org'})
        busqueda = {'num-found': 1, 'expanded-result': [
            {'orcid-id': '0000-0002-1825-0097', 'given-names': 'Juan Carlos', 'family-names': 'Pérez García'}]}
        with mock.patch('nucleo.externos.obtener_json', return_value=busqueda):
            datos = self.client.get(url, {'email': 'jcperez@ejemplo.org'}).json()
        self.assertEqual(datos['orcid'], '0000-0002-1825-0097')
        self.assertContains(self.client.get(reverse('admin:nucleo_persona_add')), 'Buscar en ORCID')


class PersonasConCuentaTests(Datos):
    def test_lista_y_detalle_muestran_la_cuenta(self):
        self.client.force_login(self.admin)
        lista = self.client.get(reverse('admin:nucleo_persona_changelist'), {'cuenta': 'si'})
        self.assertContains(lista, 'ana@ciga.unam.mx')
        self.assertNotContains(lista, 'Externa, C.')
        self.assertContains(self.client.get(reverse('admin:nucleo_persona_changelist'), {'cuenta': 'no'}), 'Externa, C.')
        detalle = self.client.get(reverse('admin:nucleo_persona_change', args=[self.ana.persona_id]))
        self.assertContains(detalle, reverse('admin:nucleo_user_change', args=[self.ana.pk]))
        self.assertContains(self.client.get(reverse('admin:nucleo_persona_change', args=[self.externo.pk])),
                            'Sin cuenta')

    def test_academico_edita_su_adscripcion_pero_no_su_tipo(self):
        self.client.force_login(self.ana)
        formulario = self.client.get(reverse('admin:perfil'), follow=True).context['adminform'].form
        self.assertIn('ingreso_entidad', formulario.fields)
        self.assertNotIn('tipo', formulario.fields)


class AdscripcionPersonaTests(Datos):
    def test_selectores_indican_adscripcion_pero_str_no_cambia(self):
        from nucleo.admin_base import adscripcion
        User.objects.filter(pk=self.beto.pk).update(egreso_entidad=date(2020, 1, 1))
        beto = Persona.objects.get(pk=self.beto.persona_id)
        self.assertEqual([adscripcion(self.ana.persona), adscripcion(beto), adscripcion(self.externo)],
                         ['actual', 'ex', 'externa'])
        self.assertEqual(str(self.ana.persona), 'López Pérez, A.')  # Informes, PDF y exportaciones: sin marca.
        self.client.force_login(self.ana)
        resultados = self.client.get(reverse('admin:autocomplete'), {
            'app_label': 'investigacion', 'model_name': 'articulocientificoautor', 'field_name': 'persona',
            'term': 'López'}).json()['results']
        self.assertIn({'id': str(self.ana.persona_id), 'text': 'López Pérez, A.', 'adscripcion': 'actual'}, resultados)

    def test_opcion_elegida_lleva_su_adscripcion_y_se_carga_el_script(self):
        articulo = self.articulo('Con Ana', self.ana.persona, self.externo)
        self.client.force_login(self.ana)
        pagina = self.client.get(reverse('admin:investigacion_articulocientifico_change', args=[articulo.pk]))
        self.assertContains(pagina, 'data-adscripcion="actual"')
        self.assertContains(pagina, 'data-adscripcion="externa"')
        self.assertContains(pagina, 'sia/personas.js')
