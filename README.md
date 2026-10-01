# SIA — Sistema de Información Académica

Registro de la producción académica del personal de la entidad (CIGA, UNAM): formación, investigación,
difusión, divulgación, docencia, formación de recursos humanos, vinculación, distinciones y formatos
administrativos. La interfaz es el **admin de Django** con el tema [Unfold](https://unfoldadmin.com): cada académico entra con su
cuenta y solo ve y edita sus propios registros; los administradores ven todo.

## Requisitos

- Python 3.12+ y Django 6.1
- PostgreSQL (en desarrollo también funciona con SQLite)
- Pango (biblioteca de sistema que usa WeasyPrint para los PDF): `brew install pango` en macOS,
  `apt install libpango-1.0-0 libpangoft2-1.0-0` en Debian/Ubuntu

## Instalación

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env        # y edita SECRET_KEY y los datos de la base de datos
.venv/bin/python manage.py migrate
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py runserver
```

`migrate` crea también los grupos **Académicos** y **Administración** con sus permisos (se resincronizan en cada
`migrate`).

### Variables de entorno (`.env`)

| Variable | Descripción |
| --- | --- |
| `SECRET_KEY` | Obligatoria. Cadena larga y aleatoria. |
| `DEBUG` | `True` solo en desarrollo. |
| `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` | Separados por comas. |
| `DB_ENGINE` | `postgresql` (por defecto) o `sqlite`. |
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | Conexión a PostgreSQL. |
| `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL` | Servidor de correo (recuperar contraseñas). Por defecto se imprime en la consola. |
| `PRIVATE_MEDIA_ROOT` | Carpeta de las evidencias adjuntas (fuera de `MEDIA_ROOT`; se descargan solo con permiso). |

### Configuración de la entidad

Los datos propios de la entidad **no van en `.env`**: se editan en el admin, en *Configuración de la entidad*
(nombre, siglas, institución a la que pertenece, logo, titular y su cargo, dirección, consejo técnico, país sede,
remitente de correos, años del tablero y meses para marcar publicaciones pendientes). `.env` queda solo para lo que
depende del despliegue (base de datos, clave secreta, servidor de correo).

El código lee esos datos únicamente con `ConfiguracionEntidad.actual(request)`. Hoy hay un solo registro; cuando el
sistema atienda a varias entidades (multitenant), ese será el punto donde se resuelva la entidad de cada petición.

## Importar los datos del SIA anterior

Los volcados legacy (`dumpdata` de la versión Django 2.0) se convierten al esquema actual y se cargan con
`loaddata`. La carpeta `datos/` está en `.gitignore` porque contiene datos personales y hashes de contraseñas.

```bash
.venv/bin/python manage.py convertir_legacy datos/legacy/sia_legacy.json datos/fixtures/sia.json
.venv/bin/python manage.py loaddata datos/fixtures/sia.json
.venv/bin/python manage.py normalizar_datos
```

`datos/legacy/sia_legacy.json` combina los volcados de `_misc/json*` (se eliminaron del repositorio), tomando la
versión más reciente de cada modelo. Qué hace la conversión:

- Los ~2,200 "usuarios" legacy se vuelven **Personas**. Solo ~60 son **cuentas** (quienes iniciaron sesión, el
  personal académico y los dueños de registros); conservan su contraseña y quedan en el grupo Académicos.
- Se fusionan catálogos duplicados: `Institucion` + `InstitucionSimple` + `Dependencia` → `Institucion`;
  `Evento` + `EventoDifusion` + `EventoDivulgacion` → `Evento`; `Revista` + `RevistaDivulgacion` → `Revista`;
  programas de licenciatura, maestría y doctorado → `ProgramaAcademico`.
- Se fusionan modelos equivalentes: licenciatura/maestría/doctorado → `Grado`; los tres tipos de movilidad →
  `MovilidadAcademica`; apoyos técnicos y otras actividades → `ApoyoInstitucional`.
- Se omiten las 25 reseñas (el modelo ya no existía en el código legacy) y el proyecto marcador "Ninguno".

`normalizar_datos` (idempotente) separa dependencias de su institución padre ("Facultad de Ciencias, UNAM"),
recalcula el ámbito nacional/internacional a partir del país, limpia los DOIs y pasa el factor de impacto capturado en
cada artículo a las métricas por año de su revista.

Las cuentas se identifican por correo electrónico (no hay nombre de usuario). Las cuentas legacy sin correo reciben
uno provisional `…@sin-correo.invalid`, que un administrador debe reemplazar por el real desde *Usuarios*.

Los nombres de las personas se convierten al formato de cita (`Pérez García, J. C.`). Para las que tengan ORCID,
`completar_orcid` propone el nombre de su registro público (`--aplicar` para guardarlo):

```bash
.venv/bin/python manage.py completar_orcid
```

## Funciones para la operación diaria

- **Sin fecha**: las fechas son obligatorias; si no se conoce, se captura 01/01/1900 (o cualquier fecha anterior,
  que se guarda igual) y se muestra «s.f.» en el CV y los informes, sin caer en ningún año.
- **Fechas dudosas**: `revisar_fechas` busca fechas imposibles (años como 1925 o 2916) y las corrige de la más a la
  menos segura: fecha de Crossref para publicaciones (también las que están «sin fecha»), año mal tecleado
  (2916 → 2016), evento de un día, o «sin fecha». Sin `--aplicar` solo informa; al aplicar, el motivo queda en el
  historial.

- **Mi perfil** (menú principal): cada quien ajusta sus datos personales, su nombre en publicaciones, ORCID y
  perfil académico, sin ver grupos ni permisos (aunque sea administrador), y cambia su contraseña. Debajo están su
  **formación académica** y **experiencia profesional**, que se agregan y editan desde ahí (y ya no aparecen en el
  menú de los académicos).

- **Nombre en publicaciones**: cada persona tiene un solo *nombre para mostrar* en formato de cita
  (`Pérez García, J. C.`), que es también su orden alfabético. Si se captura su ORCID y no el nombre, el nombre se
  toma del registro público de ORCID; si falta el ORCID, se busca en ORCID por el correo (si la persona lo hizo público).
- **Alta de cuentas**: la cuenta se liga a su persona por el ORCID: si ya está en el catálogo se usa esa; si no, se
  crea con el nombre de ORCID o, sin ORCID, con el nombre y el correo de la cuenta. Si hay coautores con nombre
  parecido y sin ORCID, se pregunta si es alguno, para que la cuenta conserve su producción.
- **Perfil**: el académico ajusta su nombre para mostrar y captura su ORCID. Si un administrador captura un ORCID que
  ya tiene otra persona sin cuenta (p. ej. un coautor importado), se fusiona con la de la cuenta.

- **Captura asistida**: en *Artículos científicos → Importar* se llena el alta desde un DOI (Crossref), un BibTeX o
  la lista de obras de un ORCID. Los autores se reconocen en el catálogo de personas, primero por su ORCID y luego
  por parecido del nombre (o se agregan al catálogo).
- **Evidencias**: cada registro de producción tiene una pestaña para adjuntar constancias o PDF (máx. 15 MB).
  Se guardan en `PRIVATE_MEDIA_ROOT` y solo las descarga quien puede ver el registro.
- **Guardar como nuevo** para duplicar registros recurrentes (p. ej. el mismo curso cada semestre) y **filtro por
  año** en las listas.
- **Validaciones**: fechas en un rango razonable, campos obligatorios según el caso (p. ej. "Otro" exige descripción,
  una tesis terminada exige fecha de examen, el programa debe ser del mismo nivel), páginas y periodos coherentes.
- **Duplicados**: al crear personas, instituciones, revistas, artículos, etc. se avisa si ya existe algo parecido.
  Los administradores tienen *Revisar duplicados* (pares probables) y la acción *Fusionar*, que reasigna todas las
  referencias al registro que se conserva.
- **Inicio**: pendientes del académico (publicaciones sin actualizar en 6 meses, tesis vencidas, perfil incompleto,
  informe por confirmar) y altas rápidas.
- **Bitácora**: cada cambio queda registrado (botón *Historial* en cada registro), con quién y qué cambió.

## Informe anual

1. Un administrador crea el **periodo de informe** (año y fecha límite) en *Periodos de informe* (menú principal, junto a *Avance de captura*).
2. Cada académico revisa **Mi informe** (lo capturado en ese año, con enlaces para corregir) y lo **confirma**.
3. Los administradores siguen el **Avance de captura** (registros y confirmación por académico) y descargan el
   **informe en Excel** (resumen de indicadores, avance y una hoja por sección sin duplicar coautorías).
4. Al **cerrar** el periodo, los académicos ya no pueden crear ni modificar registros de ese año: publicaciones
   publicadas ese año, actividades que terminaron ese año o registros fechados ese año. Los administradores sí.

## Roles y permisos

El acceso se da con grupos; el **tipo** de la cuenta (investigador, técnico académico, posdoctorante,
administrativo) describe a la persona para reportes, no lo que puede hacer.

- **Sysadmin**: superusuarios. Acceso total, incluidos grupos, permisos y otras cuentas de superusuario.
- **Administración** (personal administrativo): ve y edita la producción de todos los académicos; al editar un
  registro ajeno debe escribir el **motivo del cambio**, que queda en el historial junto con quién, cuándo y qué
  cambió. No borra producción ajena. Mantiene catálogos (corrige, fusiona duplicados), el informe anual (periodos,
  avance, confirmaciones), la configuración de la entidad y las cuentas (altas, contraseñas, ORCID), pero no asigna
  grupos ni permisos, ni edita superusuarios u otras cuentas de Administración.
- **Académicos** (investigadores, técnicos académicos y posdoctorantes): ven solo sus registros (los que tienen su
  usuario o en los que figuran como autor, responsable, tutor, etc.) y editan su perfil. Pueden ampliar los
  catálogos compartidos (instituciones, revistas, eventos, personas...). Si el registro tiene titulares con
  cuenta (autores, editores... de un libro; la cuenta de una persona), lo edita cualquiera de ellos; si no, lo edita
  cualquiera mientras nadie lo use, solo su usuario mientras lo use una sola cuenta (aunque sea en varios
  registros) y solo Administración cuando lo usan varias cuentas; Administración ve un aviso de que el cambio se
  refleja en todos los registros vinculados. Las cuentas nuevas creadas desde el admin entran a este grupo.

Los grupos se definen en `nucleo/permisos.py`: los permisos de Académicos se declaran en cada `ModelAdmin`
(`permisos_investigador`) y los de Administración se derivan del tipo de admin (catálogo o producción).

## Países

El catálogo de países es `cities_light.Country` (django-cities-light). Se llena desde el fixture
`nucleo/fixtures/paises.json`, que está en el repositorio y lo carga la migración `nucleo.0012` con ids fijos: **no se
usa** el comando de importación de GeoNames del paquete (`cities_light`), para que las llaves no cambien. Tiene los
países ISO de GeoNames con nombre en español y, sin código ISO, los que usaba el SIA anterior (Inglaterra, Gales,
Desconocido, Interamericano...; Inglaterra y Gales se unieron a Reino Unido). No se administra desde el SIA: solo se elige en los campos de país.

## Arquitectura

```
SIA/            configuración, sitio admin (Unfold), menú lateral y tablero del inicio
nucleo/         Persona/User, catálogos compartidos, bases abstractas y utilidades
  admin_base.py   PropietarioAdmin, CompartidoAdmin, CatalogoAdmin, inlines de personas ordenadas
  cv.py           CV en PDF, Word o HTML, con filtro por periodo y secciones
  documentos.py   HTML → PDF con WeasyPrint (CV y formatos)
  management/commands/convertir_legacy.py
<secciones>/    una app por sección del informe: modelos + admin
formatos/       solicitudes administrativas con descarga en PDF
locale/         traducciones al español de Unfold (no trae las suyas)
```

- **Persona vs. User**: `Persona` es cualquier persona que aparece en la producción (coautores externos,
  estudiantes, invitados); `User` es una cuenta con el perfil académico. Cada cuenta apunta a su Persona
  (`User.persona`, obligatoria, solo la cambia un administrador); desde la persona, `persona.usuario` es su cuenta,
  y los filtros de propiedad (`autores__usuario=...`) usan esa relación. Nombre y apellidos de la cuenta son el
  nombre legal para trámites; el nombre en publicaciones es el de la persona.
- **Autores ordenados**: las relaciones donde importa el orden (autores, responsables, tutores, sinodales) usan
  tablas intermedias con `orden` y se capturan como inlines que se reordenan arrastrando las filas.
- **Bases abstractas**: `EstadoPublicacion` (estado editorial y fechas), `Periodo` (fecha de inicio/fin con
  validación), `Compartido` (catálogos ampliables) y `Participante` (tablas intermedias ordenadas).

## Traducciones

Unfold no incluye traducción al español; `locale/es/LC_MESSAGES/django.po` la agrega. Si una actualización de Unfold
trae textos nuevos, agrégalos al `.po` y compílalo (`django-admin compilemessages`, requiere GNU gettext).

## Pruebas

```bash
DB_ENGINE=sqlite SECRET_KEY=pruebas .venv/bin/python manage.py test
```
