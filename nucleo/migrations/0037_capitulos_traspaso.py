"""Pasa los capítulos de investigación y de divulgación (y sus autores, historial y evidencias) al modelo único
`nucleo.CapituloLibro`. Los de investigación conservan su id; los de divulgación se recorren con un desfase. Si un
capítulo de divulgación repite título y libro de uno de investigación, se une a él."""

from django.db import migrations

CAMPOS_CAPITULO = ('titulo', 'libro_id', 'pagina_inicio', 'pagina_fin')
CAMPOS_AUTOR = ('persona_id', 'orden')
CAMPOS_HISTORIAL = ('history_date', 'history_change_reason', 'history_type', 'history_user_id')


def traspasar(apps, schema_editor):
    from django.core.management.color import no_style

    Capitulo = apps.get_model('nucleo', 'CapituloLibro')
    Autor = apps.get_model('nucleo', 'CapituloLibroAutor')
    HCapitulo = apps.get_model('nucleo', 'HistoricalCapituloLibro')
    HAutor = apps.get_model('nucleo', 'HistoricalCapituloLibroAutor')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Evidencia = apps.get_model('nucleo', 'Evidencia')
    origenes = [('investigacion', 'CapituloLibroInvestigacion'), ('divulgacion_cientifica', 'CapituloLibroDivulgacion')]

    desfase_cap = desfase_autor = 0
    for app, nombre in origenes:
        Viejo = apps.get_model(app, nombre)
        ViejoAutor = apps.get_model(app, f'{nombre}Autor')
        HViejo = apps.get_model(app, f'Historical{nombre}')
        HViejoAutor = apps.get_model(app, f'Historical{nombre}Autor')

        mapa = {}  # id viejo → id nuevo
        for c in Viejo.objects.order_by('pk'):
            igual = Capitulo.objects.filter(libro_id=c.libro_id, titulo=c.titulo).first()
            if igual is not None:
                mapa[c.pk] = igual.pk
                continue
            mapa[c.pk] = c.pk + desfase_cap
            Capitulo.objects.create(pk=mapa[c.pk], **{k: getattr(c, k) for k in CAMPOS_CAPITULO})
        for a in ViejoAutor.objects.order_by('pk'):
            capitulo = mapa[a.capitulo_id]
            if not Autor.objects.filter(capitulo_id=capitulo, persona_id=a.persona_id).exists():
                Autor.objects.create(pk=a.pk + desfase_autor, capitulo_id=capitulo,
                                     **{k: getattr(a, k) for k in CAMPOS_AUTOR})
        for h in HViejo.objects.order_by('history_id'):
            HCapitulo.objects.create(id=mapa.get(h.id, h.id + desfase_cap),
                                     **{k: getattr(h, k) for k in CAMPOS_CAPITULO + CAMPOS_HISTORIAL})
        for h in HViejoAutor.objects.order_by('history_id'):
            HAutor.objects.create(id=h.id + desfase_autor, capitulo_id=mapa.get(h.capitulo_id, h.capitulo_id + desfase_cap),
                                  **{k: getattr(h, k) for k in CAMPOS_AUTOR + CAMPOS_HISTORIAL})

        viejo_ct = ContentType.objects.filter(app_label=app, model=nombre.lower()).first()
        if viejo_ct is not None:
            nuevo_ct, _ = ContentType.objects.get_or_create(app_label='nucleo', model='capitulolibro')
            for e in Evidencia.objects.filter(content_type=viejo_ct):
                e.content_type, e.object_id = nuevo_ct, mapa.get(e.object_id, e.object_id + desfase_cap)
                e.save(update_fields=['content_type', 'object_id'])

        # El siguiente origen arranca después de todo lo usado (registros vivos y del historial).
        desfase_cap = max([desfase_cap, *mapa.values(), *(i + desfase_cap for i in HViejo.objects.values_list('id', flat=True))]) + 1
        desfase_autor = max([desfase_autor, *Autor.objects.values_list('pk', flat=True),
                             *(i + desfase_autor for i in HViejoAutor.objects.values_list('id', flat=True))]) + 1

    with schema_editor.connection.cursor() as cursor:
        for sql in schema_editor.connection.ops.sequence_reset_sql(no_style(), [Capitulo, Autor]):
            cursor.execute(sql)


class Migration(migrations.Migration):
    dependencies = [
        ('nucleo', '0036_capitulos_libro'),
        ('investigacion', '0009_financiamiento_y_prioridad'),
        ('divulgacion_cientifica', '0008_historicalorganizacioneventodivulgacion_organizado_por_and_more'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [migrations.RunPython(traspasar, migrations.RunPython.noop)]
