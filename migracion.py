import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SIA.settings")

django.setup()

from datetime import datetime, date
from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.conf import settings

# from autoslug import AutoSlugField
from nucleo.models import *
from apoyo_institucional.models import Comision, Representacion, CargoAcademicoAdministrativo, \
    RepresentacionOrganoColegiado, ComisionAcademica, ApoyoTecnico, ApoyoOtraActividad
from desarrollo_tecnologico.models import TipoDesarrollo, Licencia, DesarrolloTecnologico
from difusion_cientifica.models import MemoriaInExtenso, PrologoLibro, Resena, OrganizacionEventoAcademico, \
    ParticipacionEventoAcademico

from formacion_academica.models import CursoEspecializacion, Licenciatura, Maestria, Doctorado, PostDoctorado
from experiencia_laboral.models import *

from investigacion.models import ArticuloCientifico

import uuid

print("Borrando articulos")
ArticuloCientifico.objects.all().delete()

print("Borrando libros")
Libro.objects.all().delete()

print("Borrando libros")
Revista.objects.all().delete()

print("Borrando editoriales")
Editorial.objects.all().delete()

print("Borrando Eventos")
Evento.objects.all().delete()

print("Borrando Tipos Evento")
TipoEvento.objects.all().delete()

print("Borrando Tipos Evento")
TipoEvento.objects.all().delete()

print("Borrando problemas conacyt")
ProblemaNacionalConacyt.objects.all().delete()

print("Borrando Indices")
Indice.objects.all().delete()

print("Borrando Revistas")
Revista.objects.all().delete()

print("Borrando ExperienciaLaboral")
ExperienciaLaboral.objects.all().delete()

print("Borrando Cargos")
Cargo.objects.all().delete()

print("Borrando Nombramientos")
Nombramiento.objects.all().delete()
print("Borrando PostDoctorados")
PostDoctorado.objects.all().delete()
print("Borrando Doctorados")
Doctorado.objects.all().delete()
print("Borrando ProgramasDoctorado")
ProgramaDoctorado.objects.all().delete()
print("Borrando Proyectos")
Proyecto.objects.all().delete()
print("Borrando Maestrias")
Maestria.objects.all().delete()
print("Borrando ProgramaMaestria")
ProgramaMaestria.objects.all().delete()
print("Borrando Licenciatura")
Licenciatura.objects.all().delete()
print("Borrando ProgramaLicenciatura")
ProgramaLicenciatura.objects.all().delete()
print("Borrando CursoEspecializacion")
CursoEspecializacion.objects.all().delete()
print("Borrando AreaConocimiento")
AreaConocimiento.objects.all().delete()
print("Borrando Dependencia")
Dependencia.objects.all().delete()
print("Borrando Institucion")
Institucion.objects.all().delete()
print("Borrando Ciudad")
Ciudad.objects.all().delete()
print("Borrando Estado")
Estado.objects.all().delete()
print("Borrando Pais")
Pais.objects.all().delete()
print("Borrando ZonaPais")
ZonaPais.objects.all().delete()
print("Borrando User")
User.objects.all().delete()

Zonas = ('América del Norte', 'América Central', 'América del Sur', 'Antillas', 'Europa', 'Asia', 'Europa-Asia',
         'África', 'Oceanía', 'Oceano Atlántico')

for i in Zonas:
    print(i)
    z = ZonaPais(nombre=i)
    z.save()

Paises = (('México', 'Estados Unidos Mexicanos', 'MX', ZonaPais.objects.get(nombre='América del Norte').id),
          ('Abjasia', 'República de Abjasia', 'AB', ZonaPais.objects.get(nombre='Asia').id),
          ('Acrotiri y Dhekelia', 'Bases Soberanas de Acrotiri y Dhekelia', 'QM',
           ZonaPais.objects.get(nombre='Europa').id),
          ('Afganistán', 'República Islámica de Afganistán', 'AF', ZonaPais.objects.get(nombre='Asia').id),
          ('Albania', 'República de Albania', 'AL', ZonaPais.objects.get(nombre='Europa').id),
          ('Alemania', 'República Federal de Alemania', 'DE', ZonaPais.objects.get(nombre='Europa').id),
          ('Andorra', 'Principado de Andorra', 'AD', ZonaPais.objects.get(nombre='Europa').id),
          ('Angola', 'República de Angola', 'AO', ZonaPais.objects.get(nombre='África').id),
          ('Anguila', 'Anguila', 'AI', ZonaPais.objects.get(nombre='América Central').id),
          ('Antigua y Barbuda', 'Antigua y Barbuda', 'AG', ZonaPais.objects.get(nombre='Antillas').id),
          ('Arabia Saudita', 'Reino de Arabia Saudita', 'SA', ZonaPais.objects.get(nombre='Asia').id),
          ('Argelia', 'República Argelina Democrática y Popular', 'DZ', ZonaPais.objects.get(nombre='África').id),
          ('Argentina', 'República Argentina', 'AR', ZonaPais.objects.get(nombre='América del Sur').id),
          ('Armenia', 'República de Armenia', 'AM', ZonaPais.objects.get(nombre='Asia').id),
          ('Aruba', 'Aruba', 'AW', ZonaPais.objects.get(nombre='América Central').id),
          ('Australia', 'Mancomunidad de Australia', 'AU', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Austria', 'República de Austria', 'AT', ZonaPais.objects.get(nombre='Europa').id),
          ('Azawad', 'Estado Independiente del Azawad', '00', ZonaPais.objects.get(nombre='África').id),
          ('Azerbaiyán', 'República de Azerbaiyán', 'AZ', ZonaPais.objects.get(nombre='Asia').id),
          ('Bahamas', 'Mancomunidad de las Bahamas', 'BS', ZonaPais.objects.get(nombre='Antillas').id),
          ('Bangladés', 'República Popular de Bangladesh', 'BD', ZonaPais.objects.get(nombre='Asia').id),
          ('Barbados', 'Barbados', 'BB', ZonaPais.objects.get(nombre='América Central').id),
          ('Baréin', 'Reino de Baréin', 'BH', ZonaPais.objects.get(nombre='Asia').id),
          ('Bélgica', 'Reino de Bélgica', 'BE', ZonaPais.objects.get(nombre='Europa').id),
          ('Belice', 'Belice', 'BZ', ZonaPais.objects.get(nombre='América Central').id),
          ('Benín', 'República de Benín', 'BJ', ZonaPais.objects.get(nombre='África').id),
          ('Bermudas', 'Bermudas', 'BM', ZonaPais.objects.get(nombre='América del Norte').id),
          ('Bielorrusia', 'República de Bielorrusia', 'BY', ZonaPais.objects.get(nombre='Europa').id),
          ('Birmania', 'Unión de Myanmar (antes Birmania)', 'MM', ZonaPais.objects.get(nombre='Asia').id),
          ('Bolivia', 'Estado Plurinacional de Bolivia', 'BO', ZonaPais.objects.get(nombre='América del Sur').id),
          ('Bosnia y Herzegovina', 'Bosnia y Herzegovina', 'BA', ZonaPais.objects.get(nombre='Europa').id),
          ('Botsuana', 'República de Botsuana', 'BW', ZonaPais.objects.get(nombre='África').id),
          ('Brasil', 'República Federativa del Brasil', 'BR', ZonaPais.objects.get(nombre='América del Sur').id),
          ('Brunéi', 'Estado de Brunéi, Morada de la Paz', 'BN', ZonaPais.objects.get(nombre='Asia').id),
          ('Bulgaria', 'República de Bulgaria', 'BG', ZonaPais.objects.get(nombre='Europa').id),
          ('Burkina Faso', 'Burkina Faso (antes Republica del Alto Volta)', 'BF',
           ZonaPais.objects.get(nombre='África').id),
          ('Burundi', 'República de Burundi', 'BI', ZonaPais.objects.get(nombre='África').id),
          ('Bután', 'Reino de Bután', 'BT', ZonaPais.objects.get(nombre='Asia').id),
          ('Cabo Verde', 'República de Cabo Verde', 'CV', ZonaPais.objects.get(nombre='África').id),
          ('Camboya', 'Reino de Camboya', 'KH', ZonaPais.objects.get(nombre='Asia').id),
          ('Camerún', 'República de Camerún', 'CM', ZonaPais.objects.get(nombre='África').id),
          ('Canadá', 'Canadá', 'CA', ZonaPais.objects.get(nombre='América del Norte').id),
          ('Catar', 'Estado de Catar', 'QA', ZonaPais.objects.get(nombre='Asia').id),
          ('Chad', 'República del Chad', 'TD', ZonaPais.objects.get(nombre='África').id),
          ('Chile', 'República de Chile', 'CL', ZonaPais.objects.get(nombre='América del Sur').id),
          ('China', 'República Popular China', 'CN', ZonaPais.objects.get(nombre='Asia').id),
          ('Chipre', 'República de Chipre', 'CY', ZonaPais.objects.get(nombre='Europa-Asia').id),
          ('Ciudad del Vaticano', 'Estado de la Ciudad del Vaticano', 'VA', ZonaPais.objects.get(nombre='Europa').id),
          ('Colombia', 'República de Colombia', 'CO', ZonaPais.objects.get(nombre='América del Sur').id),
          ('Comoras', 'Unión de las Comoras', 'KM', ZonaPais.objects.get(nombre='África').id),
          ('Corea del Norte', 'República Popular Democrática de Corea', 'KP', ZonaPais.objects.get(nombre='Asia').id),
          ('Corea del Sur', 'República de Corea', 'KR', ZonaPais.objects.get(nombre='Asia').id),
          ('Costa de Marfil', 'República de Costa de Marfil', 'CI', ZonaPais.objects.get(nombre='África').id),
          ('Costa Rica', 'República de Costa Rica', 'CR', ZonaPais.objects.get(nombre='América Central').id),
          ('Croacia', 'República de Croacia', 'HR', ZonaPais.objects.get(nombre='Europa').id),
          ('Cuba', 'República de Cuba', 'CU', ZonaPais.objects.get(nombre='Antillas').id),
          ('Curazao', 'Curazao', 'CW', ZonaPais.objects.get(nombre='América Central').id),
          ('Dinamarca', 'Reino de Dinamarca', 'DK', ZonaPais.objects.get(nombre='Europa').id),
          ('Dominica', 'Mancomunidad de Dominica', 'DM', ZonaPais.objects.get(nombre='Antillas').id),
          ('Ecuador', 'República del Ecuador', 'EC', ZonaPais.objects.get(nombre='América del Sur').id),
          ('Egipto', 'República Árabe de Egipto', 'EG', ZonaPais.objects.get(nombre='África').id),
          ('El Salvador', 'República de El Salvador', 'SV', ZonaPais.objects.get(nombre='América Central').id),
          ('Emiratos Árabes Unidos', 'Emiratos Árabes Unidos', 'AE', ZonaPais.objects.get(nombre='Asia').id),
          ('Eritrea', 'Estado de Eritrea', 'ER', ZonaPais.objects.get(nombre='África').id),
          ('Eslovaquia', 'República de Eslovaquia', 'SK', ZonaPais.objects.get(nombre='Europa').id),
          ('Eslovenia', 'República de Eslovenia', 'SI', ZonaPais.objects.get(nombre='Europa').id),
          ('España', 'Reino de España', 'ES', ZonaPais.objects.get(nombre='Europa').id),
          ('Estados Unidos de América', 'Estados Unidos de América', 'US',
           ZonaPais.objects.get(nombre='América del Norte').id),
          ('Estonia', 'República de Estonia', 'EE', ZonaPais.objects.get(nombre='Europa').id),
          ('Etiopía', 'República Democrática Federal de Etiopía', 'ET', ZonaPais.objects.get(nombre='África').id),
          ('Filipinas', 'República de las Filipinas', 'PH', ZonaPais.objects.get(nombre='Asia').id),
          ('Finlandia', 'República de Finlandia', 'FI', ZonaPais.objects.get(nombre='Europa').id),
          ('Fiyi', 'República de las Islas Fiyi (Fiji)', 'FJ', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Francia', 'República Francesa', 'FR', ZonaPais.objects.get(nombre='Europa').id),
          ('Gabón', 'República Gabonesa', 'GA', ZonaPais.objects.get(nombre='África').id),
          ('Gambia', 'República de la Gambia', 'GM', ZonaPais.objects.get(nombre='África').id),
          ('Georgia', 'Georgia', 'GE', ZonaPais.objects.get(nombre='Asia').id),
          ('Ghana', 'República de Ghana', 'GH', ZonaPais.objects.get(nombre='África').id),
          ('Gibraltar', 'Gibraltar', 'GI', ZonaPais.objects.get(nombre='Europa').id),
          ('Granada', 'Granada', 'GD', ZonaPais.objects.get(nombre='Antillas').id),
          ('Grecia', 'República Helénica', 'GR', ZonaPais.objects.get(nombre='Europa').id),
          ('Groenlandia', 'Groenlandia', 'GL', ZonaPais.objects.get(nombre='América del Norte').id),
          ('Guam', 'Territorio de Guam', 'GU', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Guatemala', 'República de Guatemala', 'GT', ZonaPais.objects.get(nombre='América Central').id),
          ('Guernsey', 'Bailiazgo de Guernsey', 'GF', ZonaPais.objects.get(nombre='Europa').id),
          ('Guinea', 'República de Guinea', 'GN', ZonaPais.objects.get(nombre='África').id),
          ('Guinea Ecuatorial', 'República de Guinea Ecuatorial', 'GQ', ZonaPais.objects.get(nombre='África').id),
          ('Guinea-Bissau', 'República de Guinea-Bissau', 'GW', ZonaPais.objects.get(nombre='África').id),
          ('Guyana', 'República Cooperativa de Guyana', 'GY', ZonaPais.objects.get(nombre='América del Sur').id),
          ('Haití', 'República de Haití', 'HT', ZonaPais.objects.get(nombre='Antillas').id),
          ('Honduras', 'República de Honduras', 'HN', ZonaPais.objects.get(nombre='América Central').id),
          ('Hong Kong', 'Región Administrativa Especial de Hong Kong', 'HK', ZonaPais.objects.get(nombre='Asia').id),
          ('Hungría', 'República de Hungría', 'HU', ZonaPais.objects.get(nombre='Europa').id),
          ('India', 'República de India', 'IN', ZonaPais.objects.get(nombre='Asia').id),
          ('Indonesia', 'República de Indonesia', 'ID', ZonaPais.objects.get(nombre='Asia').id),
          ('Irak', 'República de Irak', 'IQ', ZonaPais.objects.get(nombre='Asia').id),
          ('Irán', 'República Islámica de Irán', 'IR', ZonaPais.objects.get(nombre='Asia').id),
          ('Irlanda', 'República de Irlanda', 'IE', ZonaPais.objects.get(nombre='Europa').id),
          ('Isla de Man', 'Isla de Man', 'IM', ZonaPais.objects.get(nombre='Europa').id),
          ('Isla de Navidad', 'Territorio de la Isla de Navidad', 'CX', ZonaPais.objects.get(nombre='Asia').id),
          ('Isla Norfolk', 'Territorio de las Islas Norfolk', 'NF', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Islandia', 'República de Islandia', 'IS', ZonaPais.objects.get(nombre='Europa').id),
          ('Islas Caimán', 'Islas Caimán', 'KY', ZonaPais.objects.get(nombre='América Central').id),
          ('Islas Cocos', 'Islas Cocos', 'CC', ZonaPais.objects.get(nombre='Asia').id),
          ('Islas Cook', 'Islas Cook', 'CK', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Islas Feroe', 'Islas Feroe', 'FO', ZonaPais.objects.get(nombre='Europa').id),
          ('Islas Malvinas', 'Islas Malvinas', 'FK', ZonaPais.objects.get(nombre='Oceano Atlántico').id),
          ('Islas Marianas del Norte', 'Estado Libre Asociado de las Islas Marianas del Norte', 'MP',
           ZonaPais.objects.get(nombre='Oceanía').id),
          ('Islas Marshall', 'República de las Islas Marshall', 'MH', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Islas Pitcairn', 'Islas Pitcairn', 'PN', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Islas Salomón', 'Islas Salomón', 'SB', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Islas Turcas y Caicos', 'Islas Turcas y Caicos', 'TC', ZonaPais.objects.get(nombre='América Central').id),
          ('Islas Vírgenes Británicas', 'Islas Vírgenes Británicas', 'VG',
           ZonaPais.objects.get(nombre='América Central').id),
          ('Islas Vírgenes de los Estados Unidos', 'Islas Vírgenes de los Estados Unidos', 'VI',
           ZonaPais.objects.get(nombre='América Central').id),
          ('Israel', 'Estado de Israel', 'IL', ZonaPais.objects.get(nombre='Asia').id),
          ('Italia', 'República Italiana', 'IT', ZonaPais.objects.get(nombre='Europa').id),
          ('Jamaica', 'Jamaica', 'JM', ZonaPais.objects.get(nombre='Antillas').id),
          ('Japón', 'Japón', 'JP', ZonaPais.objects.get(nombre='Asia').id),
          ('Jersey', 'Bailiazgo de Jersey', 'JE', ZonaPais.objects.get(nombre='Europa').id),
          ('Jordania', 'Reino Hachemita de Jordania', 'JO', ZonaPais.objects.get(nombre='Asia').id),
          ('Kazajistán', 'República de Kazajistán', 'KZ', ZonaPais.objects.get(nombre='Asia').id),
          ('Kenia', 'República de Kenia', 'KE', ZonaPais.objects.get(nombre='África').id),
          ('Kirguistán', 'República Kirguiza', 'KG', ZonaPais.objects.get(nombre='Asia').id),
          ('Kiribati', 'República de Kiribati', 'KI', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Kosovo', 'República de Kosovo', 'XK', ZonaPais.objects.get(nombre='Europa').id),
          ('Kuwait', 'Estado de Kuwait', 'KW', ZonaPais.objects.get(nombre='Asia').id),
          ('Laos', 'República Democrática Popular Lao', 'LA', ZonaPais.objects.get(nombre='Asia').id),
          ('Lesoto', 'Reino de Lesoto', 'LS', ZonaPais.objects.get(nombre='África').id),
          ('Letonia', 'República de Letonia', 'LV', ZonaPais.objects.get(nombre='Europa').id),
          ('Líbano', 'República del Líbano', 'LB', ZonaPais.objects.get(nombre='Asia').id),
          ('Liberia', 'República de Liberia', 'LR', ZonaPais.objects.get(nombre='África').id),
          ('Libia', 'República de Libia', 'LY', ZonaPais.objects.get(nombre='África').id),
          ('Liechtenstein', 'Principado de Liechtenstein', 'LI', ZonaPais.objects.get(nombre='Europa').id),
          ('Lituania', 'República de Lituania', 'LT', ZonaPais.objects.get(nombre='Europa').id),
          ('Luxemburgo', 'Gran Ducado de Luxemburgo', 'LU', ZonaPais.objects.get(nombre='Europa').id),
          ('Macao', 'Región Administrativa Especial de Macao', 'MO', ZonaPais.objects.get(nombre='Asia').id),
          ('Macedonia', 'República de Macedonia3', 'MK', ZonaPais.objects.get(nombre='Europa').id),
          ('Madagascar', 'República de Madagascar', 'MG', ZonaPais.objects.get(nombre='África').id),
          ('Malasia', 'Federación de Malasia', 'MY', ZonaPais.objects.get(nombre='Asia').id),
          ('Malaui', 'República de Malaui', 'MW', ZonaPais.objects.get(nombre='África').id),
          ('Maldivas', 'República de las Maldivas', 'MV', ZonaPais.objects.get(nombre='Asia').id),
          ('Malí', 'República de Malí', 'ML', ZonaPais.objects.get(nombre='África').id),
          ('Malta', 'República de Malta', 'MT', ZonaPais.objects.get(nombre='Europa').id),
          ('Marruecos', 'Reino de Marruecos', 'MA', ZonaPais.objects.get(nombre='África').id),
          ('Mauricio', 'República de Mauricio', 'MU', ZonaPais.objects.get(nombre='África').id),
          ('Mauritania', 'República Islámica de Mauritania', 'MR', ZonaPais.objects.get(nombre='África').id),
          ('Micronesia', 'Estados Federados de Micronesia', 'FM', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Moldavia', 'República de Moldavia', 'MD', ZonaPais.objects.get(nombre='Europa').id),
          ('Mónaco', 'Principado de Mónaco', 'MC', ZonaPais.objects.get(nombre='Europa').id),
          ('Mongolia', 'Mongolia', 'MN', ZonaPais.objects.get(nombre='Asia').id),
          ('Montenegro', 'República de Montenegro', 'ME', ZonaPais.objects.get(nombre='Europa').id),
          ('Montserrat', 'Montserrat', 'MS', ZonaPais.objects.get(nombre='América Central').id),
          ('Mozambique', 'República de Mozambique', 'MZ', ZonaPais.objects.get(nombre='África').id),
          ('Nagorno Karabaj', 'República de Nagorno Karabaj', 'XA', ZonaPais.objects.get(nombre='Europa-Asia').id),
          ('Namibia', 'República de Namibia', 'NA', ZonaPais.objects.get(nombre='África').id),
          ('Nauru', 'República de Nauru', 'NR', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Nepal', 'República Federal Democrática de Nepal', 'NP', ZonaPais.objects.get(nombre='Asia').id),
          ('Nicaragua', 'República de Nicaragua', 'NI', ZonaPais.objects.get(nombre='América Central').id),
          ('Níger', 'República del Níger', 'NE', ZonaPais.objects.get(nombre='África').id),
          ('Nigeria', 'República Federal de Nigeria', 'NG', ZonaPais.objects.get(nombre='África').id),
          ('Niue', 'Niue', 'NU', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Noruega', 'Reino de Noruega', 'NO', ZonaPais.objects.get(nombre='Europa').id),
          ('Nueva Caledonia', 'Territorio de Nueva Caledonia y dependencias', 'NC',
           ZonaPais.objects.get(nombre='Oceanía').id),
          ('Nueva Zelanda', 'Nueva Zelanda', 'NZ', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Omán', 'Sultanato de Omán', 'OM', ZonaPais.objects.get(nombre='Asia').id),
          ('Osetia del Sur', 'República de Osetia del Sur', 'XB', ZonaPais.objects.get(nombre='Europa-Asia').id),
          ('Países Bajos / Holanda', 'Reino de los Países Bajos', 'NL', ZonaPais.objects.get(nombre='Europa').id),
          ('Pakistán', 'República Islámica de Pakistán', 'PK', ZonaPais.objects.get(nombre='Asia').id),
          ('Palaos', 'República de Palaos', 'PW', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Palestina', 'Autoridad Palestina de Cisjordania y la Franja de Gaza', 'PS',
           ZonaPais.objects.get(nombre='Asia').id),
          ('Panamá', 'República de Panamá', 'PA', ZonaPais.objects.get(nombre='América Central').id),
          ('Papúa Nueva Guinea', 'Estado Independiente de Papúa Nueva Guinea', 'PG',
           ZonaPais.objects.get(nombre='Oceanía').id),
          ('Paraguay', 'República del Paraguay', 'PY', ZonaPais.objects.get(nombre='América del Sur').id),
          ('Perú', 'República del Perú', 'PE', ZonaPais.objects.get(nombre='América del Sur').id),
          ('Polinesia Francesa', 'Polinesia Francesa', 'PF', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Polonia', 'República de Polonia', 'PL', ZonaPais.objects.get(nombre='Europa').id),
          ('Portugal', 'República Portuguesa', 'PT', ZonaPais.objects.get(nombre='Europa').id),
          ('Puerto Rico', 'Estado Libre Asociado de Puerto Rico', 'PR', ZonaPais.objects.get(nombre='Antillas').id),
          ('Reino Unido', 'Reino Unido de Gran Bretaña e Irlanda del Norte', 'GB',
           ZonaPais.objects.get(nombre='Europa').id),
          ('Republica Centroafricana', 'República Centroafricana', 'CF', ZonaPais.objects.get(nombre='África').id),
          ('Republica Checa', 'República Checa', 'CZ', ZonaPais.objects.get(nombre='Europa').id),
          ('Republica del Congo', 'República del Congo', 'CG', ZonaPais.objects.get(nombre='África').id),
          ('Republica del Norte de Chipre', 'República Turca del Norte de Chipre', 'XC',
           ZonaPais.objects.get(nombre='Europa').id),
          ('Republica Democratica del Congo', 'República Democrática del Congo', 'CD',
           ZonaPais.objects.get(nombre='África').id),
          ('República Dominicana', 'República Dominicana', 'DO', ZonaPais.objects.get(nombre='Antillas').id),
          ('Ruanda', 'República de Ruanda', 'RW', ZonaPais.objects.get(nombre='África').id),
          ('Rumania', 'Rumania', 'RO', ZonaPais.objects.get(nombre='Europa').id),
          ('Rusia', 'Federación Rusa', 'RU', ZonaPais.objects.get(nombre='Europa-Asia').id),
          ('Sahara Occidental', 'República Árabe Saharaui Democrática', 'EH', ZonaPais.objects.get(nombre='África').id),
          ('Samoa', 'Estado Independiente de Samoa', 'WS', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Samoa Americana', 'Territorio de la Samoa Americana', 'AS', ZonaPais.objects.get(nombre='Oceanía').id),
          ('San Bartolomé', 'San Bartolomé', 'BL', ZonaPais.objects.get(nombre='América Central').id),
          ('San Cristóbal y Nieves', 'Federación de San Cristóbal y Nieves', 'KN',
           ZonaPais.objects.get(nombre='Antillas').id),
          ('San Marino', 'Serenísima República de San Marino', 'SM', ZonaPais.objects.get(nombre='Europa').id),
          ('San Martín (Francia)', 'San Martín', 'MF', ZonaPais.objects.get(nombre='América Central').id),
          ('San Martín (Países Bajos)', 'Sint Maarten', 'SX', ZonaPais.objects.get(nombre='América Central').id),
          ('San Pedro y Miquelón', 'San Pedro y Miquelón', 'PM', ZonaPais.objects.get(nombre='América del Norte').id),
          ('San Vicente y las Granadinas', 'San Vicente y las Granadinas', 'VC',
           ZonaPais.objects.get(nombre='Antillas').id),
          ('Santa Elena, Ascensión y Tristán de Acuña', 'Santa Elena, Ascensión y Tristán de Acuña', 'SH',
           ZonaPais.objects.get(nombre='Oceano Atlántico').id),
          ('Santa Lucía', 'Santa Lucía', 'LC', ZonaPais.objects.get(nombre='Antillas').id),
          ('Santo Tomé y Príncipe', 'República Democrática de Santo Tomé y Príncipe', 'ST',
           ZonaPais.objects.get(nombre='África').id),
          ('Senegal', 'República de Senegal', 'SN', ZonaPais.objects.get(nombre='África').id),
          ('Serbia', 'República de Serbia', 'RS', ZonaPais.objects.get(nombre='Europa').id),
          ('Seychelles', 'República de Seychelles', 'SC', ZonaPais.objects.get(nombre='África').id),
          ('Sierra Leona', 'República de Sierra Leona', 'SL', ZonaPais.objects.get(nombre='África').id),
          ('Singapur', 'República de Singapur', 'SG', ZonaPais.objects.get(nombre='Asia').id),
          ('Siria', 'República Árabe Siria', 'SY', ZonaPais.objects.get(nombre='Asia').id),
          ('Somalia', 'Somalia', 'SO', ZonaPais.objects.get(nombre='África').id),
          ('Somalilandia', 'República de Somalilandia', 'XD', ZonaPais.objects.get(nombre='África').id),
          ('Sri Lanka', 'República Democrática Socialista de Sri Lanka', 'LK', ZonaPais.objects.get(nombre='Asia').id),
          ('Suazilandia', 'Reino de Suazilandia', 'SZ', ZonaPais.objects.get(nombre='África').id),
          ('Sudáfrica', 'República de Sudáfrica', 'ZA', ZonaPais.objects.get(nombre='África').id),
          ('Sudán', 'República del Sudán', 'SD', ZonaPais.objects.get(nombre='África').id),
          ('Sudán del Sur', 'República de Sudán del Sur', 'SS', ZonaPais.objects.get(nombre='África').id),
          ('Suecia', 'Reino de Suecia', 'SE', ZonaPais.objects.get(nombre='Europa').id),
          ('Suiza', 'Confederación Helvética', 'CH', ZonaPais.objects.get(nombre='Europa').id),
          ('Surinam', 'República de Surinam', 'SR', ZonaPais.objects.get(nombre='América del Sur').id),
          ('Svalbard', 'Svalbard y Jan Mayen', 'SJ', ZonaPais.objects.get(nombre='Europa').id),
          ('Tailandia', 'Reino de Tailandia', 'TH', ZonaPais.objects.get(nombre='Asia').id),
          ('Taiwán', 'República de China', 'TW', ZonaPais.objects.get(nombre='Asia').id),
          ('Tanzania', 'República Unida de Tanzania', 'TZ', ZonaPais.objects.get(nombre='África').id),
          ('Tayikistán', 'República de Tayikistán', 'TJ', ZonaPais.objects.get(nombre='Asia').id),
          ('Timor Oriental', 'República Democrática de Timor Oriental', 'TL', ZonaPais.objects.get(nombre='Asia').id),
          ('Togo', 'República Togolesa', 'TG', ZonaPais.objects.get(nombre='África').id),
          ('Tokelau', 'Tokelau', 'TK', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Tonga', 'Reino de Tonga', 'TO', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Transnistria', 'República Moldava Pridnestroviana', 'XE', ZonaPais.objects.get(nombre='Europa').id),
          ('Trinidad y Tobago', 'República de Trinidad y Tobago', 'TT', ZonaPais.objects.get(nombre='Antillas').id),
          ('Túnez', 'República Tunecina', 'TN', ZonaPais.objects.get(nombre='África').id),
          ('Turkmenistán', 'República de Turkmenistán', 'TM', ZonaPais.objects.get(nombre='Asia').id),
          ('Turquía', 'República de Turquía', 'TR', ZonaPais.objects.get(nombre='Europa-Asia').id),
          ('Tuvalu', 'Tuvalu', 'TV', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Ucrania', 'Ucrania', 'UA', ZonaPais.objects.get(nombre='Europa').id),
          ('Uganda', 'República de Uganda', 'UG', ZonaPais.objects.get(nombre='África').id),
          ('Uruguay', 'República Oriental del Uruguay', 'UY', ZonaPais.objects.get(nombre='América del Sur').id),
          ('Uzbekistán', 'República de Uzbekistán', 'UZ', ZonaPais.objects.get(nombre='Asia').id),
          ('Vanuatu', 'República de Vanuatu', 'VU', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Venezuela', 'República Bolivariana de Venezuela', 'VE', ZonaPais.objects.get(nombre='América del Sur').id),
          ('Vietnam', 'República Socialista de Vietnam', 'VN', ZonaPais.objects.get(nombre='Asia').id),
          ('Wallis y Futuna', 'Islas Wallis y Futuna', 'WF', ZonaPais.objects.get(nombre='Oceanía').id),
          ('Yemen', 'República del Yemen', 'YE', ZonaPais.objects.get(nombre='Asia').id),
          ('Yibuti', 'República de Yibuti', 'DJ', ZonaPais.objects.get(nombre='África').id),
          ('Zambia', 'República de Zambia', 'ZM', ZonaPais.objects.get(nombre='África').id),
          ('Zimbabue', 'República de Zimbabue', 'ZW', ZonaPais.objects.get(nombre='África').id))

for i in Paises:
    p = Pais(nombre=i[0], nombre_extendido=i[1], codigo=i[2], zona=ZonaPais(pk=i[3]))
    p.save()
    print("Agregado el país " + i[0] + " para la zona " + str(ZonaPais.objects.get(pk=i[3]).nombre))

Estados = (
    ('Aguascalientes', Pais.objects.get(nombre='México').id),
    ('Baja California', Pais.objects.get(nombre='México').id),
    ('Baja California Sur', Pais.objects.get(nombre='México').id),
    ('Campeche', Pais.objects.get(nombre='México').id),
    ('Chiapas', Pais.objects.get(nombre='México').id),
    ('Chihuahua', Pais.objects.get(nombre='México').id),
    ('Ciudad de México', Pais.objects.get(nombre='México').id),
    ('Coahuila de Zaragoza', Pais.objects.get(nombre='México').id),
    ('Colima', Pais.objects.get(nombre='México').id),
    ('Durango', Pais.objects.get(nombre='México').id),
    ('Guanajuato', Pais.objects.get(nombre='México').id),
    ('Guerrero', Pais.objects.get(nombre='México').id),
    ('Hidalgo', Pais.objects.get(nombre='México').id),
    ('Jalisco', Pais.objects.get(nombre='México').id),
    ('Estado de México', Pais.objects.get(nombre='México').id),
    ('Michoacán de Ocampo', Pais.objects.get(nombre='México').id),  # 16
    ('Morelos', Pais.objects.get(nombre='México').id),
    ('Nayarit', Pais.objects.get(nombre='México').id),
    ('Nuevo León', Pais.objects.get(nombre='México').id),
    ('Oaxaca', Pais.objects.get(nombre='México').id),
    ('Puebla', Pais.objects.get(nombre='México').id),
    ('Querétaro de Arteaga', Pais.objects.get(nombre='México').id),
    ('Quintana Roo', Pais.objects.get(nombre='México').id),
    ('San Luis Potosí', Pais.objects.get(nombre='México').id),  # 24
    ('Sinaloa', Pais.objects.get(nombre='México').id),
    ('Sonora', Pais.objects.get(nombre='México').id),
    ('Tabasco', Pais.objects.get(nombre='México').id),
    ('Tamaulipas', Pais.objects.get(nombre='México').id),
    ('Tlaxcala', Pais.objects.get(nombre='México').id),
    ('Veracruz de Ignacio de la Llave', Pais.objects.get(nombre='México').id),
    ('Yucatán', Pais.objects.get(nombre='México').id),
    ('Zacatecas', Pais.objects.get(nombre='México').id),
    ('Bogotá', Pais.objects.get(nombre='Colombia').id),
    ('Antioquia', Pais.objects.get(nombre='Colombia').id),
    ('Meta', Pais.objects.get(nombre='Colombia').id),
    ('Bern', Pais.objects.get(nombre='Suiza').id),
    ('Zúrich', Pais.objects.get(nombre='Suiza').id),
    ('Cantón de Vaud', Pais.objects.get(nombre='Suiza').id),
    ('Provincia de León', Pais.objects.get(nombre='España').id),
    ('Comunidad de Madrid', Pais.objects.get(nombre='España').id),
    ('Alicante', Pais.objects.get(nombre='España').id),
    ('Cataluña', Pais.objects.get(nombre='España').id),
    ('Andalucía', Pais.objects.get(nombre='España').id),
    ('Valencia', Pais.objects.get(nombre='España').id),
    ('Galicia', Pais.objects.get(nombre='España').id),
    ('Granada', Pais.objects.get(nombre='España').id),
    ('Aragón', Pais.objects.get(nombre='España').id),
    ('Región de Murcia', Pais.objects.get(nombre='España').id),
    ('Provincia de Macerata', Pais.objects.get(nombre='Italia').id),
    ('Trento', Pais.objects.get(nombre='Italia').id),
    ('Cerdeña', Pais.objects.get(nombre='Italia').id),
    ('Ciudad metropolitana de Roma Capital', Pais.objects.get(nombre='Italia').id),
    ('Isla de Francia', Pais.objects.get(nombre='Francia').id),
    ('Alto Garona', Pais.objects.get(nombre='Francia').id),
    ('El Cairo', Pais.objects.get(nombre='Egipto').id),
    ('Santiago', Pais.objects.get(nombre='Chile').id),
    ('Lima', Pais.objects.get(nombre='Perú').id),
    ('Viena', Pais.objects.get(nombre='Austria').id),
    ('Georgia', Pais.objects.get(nombre='Estados Unidos de América').id),
    ('Virginia', Pais.objects.get(nombre='Estados Unidos de América').id),
    ('Texas', Pais.objects.get(nombre='Estados Unidos de América').id),
    ('California', Pais.objects.get(nombre='Estados Unidos de América').id),
    ('Massachusetts', Pais.objects.get(nombre='Estados Unidos de América').id),
    ('Míchigan', Pais.objects.get(nombre='Estados Unidos de América').id),
    ('Indiana', Pais.objects.get(nombre='Estados Unidos de América').id),
    ('Nueva York', Pais.objects.get(nombre='Estados Unidos de América').id),
    ('Illinois', Pais.objects.get(nombre='Estados Unidos de América').id),
    ('Washington', Pais.objects.get(nombre='Estados Unidos de América').id),
    ('Luisiana', Pais.objects.get(nombre='Estados Unidos de América').id),
    ('Florida', Pais.objects.get(nombre='Estados Unidos de América').id),
    ('Wiltshire', Pais.objects.get(nombre='Reino Unido').id),
    ('Inglaterra', Pais.objects.get(nombre='Reino Unido').id),
    ('Caracas', Pais.objects.get(nombre='Venezuela').id),
    ('Miranda', Pais.objects.get(nombre='Venezuela').id),
    ('Loreto', Pais.objects.get(nombre='Perú').id),
    ('Leoncio Prado', Pais.objects.get(nombre='Perú').id),
    ('Montevideo', Pais.objects.get(nombre='Uruguay').id),
    ('Overijssel', Pais.objects.get(nombre='Países Bajos / Holanda').id),
    ('Holanda Septentrional', Pais.objects.get(nombre='Países Bajos / Holanda').id),
    ('Güeldres', Pais.objects.get(nombre='Países Bajos / Holanda').id),
    ('Queensland', Pais.objects.get(nombre='Australia').id),
    ('Cochabamba', Pais.objects.get(nombre='Bolivia').id),
    ('Baviera', Pais.objects.get(nombre='Alemania').id),
    ('Renania del Norte-Westfalia', Pais.objects.get(nombre='Alemania').id),
    ('Buenos Aires', Pais.objects.get(nombre='Argentina').id),
    ('Córdoba', Pais.objects.get(nombre='Argentina').id),
    ('Tucumán', Pais.objects.get(nombre='Argentina').id),
    ('Escalante', Pais.objects.get(nombre='Argentina').id),
    ('Río Negro', Pais.objects.get(nombre='Argentina').id),
    ('Mendoza', Pais.objects.get(nombre='Argentina').id),
    ('La Habana', Pais.objects.get(nombre='Cuba').id),
    ('Sinkiang', Pais.objects.get(nombre='China').id),
    ('Hokkaido', Pais.objects.get(nombre='Japón').id),
    ('Vancouver', Pais.objects.get(nombre='Canadá').id),
    ('Quebec', Pais.objects.get(nombre='Canadá').id),
    ('Minas Gerais', Pais.objects.get(nombre='Brasil').id),
    ('Bahía', Pais.objects.get(nombre='Brasil').id),
    ('Espírito Santo', Pais.objects.get(nombre='Brasil').id),
    ('Provincia Occidental del Cabo', Pais.objects.get(nombre='Sudáfrica').id),
    ('Praia', Pais.objects.get(nombre='Cabo Verde').id),
    ('Akershus', Pais.objects.get(nombre='Noruega').id),
    ('Francisco Morazán', Pais.objects.get(nombre='Honduras').id),
    ('Minho', Pais.objects.get(nombre='Portugal').id),
    ('Guatemala', Pais.objects.get(nombre='Guatemala').id),
    ('Dar es-Salam', Pais.objects.get(nombre='Tanzania').id),
    ('Santa Cruz', Pais.objects.get(nombre='Argentina').id),
    ('Witney', Pais.objects.get(nombre='Reino Unido').id),
    ('Luxemburgo', Pais.objects.get(nombre='Luxemburgo').id),
    ('Cambridgeshire', Pais.objects.get(nombre='Reino Unido').id),
    ('Baden-Wurtemberg', Pais.objects.get(nombre='Alemania').id),
    ('Oxfordshire', Pais.objects.get(nombre='Reino Unido').id),
    ('Provincia de Estocolmo', Pais.objects.get(nombre='Suecia').id),
)

for i in Estados:
    e = Estado(nombre=i[0], pais=Pais(pk=i[1]))
    e.save()

    print("Agregado el estado " + i[0] + " para el país " + str(Pais.objects.get(pk=i[1]).nombre))

Ciudades = (
    ('Morelia', Estado.objects.get(nombre='Michoacán de Ocampo').id),
    ('Áporo', Estado.objects.get(nombre='Michoacán de Ocampo').id),
    ('Huetamo', Estado.objects.get(nombre='Michoacán de Ocampo').id),
    ('Tingambato', Estado.objects.get(nombre='Michoacán de Ocampo').id),
    ('Zamora', Estado.objects.get(nombre='Michoacán de Ocampo').id),
    ('Uruapan', Estado.objects.get(nombre='Michoacán de Ocampo').id),
    ('El Rosario', Estado.objects.get(nombre='Michoacán de Ocampo').id),
    ('Tacámbaro', Estado.objects.get(nombre='Michoacán de Ocampo').id),
    ('Ciudad Hidalgo', Estado.objects.get(nombre='Michoacán de Ocampo').id),
    ('Puruándiro', Estado.objects.get(nombre='Michoacán de Ocampo').id),
    ('Taretan', Estado.objects.get(nombre='Michoacán de Ocampo').id),
    ('Morelos', Estado.objects.get(nombre='Michoacán de Ocampo').id),
    ('Ciudad de México, CDMX', Estado.objects.get(nombre='Ciudad de México').id),
    ('Texcoco de Mora', Estado.objects.get(nombre='Estado de México').id),
    ('Naucalpan de Juárez', Estado.objects.get(nombre='Estado de México').id),
    ('Toluca', Estado.objects.get(nombre='Estado de México').id),
    ('El Batán', Estado.objects.get(nombre='Estado de México').id),
    ('Chetumal', Estado.objects.get(nombre='Quintana Roo').id),
    ('Cozumel', Estado.objects.get(nombre='Quintana Roo').id),
    ('Guadalajara', Estado.objects.get(nombre='Jalisco').id),
    ('Monterrey', Estado.objects.get(nombre='Nuevo León').id),
    ('Bogotá D.C.', Estado.objects.get(nombre='Bogotá').id),
    ('Bern', Estado.objects.get(nombre='Bern').id),
    ('León', Estado.objects.get(nombre='Provincia de León').id),
    ('Madrid', Estado.objects.get(nombre='Comunidad de Madrid').id),
    ('Recanati', Estado.objects.get(nombre='Provincia de Macerata').id),
    ('León', Estado.objects.get(nombre='Guanajuato').id),
    ('Guanajuato', Estado.objects.get(nombre='Guanajuato').id),
    ('París', Estado.objects.get(nombre='Isla de Francia').id),
    ('El Cairo', Estado.objects.get(nombre='El Cairo').id),
    ('Ciudad Juárez', Estado.objects.get(nombre='Chihuahua').id),
    ('San Luis Potosí', Estado.objects.get(nombre='San Luis Potosí').id),
    ('Santiago', Estado.objects.get(nombre='Santiago').id),
    ('Xalapa', Estado.objects.get(nombre='Veracruz de Ignacio de la Llave').id),
    ('Lima', Estado.objects.get(nombre='Lima').id),
    ('Camerino', Estado.objects.get(nombre='Provincia de Macerata').id),
    ('Viena', Estado.objects.get(nombre='Viena').id),
    ('Washington, D.C.', Estado.objects.get(nombre='Virginia').id),
    ('Blacksburg', Estado.objects.get(nombre='Virginia').id),
    ('Arlington', Estado.objects.get(nombre='Texas').id),
    ('College Station', Estado.objects.get(nombre='Texas').id),
    ('Swindon', Estado.objects.get(nombre='Wiltshire').id),
    ('Pichátaro', Estado.objects.get(nombre='Michoacán de Ocampo').id),
    ('La Piedad de Cabadas', Estado.objects.get(nombre='Michoacán de Ocampo').id),
    ('Caracas', Estado.objects.get(nombre='Caracas').id),
    ('Londres', Estado.objects.get(nombre='Inglaterra').id),
    ('Pátzcuaro', Estado.objects.get(nombre='Michoacán de Ocampo').id),
    ('Apatzingán de la Constitución', Estado.objects.get(nombre='Michoacán de Ocampo').id),
    ('Ciudad de Iquitos', Estado.objects.get(nombre='Loreto').id),
    ('Tingo María', Estado.objects.get(nombre='Leoncio Prado').id),
    ('Mérida', Estado.objects.get(nombre='Yucatán').id),
    ('Ciudad Victoria', Estado.objects.get(nombre='Tamaulipas').id),
    ('Montevideo', Estado.objects.get(nombre='Montevideo').id),
    ('Mexicali', Estado.objects.get(nombre='Baja California').id),
    ('Davis', Estado.objects.get(nombre='California').id),
    ('Redlands', Estado.objects.get(nombre='California').id),
    ('Medellín', Estado.objects.get(nombre='Antioquia').id),
    ('Norfolk', Estado.objects.get(nombre='Inglaterra').id),
    ('Enschede', Estado.objects.get(nombre='Overijssel').id),
    ('Buenos Aires', Estado.objects.get(nombre='Buenos Aires').id),
    ('La Plata', Estado.objects.get(nombre='Buenos Aires').id),
    ('Brisbane', Estado.objects.get(nombre='Queensland').id),
    ('Bellaterra', Estado.objects.get(nombre='Cataluña').id),
    ('Barcelona', Estado.objects.get(nombre='Cataluña').id),
    ('Lérida', Estado.objects.get(nombre='Cataluña').id),
    ('Aguascalientes', Estado.objects.get(nombre='Aguascalientes').id),
    ('Wayland', Estado.objects.get(nombre='Massachusetts').id),
    ('Cambridge', Estado.objects.get(nombre='Cambridgeshire').id),
    ('Norcross', Estado.objects.get(nombre='Georgia').id),
    ('Tepic', Estado.objects.get(nombre='Nayarit').id),
    ('Boston', Estado.objects.get(nombre='Massachusetts').id),
    ('Bloomington', Estado.objects.get(nombre='Indiana').id),
    ('Cochabamba', Estado.objects.get(nombre='Cochabamba').id),
    ('Zúrich', Estado.objects.get(nombre='Zúrich').id),
    ('Ann Arbor', Estado.objects.get(nombre='Míchigan').id),
    ('Wurzburgo', Estado.objects.get(nombre='Baviera').id),
    ('San Vicente del Raspeig', Estado.objects.get(nombre='Alicante').id),
    ('Nueva York', Estado.objects.get(nombre='Nueva York').id),
    ('Hermosillo', Estado.objects.get(nombre='Sonora').id),
    ('Heroica Guaymas de Zaragoza', Estado.objects.get(nombre='Sonora').id),
    ('San Miguel de Tucumán', Estado.objects.get(nombre='Tucumán').id),
    ('Cádiz', Estado.objects.get(nombre='Andalucía').id),
    ('Sevilla', Estado.objects.get(nombre='Andalucía').id),
    ('La Habana', Estado.objects.get(nombre='La Habana').id),
    ('Toulouse', Estado.objects.get(nombre='Alto Garona').id),
    ('Valencia', Estado.objects.get(nombre='Valencia').id),
    ('Albuixech', Estado.objects.get(nombre='Valencia').id),
    ('Brístol', Estado.objects.get(nombre='Inglaterra').id),
    ('Córdoba', Estado.objects.get(nombre='Córdoba').id),
    ('Urumchi', Estado.objects.get(nombre='Sinkiang').id),
    ('La Paz', Estado.objects.get(nombre='Baja California Sur').id),
    ('Santiago de Querétaro', Estado.objects.get(nombre='Querétaro de Arteaga').id),
    ('Evanston', Estado.objects.get(nombre='Illinois').id),
    ('Urbana-Champaign', Estado.objects.get(nombre='Illinois').id),
    ('Sapporo', Estado.objects.get(nombre='Hokkaido').id),
    ('Santiago de Compostela', Estado.objects.get(nombre='Galicia').id),
    ('West Point Grey', Estado.objects.get(nombre='Vancouver').id),
    ('Campeche', Estado.objects.get(nombre='Campeche').id),
    ('San Cristóbal de las Casas', Estado.objects.get(nombre='Chiapas').id),
    ('Tuxtla Gutiérrez', Estado.objects.get(nombre='Chiapas').id),
    ('Belo Horizonte', Estado.objects.get(nombre='Minas Gerais').id),
    ('Feira de Santana', Estado.objects.get(nombre='Bahía').id),
    ('Granada', Estado.objects.get(nombre='Granada').id),
    ('Culiacán Rosales', Estado.objects.get(nombre='Sinaloa').id),
    ('Ámsterdam', Estado.objects.get(nombre='Holanda Septentrional').id),
    ('Trento', Estado.objects.get(nombre='Trento').id),
    ('Austin', Estado.objects.get(nombre='Texas').id),
    ('Murcia', Estado.objects.get(nombre='Región de Murcia').id),
    ('Comodoro Rivadavia', Estado.objects.get(nombre='Escalante').id),
    ('Viedma', Estado.objects.get(nombre='Río Negro').id),
    ('Roma', Estado.objects.get(nombre='Ciudad metropolitana de Roma Capital').id),
    ('Gland', Estado.objects.get(nombre='Cantón de Vaud').id),
    ('Pullman', Estado.objects.get(nombre='Washington').id),
    ('Ciudad del Cabo', Estado.objects.get(nombre='Provincia Occidental del Cabo').id),
    ('Quebec', Estado.objects.get(nombre='Quebec').id),
    ('Nueva Orleans', Estado.objects.get(nombre='Luisiana').id),
    ('Praia', Estado.objects.get(nombre='Praia').id),
    ('Cagliari', Estado.objects.get(nombre='Cerdeña').id),
    ('Pula', Estado.objects.get(nombre='Cerdeña').id),
    ('Oslo', Estado.objects.get(nombre='Akershus').id),
    ('Cuernavaca', Estado.objects.get(nombre='Morelos').id),
    ('Chilpancingo de los Bravo', Estado.objects.get(nombre='Guerrero').id),
    ('Bonn', Estado.objects.get(nombre='Renania del Norte-Westfalia').id),
    ('Gainesville', Estado.objects.get(nombre='Florida').id),
    ('Tegucigalpa', Estado.objects.get(nombre='Francisco Morazán').id),
    ('Puebla de Zaragoza', Estado.objects.get(nombre='Puebla').id),
    ('Villavicencio', Estado.objects.get(nombre='Meta').id),
    ('Mendoza', Estado.objects.get(nombre='Mendoza').id),
    ('Vitória', Estado.objects.get(nombre='Espírito Santo').id),
    ('Braga', Estado.objects.get(nombre='Minho').id),
    ('Ciudad de Guatemala', Estado.objects.get(nombre='Guatemala').id),
    ('Los Salias', Estado.objects.get(nombre='Miranda').id),
    ('Dar es-Salam', Estado.objects.get(nombre='Dar es-Salam').id),
    ('Berkeley', Estado.objects.get(nombre='California').id),
    ('Wageningen', Estado.objects.get(nombre='Güeldres').id),
    ('Tlaxcala de Xicohténcatl', Estado.objects.get(nombre='Tlaxcala').id),
    ('Zaragoza', Estado.objects.get(nombre='Aragón').id),
    ('Río Gallegos', Estado.objects.get(nombre='Santa Cruz').id),
    ('Long Hanborough', Estado.objects.get(nombre='Witney').id),
    ('Luxemburgo', Estado.objects.get(nombre='Luxemburgo').id),
    ('Stuttgart', Estado.objects.get(nombre='Baden-Wurtemberg').id),
    ('Oxford', Estado.objects.get(nombre='Oxfordshire').id),
    ('Estocolmo', Estado.objects.get(nombre='Provincia de Estocolmo').id),
)

for i in Ciudades:
    c = Ciudad(nombre=i[0], estado=Estado(pk=i[1]))
    c.save()
    print("Agregada la ciudad " + i[0] + "para el estado " + str(Estado.objects.get(pk=i[1]).nombre))

Instituciones = (
    ('Universidad Nacional Autónoma de México (UNAM)', Pais.objects.get(nombre='México').id,
     [
         ('Universidad Nacional Autónoma de México (UNAM)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Universidad Nacional Autónoma de México, Campus Morelia (UNAM Morelia)',
          Ciudad.objects.get(nombre='Morelia').id),
         ('Unidad Académica de Geografía, Morelia (UNAM Morelia)', Ciudad.objects.get(nombre='Morelia').id),
         ('Centro de Investigaciones en Geografía Ambiental (CIGA)', Ciudad.objects.get(nombre='Morelia').id),
         ('Dirección General de Cooperación e Internacionalización (DGECI)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Instituto de Investigaciones en Ecosistemas y Sustentabilidad (IIES)',
          Ciudad.objects.get(nombre='Morelia').id),
         ('Centro de Ciencias de la Atmósfera', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Centro Regional de Investigaciones Multidisciplinarias (CRIM)', Ciudad.objects.get(nombre='Cuernavaca').id),
         ('Unidad de Posgrado', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Escuela Nacional de Estudios Superiores, Unidad Morelia (ENES Morelia)',
          Ciudad.objects.get(nombre='Morelia').id),
         ('Escuela Nacional de Estudios Superiores, Unidad León (ENES León)',
          Ciudad.objects.filter(nombre='León', estado=Estado.objects.get(nombre='Guanajuato').id)[0].id),
         ('Instituto de Biología', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Instituto de Ecología', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Instituto de Investigaciones Antropológicas', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Instituto de Investigaciones Filológicas', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Instituto de Geografía', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Instituto de Geología', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Instituto de Geofísica', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Instituto de Geofísica, Unidad Morelia (UNAM Morelia)', Ciudad.objects.get(nombre='Morelia').id),
         ('Instituto de Geografía, Unidad Morelia (UNAM Morelia)', Ciudad.objects.get(nombre='Morelia').id),
         ('Colegio de Geografía', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Consejo Académico de Área en Ciencias Sociales (CAACS)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Facultad de Ciencias', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Facultad de Filosofía y Letras', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Facultad de Arquitectura', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Facultad de Ciencias Políticas y Sociales', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Facultad de Economía', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Facultad de Ingeniería', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Facultad de Medicina Veterinaria y Zootecnia', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Programa de Apoyo a Proyectos de Investigación e Innovación Tecnológica (PAPIIT)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Dirección General Asuntos del Personal Académico (DGAPA)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Posgrado en Geografia', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Laboratorio de Edafología "Nicolás Aguilera"', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Dirección General de Bibiotecas (DGB)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Programa de Actualización y Superación Docente (PASD)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Dirección General de Planeación', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Secretaría de Desarrollo Institucional (SDI)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Consejo Técnico de la Investigación Científica (CIC-CTIC)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Colegio de Historia', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Laboratorio de Análisis Físicos y Químicos del Ambiente (LAFQA)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Colegio de Geografia (Facultad de Filosofía y Letras)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
     ]
     ),

    ('Universidad Michoacana de San Nicolás de Hidalgo (UMSNH)', Pais.objects.get(nombre='México').id,
     [
         ('Universidad Michoacana de San Nicolás de Hidalgo (UMSNH)', Ciudad.objects.get(nombre='Morelia').id),
         ('Instituto de Investigaciones Económicas y Empresariales (ININEE)', Ciudad.objects.get(nombre='Morelia').id),
         ('Instituto de Investigaciones Históricas', Ciudad.objects.get(nombre='Morelia').id),
         ('Instituto de Investigaciones en Ciencias de la Tierra', Ciudad.objects.get(nombre='Morelia').id),
         ('Coordinación de la Investigación Científica (CIC)', Ciudad.objects.get(nombre='Morelia').id),
         ('Facultad de Ingeniería Eléctrica (FIE)', Ciudad.objects.get(nombre='Morelia').id),
         ('Facultad de Filosofía "Samuel Ramos"', Ciudad.objects.get(nombre='Morelia').id),
         ('Facultad de Economía "Vasco de Quiroga"', Ciudad.objects.get(nombre='Morelia').id),
         ('Facultad de Ingeniería Eléctrica', Ciudad.objects.get(nombre='Morelia').id),
         ('Facultad de Biología', Ciudad.objects.get(nombre='Morelia').id),
         ('Escuela de Ciencias Agropecuarias', Ciudad.objects.get(nombre='Apatzingán de la Constitución').id)
     ]
     ),

    ('Universidad de Camerino', Pais.objects.get(nombre='Italia').id,
     [
         ('Departamento de Geobotánica', Ciudad.objects.get(nombre='Camerino').id),
         ('Braun Blanquetia', Ciudad.objects.get(nombre='Camerino').id)
     ]
     ),

    ('Universidad Nacional de Colombia', Pais.objects.get(nombre='Colombia').id,
     [
         ('Universidad Nacional de Colombia', Ciudad.objects.get(nombre='Bogotá D.C.').id),
         ('Universidad Nacional de Colombia Sede Medellín', Ciudad.objects.get(nombre='Medellín').id),
         ('Instituto de Ciencias Naturales', Ciudad.objects.get(nombre='Bogotá D.C.').id),
         ('Caldasia', Ciudad.objects.get(nombre='Bogotá D.C.').id),
         ('Facultad de Minas', Ciudad.objects.get(nombre='Bogotá D.C.').id)
     ]
     ),

    ('Universidad Intercultural Indígena de Michoacán (UIIM)', Pais.objects.get(nombre='México').id,
     [
         ('UIIM Sede Pichátaro', Ciudad.objects.get(nombre='Pichátaro').id),
         ('UIIM Unidad Académica Purépecha', Ciudad.objects.get(nombre='Pátzcuaro').id)
     ]
     ),

    ('University of Bern', Pais.objects.get(nombre='Suiza').id,
     [('Mountain Research and Development', Ciudad.objects.get(nombre='Bern').id)]),

    ('Universidad de León', Pais.objects.get(nombre='España').id,
     [
         ('Universidad de León',
          Ciudad.objects.filter(nombre='León', estado=Estado.objects.get(nombre='Provincia de León'))[0].id)
     ]
     ),

    ('Universidad Complutense de Madrid', Pais.objects.get(nombre='España').id,
     [('Universidad Complutense de Madrid', Ciudad.objects.get(nombre='Madrid').id)]),

    ('Consejo Nacional de Ciencia y Tecnología (CONACYT)', Pais.objects.get(nombre='México').id,
     [
         ('Consejo Nacional de Ciencia y Tecnología (CONACYT)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Fomento Regional para el Desarrollo Científico, Tecnológico y de Innovación (FORDECYT)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Innovate UK - CONACYT', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)
     ]
     ),

    ('Gobierno de la República Mexicana', Pais.objects.get(nombre='México').id,
     [
         ('Secretaría de Desarrollo Social (SEDESOL)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Comisión Nacional Para el Conocimiento y Uso de la Biodiversidad (CONABIO)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Comisión Nacional de Áreas Naturales Portegidas (CONANP)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Comisión Nacional de Vivienda (CONAVI)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Comisión Nacional Forestal (CONAFOR)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Comisión Nacional del Agua (CONAGUA)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Consejo Nacional de Población (CONAPO)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Secretaría de Relaciones Exteriores (SRE)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Dirección General de Desarrollo Institucional y Promoción',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Dirección de Manejo Integral de Cuencas Hídricas', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Dirección General de Educación Tecnológica Agropecuaria (DGTA)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Secretaría de Educación Pública (SEP)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Petróleos Mexicanos (PEMEX)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Secretaría de Comunicaciones y Transportes (SCT)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Secretaría de Gobernación (SEGOB)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)
     ]
     ),

    ('Gobierno del Estado de Michoacán de Ocampo', Pais.objects.get(nombre='México').id,
     [
         ('Gobierno del Estado de Michoacán de Ocampo', Ciudad.objects.get(nombre='Morelia').id),
         ('Secretaría de Innovación, Ciencia y Desarrollo Tecnológico (SICDET)',
          Ciudad.objects.get(nombre='Morelia').id),
         ('Consejo Estatal de Ciencia y Tecnología (CECTI)', Ciudad.objects.get(nombre='Morelia').id),
         ('Centro Estatal para el Desarrollo Municipal (CEDEMUN)', Ciudad.objects.get(nombre='Morelia').id),
         ('Secretaría de Urbanismo y Medio Ambiente', Ciudad.objects.get(nombre='Morelia').id),
         ('Centro Estatal de Tecnologías de Información y Comunicaciones (CETIC)',
          Ciudad.objects.get(nombre='Morelia').id),
         ('Universidad Tecnológica de Morelia (UTM)', Ciudad.objects.get(nombre='Morelia').id),
         ('Secretaria de Educación en el Estado de Michoacán de Ocampo (SEE Michoacán)',
          Ciudad.objects.get(nombre='Morelia').id),
         ('Universidad Virtual del Estado de Michoacán (UNIVIM)', Ciudad.objects.get(nombre='Morelia').id),
         ('Coordinación General de Gabinete y Planeación (CPLADE)', Ciudad.objects.get(nombre='Morelia').id),
         ('Telebachillerato Michoacán', Ciudad.objects.get(nombre='Morelia').id)
     ]
     ),

    ('Organización de las Naciones Unidas para la Educación, la Ciencia y la Cultura (UNESCO)',
     Pais.objects.get(nombre='Francia').id, [(
        'Organización de las Naciones Unidas para la Educación, la Ciencia y la Cultura (UNESCO)',
        Ciudad.objects.get(nombre='París').id)]),

    ('El Colegio de Michoacán, A.C. (COLMICH)', Pais.objects.get(nombre='México').id,
     [('El Colegio de Michoacán, A.C. (COLMICH)', Ciudad.objects.get(nombre='La Piedad de Cabadas').id)]),

    ('Interciencia, Revista de Ciencia y Tecnología de América Latina', Pais.objects.get(nombre='Venezuela').id,
     [('Interciencia, Revista de Ciencia y Tecnología de América Latina', Ciudad.objects.get(nombre='Caracas').id)]),

    ('Hindawi Publishing Corporation', Pais.objects.get(nombre='Reino Unido').id,
     [('Advances in Meteorology', Ciudad.objects.get(nombre='Londres').id)]),

    ('Universidad Autónoma de Ciudad Juárez', Pais.objects.get(nombre='México').id,
     (
         ('Instituto de Arquitectura, Diseño y Arte', Ciudad.objects.get(nombre='Ciudad Juárez').id),
         ('Departamento. de Arquitectura', Ciudad.objects.get(nombre='Ciudad Juárez').id),
         ('Programa Académico de Geoinformática', Ciudad.objects.get(nombre='Ciudad Juárez').id)
     )
     ),

    ('Universidad Valladolid', Pais.objects.get(nombre='México').id,
     [('Instituto Valladolid Preparatoria', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Instituto Tecnológico de Morelia (ITM)', Pais.objects.get(nombre='México').id,
     (
         ('Instituto Tecnológico de Morelia (ITM)', Ciudad.objects.get(nombre='Morelia').id),
         ('Departamento de Sistemas y Computación', Ciudad.objects.get(nombre='Morelia').id)
     )
     ),

    ('Universidad Autónoma de San Luis Potosí', Pais.objects.get(nombre='México').id,
     [('Universidad Autónoma de San Luis Potosí', Ciudad.objects.get(nombre='San Luis Potosí').id)]),

    ('Pontificia Universidad Católica de Chile', Pais.objects.get(nombre='Chile').id,
     (
         ('Pontificia Universidad Católica de Chile', Ciudad.objects.get(nombre='Santiago').id),
         ('Comisión Nacional de Acreditación', Ciudad.objects.get(nombre='Santiago').id)
     )
     ),

    ('Instituto de Ecología, A.C. (INECOL)', Pais.objects.get(nombre='México').id,
     [('Instituto de Ecología, A.C. (INECOL)', Ciudad.objects.get(nombre='Xalapa').id)]),

    ('Red Mexicana de Cuencas Hidrográficas', Pais.objects.get(nombre='México').id,
     [('Red Mexicana de Cuencas Hidrográficas', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Universidad Agraria de la Selva', Pais.objects.get(nombre='Perú').id,
     [('Revista Investigación y Amazonía', Ciudad.objects.get(nombre='Tingo María').id)]),

    ('Instituto de Investigaciones de la Amazonía Peruana', Pais.objects.get(nombre='Perú').id,
     [('Instituto de Investigaciones de la Amazonía Peruana', Ciudad.objects.get(nombre='Lima').id)]),

    ('Asociación Española de Fitosociología (AEFA)', Pais.objects.get(nombre='España').id,
     (
         ('Global Geobotany', Ciudad.objects.get(nombre='Madrid').id),
         ('International Journal of Geobotanical Research', Ciudad.objects.get(nombre='Madrid').id)
     )
     ),

    ('Austrian Development Cooperation (ADC)', Pais.objects.get(nombre='Austria').id,
     [('APPEAR', Ciudad.objects.get(nombre='Viena').id)]),

    ('National Geographic Society (NGS)', Pais.objects.get(nombre='Estados Unidos de América').id,
     [('National Geographic Society (NGS)', Ciudad.objects.get(nombre='Washington, D.C.').id)]),

    ('National Science Foundation (NSF)', Pais.objects.get(nombre='Estados Unidos de América').id,
     [('National Science Foundation (NSF)', Ciudad.objects.get(nombre='Arlington').id)]),

    ('National Environmental Research Council (NERC)', Pais.objects.get(nombre='Reino Unido').id,
     [('National Environmental Research Council (NERC)', Ciudad.objects.get(nombre='Swindon').id)]),

    ('Gobierno del Estado de Yucatán', Pais.objects.get(nombre='México').id,
     [('Fondo Mixto Conacyt-Gobierno del Estado de Yucatán (FOMIX)', Ciudad.objects.get(nombre='Mérida').id)]),

    ('Universidad Autónoma de Tamaulipas', Pais.objects.get(nombre='México').id,
     (
         ('Universidad Autonoma de Tamaulipas', Ciudad.objects.get(nombre='Ciudad Victoria').id),
         ('Instituto de Ecología Aplicada', Ciudad.objects.get(nombre='Ciudad Victoria').id)
     )
     ),

    ('Agencia Nacional de Investigación e Innovación de Uruguay (ANII)', Pais.objects.get(nombre='Uruguay').id,
     [('Fondo María Viñas', Ciudad.objects.get(nombre='Montevideo').id)]),

    ('Universidad Autónoma de Baja California', Pais.objects.get(nombre='México').id,
     [('Universidad Autónoma de Baja California', Ciudad.objects.get(nombre='Mexicali').id)]),

    ('Universidad de California Davis', Pais.objects.get(nombre='Estados Unidos de América').id,
     [('Universidad de California Davis', Ciudad.objects.get(nombre='Davis').id)]),

    ('Universidad de Antioquia', Pais.objects.get(nombre='Colombia').id,
     [('Universidad de Antioquia', Ciudad.objects.get(nombre='Medellín').id)]),

    ('University of East Anglia', Pais.objects.get(nombre='Reino Unido').id,
     [('University of East Anglia', Ciudad.objects.get(nombre='Norfolk').id)]),

    ('Universidad París 1 Panteón-Sorbona', Pais.objects.get(nombre='Francia').id,
     [('Universidad París 1 Panteón-Sorbona', Ciudad.objects.get(nombre='París').id)]),

    ('Universidad Northwestern', Pais.objects.get(nombre='Estados Unidos de América').id,
     [('Universidad Northwestern', Ciudad.objects.get(nombre='Evanston').id)]),

    ('University of Twente', Pais.objects.get(nombre='Países Bajos / Holanda').id,
     (
         ('University of Twente', Ciudad.objects.get(nombre='Enschede').id),
         ('International Institute for Geo-Information Sciences and Earth Observation (ITC)',
          Ciudad.objects.get(nombre='Enschede').id),
         ('Faculty of Geo-Information Science and Earth Observation (ITC)', Ciudad.objects.get(nombre='Enschede').id),
         ('Department of Governance and Technology for Sustainability (CSTM)', Ciudad.objects.get(nombre='Enschede').id)
     )
     ),

    ('Universidad Autónoma de Madrid', Pais.objects.get(nombre='España').id,
     [('Universidad Autónoma de Madrid', Ciudad.objects.get(nombre='Madrid').id)]),

    ('Universidad de Buenos Aires (UBA)', Pais.objects.get(nombre='Argentina').id,
     (
         ('Universidad de Buenos Aires (UBA)', Ciudad.objects.get(nombre='Buenos Aires').id),
         ('Proyecto Arqueológico Yocavil', Ciudad.objects.get(nombre='Buenos Aires').id)
     )
     ),

    ('Universidad de Queensland', Pais.objects.get(nombre='Australia').id,
     [('Universidad de Queensland', Ciudad.objects.get(nombre='Brisbane').id)]),

    ('Universidad Autónoma de Barcelona (UAB)', Pais.objects.get(nombre='España').id,
     (
         ('Universidad Autónoma de Barcelona (UAB)', Ciudad.objects.get(nombre='Barcelona').id),
         ('Instituto Catalán de Tecnología Ambiental (ICTA)', Ciudad.objects.get(nombre='Barcelona').id)
     )
     ),

    ('El Colegio de México, A.C.', Pais.objects.get(nombre='México').id,
     [('El Colegio de México, A.C.', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('LEAD International', Pais.objects.get(nombre='México').id,
     [('LEAD International', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Instituto Nacional de Estadística y Geografía (INEGI)', Pais.objects.get(nombre='México').id,
     [('Instituto Nacional de Estadística y Geografía (INEGI)', Ciudad.objects.get(nombre='Aguascalientes').id)]),

    ('Sociedad Latinoamericana de Percepción Remota y Sistemas de Información Espacial (SELPER México)',
     Pais.objects.get(nombre='México').id, [(
        'Sociedad Latinoamericana de Percepción Remota y Sistemas de Información Espacial (SELPER México)',
        Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Universidad Autónoma del Estado de México (UAEMex)', Pais.objects.get(nombre='México').id,
     (
         ('Universidad Autónoma del Estado de México (UAEMex)', Ciudad.objects.get(nombre='Toluca').id),
         ('Facultad de Geografía', Ciudad.objects.get(nombre='Toluca').id)
     )
     ),

    ('Open Geospatial Consortium (OGC)', Pais.objects.get(nombre='Estados Unidos de América').id,
     [('Open Geospatial Consortium (OGC)', Ciudad.objects.get(nombre='Wayland').id)]),

    ('Gtt Imaging, S.A. de C.V.', Pais.objects.get(nombre='México').id,
     [('Gtt Imaging, S.A. de C.V.', Ciudad.objects.get(nombre='Guadalajara').id)]),

    ('Instituto Nacional para el Federalismo y el Desarrollo Municipal (INAFED)', Pais.objects.get(nombre='México').id,
     [('Instituto Nacional para el Federalismo y el Desarrollo Municipal (INAFED)',
       Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Secretaría de Medio Ambiente y Recursos Naturales (SEMARNAT)', Pais.objects.get(nombre='México').id,
     (
         ('Secretaría de Medio Ambiente y Recursos Naturales (SEMARNAT)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Instituto Nacional de Ecología y Cambio Climático (INECC)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)
     )
     ),

    ('Universidad Iberoamericana (UIA)', Pais.objects.get(nombre='México').id,
     [
         ('Ibero OnLine', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)
     ]
     ),

    ('Centro de Capacitación en Calidad Sanitaria S.A. DE C.V.', Pais.objects.get(nombre='México').id,
     [('Centro de Capacitación en Calidad Sanitaria S.A. DE C.V.', Ciudad.objects.get(nombre='Monterrey').id)]),

    ('Instituto Nacional de Antropología e Historia (INAH)', Pais.objects.get(nombre='México').id,
     (
         ('Centro de Investigaciones y Estudios Superiores en Antropología Social (CIESAS)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Coordinación de Antropología', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Escuela Nacional de Antropología e Historia', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)
     )
     ),

    ('Universidad Autónoma Chapingo', Pais.objects.get(nombre='México').id,
     [('Universidad Autónoma Chapingo', Ciudad.objects.get(nombre='Texcoco de Mora').id)]),

    ('Sistema de la Integración Centroamericana (SICA)', Pais.objects.get(nombre='México').id, [(
        'Comisión Centroamericana de Ambiente y Desarrollo (CCAD)',
        Ciudad.objects.get(
            nombre='Ciudad de México, CDMX').id)]),

    ('National Aeronautics and Space Administration (NASA)', Pais.objects.get(nombre='Estados Unidos de América').id,
     [('National Aeronautics and Space Administration (NASA)', Ciudad.objects.get(nombre='Washington, D.C.').id)]),

    ('Organización de las Naciones Unidas (ONU)', Pais.objects.get(nombre='Estados Unidos de América').id,
     (
         ('Banco Mundial (The World Bank)', Ciudad.objects.get(nombre='Washington, D.C.').id),
         ('Organización de las Naciones Unidas para la Alimentación y la Agricultura (FAO)',
          Ciudad.objects.get(nombre='Roma').id)
     )
     ),

    ('Environmental Systems Research Institute (ESRI)', Pais.objects.get(nombre='Estados Unidos de América').id,
     [('Environmental Systems Research Institute (ESRI)', Ciudad.objects.get(nombre='Redlands').id)]),

    ('Hexagon Geospatial', Pais.objects.get(nombre='Estados Unidos de América').id,
     [('ERDAS Imagine', Ciudad.objects.get(nombre='Norcross').id)]),

    ('Sistemas de Información Geográfica, S.A. de C.V.', Pais.objects.get(nombre='México').id,
     [('Sistemas de Información Geográfica, S.A. de C.V.', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Centro de Información y Comunicación Ambiental de Norte América, A.C. (CICEANA)',
     Pais.objects.get(nombre='México').id, [(
        'Centro de Información y Comunicación Ambiental de Norte América, A.C. (CICEANA)',
        Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Sociedad Mexicana de Geografía y Estadística, A.C.', Pais.objects.get(nombre='México').id,
     [('Sociedad Mexicana de Geografía y Estadística, A.C.', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Dirección General de Geografía y Medio Ambiente', Pais.objects.get(nombre='México').id,
     [('Dirección General de Geografía y Medio Ambiente', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Universidad Autónoma de Nayarit', Pais.objects.get(nombre='México').id,
     [('Universidad Autónoma de Nayarit', Ciudad.objects.get(nombre='Tepic').id)]),

    ('El Colegio de Jalisco A.C.', Pais.objects.get(nombre='México').id,
     [('El Colegio de Jalisco A.C.', Ciudad.objects.get(nombre='Guadalajara').id)]),

    ('Fundación Premio Nacional de Tecnología A.C.', Pais.objects.get(nombre='México').id,
     [('Fundación Premio Nacional de Tecnología A.C.', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Universidad de Harvard', Pais.objects.get(nombre='Estados Unidos de América').id,
     [
         ('Harvard Business Publishing', Ciudad.objects.get(nombre='Boston').id)
     ]
     ),

    ('Instituto Mexicano de la Propiedad Industrial (IMPI)', Pais.objects.get(nombre='México').id, [(
        'Instituto Mexicano de la Propiedad Industrial (IMPI)',
        Ciudad.objects.get(
            nombre='Ciudad de México, CDMX').id)]),

    ('Universidad Tecmilenio', Pais.objects.get(nombre='México').id,
     (
         ('Universidad Tecmilenio', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Buzan Latin America', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)
     )
     ),

    ('La Universidad de Indiana Bloomington', Pais.objects.get(nombre='Estados Unidos de América').id,
     (
         ('Department of Political Science and Workshop in Political Theory and Policy Analysis',
          Ciudad.objects.get(nombre='Bloomington').id),
         ('Workshop in Political Theory and Policy Analysis', Ciudad.objects.get(nombre='Bloomington').id),
         ('Vincent and Elinor Ostrom Workshop in Political Theory and Policy Analysis',
          Ciudad.objects.get(nombre='Bloomington').id)
     )
     ),

    ('Universidad Mayor se San Simón', Pais.objects.get(nombre='Bolivia').id,
     (
         ('Universidad Mayor se San Simón', Ciudad.objects.get(nombre='Cochabamba').id),
         (
             'Centro de Levantamientos Aeroespaciales y Aplicaciones SIG para el Desarrollo Sostenible de los Recursos Naturales (CLAS)',
             Ciudad.objects.get(nombre='Cochabamba').id)
     )
     ),

    ('Escuela Politécnica Federal de Zúrich (ETHZ)', Pais.objects.get(nombre='Suiza').id,
     [('Institute of Hydromechanics and Water Management', Ciudad.objects.get(nombre='Zúrich').id)]),

    ('Universidad de Míchigan', Pais.objects.get(nombre='Estados Unidos de América').id,
     [('Universidad de Míchigan', Ciudad.objects.get(nombre='Ann Arbor').id)]),

    ('ASPEL', Pais.objects.get(nombre='México').id, [('ASPEL', Ciudad.objects.get(nombre='Guadalajara').id)]),

    ('Técnica Aplicada Internacional S.A. de C.V.', Pais.objects.get(nombre='México').id,
     [('Técnica Aplicada Internacional S.A. de C.V.', Ciudad.objects.get(nombre='Naucalpan de Juárez').id)]),

    ('Universidad de Wurzburgo', Pais.objects.get(nombre='Alemania').id,
     [('Universidad de Wurzburgo', Ciudad.objects.get(nombre='Wurzburgo').id)]),

    ('The Big Van Theory: científicos sobre ruedas', Pais.objects.get(nombre='España').id,
     [('The Big Van Theory: científicos sobre ruedas', Ciudad.objects.get(nombre='Madrid').id)]),

    ('Universidad Complutense Madrid', Pais.objects.get(nombre='España').id,
     [('Universidad Complutense Madrid', Ciudad.objects.get(nombre='Madrid').id)]),

    ('Escuela de Organización Industrial', Pais.objects.get(nombre='España').id,
     [('Escuela de Organización Industrial', Ciudad.objects.get(nombre='Madrid').id)]),

    ('Gobierno de España', Pais.objects.get(nombre='España').id,
     [('Gobierno de España', Ciudad.objects.get(nombre='Madrid').id)]),

    ('Universidad de Alicante', Pais.objects.get(nombre='España').id,
     [('Instituto de Economía Internacional', Ciudad.objects.get(nombre='San Vicente del Raspeig').id)]),

    ('Interactive Advertising Bureau (IAB)', Pais.objects.get(nombre='Estados Unidos de América').id,
     [('Interactive Advertising Bureau (IAB)', Ciudad.objects.get(nombre='Nueva York').id)]),

    ('Universidad Don Vasco', Pais.objects.get(nombre='México').id,
     [('Universidad Don Vasco', Ciudad.objects.get(nombre='Uruapan').id)]),

    ('Arkinet, S.A. De C.V.', Pais.objects.get(nombre='México').id,
     [('Centro de capacitación de alto rendimiento', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Corporación Universitaria para el Desarrollo de Internet, A.C. (CUDI)', Pais.objects.get(nombre='México').id, [(
        'Corporación Universitaria para el Desarrollo de Internet, A.C. (CUDI)',
        Ciudad.objects.get(
            nombre='Ciudad de México, CDMX').id)]),

    ('Universidad Politécnica de Madrid', Pais.objects.get(nombre='España').id,
     [('Universidad Politécnica de Madrid', Ciudad.objects.get(nombre='Madrid').id)]),

    ('Academia Mexicana de Impacto Ambiental, A.C.(AMIA, A.C.)', Pais.objects.get(nombre='México').id, [(
        'Academia Mexicana de Impacto Ambiental, A.C.(AMIA, A.C.)',
        Ciudad.objects.get(
            nombre='Ciudad de México, CDMX').id)]),

    ('Advanced Analytical Systems, S.A. de C.V.', Pais.objects.get(nombre='México').id,
     [('Advanced Analytical Systems, S.A. de C.V.', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Universidad de Sonora', Pais.objects.get(nombre='México').id,
     [('Universidad de Sonora', Ciudad.objects.get(nombre='Hermosillo').id)]),

    ('Universidad Estatal de Sonora', Pais.objects.get(nombre='México').id,
     [('Universidad Estatal de Sonora', Ciudad.objects.get(nombre='Hermosillo').id)]),

    ('Banco Interamericano de Desarrollo (BID)', Pais.objects.get(nombre='Estados Unidos de América').id,
     [('Banco Interamericano de Desarrollo (BID)', Ciudad.objects.get(nombre='Washington, D.C.').id)]),

    ('Universidad Nacional de Tucumán', Pais.objects.get(nombre='Argentina').id,
     (
         ('Universidad Nacional de Tucumán', Ciudad.objects.get(nombre='San Miguel de Tucumán').id),
         ('Facultad de Ciencias Naturales', Ciudad.objects.get(nombre='San Miguel de Tucumán').id),
         ('Laboratorio de Geoarqueología de la Facultad de Ciencias Naturales',
          Ciudad.objects.get(nombre='San Miguel de Tucumán').id)
     )
     ),

    ('Sociedad Mexicana para la Divulgación de la Ciencia y la Técnica, A.C.', Pais.objects.get(nombre='México').id, [(
        'Sociedad Mexicana para la Divulgación de la Ciencia y la Técnica, A.C.',
        Ciudad.objects.get(
            nombre='Ciudad de México, CDMX').id)]),

    ('Centro de Investigación en Matemáticas (CIMAT)', Pais.objects.get(nombre='México').id,
     [('Centro de Investigación en Matemáticas (CIMAT)', Ciudad.objects.get(nombre='Guanajuato').id)]),

    ('Universidad de Guadalajara', Pais.objects.get(nombre='México').id,
     (
         ('Universidad de Guadalajara', Ciudad.objects.get(nombre='Guadalajara').id),
         ('Centro Universitario de Ciencias Sociales y Humanidades', Ciudad.objects.get(nombre='Guadalajara').id)
     )
     ),

    ('Universidad de Cádiz', Pais.objects.get(nombre='España').id,
     [('Universidad de Cádiz', Ciudad.objects.get(nombre='Cádiz').id)]),

    ('Universidad de La Habana', Pais.objects.get(nombre='Cuba').id,
     [('Facultad de Geografía', Ciudad.objects.get(nombre='La Habana').id)]),

    ('Universidad Paul Sabatier', Pais.objects.get(nombre='Francia').id,
     [('Universidad Paul Sabatier', Ciudad.objects.get(nombre='Toulouse').id)]),

    ('Universidad Politécnica de Valencia', Pais.objects.get(nombre='España').id,
     [('Universidad Politécnica de Valencia', Ciudad.objects.get(nombre='Valencia').id)]),

    ('International Social Science Council (ISSC)', Pais.objects.get(nombre='Francia').id,
     [('International Social Science Council (ISSC)', Ciudad.objects.get(nombre='París').id)]),

    ('Universidad de París I Panthéon-Sorbonne', Pais.objects.get(nombre='Francia').id,
     [('Universidad de París I Panthéon-Sorbonne', Ciudad.objects.get(nombre='París').id)]),

    ('Universidad Politécnica de Cataluña', Pais.objects.get(nombre='España').id,
     [('Universidad Politécnica de Cataluña', Ciudad.objects.get(nombre='Barcelona').id)]),

    ('Universidad de Lérida', Pais.objects.get(nombre='España').id,
     [('Universidad de Lérida', Ciudad.objects.get(nombre='Lérida').id)]),

    ('Universidad de Brístol', Pais.objects.get(nombre='Reino Unido').id,
     [('Universidad de Brístol', Ciudad.objects.get(nombre='Brístol').id)]),

    ('Universidad Nacional de Córdoba (UNC)', Pais.objects.get(nombre='Argentina').id,
     [('Universidad Nacional de Córdoba (UNC)', Ciudad.objects.get(nombre='Córdoba').id)]),

    ('Universidad de Sinkiang (XinJiang University)', Pais.objects.get(nombre='China').id,
     [('Universidad de Sinkiang (XinJiang University)', Ciudad.objects.get(nombre='Urumchi').id)]),

    ('Universidad Autónoma de Baja California Sur (UABCS)', Pais.objects.get(nombre='México').id,
     [('Universidad Autónoma de Baja California Sur (UABCS)', Ciudad.objects.get(nombre='La Paz').id)]),

    ('Academia de Ciencias de Cuba', Pais.objects.get(nombre='Cuba').id,
     [('Instituto de Ecología y Sistemática', Ciudad.objects.get(nombre='La Habana').id)]),

    ('Universidad Interamericana para el Desarrollo (UNID)', Pais.objects.get(nombre='México').id,
     [
         ('Universidad Interamericana para el Desarrollo, Morelia (UNID Morelia)',
          Ciudad.objects.get(nombre='Morelia').id)
     ]
     ),

    ('Universidad Autónoma de Querétaro', Pais.objects.get(nombre='México').id,
     [('Universidad Autónoma de Querétaro', Ciudad.objects.get(nombre='Santiago de Querétaro').id)]),

    ('Instituto Tecnológico y de Estudios Superiores de Monterrey (ITESM)', Pais.objects.get(nombre='México').id,
     (
         ('Instituto Tecnológico y de Estudios Superiores de Monterrey (ITESM)',
          Ciudad.objects.get(nombre='Monterrey').id),
         ('Instituto Tecnológico y de Estudios Superiores de Monterrey, Campus Guaymas (ITESM, Campus Guaymas)',
          Ciudad.objects.get(nombre='Heroica Guaymas de Zaragoza').id)
     )
     ),

    ('Universidad de Wageningen (WUR)', Pais.objects.get(nombre='Países Bajos / Holanda').id,
     [('Wageningen University and Research Centre', Ciudad.objects.get(nombre='Wageningen').id)]),

    ('Universidad de Hokkaido', Pais.objects.get(nombre='Japón').id,
     [('Universidad de Hokkaido', Ciudad.objects.get(nombre='Sapporo').id)]),

    ('Biocenosis, A.C.', Pais.objects.get(nombre='México').id,
     [('Biocenosis, A.C.', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Alternare, A.C.', Pais.objects.get(nombre='México').id,
     [('Alternare, A.C.', Ciudad.objects.get(nombre='Áporo').id)]),

    ('Espacio Autónomo, A.C.', Pais.objects.get(nombre='México').id,
     [('Espacio Autónomo, A.C.', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('H. Ayuntamiento de Morelia', Pais.objects.get(nombre='México').id,
     (
         ('H. Ayuntamiento de Morelia', Ciudad.objects.get(nombre='Morelia').id),
         ('Instituto Municipal de Planeación Morelia (IMPLAN)', Ciudad.objects.get(nombre='Morelia').id)
     )
     ),

    ('H. Ayuntamiento de Morelos', Pais.objects.get(nombre='México').id,
     [
         ('H. Ayuntamiento de Morelos', Ciudad.objects.get(nombre='Morelos').id)
     ]
     ),

    ('Universidad de Santiago de Compostela', Pais.objects.get(nombre='España').id,
     (
         ('Universidad de Santiago de Compostela', Ciudad.objects.get(nombre='Santiago de Compostela').id),
         ('Departamento de Farmacia y Tecnología Farmacéutica', Ciudad.objects.get(nombre='Santiago de Compostela').id)
     )
     ),

    ('Universidad de Columbia Británica (University of British Columbia (UBC))', Pais.objects.get(nombre='Canadá').id, [
        ('Universidad de Columbia Británica (University of British Columbia (UBC))',
         Ciudad.objects.get(nombre='West Point Grey').id)]),

    ('Universidad de Illinois en Urbana-Champaign', Pais.objects.get(nombre='Estados Unidos de América').id,
     [('Universidad de Illinois en Urbana-Champaign', Ciudad.objects.get(nombre='Urbana-Champaign').id)]),

    ('Universidad Autónoma de Campeche (UACAM)', Pais.objects.get(nombre='México').id,
     (
         ('Universidad Autónoma de Campeche (UACAM)', Ciudad.objects.get(nombre='Campeche').id),
         ('Instituto de Ecología, Pesquerías y Oceanografía del Golfo de México (EPOMEX)',
          Ciudad.objects.get(nombre='Campeche').id)
     )
     ),

    ('El Colegio de la Frontera Sur Unidad San Cristóbal (ECOSUR)', Pais.objects.get(nombre='México').id, [(
        'El Colegio de la Frontera Sur Unidad San Cristóbal (ECOSUR)',
        Ciudad.objects.get(
            nombre='San Cristóbal de las Casas').id)]),

    ('Universidad Federal de Minas Gerais', Pais.objects.get(nombre='Brasil').id,
     [('Universidad Federal de Minas Gerais', Ciudad.objects.get(nombre='Belo Horizonte').id)]),

    ('Universidad Estatal de Feira de Santana', Pais.objects.get(nombre='Brasil').id,
     [('Universidad Estatal de Feira de Santana', Ciudad.objects.get(nombre='Feira de Santana').id)]),

    ('Universidad de Toulouse', Pais.objects.get(nombre='Francia').id,
     [('Universidad de Toulouse', Ciudad.objects.get(nombre='Toulouse').id)]),

    ('Universidad de Granada', Pais.objects.get(nombre='España').id,
     [('Universidad de Granada', Ciudad.objects.get(nombre='Granada').id)]),

    ('Centro de Investigación en Alimentación y Desarrollo, A.C. (CIAD)', Pais.objects.get(nombre='México').id, [(
        'Centro de Investigación en Alimentación y Desarrollo, A.C. (CIAD)',
        Ciudad.objects.get(
            nombre='Culiacán Rosales').id)]),

    ('Instituto Nacional de Investigaciones Forestles, Agrícolas y Pecuarias (INIFAP)',
     Pais.objects.get(nombre='México').id, [(
        'Instituto Nacional de Investigaciones Forestles, Agrícolas y Pecuarias (INIFAP)',
        Ciudad.objects.get(nombre='Morelia').id)]),

    ('Universidad de Guanajuato', Pais.objects.get(nombre='México').id,
     (
         ('Universidad de Guanajuato', Ciudad.objects.get(nombre='Guanajuato').id),
         ('Departamento de Geomática e Hidráulica', Ciudad.objects.get(nombre='Guanajuato').id)
     )
     ),

    ('Instituto Tecnológico del Valle de Morelia', Pais.objects.get(nombre='México').id,
     [('Instituto Tecnológico del Valle de Morelia', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Universidad de Trento', Pais.objects.get(nombre='Italia').id,
     [('Universidad de Trento', Ciudad.objects.get(nombre='Trento').id)]),

    ('Diputación Provincial de Barcelona', Pais.objects.get(nombre='España').id,
     [('Diputación Provincial de Barcelona', Ciudad.objects.get(nombre='Barcelona').id)]),

    ('Netherlands Organization for Scientific Research (NWO)', Pais.objects.get(nombre='Países Bajos / Holanda').id,
     (
         ('Netherlands Organization for Scientific Research (NWO)', Ciudad.objects.get(nombre='Ámsterdam').id),
         ('Netherlands Organization for Scientific Research (WOTRO)', Ciudad.objects.get(nombre='Ámsterdam').id)
     )
     ),

    ('Alianza México REDD+', Pais.objects.get(nombre='México').id,
     [('Alianza México REDD+', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Reserva de la Biosfera de la Mariposa Monarca', Pais.objects.get(nombre='México').id,
     [('Reserva de la Biosfera de la Mariposa Monarca', Ciudad.objects.get(nombre='El Rosario').id)]),

    ('Fondo Mexicano para la Conservación de la Naturaleza, A.C. (FMCN)', Pais.objects.get(nombre='México').id, [(
        'Fondo Mexicano para la Conservación de la Naturaleza, A.C. (FMCN)',
        Ciudad.objects.get(
            nombre='Ciudad de México, CDMX').id)]),

    ('Agencia Nacional de Promoción Científica y Tecnológica', Pais.objects.get(nombre='Argentina').id,
     [('Agencia Nacional de Promoción Científica y Tecnológica', Ciudad.objects.get(nombre='Buenos Aires').id)]),

    ('Consejo Nacional de Investigaciones Científicas y Técnicas (CONICET)', Pais.objects.get(nombre='Argentina').id, [(
        'Consejo Nacional de Investigaciones Científicas y Técnicas (CONICET)',
        Ciudad.objects.get(
            nombre='Buenos Aires').id)]),

    ('Global Water Watch México', Pais.objects.get(nombre='México').id,
     [('Global Water Watch México', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Grupo Balsas para Estudio y Manejo de Ecosistemas, A.C.', Pais.objects.get(nombre='México').id,
     [('Grupo Balsas para Estudio y Manejo de Ecosistemas, A.C.', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Fundación Produce Michoacán, A.C.', Pais.objects.get(nombre='México').id,
     [('Fundación Produce Michoacán, A.C.', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Fundación Gonzalo Río Arronte I.A.P.', Pais.objects.get(nombre='México').id,
     [('Fundación Gonzalo Río Arronte I.A.P.', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Inter-American Institute for Global Change Research', Pais.objects.get(nombre='Estados Unidos de América').id,
     [('Inter-American Institute for Global Change Research', Ciudad.objects.get(nombre='Montevideo').id)]),

    ('Gobierno del Estado de Jalisco', Pais.objects.get(nombre='México').id,
     (
         ('Gobierno del Estado de Jalisco', Ciudad.objects.get(nombre='Guadalajara').id),
         ('Secretaria de Medio Ambiente', Ciudad.objects.get(nombre='Guadalajara').id),
         ('Secretaría de Medio Ambiente y Desarrollo Territorial (SEMADET Jalisco)',
          Ciudad.objects.get(nombre='Guadalajara').id)
     )
     ),

    ('Universidad de Murcia', Pais.objects.get(nombre='España').id,
     [('Universidad de Murcia', Ciudad.objects.get(nombre='Murcia').id)]),

    ('Universidad Nacional de la Patagonia San Juan Bosco', Pais.objects.get(nombre='Argentina').id,
     [('Universidad Nacional de la Patagonia San Juan Bosco', Ciudad.objects.get(nombre='Comodoro Rivadavia').id)]),

    ('Centro de Estudios Patagonia', Pais.objects.get(nombre='Argentina').id,
     [('Centro de Estudios Patagonia', Ciudad.objects.get(nombre='Viedma').id)]),

    ('Colegio de Postgraduados (COLPOS)', Pais.objects.get(nombre='México').id,
     [('Colegio de Postgraduados (COLPOS)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Centro Nacional para la Investigación Científica (Centre National de la Recherche Scientifique CNRS)',
     Pais.objects.get(nombre='Francia').id, [(
        'Centro Nacional para la Investigación Científica (Centre National de la Recherche Scientifique CNRS)',
        Ciudad.objects.get(nombre='París').id)]),

    ('Ministerio de Asuntos Exteriores y Desarrollo Internacional francés', Pais.objects.get(nombre='Francia').id,
     [('Ministerio de Asuntos Exteriores y Desarrollo Internacional francés', Ciudad.objects.get(nombre='París').id)]),

    ('Universidad Autónoma de Chiapas (UNACH)', Pais.objects.get(nombre='México').id,
     [('Universidad Autónoma de Chiapas (UNACH)', Ciudad.objects.get(nombre='Tuxtla Gutiérrez').id)]),

    ('Universidad de Texas en Austin', Pais.objects.get(nombre='Estados Unidos de América').id,
     [('Universidad de Texas en Austin', Ciudad.objects.get(nombre='Austin').id)]),

    ('WWF México', Pais.objects.get(nombre='México').id,
     [('WWF México', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('International Union for Conservation of Nature (IUCN)', Pais.objects.get(nombre='Suiza').id,
     [('International Union for Conservation of Nature (IUCN)', Ciudad.objects.get(nombre='Gland').id)]),

    ('Universidad de Toulouse-Jean Jaurès', Pais.objects.get(nombre='Francia').id,
     [('Universidad de Toulouse-Jean Jaurès', Ciudad.objects.get(nombre='Toulouse').id)]),

    ('Instituto Politécnico Nacional (IPN)', Pais.objects.get(nombre='México').id,
     (
         ('Instituto Politécnico Nacional (IPN)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Centro de Investigación y de Estudios Avanzados (CINVESTAV)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)
     )
     ),

    ('Instituto Politécnico y Universidad Estatal de Virginia (Virginia Tech, VT)',
     Pais.objects.get(nombre='Estados Unidos de América').id,
     [('Department of Biological Systems Engineering (BSE)', Ciudad.objects.get(nombre='Blacksburg').id)]),

    ('Universidad Estatal de Washington', Pais.objects.get(nombre='Estados Unidos de América').id,
     [('Universidad Estatal', Ciudad.objects.get(nombre='Pullman').id)]),

    ('Consejo Superior de Investigaciones Científicas (CSIC)', Pais.objects.get(nombre='España').id,
     [('Centro de Edafología y Biología Aplicada del Segura (CEBAS)', Ciudad.objects.get(nombre='Murcia').id)]),

    ('Universidad Pablo de Olavide (UPO)', Pais.objects.get(nombre='España').id,
     [('Universidad Pablo de Olavide (UPO)', Ciudad.objects.get(nombre='Sevilla').id)]),

    ('Unión Geográfica Internacional (UGI)', Pais.objects.get(nombre='Sudáfrica').id,
     [('Unión Geográfica Internacional (UGI)', Ciudad.objects.get(nombre='Ciudad del Cabo').id)]),

    ('Consejo Latinoamericano de Ciencias Sociales (CLACSO)', Pais.objects.get(nombre='Argentina').id,
     [('Consejo Latinoamericano de Ciencias Sociales (CLACSO)', Ciudad.objects.get(nombre='Buenos Aires').id)]),

    ('La Universidad de Texas A&M', Pais.objects.get(nombre='Estados Unidos de América').id,
     [('La Universidad de Texas A&M', Ciudad.objects.get(nombre='College Station').id)]),

    ('Universidad de Montreal', Pais.objects.get(nombre='Canadá').id,
     [('HEC Montreal', Ciudad.objects.get(nombre='Quebec').id)]),

    ('Universidad Tulane', Pais.objects.get(nombre='Estados Unidos de América').id,
     [('Universidad Tulane', Ciudad.objects.get(nombre='Nueva Orleans').id)]),

    ('Universidad Nacional de General Sarmiento (UNGS)', Pais.objects.get(nombre='Argentina').id,
     [
         ('Instituto del Conurbano (ICO)', Ciudad.objects.get(nombre='Buenos Aires').id)
     ]
     ),

    ('Universidad de Cabo Verde', Pais.objects.get(nombre='Cabo Verde').id,
     [('Universidad de Cabo Verde', Ciudad.objects.get(nombre='Praia').id)]),

    ('Centro di Ricerca, Sviluppo e Studi Superiori in Sardegna (CRS4)', Pais.objects.get(nombre='Italia').id,
     [('Centro di Ricerca, Sviluppo e Studi Superiori in Sardegna (CRS4)', Ciudad.objects.get(nombre='Pula').id)]),

    ('Universidad de Ciencias de Vida de Noruega (NMBU)', Pais.objects.get(nombre='Noruega').id,
     [('International Environment and Development Studies', Ciudad.objects.get(nombre='Oslo').id)]),

    ('Gobierno de Cataluña (Generalitat de Catalunya)', Pais.objects.get(nombre='España').id,
     [('Gobierno de Cataluña (Generalitat de Catalunya)', Ciudad.objects.get(nombre='Barcelona').id)]),

    ('Sociedad Científica Latinoamericana de Agroecología (SOCLA)', Pais.objects.get(nombre='Argentina').id,
     [('Sociedad Científica Latinoamericana de Agroecología (SOCLA)', Ciudad.objects.get(nombre='Buenos Aires').id)]),

    ('Partido de La Costa', Pais.objects.get(nombre='Argentina').id,
     [('Honorable Concejo Deliberante', Ciudad.objects.get(nombre='Buenos Aires').id)]),

    ('Asociación Etnobiológica Mexicana, A.C.', Pais.objects.get(nombre='México').id,
     [('Asociación Etnobiológica Mexicana, A.C.', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Universidad Autónoma de Guerrero', Pais.objects.get(nombre='México').id,
     [
         ('Universidad Autónoma de Guerrero', Ciudad.objects.get(nombre='Chilpancingo de los Bravo').id),
         ('Unidad de Ciencias de la Tierra', Ciudad.objects.get(nombre='Chilpancingo de los Bravo').id)
     ]
     ),

    ('Academia Mexicana de Ciencias', Pais.objects.get(nombre='México').id,
     [('Academia Mexicana de Ciencias', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Instituto Tecnológico Superior de Huetamo', Pais.objects.get(nombre='México').id,
     [('Instituto Tecnológico Superior de Huetamo', Ciudad.objects.get(nombre='Huetamo').id)]),

    ('Universidad Pedagógica Nacional', Pais.objects.get(nombre='México').id,
     (
         ('Universidad Pedagógica Nacional', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Unidad 161 Morelia', Ciudad.objects.get(nombre='Morelia').id)
     )
     ),

    ('Grupo Interdisciplinario de Tecnología Rural Apropiada, A.C. (GIRA)', Pais.objects.get(nombre='México').id, [(
        'Grupo Interdisciplinario de Tecnología Rural Apropiada, A.C. (GIRA)',
        Ciudad.objects.get(
            nombre='Pátzcuaro').id)]),

    ('International Maize and Wheat Improvement Center (CIMMYT)', Pais.objects.get(nombre='México').id,
     [('International Maize and Wheat Improvement Center (CIMMYT)', Ciudad.objects.get(nombre='El Batán').id)]),

    ('Cooperación Alemana al Desarrollo GIZ', Pais.objects.get(nombre='Alemania').id,
     [('Cooperación Alemana al Desarrollo GIZ', Ciudad.objects.get(nombre='Bonn').id)]),

    ('Universidad de Florida', Pais.objects.get(nombre='Estados Unidos de América').id,
     (
         ('Universidad de Florida', Ciudad.objects.get(nombre='Gainesville').id),
         ('Center for Latin American Studies', Ciudad.objects.get(nombre='Gainesville').id)
     )
     ),

    ('Instituto Tecnológico Superior de Tacámbaro', Pais.objects.get(nombre='México').id,
     (
         ('Instituto Tecnológico Superior de Tacámbaro', Ciudad.objects.get(nombre='Tacámbaro').id),
         ('Departamento de Geociencias', Ciudad.objects.get(nombre='Tacámbaro').id)
     )
     ),

    ('Universidad Católica de Honduras (UNICAH)', Pais.objects.get(nombre='Honduras').id,
     [('Universidad Católica de Honduras (UNICAH)', Ciudad.objects.get(nombre='Tegucigalpa').id)]),

    ('Universidad Autónoma Metropolitana (UAM)', Pais.objects.get(nombre='México').id,
     (
         ('Universidad Autónoma Metropolitana (UAM)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Universidad Autónoma Metropolitana, Unidad Xochimilco (UAM)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)
     )
     ),

    ('Instituto Tecnológico Superior de Ciudad Hidalgo', Pais.objects.get(nombre='México').id,
     [('Instituto Tecnológico Superior de Ciudad Hidalgo', Ciudad.objects.get(nombre='Ciudad Hidalgo').id)]),

    ('Universidad de Morelia (UDEM)', Pais.objects.get(nombre='México').id,
     (
         ('Universidad de Morelia (UDEM)', Ciudad.objects.get(nombre='Morelia').id),
         ('Escuela de Tecnologías de la Información', Ciudad.objects.get(nombre='Morelia').id)
     )
     ),

    ('Instituto Tecnológico Superior de Puruándiro (ITESP)', Pais.objects.get(nombre='México').id,
     [('Instituto Tecnológico Superior de Puruándiro (ITESP)', Ciudad.objects.get(nombre='Puruándiro').id)]),

    ('Benemérita Universidad Autónoma de Puebla (BUAP)', Pais.objects.get(nombre='México').id,
     (
         ('Benemérita Universidad Autónoma de Puebla (BUAP)', Ciudad.objects.get(nombre='Puebla de Zaragoza').id),
         ('Instituto de Ciencias', Ciudad.objects.get(nombre='Puebla de Zaragoza').id)
     )
     ),

    ('Universidad de Zaragoza', Pais.objects.get(nombre='España').id,
     [('Departamento de Geografía y Ordenación del Territorio', Ciudad.objects.get(nombre='Zaragoza').id)]),

    ('Universidad Internacional de Andalucía (UNIA)', Pais.objects.get(nombre='España').id,
     [('Universidad Internacional de Andalucía (UNIA)', Ciudad.objects.get(nombre='Sevilla').id)]),

    ('Universidad de los Llanos (UNILLANOS)', Pais.objects.get(nombre='Colombia').id, [(
        'Facultad de Ciencias Agropecuarias y Recursos Naturales (FCARN)',
        Ciudad.objects.get(
            nombre='Villavicencio').id)]),

    ('Universidad Nacional de La Plata (UNLP)', Pais.objects.get(nombre='Argentina').id,
     [('Facultad de Humanidades y Ciencias de la Educación', Ciudad.objects.get(nombre='La Plata').id)]),

    ('Universidad Nacional de Cuyo (UNCUYO)', Pais.objects.get(nombre='Argentina').id,
     [('Universidad Nacional de Cuyo (UNCUYO)', Ciudad.objects.get(nombre='Mendoza').id)]),

    ('Facultad Latinoamericana de Ciencias Sociales (FLACSO)', Pais.objects.get(nombre='México').id, [(
        'Facultad Latinoamericana de Ciencias Sociales (FLACSO)',
        Ciudad.objects.get(
            nombre='Ciudad de México, CDMX').id)]),

    ('Universidad Autónoma del Estado de Morelos', Pais.objects.get(nombre='México').id,
     [('Universidad Autónoma del Estado de Morelos', Ciudad.objects.get(nombre='Cuernavaca').id)]),

    ('Universidad de Quintana Roo', Pais.objects.get(nombre='México').id,
     (
         ('Universidad de Quintana Roo', Ciudad.objects.get(nombre='Chetumal').id),
         ('Universidad de Quintana Roo, Campus Cozumel', Ciudad.objects.get(nombre='Cozumel').id)
     )
     ),

    ('Universidad Tecnológica de Madrid', Pais.objects.get(nombre='España').id,
     [('Universidad Tecnológica de Madrid', Ciudad.objects.get(nombre='Madrid').id)]),

    ('Universidad Internacional Jefferson', Pais.objects.get(nombre='México').id,
     [('Universidad Internacional Jefferson', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Universidad Federal de Espírito Santo (UFES)', Pais.objects.get(nombre='Brasil').id,
     [('Universidad Federal de Espírito Santo (UFES)', Ciudad.objects.get(nombre='Vitória').id)]),

    ('Universidad del Minho', Pais.objects.get(nombre='Portugal').id,
     [('Universidad del Minho', Ciudad.objects.get(nombre='Braga').id)]),

    ('Universidad de San Carlos de Guatemala', Pais.objects.get(nombre='Guatemala').id,
     (
         ('Universidad de San Carlos de Guatemala', Ciudad.objects.get(nombre='Ciudad de Guatemala').id),
         ('Escuela de Biología', Ciudad.objects.get(nombre='Ciudad de Guatemala').id),
         ('Facultad de Ciencias Químicas y Farmacia', Ciudad.objects.get(nombre='Ciudad de Guatemala').id)
     )
     ),

    ('Universidad Veracruzana (UV)', Pais.objects.get(nombre='México').id,
     (
         ('Universidad Veracruzana (UV)', Ciudad.objects.get(nombre='Xalapa').id),
         ('Facultad de Biología', Ciudad.objects.get(nombre='Xalapa').id)
     )
     ),

    ('Pontificia Universidad Javeriana', Pais.objects.get(nombre='Colombia').id,
     [('Pontificia Universidad Javeriana', Ciudad.objects.get(nombre='Bogotá D.C.').id)]),

    ('Universidad de Ámsterdam', Pais.objects.get(nombre='Países Bajos / Holanda').id,
     (
         ('Universidad de Ámsterdam', Ciudad.objects.get(nombre='Ámsterdam').id),
         ('Amsterdam Institute for Social Science Research (AISSR)', Ciudad.objects.get(nombre='Ámsterdam').id)
     )
     ),

    ('Instituto Federal Electoral', Pais.objects.get(nombre='México').id,
     [('Instituto Federal Electoral', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Centro de Bachillerato Tecnológico Agropecuario (CBTA)', Pais.objects.get(nombre='México').id,
     (
         ('Centro de Bachillerato Tecnológico Agropecuario (CBTA)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Centro de Bachillerato Tecnológico Agropecuario #89 José Vasconcelos (CBTA 89)',
          Ciudad.objects.get(nombre='Taretan').id)
     )
     ),

    ('Tecnológico Nacional de México (TecNM)', Pais.objects.get(nombre='México').id,
     [('Tecnológico Nacional de México (TecNM)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Instituto Venezolano de Investigaciones Científicas (IVIC)', Pais.objects.get(nombre='Venezuela').id,
     [('Instituto Venezolano de Investigaciones Científicas (IVIC)', Ciudad.objects.get(nombre='Los Salias').id)]),

    ('Instituto para el Desarrollo Sustentable en Mesoamérica, A.C.', Pais.objects.get(nombre='México').id, [(
        'Instituto para el Desarrollo Sustentable en Mesoamérica, A.C.',
        Ciudad.objects.get(
            nombre='San Cristóbal de las Casas').id)]),

    ('Signos Diseño & Publicidad', Pais.objects.get(nombre='México').id,
     [('Signos Diseño & Publicidad', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Tecnologías y Servicios Agrarios, S.A (Tragsatec)', Pais.objects.get(nombre='España').id,
     [('Tecnologías y Servicios Agrarios, S.A (Tragsatec)', Ciudad.objects.get(nombre='Lérida').id)]),

    ('Meneu Distribución, S.A.', Pais.objects.get(nombre='España').id,
     [('Meneu Distribución, S.A.', Ciudad.objects.get(nombre='Albuixech').id)]),

    ('Instituto Cartográfico y Geológico de Cataluña (ICGC)', Pais.objects.get(nombre='España').id,
     [('Instituto Cartográfico y Geológico de Cataluña', Ciudad.objects.get(nombre='Barcelona').id)]),

    ('Universidad de Dar es-Salam', Pais.objects.get(nombre='Tanzania').id,
     [('Universidad de Dar es-Salam', Ciudad.objects.get(nombre='Dar es-Salam').id)]),

    ('Universidad Autónoma de Tlaxcala', Pais.objects.get(nombre='México').id,
     [('Universidad Autónoma de Tlaxcala', Ciudad.objects.get(nombre='Tlaxcala de Xicohténcatl').id)]),

    ('Harlen Administrativo SA de CV', Pais.objects.get(nombre='México').id,
     [('Harlen Administrativo SA de CV', Ciudad.objects.get(nombre='Morelia').id)]),

    ('CodiNet S.A. DE C.V.', Pais.objects.get(nombre='México').id,
     [('CodiNet S.A. DE C.V.', Ciudad.objects.get(nombre='Morelia').id)]),

    ('International Society for the Study of Religion, Nature and Culture (ISSRNC)',
     Pais.objects.get(nombre='Estados Unidos de América').id, [(
        'International Society for the Study of Religion, Nature and Culture (ISSRNC)',
        Ciudad.objects.get(nombre='Gainesville').id)]),

    ('Conference of Latin Americanist Geographers (CLAG)', Pais.objects.get(nombre='Estados Unidos de América').id,
     [('Conference of Latin Americanist Geographers (CLAG)', Ciudad.objects.get(nombre='Gainesville').id)]),

    ('Ayuntamiento de Cuernavaca', Pais.objects.get(nombre='México').id,
     [('Ayuntamiento de Cuernavaca', Ciudad.objects.get(nombre='Cuernavaca').id)]),

    ('Gobierno del Estado de Morelos', Pais.objects.get(nombre='México').id,
     [('Gobierno del Estado de Morelos', Ciudad.objects.get(nombre='Cuernavaca').id)]),

    ('TECIF', Pais.objects.get(nombre='México').id, [('TECIF', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Fideicomisos Instituidos en Relación con la Agrícultura (FIRA)', Pais.objects.get(nombre='México').id,
     [('Fideicomisos Instituidos en Relación con la Agrícultura (FIRA)', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Commission for Environmental Cooperation', Pais.objects.get(nombre='México').id,
     [('Commission for Environmental Cooperation', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Universidad Vasco de Quiroga (UVAQ)', Pais.objects.get(nombre='México').id,
     [('Universidad Vasco de Quiroga (UVAQ)', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Ministerio de Infraestructura, Provincia de Buenos Aires', Pais.objects.get(nombre='Argentina').id,
     [('Ministerio de Infraestructura', Ciudad.objects.get(nombre='Buenos Aires').id)]),

    ('Fondo Monarca, A.C.', Pais.objects.get(nombre='México').id,
     [('Fondo Monarca, A.C.', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Universidad de California en Berkeley', Pais.objects.get(nombre='Estados Unidos de América').id,
     (
         ('Universidad de California en Berkeley', Ciudad.objects.get(nombre='Berkeley').id),
         ('Center for Latin American Studies (CLAS)', Ciudad.objects.get(nombre='Berkeley').id)
     )
     ),

    ('EcoLogic Development Fund', Pais.objects.get(nombre='Estados Unidos de América').id,
     [('EcoLogic Development Fund', Ciudad.objects.get(nombre='Cambridge').id)]),

    ('Ecotecnologías, A.C.', Pais.objects.get(nombre='México').id,
     [('Ecotecnologías, A.C.', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Universidad Nacional Agraria La Molina (UNALM)', Pais.objects.get(nombre='Perú').id,
     [('Universidad Nacional Agraria La Molina (UNALM)', Ciudad.objects.get(nombre='Lima').id)]),
)

for i in Instituciones:
    e = Institucion(nombre=i[0], pais=Pais(pk=i[1]))
    e.save()
    print("Agregada la Institución " + i[0].upper() + " para el país " + str(Pais.objects.get(pk=i[1]).nombre))

    for j in i[2]:
        f = Dependencia(nombre=j[0], ciudad=Ciudad(pk=j[1]), institucion=Institucion(pk=e.pk))
        f.save()
        print(" --- Agregada la Dependencia " + j[0].upper() + " para la institución " + str(
            Institucion.objects.get(pk=e.pk).nombre))

User.objects.create_superuser(username='admin', email='cesar.benjamin@enesmorelia.unam.mx', password='ciga2017',
                              pais_origen=Pais.objects.get(nombre='México'),
                              pais=Pais.objects.get(nombre='México'),
                              estado=Estado.objects.get(nombre='Michoacán de Ocampo'),
                              ciudad=Ciudad.objects.get(nombre='Morelia'))

Usuarios = (
    (
        'usr_st', 'usr_st', 'usr_st', 'OTRO', Pais.objects.get(nombre='México').id,
        Ciudad.objects.get(nombre='Morelia').id,
        '-', 'Aso3U'),
    ('mario.figueroa', 'Figueroa Cárdenas', 'Mario', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '16ymf'),
    ('yunsh', 'yunsh', 'yunsh', 'OTRO', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').id,
     '-', 'yunsh'),

    ('berenice.solis', 'Berenice', 'Solis Castillo', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '6ESlj'),
    ('saray.bucio', 'Saray', 'Bucio Mendoza', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'usmv1'),
    ('quetzalcoatl.orozco', 'Quetzalcoatl', 'Orozco Ramirez', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ubFaE'),
    ('lourdes.gonzalez', 'Maria Lourdes', 'González Arqueros', 'INVESTIGADOR', Pais.objects.get(nombre='España').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'EeGJW'),
    ('karine.lefebvre', 'Karine', 'Lefebvre', 'INVESTIGADOR', Pais.objects.get(nombre='Francia').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '7Gs53'),
    ('lorena.poncela', 'Lorena', 'Poncela Rodríguez', 'INVESTIGADOR', Pais.objects.get(nombre='España').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'hnSDn'),
    ('pedro.urquijo', 'Pedro Sergio', 'Urquijo Torres', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'D', 'fEVor'),
    ('hilda.rivas', 'Hilda', 'Rivas', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'C', 'OH7fq'),
    ('jose.navarrete', 'José Antonio', 'Navarrete Pacheco', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'd2BFg'),
    ('luis.morales', 'Luis Miguel', 'Morales Manilla', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'C', 'ftTrS'),
    ('alejandra.larrazabal', 'Alejandra Patricia', 'Larrazábal De la Via', 'TECNICO',
     Pais.objects.get(nombre='Bolivia').id, Ciudad.objects.get(nombre='Morelia').id, 'C', 'Ersp5'),
    ('maria.carmona', 'María Estela', 'Carmona Jiménez', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'C', 'Yrcbo'),
    ('manuel.bollo', 'Manuel', 'Bollo Manent', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'D', 'zF8gk'),
    ('yan.gao', 'Yan', 'Gao', 'INVESTIGADOR', Pais.objects.get(nombre='China').id,
     Ciudad.objects.get(nombre='Morelia').id, 'B', 'UiSNj'),
    ('gabriela.cuevas', 'Gabriela', 'Cuevas García', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'B', 'J8YEd'),
    ('margaret.skutsch', 'Margaret', 'Skutsch', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'YxU7H'),
    ('angel.priego', 'Angel Guadalupe', 'Priego Santander', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'C', '9hUCZ'),
    ('brian.napoletano', 'Brian', 'Napoletano', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'B', '9OzFa'),
    ('manuel.mendoza', 'Manuel Eduardo', 'Mendoza Cantú', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'D', 'wjZ8d'),
    ('keith.mccall', 'Keith Michael', 'McCall', 'INVESTIGADOR', Pais.objects.get(nombre='Reino Unido').id,
     Ciudad.objects.get(nombre='Morelia').id, 'D', 'dNnfH'),
    ('jean.mas', 'Jean Francois', 'Mas', 'INVESTIGADOR', Pais.objects.get(nombre='Francia').id,
     Ciudad.objects.get(nombre='Morelia').id, 'D', 'GUKjy'),
    ('adrian.ghilardi', 'Adrián', 'Ghilardi', 'INVESTIGADOR', Pais.objects.get(nombre='Italia').id,
     Ciudad.objects.get(nombre='Morelia').id, 'B', 'DgFdm'),
    ('claudio.garibay', 'Claudio', 'Garibay Orozco', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'C', '88SSU'),
    ('ana.burgos', 'Ana Laura', 'Burgos Tornadú', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jEvFg'),
    ('gerardo.bocco', 'Gerardo Héctor Rubén', 'Bocco Verdinelli', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'D', 'f4r8Q'),
    ('francisco.bautista', 'Francisco', 'Bautista Zúñiga', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'C', '98big'),
    ('sara.barrasa', 'Sara', 'Barrasa García', 'INVESTIGADOR', Pais.objects.get(nombre='España').id,
     Ciudad.objects.get(nombre='Morelia').id, 'B', 'prgh0'),
    ('marta.astier', 'Marta', 'Astier', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'sNeKu'),
    ('antonio.vieyra', 'Jose Antonio', 'Vieyra Medrano', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'C', 'fs3S7'),
    ('hugo.zavala', 'Hugo Alejandro', 'Zavala Vaca', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'C', 'n80rn'),
    ('rosaura.paez', 'Rosaura', 'Páez Bistrain', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'C', 'puYq7'),
    ('yadira.mendez', 'Yadira Mireya', 'Méndez Lemus', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'B', '58Tln'),
    ('gabriela.lemus', 'Gabriela', 'Lemus', 'ADMINISTRATIVO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'B', 'Hj7Jx'),
    ('fabiola.velazquez', 'Fabiola Araceli', 'Velázquez Ayala', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'c3fhV'),
    ('alejandro.velazquez', 'Alejandro', 'Velázquez Montes', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'rWKXd'),
    ('alina.alvarez', 'Alina', 'Alvarez Larrain', 'OTRO', Pais.objects.get(nombre='Argentina').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'h8fvn'),
    ('arturo.muniz', 'Arturo', 'Muñiz Jauregui', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '10002'),
    ('maria.ramirez', 'María Isabel', 'Ramírez Ramírez', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'D', 'Y9jOf'),
    ('jaime.paneque', 'Jaime', 'Paneque Gálvez', 'INVESTIGADOR', Pais.objects.get(nombre='España').id,
     Ciudad.objects.get(nombre='Morelia').id, 'B', 'Y6pdF'),
    ('frida.guiza', 'Frida Nadiezda', 'Güiza Valverde', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'Yl5I4'),
    ('mariana.vallejo', 'Mariana', 'Vallejo Ramos', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '4th7o'),
    ('hebe.vessuri', 'Hebe', 'Vessuri', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'vmh1r'),
    ('rosa.rivas', 'Rosa', 'Rivas', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00002'),
    ('manuel.zavala', 'Manuel', 'Zavala', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00003'),
    ('raquel.gonzalez', 'Raquel', 'González García', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'biabG'),
    ('omar.montano', 'Omar', 'Montaño', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00004'),
    ('arturo.balderas', 'Arturo', 'Balderas Torres', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00005'),
    ('adriana.flores', 'Adriana Carolina', 'Flores Díaz', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'df4ty'),
    ('armonia.borrego', 'Armonía', 'Borrego', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'gb4go'),

    ('hernando.rodriguez', 'Hernando', 'Rodriguez', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00006'),
    ('sara.ortiz', 'Sara', 'Ortiz', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00007'),
    ('roser.manejo', 'Roser', 'Manejo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00008'),
    ('pablo.argueta', 'Pablo', 'Argueta', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00009'),
    ('beatriz.tejera', 'Beatriz', 'Tejera', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00010'),
    ('ana.moreno', 'Ana Isabel', 'Moreno Calles', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00011'),
    ('marcela.morales', 'Marcela', 'Morales', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00012'),
    ('jorge.gonzalez', 'Jorge', 'Gonzalez', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00013'),
    ('dante.ayala', 'Dante Ariel ', 'Ayala Ortiz', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00014'),
    ('jose.pimentel', 'Jose', 'Pimentel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00015'),
    ('martha.velazquez', 'Martha', 'Velazquez', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00016'),
    ('rocio.aguirre', 'Rocío', 'Aguirre', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00017'),
    ('margarita.alvarado', 'Margarita', 'Alvarado', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00018'),
    ('carina.grajales', 'Carina', 'Grajales', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00019'),
    ('luis.garcia', 'Luis', 'García', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00020'),
    ('luz.garcia', 'Luz Elena', 'García Martínez', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00021'),
    ('luis.ramirez', 'Luis', 'Ramírez', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00022'),
    ('maria.vizcaino', 'María', 'Vizcaíno', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00023'),
    ('andrew.boni', 'Andrew', 'Boni', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00024'),
    ('john.healey', 'John', 'Healey', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00025'),
    ('eduardo.frapolli', 'Eduardo', 'Frapolli', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00026'),
    ('miguel.martinez', 'Miguel', 'Martínez', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00027'),
    ('g.legorreta.paulin', 'G', 'Legorreta Paulin', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00028'),
    ('j.tiburio', 'J', 'Tiburio', 'OTRO', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').id,
     '-', '00029'),
    ('lucia.almeida', 'Lucia', 'Almeida', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00030'),
    ('roberto.lindig', 'Roberto', 'Lindig', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00031'),
    ('enrique.ojeda', 'Enrique', 'Ojeda', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00032'),
    ('jose.farina', 'José', 'Fariña', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00033'),
    ('jesus.fuentes', 'Jesús', 'Fuentes', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00034'),
    ('sophie.avila', 'Sophie', 'Avila', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00035'),
    ('guillermo.salas', 'Guillermo', 'Salas', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00036'),
    ('gian.delgado', 'Gian', 'Delgado', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00037'),
    ('octavio.gonzalez', 'Octavio', 'González', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00038'),
    ('jose.hernandez', 'José', 'Hernández', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00039'),
    ('leticia.merino', 'Leticia', 'Merino', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00040'),
    ('luis.macias', 'José Luis', 'Macías', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00041'))
for i in Usuarios:
    u = User.objects.create_user(username=i[0], first_name=i[1], last_name=i[2], tipo=i[3], pais_origen=Pais(pk=i[4]),
                                 pais=Pais.objects.get(nombre='México'),
                                 estado=Estado.objects.get(nombre='Michoacán de Ocampo'),
                                 ciudad=Ciudad(pk=i[5]), pride=i[6], rfc=i[7], direccion=i[0], password=i[7],
                                 email=i[0] + '@ciga.unam.mx')
    print(u)

Usuarios = (
    ('yameli.aguilar', 'Aguilar Duarte', 'Yameli', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'yameli.aguilar'),
    ('luis.cancer', 'Cancer Pomar', 'Luis', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'luis.cancer'),
    ('r.aguilar.romero', 'Aguilar Romero', 'R.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'r.aguilar.romero'),
    ('raul.aguirre', 'Aguirre Gómez', 'Raúl', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'raul.aguirre'),
    ('eduardo.alanis', 'Alanís Rodríguez', 'Eduardo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'eduardo.alanis'),
    ('israde.alcantara', 'Alcántara', 'Israde', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'israde.alcantara'),
    ('j.alcantar.mejía', 'Alcántar Mejía', 'J.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'j.alcantar.mejía'),
    ('sonia.altizer', 'Altizer', 'Sonia', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'sonia.altizer'),
    ('fernando.alvarado', 'Alvarado Ramos', 'Fernando', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'fernando.alvarado'),
    ('alfredo.amador', 'Amador García', 'Alfredo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alfredo.amador'),
    ('mirna.ambrosio', 'Ambrosio', 'Mirna', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'Mirna.ambrosio'),
    ('jose.anaya', 'Anaya Gomez', 'José Eduardo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jose.anaya'),
    ('carlos.anaya', 'Anaya Merchant', 'Carlos Antonio', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'carlos.anaya'),
    ('a.andablo.reyes', 'Andablo Reyes', 'A.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'a.andablo.reyes'),
    ('rene.arzuffi', 'Arzuffi Barrera', 'René', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'rene.arzuffi'),
    ('patricia.balvanera', 'Balvanera', 'Patricia', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'patricia.balvanera'),
    ('rc.barrientos.medina', 'Barrientos Medina', 'R. C.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'rc.barrientos.medina'),
    ('m.boada.junca', 'Boada Juncá', 'M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'm.boada.junca'),
    ('encarnacion.bobadilla', 'Bobadilla Soto', 'Encarnación Ernesto', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'enc.bobadilla'),
    ('nayda.bravo', 'Bravo Hernández', 'Nayda Luz', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'nayda.bravo'),
    ('miguel.bravo', 'Bravo', 'Miguel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'miguel.bravo'),
    ('lincoln.brwoer', 'Brower', 'Lincoln P.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'lincoln.brwoer'),
    ('stephen.brush', 'Brush', 'Stephen', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'stephen.brush'),
    ('bryan.pijanowski', 'Pijanowski', 'Bryan C.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'bryan.pijanowski'),
    ('matthias.bucker', 'Bücker', 'Matthias', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'matthias.bucker'),
    ('hector.cabadas', 'Cabadas Báez', 'Héctor Víctor', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'hector.cabadas'),
    ('cecilia.caballero', 'Caballero Miranda', 'Cecilia I.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'cecilia.caballero'),
    ('martin.cardena', 'Cadena Salgado', 'Martin', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'martin.cardenas'),
    ('nadia.campos', 'Campos Salas', 'Nadia', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'nadia.campos'),
    ('m.campos.sanchez', 'Campos Sánchez', 'M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'a.campos.sanchez'),
    ('jp.carbonelli', 'Carbonelli', 'J. P.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jp.carbonelli'),
    ('v.palamarczuk', 'Palamarczuk', 'V.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'v.palamarczuk'),
    ('t.carlon.allende', 'Carlón Allende', 'T.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 't.carlon.allende'),
    ('angel.carrancho', 'Carrancho', 'Ángel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'angel.carrancho'),
    ('oswaldo.carrillo', 'Carrillo', 'Oswaldo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'oswaldo.carrillo'),
    ('alejandro.casas', 'Casas Fernández', 'Alejandro', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alejandro.casas'),
    ('miguel.castillo', 'Castillo Santiago', 'Miguel Angel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'miguel.castillo'),
    ('alicia.castillo', 'Castillo', 'Alicia', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alicia.castillo'),
    ('federico.castrejon', 'Castrejón Ayala', 'Federico', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'federico.castrejon'),
    ('raul.cejudo', 'Cejudo Ruiz', 'Raul', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'raul.cejudo'),
    ('laura.chang', 'Chang Martínez', 'Laura', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'laura.chang'),
    ('noah.chutz', 'Chutz', 'Noah', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'noah.chutz'),
    ('alejandro.collantes', 'Collantes', 'Alejandro', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alejandro.collantes'),
    ('camilo.correa', 'Correa Ayram', 'Camilo A.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'camilo.correa'),
    ('stephane.couturier', 'Couturier', 'Stéphane', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'stephane.couturier'),
    ('zoila.cardenas', 'Cárdenas Mendoza', 'Zoila', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'zoila.cardenas'),
    ('o.delgado.carranza', 'Delgado Carranza', 'O.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'o.delgado.carranza'),
    ('luis.dourado', 'Dourado', 'Luís', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'luis,dourado'),
    ('inna.dubrovina', 'Dubrovina', 'Inna', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'inna.dubrovina'),
    ('ek.del.val', 'de Gortari', 'Ek del Val', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ek.del.val'),
    ('miguel.escalona', 'Escalona', 'Miguel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'miguel.escalona'),
    ('ileana.espejel', 'Espejel', 'Ileana', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ileana.espejel.'),
    ('lm.espinosa.rodriguez', 'Espinosa Rodríguez', 'L. M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'e.rodriguez'),
    ('a.espinoza.maya', 'Espinoza Maya', 'A.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'a.espinoza.maya'),
    ('bailis.espinoza', 'Espinoza Medrano', 'Bailis', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'bailis.Espinoza'),
    ('fabricio.espinoza', 'Espinoza Medrano', 'Fabricio', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'fabricio.espinoza'),
    ('osvaldo.esquivel', 'Esquivel Lucatero', 'Osvaldo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'osvaldo.esquivel'),
    ('andres.etter', 'Etter', 'Andrés', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'andres.etter'),

    ('b.figueroa.rangel', 'Figueroa Rangel', 'B.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'figueroa.rangel'),
    ('linda.fink', 'Fink', 'Linda S.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'linda.fink'),
    ('roberto.fisher', 'Fisher Ortíz', 'Roberto Alexander', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'roberto.fisher'),
    ('a.flamenco.sandoval', 'Flamenco Sandoval', 'A.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'flamenco.sandoval'),
    ('angel.flores', 'Flores Domínguez', 'Angel David', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'angel.flores'),
    ('ivan.franch', 'Franch Pardo', 'Iván', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ivan.franch'),
    ('oscar.frausto', 'Frausto', 'Oscar', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'oscar.frausto'),
    ('mario.freitas', 'Freitas', 'Mário', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'mario.freitas'),
    ('gabriel.vazquez', 'Vázquez', 'C. Gabriel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'gabriel.vazquez'),
    ('artemio.gallegos', 'Gallegos García', 'Artemio', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'artemio.gallegos'),
    ('angeles.gallegos', 'Gallegos A.', 'Angeles', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'angeles.gallegos'),
    ('victoria.reyes', 'Reyes García', 'Victoria', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'victoria.reyes'),
    ('manuel.macia', 'J. Macía', 'Manuel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'manuel.macia'),
    ('m.farfan.gutierez', 'Farfán Gutiérrez', 'M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'm.farfan.gutierez'),

    ('jorge.gama', 'Gama Castro', 'Jorge E.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jorge.gama'),
    ('andres.garcia', 'Garcia', 'Andres', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'andres.garcia'),
    ('ana.garcia', 'García de Fuentes', 'Ana', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ana.garcia'),
    ('eduardo.garcia', 'García', 'Eduardo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'eduardo.garcia'),
    ('f.gavi.reyes', 'Gavi Reyes', 'F.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'f.gavi.reyes'),
    ('mayra.gavito', 'Gavito', 'Mayra', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'mayra.gavito'),
    ('gilberto.gaxiola', 'Gaxiola Castro', 'Gilberto', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'gilberto.gaxiola'),
    ('d.geissert.kientz', 'Geissert Kientz', 'D.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'd.geissert.kientz'),
    ('peter.gerritsen', 'W. Gerritsen', 'Peter R.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'peter.gerritsen'),
    ('joaquin.gimenez', 'Giménez de Azcarate', 'Joaquin', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'joaquin.gimenez'),
    ('pierre.glynn', 'Glynn', 'Pierre', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'pierre.glynn'),
    ('avto.gogichaishvili', 'Gogichaishvili', 'Avto', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'gogichaishvili'),
    ('j.gonzález.areu', 'González Areu', 'J.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'gonzález.areu'),
    ('claudio.gonzalez', 'González Arqueros', 'Claudio', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'claudio.gonzalez'),
    ('carlos.gonzalez', 'González Esquivel', 'Carlos', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'carlos.gonzalez'),
    ('gaspar.gonzalez', 'González Sansón', 'Gaspar', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'gaspar.gonzalez'),
    ('maria.gonzalez', 'González Santiago', 'María Virginia', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'maria.gonzalez'),
    ('luis.gopar', 'Gopar Merino', 'Luis Fernando', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'luis.gopar'),
    ('solange.grimoldi', 'Grimoldi', 'Solange', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'solange.grimoldi'),
    ('maximilien.gueze', 'Gueze', 'Maximilien', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'maximilien.gueze'),
    ('francisco.gurri', 'Gurri', 'Francisco', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'francisco.gurri'),
    ('gemma.gomez', 'Gómez Castillo', 'Gemma', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'gemma.gomez'),
    ('enrique.gomez', 'Gómez Pech', 'Enrique', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'enrique.gomez'),
    ('ernest.williams', 'H. Williams', 'Ernest', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ernest.williams'),
    ('muki.haklay', 'Haklay', 'Muki', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'muki.haklay'),
    ('vm.hernandez.madrigal', 'Hernández Madrigal', 'V. M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'vm.hernandez'),
    ('aldo.hernandez', 'Hernández  Magaña', 'Aldo I.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'aldo.hernandez'),
    ('benigno.hernandez', 'Hernández de la Torre', 'Benigno', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'benigno.hernandez'),
    ('ruben.hernandez', 'Hernández Morales', 'Ruben', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ruben.hernandez'),
    ('keith.hobson', 'Hobson', 'Keith A.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'hobson.keith'),
    ('isabel.ramirez', 'Ramirez', 'M. Isabel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'isabel.ramirez'),
    ('e.vera.isunza', 'Isunza Vera', 'E.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'e.vera.isunza'),
    ('daniel.iura', 'Iura Gonzalez', 'Daniel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'daniel.iura'),
    ('thomas.j.ihl', 'J. Ihl', 'Thomas', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'thomas.j.ihl'),
    ('jaime.urrutia', 'Urrutia Fucugauchi', 'Jaime', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jaime.urrutia'),
    ('pablo.jaramillo', 'Jaramillo López', 'Pablo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'pablo.jaramillo'),
    ('ramon.jarquin', 'Jarquin Gálvez', 'Ramón', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ramon.jarquin'),
    ('adrian.mas', 'Jean François', 'Adrián Mas', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'adrian.mas'),
    ('r.jimenez.ramirez', 'Jiménez Ramírez', 'R.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'r.jimenez'),
    ('erik.juarez', 'Juarez Blanquet', 'Erik', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'erik.juarez'),
    ('elias.ucakuwun', 'K. Ucakuwun', 'Elias', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'elias.ucakuwun'),
    ('ken.oyama', 'Oyama', 'Alberto Ken', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ken.oyama'),
    ('maxime.kieffer', 'Kieffer', 'Maxime', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'maxime.kieffer'),
    ('nagesh.kolagani', 'Kolagani', 'Nagesh', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'nagesh.kolagani'),
    ('marit.kraagt', 'Kraagt', 'Marit', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'marit.kraagt'),
    ('rosario.langrave', 'Langrave', 'Rosario', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'rosario.langrave'),
    ('Lemoine,rodríguez', 'Lemoine Rodríguez', 'R.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'Lemoine,rodríguez'),
    ('rodrigo.liendo', 'Liendo', 'Rodrigo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'rodrigo.liendo'),
    ('a.lomelí.jimenez', 'Lomelí Jiménez', 'A.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'a.lomelí'),
    ('lourdes,gonzalez', 'González Arqueros', 'M. Lourdes', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'lourdes,gonzalez'),
    ('jesus.luna', 'Luna Béjar', 'Jesús Alonso', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jesus.luna'),
    ('cruz.lopez', 'López Contreras', 'Cruz', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'cruz.lopez'),
    ('erna.lopez', 'López Granados', 'Erna M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'erna.lopez'),
    ('gilbert.nduru', 'M. Nduru', 'Gilbert', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'gilbert.nduru'),
    ('miguel.maass', 'Maass Moreno', 'Miguel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'miguel.maass'),
    ('javier.martinez', 'Martínez', 'Javier', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'javier.martinez'),
    ('y.martinez.ruiz', 'Martínez Ruíz', 'Y.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'y.martinez.ruiz'),
    ('tomas.martinez', 'Martínez Saldaña', 'Tomás', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'tomas.martinez'),
    ('ayesa.martinez', 'Martínez Serrano', 'Ayesa', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ayesa.martinez'),
    ('leonardo.martinez', 'Martínez Torres', 'H. Leonardo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'leonardo.martinez'),
    ('emily.mcclung', 'McClung de Tapia', 'Emily', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'emily.mcclung'),
    ('paula.melic', 'Melic', 'Paula', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'paula.melic'),
    ('josemaria.michel', 'Michel Fuentes', 'Jose Maria', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'josemaria.michel'),
    ('rosa.molina', 'Molina Rojas', 'Rosa María', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'rosa.molina'),
    ('jc.mora.chaparro', 'Mora Chaparro', 'J. C.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jc.mora.chaparro'),
    ('j.morales.contreras', 'Morales Contreras', 'J.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'j.morales.contreras'),
    ('jaime.morales', 'Morales Hernández', 'Jaime', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jaime.morales'),
    ('helda.morales', 'Morales Iglesias', 'Helda', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'h.morales.iglesias'),
    ('juan.morales', 'Morales', 'Juan J.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'juan.morales'),
    ('wendy.morales', 'Morales', 'Wendy', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'wendy.morales'),

    ('julius.muchemi', 'Muchemi', 'Julius G.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'julius.muchemi'),
    ('antonio.mendez', 'Méndez Lemus', 'Antonio', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'antonio.mendez'),
    ('alfred.gichu', 'N. Gichu', 'Alfred', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alfred.gichu'),
    ('francis.wegulo', 'N. Wegulo', 'Francis', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'francis.wegulo'),
    ('alejandro.nene', 'Nené Preciado', 'Alejandro Jalmacin', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alejandro.nene'),
    ('julie.noriega', 'Noriega', 'Julie', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'julie.noriega'),
    ('ricardo.napoles', 'Nápoles', 'Ricardo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ricardo.napoles'),
    ('karen.oberhauser', 'Oberhauser', 'Karen S.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'karen.oberhauser'),
    ('luis.olivares', 'Olivares Martínez', 'Luis Daniel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'luis.olivares'),
    ('eduardo.orihuela', 'Orihuela Estefan', 'Eduardo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'eduardo.orihuela'),
    ('alberto.orozco', 'Orozco Moreno', 'Alberto', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alberto.orozco'),
    ('marti.orta', 'Orta Martínez', 'Martí', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'marti.orta'),
    ('beatriz.ortega', 'Ortega', 'Beatriz', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'beatriz.ortega'),
    ('s.ortiz.garcia', 'Ortiz García', 'S.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 's.ortiz.garcia'),
    ('laura.osorio', 'Osorio', 'Laura P.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'laura.osorio'),
    ('frank.ostermann', 'Ostermann', 'Frank', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'frank.ostermann'),
    ('d.palma.lopez', 'Palma López', 'D.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'd.palma.lopez'),
    ('hugo.perales', 'Perales', 'Hugo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'hugo.perales'),
    ('sol.perez', 'Perez Jimenez', 'Sol', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'sol.perez'),
    ('suzanne.pierce', 'Pierce', 'Suzanne', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'suzanne.pierce'),
    ('jose.plancarte', 'Plancarte Trujillo', 'José Aldo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jose.plancarte'),
    ('sandra.pola', 'Pola Villaseñor', 'Sandra', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'sandra.pola'),
    ('juan.pulido', 'Pulido', 'Juan', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'juan.pulido'),
    ('irene.perez', 'Pérez Llorente', 'Irene', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'irene.perez'),
    ('diego.perez', 'Pérez Salicrup', 'Diego Raúl', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'diego.perez'),
    ('azucena.perez', 'Pérez Vega', 'Azucena', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'azucena.perez'),
    ('jorge.quetzal', 'Quetzal Argueta', 'Jorge', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jorge.quetzal'),
    ('giacomo.gambaldi', 'Rambaldi', 'Giacomo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'giacomo.gambaldi'),

    ('palaniappan.ramu', 'Ramu', 'Palaniappan', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'palaniappan.ramu'),
    ('diana.ramirez', 'Ramírez Mejía', 'Diana', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'diana.ramirez'),
    ('lg.ramirez.sanchez', 'Ramírez Sanchez', 'L. G.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'lg.ramirez.sanchez'),
    ('hugo.ramirez', 'Ramírez Tobías', 'Hugo Magdaleno', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'hugo.ramirez'),
    ('f.garcía.oliva', 'García Oliva', 'F.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'f.garcía.oliva'),
    ('f.pineda.garcia', 'Pineda-García', 'F.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'f.pineda.garcia'),
    ('i.torres.garcia', 'Torres-García', 'I.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'i.torres.garcia'),
    ('f.pena.vega', 'Peña Vega', 'F.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'f.pena.vega'),
    ('saul.alvarez', 'Álvarez Borrego', 'Saúl', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'saul.alvarez'),

    ('selene.rangel', 'Rangel Landa', 'Selene', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'selene.rangel'),
    ('omar.masera', 'Masera', 'Omar Raul', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'omar.masera'),
    ('j.reyez.lopez', 'Reyes López', 'J.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'j.reyez.lopez'),
    ('mercedes.rivera', 'Rivera León', 'Mercedes', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'mercedes.rivera'),
    ('alexis.rivero', 'Rivero Romero', 'Alexis Daniela', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alexis.rivero'),
    ('yesenia.rodriguez', 'Rodríguez López', 'Yesenia', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'yesenia.rodriguez'),
    ('g.rodriguez.tapia', 'Rodríguez Tapia', 'G.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'g.rodriguez.tapia'),
    ('paul.roge', 'Roge', 'Paul', 'OTRO', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').id,
     '-', 'paul.roge'),
    ('yessica.romero', 'Romero Bautista', 'Yessica Angélica', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'yessica.romero'),
    ('fernando.rosete', 'Rosete Vergés', 'Fernando', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'fernando.rosete'),
    ('jeffrey.ross', 'Ross Ibarra', 'Jeffrey', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jeffrey.ross'),
    ('peter.rosset', 'Rosset', 'Peter', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'peter.rosset'),
    ('andrew.roth', 'Roth', 'Andrew', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'andrew.roth'),
    ('ryan.morris', 'Ryan Norris', 'D.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ryan.morris'),
    ('amalio.santacruz', 'Santacruz Varela', 'Amalio', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'amalio.santacruz'),
    ('ge.santana.huicochea', 'Santana Huicochea', 'G. E.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ge.santana.huicochea'),
    ('laura.santillan', 'Santillán Hernández', 'Laura Alicia', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'laura.santillan'),
    ('didac.santos', 'Santos Fita', 'Didac', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'didac.santos'),
    ('daniel.schwindt', 'Schwindt', 'Daniel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'dalien.schwindt'),
    ('sergey.sedov', 'Sedov', 'Sergey', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'sergey.sedov'),
    ('paola.segundo', 'Segundo Métay', 'Paola', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'pola.segundo'),
    ('itzi.segundo', 'Segundo', 'Itzi', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'itzi.segundo'),
    ('tzitzi.sharhi', 'Sharhi Delgado', 'Tzitzi', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'tzitzi.sharhi'),
    ('francisco.silva', 'Silva Bátiz', 'Francisco de Asís', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'francisco.silva'),
    ('peter.simmons', 'Simmons', 'Peter', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'peter.simmons'),
    ('m.solange.grimoldi', 'Solange Grimoldi', 'M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'm.solange.grimoldi'),
    ('ana.soler', 'Soler Arechalde', 'Ana M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ana.soler'),
    ('jose.solis', 'Solis Navarrete', 'José Alberto', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jose.solis'),
    ('elizabeth.solleiro', 'Solleiro Rebolledo', 'Elizabeth', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'elizabeth.solleiro'),
    ('f.solis.dominguez', 'Solís Domínguez', 'F.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'f.solis.dominguez'),

    ('roger.guevara', 'Guevara Hernández', 'Roger', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'roger.guevara'),
    ('jl.palacio.prieto', 'Palacio Prieto', 'J. L.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jl.palacio.prieto'),
    ('p.moreno.casasola', 'Moreno Casasola', 'P.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'p.moreno.casasola'),
    ('ja.lopez.portillo', 'López Portillo', 'J. A.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ja.lopez.portillo'),

    ('h.hernandez.trejo', 'Hernández Trejo', 'H.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'h.hernandez.trejo'),
    ('m.vargas.sandoval', 'Vargas Sandoval', 'M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'm.vargas.sandoval'),
    ('v.rico.gray', 'Zamora Crescencio', 'V.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'v.rico.gray'),
    ('c.gutierrez.baez', 'Gutiérrez Báez', 'C.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'c.gutierrez.baez'),
    ('m.domínguez.c', 'Domìnguez Carrasco', 'M. R.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'm.domínguez.c'),
    ('mt.camacho.olmedo', 'Camacho Olmedo', 'M. T.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'mt.camacho.olmedo'),
    ('teresa.ramirez', 'Ramírez Herrera', 'María Teresa', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'teresa.ramirez'),
    ('y.calvillo.garcía', 'Calvillo García', 'Y.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'y.calvillo.garcía'),
    ('c.delgado.trejo', 'Delgado Trejo', 'C.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'c.delgado.trejo'),
    ('claudia.uberhuaga', 'Uberhuaga', 'Claudia', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'claudia.uberhuaga'),
    ('jacquie.burgess', 'Burgess', 'Jacquie', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jacquie.burgess'),
    ('m.kinyanjui', 'Kinyanjui', 'M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'm.kinyanjui'),
    ('ricardo.saucedo', 'Saucedo', 'Ricardo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ricardo.saucedo'),
    ('l.morales.barquero', 'Morales Barquero', 'L.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'l.morales.barquero'),
    ('daniel.slayback', 'A. Slayback', 'Daniel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'daniel.slayback'),
    ('guillermo.figueroa', 'Figueroa Béjar', 'Guillermo Iván', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'guillermo.figueroa'),
    ('monica.figueroa', 'Figueroa Béjar', 'Mónica Adriana', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'monica.figueroa'),
    ('maria.figueroa', 'Figueroa Béjar', 'María del Socorro', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'maria.figueroa'),
    ('yair.merlin', 'Merlín Uribe', 'Yair', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'yair.merlin'),
    ('robert.hijmans', 'Hijmans', 'Hijmans', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'robert.hijmans'),
    ('ramon.mariaca', 'Mariaca Méndez', 'Ramón', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ramon.mariaca'),
    ('bruce.ferguson', 'Ferguson', 'Bruce', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'bruce.ferguson'),
    ('jorge.morfin', 'Morfin Rios', 'Jorge', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jorge.morfin'),
    ('citlalli.lopez', 'López Binqüist', 'Citlalli', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'citlalli.lopez'),
    ('neyra.sosa', 'Sosa Gutiérrez', 'Neyra', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'neyra.sosa'),
    ('lorena.soto', 'Soto Pinto', 'Lorena', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'lorena.soto'),
    ('romina.spano', 'Spano', 'Romina C.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'romina.spano'),
    ('a.sanchez.duque', 'Sánchez Duque', 'A.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'a.sanchez.duque'),
    ('julio.sanchez', 'Sánchez Escudero', 'Julio', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'julio.sanchez'),
    ('jm.sanchez.nunez', 'Sánchez Núñez', 'J. M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jm.sanchez'),
    ('cristobal.sanchez', 'Sánchez Sánchez', 'Cristóbal Daniel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'cristobal.sanchez'),
    ('hind.taud', 'Taud', 'Hind', 'OTRO', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').id,
     '-', 'hind.taud'),
    ('keiko.tatanisho', 'Teranisho Castillo', 'Keiko', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'keiko.tatanisho'),
    ('birgit.terhorst', 'Terhorst', 'Birgit', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'birgit.terhorst'),
    ('diego.torres', 'Torres Huerta', 'Diego', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'diego.torres'),
    ('jf.torrescano.valle', 'Torrescano Valle', 'J. F.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jf.torrescano.valle'),
    ('tyler.flockhart', 'Tyler Flockhart', 'D. T.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'tyler.flockhart'),
    ('nicolas.vargas', 'Vargas Ramírez', 'Nicolás', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'nicolas.vargas'),
    ('jeroen.verplanke', 'Verplanke', 'Jeroen', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jeroen.verplanke'),
    ('laura.villamil', 'Villamil Echeverri', 'Laura', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'laura.villamil'),
    ('alexey.voinov', 'Voinov', 'Alexey', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alexey.voinov'),
    ('lorenzo.vazquez', 'Vázquez Selem', 'Lorenzo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'lorenzo.vazquez'),
    ('leonard.wassenaar', 'Wassenaar', 'Leonard I.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'leonard.wassenaar'),
    ('martina.wilde', 'Wilde', 'Martina', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'martina.wilde'),
    ('antoinette.winklerprins', 'WinklerPrins', 'Antoinette', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'winklerPrins'),
    ('j.zavala.cruz', 'Zavala Cruz', 'J.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'j.zavala.cruz'),
    ('isela.zarmeno', 'Zermeño', 'Isela', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'isela.zarmeño'),
    ('zirion.martinez', 'Zirión Martínez', 'M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'zirion.martinez'),
    ('n.aguila.carrasco', 'Águila Carrasco', 'N', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'aguila.carrasco'),
    ('pablo.alvarez', 'Álvarez', 'Pablo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'pablo.alvarez'),
    ('l.menéndez.carrera', 'Menéndez Carrera', 'L', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'l.menéndez.carrera'),
    ('georges.seingier', 'Seingier', 'Georges', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'l.menéndez.carrera'),
    ('dalma.albarracin', 'Dalma', 'Albarracín', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'dalma.albarracin'),
    ('gabriela.alvarez', 'Alvarez Gamboa', 'Gabriela', 'OTRO', Pais.objects.get(nombre='México').id,

     Ciudad.objects.get(nombre='Morelia').id, '-', 'gabriela.alvarez'),
    ('fabiana.bekerman', 'Bekerman', 'Fabiana', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'fabiana.bekerman'),
    ('ana.cinti', 'Cinti', 'Ana', 'OTRO', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').id,
     '-', 'ana.cinti'),
    ('leticia.curti', 'Curti', 'Leticia', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'leticia.curti'),
    ('cristina.flores', 'Flores', 'Cristina', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'cristina.flores'),
    ('rosana.guber', 'Guber', 'Rosana', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'rosana.guber'),
    ('sergio.kaminker', 'Kaminker', 'Sergio Andres', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'sergio.kaminker'),
    ('carolina.laztra', 'Laztra', 'Carolina', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'carolina.laztra'),
    ('isabelle.sanchez', 'Sanchez Rose', 'Isabelle', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'isabelle.sanchez'),
    ('javier.serrano', 'Serrano', 'Javier', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'javier.serrano'),
    ('marcos.sourrouille', 'Sourrouille', 'Marcos', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'marcos.sourrouille'),
    ('damian.taire', 'Taire', 'Damián Leonardo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'damian.taire'),
    ('julio.vezub', 'Vezub', 'Julio', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'julio.vezub'),
    ('joaquin.sosa', 'Sosa Ramírez', 'Joaquín', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'joaquin.sosa'),
    ('donald.brand', 'Brand', 'Donald. D', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'donald.brand'),
    ('victor.toledo', 'Toledo', 'Victor M.','OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'victor.toledo'),
    ('alfred.zinck', 'Zinck', 'Joseph Alfred', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alfred.zinck'),
    ('hector.delvalle', 'Del Valle', 'Héctor Francisco', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'hector.delvalle'),
    ('carlos.paredes', 'Paredes Martínez', 'Carlos', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'carlos.paredes'),
    ('victoria.canino', 'Canino', 'Ma Victoria', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'victoria.canino'),
    ('rosa.bolivar', 'Bolivar', 'Rosa', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'rosa.bolivar'),
    ('ana.castellanos', 'Ana', 'Castellanos', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ana.castellanos'),
    ('alejandra.aray', 'Aray', 'Maria Alejandra', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alejandra.aray'),
    ('alberto.ortiz', 'Ortiz Rivera', 'Alberto', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alberto.ortiz'),
    ('michael.kuhn', 'Kuhn', 'Michael', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'michael.kuhn'),
    ('juan.vazquez', 'Vazquez Gutierrez', 'Juan Pablo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'juan.vazquez'),
    ('pablo.reyna', 'Reyna Estévez', 'Pablo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'pablo.reyna'),
    ('leon.nkolo', 'Nkolo Njodo', 'Léon Marie', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'leon.nkolo'),
    ('christiane.hartnack', 'Hartnack', 'Christiane', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'christiane.hartnack'),
    ('roger.magazine', 'Magazine', 'Roger', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'roger.magazine'),
    ('claudia.magallanes', 'Magallanes Blanco', 'Claudia', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'claudia.magallanes'),
    ('leandro.rodriguez', 'Rodriguez Medina', 'Leandro', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'claudia.magallanes'),
    ('ivan.costa', 'da Costa Marquez', 'Ivan', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ivan.costa'),
    ('michel.christie', 'Christie', 'Michel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'michel.christie'),
    ('kumaran.rajagopal', 'Rajagopal', 'Kumaran', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'kumaran.rajagopal'),
    ('quodratullah.qorbani', 'Qorbani', 'Quodratullah', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'quodratullah.qorbani'),
    ('consuelo.medina', 'Medina García', 'Consuelo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'consuelo.medina'),
    ('elvira.duran', 'Durán Medina', 'Elvira', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'elvira.duran'),
    ('carmen.bueno', 'Bueno Castellanos', 'Carmen', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'carmen.bueno'),
    ('kwang.yeong', 'Yeong Shin', 'Kwang', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'kwang.yeong'),
    ('huri.islamoglu', 'Islamoglu', 'Huri', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'huri.islamoglu'),
    ('doris.weidermann', 'Weidermann', 'Doris', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', ''),
    ('mauricio.nieto', 'Nieto Olarte', 'Mauricio', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'mauricio.nieto'),
    ('reinerg.grundmann', 'Grundmann', 'Reiner', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'reinerg.grundmann'),
    ('sujata.patel', 'Patel', 'Sujata', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'sujata.patel'),
    ('igor.yegorov', 'Yegorov', 'Igor', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'igor.yegorov'),
    ('pal.tamas', 'Tamas', 'Pal', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'pal.tamas'),
    ('kazumi.okamoto', 'Okamoto', 'Kazumi', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'kazumi.okamoto'),
    ('ramon.hernandez', 'Hernández Santana', 'José Ramón', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ramon.hernandez'),
    ('rigel.zaragoza', 'Zaragoza', 'Rigel Alfonso', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'rigel.zaragoza'),
    ('oscar.leal', 'Leal Nares', 'Oscar Adrián', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'oscar.leal'),
    ('laura.villaseñor', 'Villaseñor Gómez', 'Laura', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'oscar.leal'),
    ('felipe.hernandez', 'Hernández', 'Felipe', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'felipe.hernandez'),
    ('jose.moncada', 'Moncada Maya', 'José Omar', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jose.moncada'),
    ('alvaro.lopez', 'López López', 'Álvaro', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alvaro.lopez'),
    ('alberto.alvarez', 'Álvarez', 'Alberto', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alberto.alvarez'),
    ('juan.ortiz', 'Ortiz Escamilla', 'Juan', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'juan.ortiz'),
    ('isolda.lunavega', 'Luna Vega', 'Isolda', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'isolda.lunavega'),
    ('rafael.camaraartigas', 'Cámara Artigas', 'Rafael', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'rafael.camaraartigas'),
    ('jesus.ruizcareaga', 'Ruiz Careaga', 'Jesús', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jesus.ruizcareaga'),
    ('mauricio.perea', 'Perea Peña', 'Mauricio', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'mauricio.perea'),

)

for i in Usuarios:
    u = User.objects.create_user(username=i[0], first_name=i[2], last_name=i[1], tipo=i[3], pais_origen=Pais(pk=i[4]),
                                 pais=Pais.objects.get(nombre='México'),
                                 estado=Estado.objects.get(nombre='Michoacán de Ocampo'), ciudad=Ciudad(pk=i[5]),
                                 pride=i[6], rfc=i[7], direccion=i[0], password=i[7], email=i[0] + '@ciga.unam.mx')
    print(u)

adscritos = (
    'jean.mas', 'adrian.ghilardi', 'maria.ramirez', 'alejandro.velazquez', 'gerardo.bocco', 'angel.priego',
    'marta.astier', 'sara.barrasa', 'francisco.bautista',
    'pedro.urquijo', 'ana.burgos', 'rosaura.paez', 'maria.carmona', 'gabriela.cuevas', 'adriana.flores',
    'manuel.mendoza', 'yan.gao', 'jaime.paneque',
    'margaret.skutsch', 'claudio.garibay', 'antonio.vieyra', 'lourdes.gonzalez', 'frida.guiza', 'keith.mccall',
    'yadira.mendez', 'lorena.poncela',
    'brian.napoletano', 'manuel.bollo', 'alejandra.larrazabal', 'teresa.ramirez', 'maria.ramirez', 'arturo.balderas',
    'mariana.vallejo', 'alejandro.velazquez'
)

LSBM = ('Agriculture', 'Allergy', 'Anatomy & Morphology', 'Anesthesiology', 'Anthropology', 'Behavioral Sciences',
        'Biochemistry & Molecular Biology', 'Biodiversity & Conservation', 'Biophysics',
        'Biotechnology & Applied Microbiology', 'Cardiovascular System & Cardiology', 'Cell Biology',
        'Critical Care Medicine', 'Dentistry, Oral Surgery & Medicine', 'Dermatology', 'Developmental Biology',
        'Emergency Medicine', 'Endocrinology & Metabolism', 'Entomology', 'Environmental Sciences & Ecology',
        'Evolutionary Biology', 'Fisheries', 'Food Science & Technology', 'Forestry', 'Gastroenterology & Hepatology',
        'General & Internal Medicine', 'Genetics & Heredity', 'Geriatrics & Gerontology',
        'Health Care Sciences & Services', 'Hematology', 'Immunology', 'Infectious Diseases',
        'Integrative & Complementary Medicine', 'Legal Medicine', 'Life Sciences Biomedicine Other Topics',
        'Marine & Freshwater Biology', 'Mathematical & Computational Biology', 'Medical Ethics', 'Medical Informatics',
        'Medical Laboratory Technology', 'Microbiology', 'Mycology', 'Neurosciences & Neurology', 'Nursing',
        'Nutrition & Dietetics', 'Obstetrics & Gynecology', 'Oncology', 'Ophthalmology', 'Orthopedics',
        'Otorhinolaryngology', 'Paleontology', 'Parasitology', 'Pathology', 'Pediatrics', 'Pharmacology & Pharmacy',
        'Physiology', 'Plant Sciences', 'Psychiatry', 'Public, Environmental & Occupational Health',
        'Radiology, Nuclear Medicine & Medical Imaging', 'Rehabilitation', 'Reproductive Biology',
        'Research & Experimental Medicine', 'Respiratory System', 'Rheumatology', 'Sport Sciences', 'Substance Abuse',
        'Surgery', 'Toxicology', 'Transplantation', 'Tropical Medicine', 'Urology & Nephrology', 'Veterinary Sciences',
        'Virology', 'Zoology')

PHYS = (
    'Astronomy & Astrophysics', 'Chemistry', 'Crystallography', 'Electrochemistry', 'Geochemistry & Geophysics',
    'Geology',
    'Mathematics', 'Meteorology & Atmospheric Sciences', 'Mineralogy', 'Mining & Mineral Processing', 'Oceanography',
    'Optics', 'Physical Geography', 'Physics', 'Polymer Science', 'Thermodynamics', 'Water Resources')
TECH = (
    'Acoustics', 'Automation & Control Systems', 'Computer Science', 'Construction & Building Technology',
    'Energy & Fuels',
    'Engineering', 'Imaging Science & Photographic Technology', 'Information Science & Library Science',
    'Instruments & Instrumentation', 'Materials Science', 'Mechanics', 'Metallurgy & Metallurgical Engineering',
    'Microscopy', 'Nuclear Science & Technology', 'Operations Research & Management Science', 'Remote Sensing',
    'Robotics',
    'Science & Technology Other Topics', 'Spectroscopy', 'Telecommunications', 'Transportation')
ARTH = ('Architecture', 'Art', 'Arts & Humanities Other Topics', 'Asian Studies', 'Classics', 'Dance',
        'Film, Radio & Television', 'History', 'History & Philosophy of Science', 'Literature', 'Music', 'Philosophy',
        'Religion', 'Theater')
SOCS = ("Archaeology", "Area Studies", "Biomedical Social Sciences", "Business & Economics", "Communication",
        "Criminology & Penology", "Cultural Studies", "Demography", "Education & Educational Research",
        "Ethnic Studies", "Family Studies", "Geography", "Government & Law", "International Relations", "Linguistics",
        "Mathematical Methods In Social Sciences", "Psychology", "Public Administration", "Social Issues",
        "Social Sciences Other Topics", "Social Work", "Sociology", "Urban Studies", "Women's Studies")

otra = AreaConocimiento(categoria='ZTRA', nombre='Otra')
otra.save()

for i in LSBM:
    a = AreaConocimiento(categoria='LSBM', nombre=i)
    a.save()
    print(a)

for i in PHYS:
    a = AreaConocimiento(categoria='PHYS', nombre=i)
    a.save()
    print(a)

for i in TECH:
    a = AreaConocimiento(categoria='TECH', nombre=i)
    a.save()
    print(a)

for i in ARTH:
    a = AreaConocimiento(categoria='ARTH', nombre=i)
    a.save()
    print(a)

for i in SOCS:
    a = AreaConocimiento(categoria='SOCS', nombre=i)
    a.save()
    print(a)

CursosEspecializacion = (
    (
        'Gobernanza y visión territorial en las políticas públicas: Orígenes y nuevas perspectivas', 'CURSO', 9, 2,
        2015, 2,
        2015, 'Public Administration', ['Facultad de Ciencias Políticas y Sociales'], '58Tln'),
    ('Estudios Avanzados en Desarrollo Sustentable y Medio Ambiente', 'CERTIFICACION', 480, 11, 2004, 9, 2006,
     'Environmental Sciences & Ecology', ['El Colegio de México, A.C.', 'LEAD International'], 'Y9jOf'),
    ('Uso de la información geográfica en la página del internet del INEGI', 'CURSO', 4, 5, 2015, 5, 2015,
     'Physical Geography', ['Instituto Nacional de Estadística y Geografía (INEGI)'], 'J8YEd'),
    ('Mito y oralidad en la tradición mesoamericana', 'CURSO', 18, 5, 2015, 5, 2015, 'Anthropology',
     ['Universidad Nacional Autónoma de México (UNAM)'], 'J8YEd'),
    ('Geografía del Paisaje', 'CURSO', 32, 1, 2015, 5, 2015, 'Physical Geography',
     ['Centro de Investigaciones en Geografía Ambiental (CIGA)'], 'J8YEd'),
    (
        'Gobernanza y visión territorial en las políticas públicas: Orígenes y nuevas perspectivas', 'CURSO', 9, 2,
        2015, 2,
        2015, 'Public Administration', ['Facultad de Ciencias Políticas y Sociales'], 'J8YEd'),
    ('Historia y paisaje', 'CURSO', 6, 2, 2015, 2, 2015, 'Physical Geography',
     ['Centro de Investigaciones en Geografía Ambiental (CIGA)'], 'J8YEd'),
    ('Manejo del SIG libre QGIS 2.2', 'CURSO', 24, 6, 2014, 6, 2014, 'Remote Sensing',
     ['Centro de Investigaciones en Geografía Ambiental (CIGA)'], 'J8YEd'),
    ('Contribuciones del Pensamiento Geográfico al Manejo de Cuencas', 'CURSO', 10, 8, 2013, 8, 2013,
     'Physical Geography', ['Centro de Investigaciones en Geografía Ambiental (CIGA)'], 'J8YEd'),
    ('Celebración del Día de la Interoperabilidad de Datos Geoespaciales', 'OTRO', 9, 5, 2013, 5, 2013,
     'Physical Geography', ['Universidad Autónoma del Estado de México (UAEMex)', 'Open Geospatial Consortium (OGC)'],
     'J8YEd'),
    (
        'Land Change Modeling: calibration, validation, extrapolation, and interpretation', 'CURSO', 16, 10, 2011, 10,
        2011,
        'Physical Geography', ['Centro de Investigaciones en Geografía Ambiental (CIGA)'], 'J8YEd'),
    ('Writing scientific papers for publication in English', 'CURSO', 40, 11, 2012, 11, 2012,
     'Education & Educational Research', ['Centro de Investigaciones en Geografía Ambiental (CIGA)'], 'J8YEd'),
    ('3er. Evento Internacional de Geotecnología y Soluciones Avanzadas en Seguridad', 'OTRO', 16, 5, 2011, 5, 2011,
     'Remote Sensing', ['Gtt Imaging, S.A. de C.V.'], 'J8YEd'),
    ('Las 8 bandas de WorldView2 y sus distintas aplicaciones', 'CURSO', 8, 5, 2011, 5, 2011, 'Remote Sensing',
     ['Gtt Imaging, S.A. de C.V.'], 'J8YEd'),
    ('Taller de Capacitación Básica en Administración Municipal', 'CURSO', 8, 2, 2011, 2, 2011, 'Public Administration',
     ['Centro Estatal para el Desarrollo Municipal (CEDEMUN)'], 'J8YEd'),
    ('Coloquio Internacional "Geografía y Medio Ambiente en América Latina"', 'OTRO', 24, 1, 2015, 1, 2015,
     'Physical Geography', ['Centro de Investigaciones en Geografía Ambiental (CIGA)'], 'J8YEd'),
    ('Modelización espacial de los procesos de cambio de cobertura del suelo y uso del software DINAMICA', 'CURSO', 20,
     1, 2015, 1, 2015, 'Physical Geography', ['Instituto de Geografía'], 'J8YEd'),
    ('Redacción de artículos y documentos técnicos', 'CURSO', 10, 6, 2005, 6, 2005, 'Education & Educational Research',
     ['Instituto Nacional de Ecología y Cambio Climático (INECC)'], 'J8YEd'),
    (
        'Aplicación de mapeo y sistemas de información geográfica participativos en espacios urbanos', 'CURSO', 50, 2,
        2005,
        3, 2005, 'Physical Geography',
        ['International Institute for Geo-Information Sciences and Earth Observation (ITC)'],
        'J8YEd'),
    ('Trabajo en equipo Nivel 3', 'CURSO', 20, 1, 2005, 1, 2005, 'Public Administration', ['Ibero OnLine'], 'J8YEd'),
    (
        'Taller con los sectores Científico y Académico para la discusión y selección de una definición operativa de humedal y de una propuesta de Sistema de Clasificación de humedales en México',
        'CURSO', 8, 1, 2015, 1, 2015, 'Environmental Sciences & Ecology',
        ['Instituto Nacional de Ecología y Cambio Climático (INECC)'], 'J8YEd'),
    ('Curso de Redacción', 'CURSO', 30, 11, 2004, 12, 2004, 'Education & Educational Research',
     ['Instituto Nacional de Ecología y Cambio Climático (INECC)'], 'J8YEd'),
    ('Introducción al Análisis de Imágenes de Satélite', 'CURSO', 48, 6, 2004, 6, 2004, 'Remote Sensing',
     ['Instituto de Geografía'], 'J8YEd'),
    ('La vegetación de México', 'CURSO', 30, 6, 2004, 6, 2004, 'Environmental Sciences & Ecology',
     ['Instituto Nacional de Ecología y Cambio Climático (INECC)'], 'J8YEd'),
    ('Planeación Estratégica', 'CURSO', 16, 6, 2003, 6, 2003, 'Public Administration',
     ['Centro de Capacitación en Calidad Sanitaria S.A. DE C.V.'], 'J8YEd'),
    (
        'Teoría y aplicaciones de modelos de elevación digital (Shuttle radar topography mision) y aplicaciones de MODIS (Moderate Resolution Imaging Spectroradiometer)',
        'CURSO', 8, 10, 2003, 10, 2003, 'Remote Sensing', ['Comisión Centroamericana de Ambiente y Desarrollo (CCAD)'],
        'J8YEd'),
    ('ArcView Spatial Analyst y ArcView 3D Analyst', 'CURSO', 40, 12, 2002, 12, 2002, 'Physical Geography',
     ['Sistemas de Información Geográfica, S.A. de C.V.'], 'J8YEd'),
    ('Redacción intermedia', 'CURSO', 15, 10, 2002, 10, 2002, 'Linguistics',
     ['Instituto Nacional de Ecología y Cambio Climático (INECC)'], 'J8YEd'),
    ('IX Conferencia Latinoamericana de Usuarios de ESRI y ERDAS', 'OTRO', 24, 9, 2002, 9, 2002, 'Remote Sensing',
     ['Sistemas de Información Geográfica, S.A. de C.V.'], 'J8YEd'),
    ('Programando MapObjects con Visual Basic', 'CURSO', 24, 1, 2015, 1, 2015, 'Physical Geography',
     ['Sistemas de Información Geográfica, S.A. de C.V.'], 'J8YEd'),
    ('Conceptos básicos y fundamentos de ERDAS IMAGINE', 'CURSO', 24, 4, 2002, 4, 2002, 'Remote Sensing',
     ['Sistemas de Información Geográfica, S.A. de C.V.'], 'J8YEd'),
    (
        'El Ordenamiento ecológico en la gestión y manejo de recursos naturales de cara al siglo XXI', 'CURSO', 24, 9,
        2001,
        9, 2001, 'Environmental Sciences & Ecology', ['Instituto Nacional de Ecología y Cambio Climático (INECC)'],
        'J8YEd'),
    ('Introducción a Oracle con SQL', 'CURSO', 20, 1, 2015, 1, 2015, 'Science & Technology Other Topics',
     ['Instituto Nacional de Ecología y Cambio Climático (INECC)'], 'J8YEd'),
    ('Introducción a la informática', 'CURSO', 8, 6, 2001, 6, 2001, 'Science & Technology Other Topics',
     ['Instituto Nacional de Ecología y Cambio Climático (INECC)'], 'J8YEd'),
    ('El estado de la información ambiental en México', 'CURSO', 16, 6, 2000, 6, 2000,
     'Environmental Sciences & Ecology',
     ['Centro de Información y Comunicación Ambiental de Norte América, A.C. (CICEANA)'], 'J8YEd'),
    (
        'Los sistemas de información geográfica en la evaluación de riesgos, prevención de desastres y operación de programas de emergencia',
        'CURSO', 24, 1, 2015, 1, 2015, 'Physical Geography', ['Sistemas de Información Geográfica, S.A. de C.V.'],
        'J8YEd'),
    ('AML (Arc Macro Language)', 'CURSO', 24, 12, 1999, 12, 1999, 'Physical Geography',
     ['Sistemas de Información Geográfica, S.A. de C.V.'], 'J8YEd'),
    ('X Congreso Nacional de Geografía', 'OTRO', 24, 3, 1985, 3, 1985, 'Physical Geography',
     ['Sociedad Mexicana de Geografía y Estadística, A.C.'], 'J8YEd'),
    ('Detección de las vulnerabilidades en servicios que ofrecen servidores de red', 'CURSO', 35, 1, 2015, 1, 2015,
     'Telecommunications', ['Instituto de Investigaciones en Ecosistemas y Sustentabilidad (IIES)'], 'n80rn'),
    ('Writing Scientific Papers for Publication in English', 'CURSO', 8, 11, 2011, 11, 2011, 'Linguistics',
     ['Instituto de Geografía'], 'EeGJW'),
    ('VI Seminario Internacional de Clasificación de Suelos', 'OTRO', 27, 9, 2009, 10, 2009, 'Physical Geography',
     ['Laboratorio de Edafología "Nicolás Aguilera"'], 'EeGJW'),
    ('XXVII Curso-Diplomado Internacional de Edafología "Nicolás Aguilera"', 'DIPLOMADO', 49, 11, 2009, 11, 2009,
     'Physical Geography', ['Universidad Autónoma de Nayarit'], 'EeGJW'),
    ('Curso-Taller Uso de información geográfica en la página del internet del INEGI', 'CURSO', 4, 5, 2015, 5, 2015,
     'Physical Geography', ['Instituto Nacional de Estadística y Geografía (INEGI)'], 'Yrcbo'),
    ('Del Barroco español al neobarroco hispanoamericano, Cátedra Extraordinaria Maestros del Exilio Español', 'CURSO',
     30, 11, 2000, 4, 2001, 'History', ['Facultad de Filosofía y Letras'], 'fEVor'),
    (
        'Narrativa cubana de adentro y de afuera, Cátedra Extraordinaria Maestros del Exilio Español', 'CURSO', 30, 5,
        2001,
        9, 2001, 'History', ['Facultad de Filosofía y Letras'], 'fEVor'),
    (
        'Sistemas de Información Geográfica y Mapeo Participativos para la Planeación en Colaboración y para el Manejo de los Recursos Naturales',
        'CURSO', 120, 1, 2005, 2, 2005, 'Remote Sensing', ['Unidad Académica de Geografía, Morelia (UNAM Morelia)'],
        'fEVor'),
    (
        'Escritura del idioma teenek', 'CURSO', 15, 5, 2005, 6, 2005, 'History', ['Coordinación de Antropología'],
        'fEVor'),
    ('Fotografìa de paisaje', 'CURSO', 18, 3, 2008, 3, 2008, 'Imaging Science & Photographic Technology',
     ['Centro de Investigaciones en Geografía Ambiental (CIGA)'], 'fEVor'),
    ('Introducción al ArcGIS 9.', 'CURSO', 10, 4, 2008, 4, 2008, 'Automation & Control Systems',
     ['Centro de Investigaciones en Geografía Ambiental (CIGA)'], 'fEVor'),
    ('Taller Geográfico Pensar el Paisaje', 'CURSO', 10, 11, 2011, 11, 2011, 'Physical Geography',
     ['El Colegio de Jalisco A.C.'], 'fEVor'),
    ('Desarrollo de aplicaciones web para visualización de información geográfica.', 'CURSO', 40, 8, 2013, 9, 2013,
     'Information Science & Library Science',
     ['Escuela Nacional de Estudios Superiores, Unidad Morelia (ENES Morelia) '], 'fEVor'),
    ('Estadisticas básicas en R', 'CURSO', 24, 8, 2015, 8, 2015, 'Computer Science',
     ['Escuela Nacional de Estudios Superiores, Unidad Morelia (ENES Morelia)'], '9OzFa'),
    ('Administración de la innovación', 'DIPLOMADO', 60, 7, 2011, 9, 2011, 'Science & Technology Other Topics',
     ['Fundación Premio Nacional de Tecnología A.C.'], 'usmv1'),
    ('Harvard ManageMentor', 'CURSO', 0, 4, 2011, 3, 2012, 'Public Administration', ['Harvard Business Publishing'],
     'usmv1'),
    ('Seminario de Propiedad Industrial, Protección y administración de las invenciones en México', 'OTRO', 15, 6, 2011,
     6, 2011, 'Social Sciences Other Topics', ['Instituto Mexicano de la Propiedad Industrial (IMPI)'], 'usmv1'),
    ('Certificación en competencias del pensamiento creativo', 'CERTIFICACION', 56, 9, 2012, 1, 2013,
     'Education & Educational Research', ['Buzan Latin America'], 'usmv1'),
    ('Diplomado en Finanzas y Mercados Financieros, módulo 1', 'DIPLOMADO', 50, 1, 2005, 4, 2005,
     'International Relations', ['Instituto de Investigaciones Económicas y Empresariales (ININEE)'], 'usmv1'),
    ('Modelado ambiental con el programa DINAMICA EGO', 'CURSO', 40, 9, 2015, 9, 2015, 'Remote Sensing',
     ['Centro de Investigaciones en Geografía Ambiental (CIGA)'], 'UiSNj'),
    ('Modelado de Flujos y Caidas de Ceniza', 'CURSO', 24, 8, 2015, 8, 2015, 'Remote Sensing',
     ['Instituto de Geofísica, Unidad Morelia (UNAM Morelia)'], 'd2BFg'),
    ('Programa de Investigación Recursos e Instituciones Forestales (IFRI).', 'CURSO', 40, 8, 1998, 9, 1998,
     'Public Administration', ['Vincent and Elinor Ostrom Workshop in Political Theory and Policy Analysis'], '88SSU'),
    ('Percepción remota y SIG II (avanzado)', 'DIPLOMADO', 200, 7, 2000, 8, 2000, 'Remote Sensing', [
        'Centro de Levantamientos Aeroespaciales y Aplicaciones SIG para el Desarrollo Sostenible de los Recursos Naturales (CLAS)'],
     'wjZ8d'),
    ('Stochastic modelling, Hydrological Forecasting and Flood Risk', 'DIPLOMADO', 60, 2, 2002, 2, 2002,
     'Physical Geography', ['Institute of Hydromechanics and Water Management'], 'wjZ8d'),
    ('Geographic Information Systems and application (Water Management)', 'DIPLOMADO', 50, 11, 2003, 11, 2003,
     'Remote Sensing', ['International Institute for Geo-Information Sciences and Earth Observation (ITC)'], 'wjZ8d'),
    (
        'Questionary design for social sciences (en linea)', 'CURSO', 36, 11, 2015, 1, 2016,
        'Social Sciences Other Topics',
        ['Universidad de Míchigan'], 'Ersp5'),
    ('Slope deposits and Processes', 'CURSO', 60, 3, 2016, 3, 2016, 'Geology', ['Universidad de Wurzburgo'], '6ESlj'),
    ('Modelación de cambio de uso del suelo', 'DIPLOMADO', 20, 3, 2016, 3, 2016, 'Geology', ['Instituto de Geografía'],
     'GUKjy'),
    ('PAISAJE CULTURAL, CONOCIMIENTO ESPACIAL LOCAL y SIG PARTICIPATIVO (PACES)', 'CURSO', 64, 4, 2016, 4, 2016,
     'Geography', ['Centro de Investigaciones en Geografía Ambiental (CIGA)'], 'h8fvn'),
    ('Manejo Integrado del Paisaje', 'OTRO', 64, 8, 2010, 9, 2010, 'Physical Geography',
     ['Centro de Investigaciones en Geografía Ambiental (CIGA)'], 'biabG'),
    ('Instalación y configuración Sistemas Aspel', 'CURSO', 8, 3, 2008, 3, 2008, 'Automation & Control Systems',
     ['ASPEL'], 'biabG'),
    ('Curso básico del programa Mantenimiento preventivo MP V8', 'CURSO', 8, 4, 2006, 4, 2006,
     'Automation & Control Systems', ['Técnica Aplicada Internacional S.A. de C.V.'], 'biabG'),
    ('Curso del programa Controle de Herramienta V1', 'CURSO', 8, 4, 2006, 4, 2006, 'Automation & Control Systems',
     ['Técnica Aplicada Internacional S.A. de C.V.'], 'biabG'),
    ('Curso del programa de Inventario de Refacciones V2', 'CURSO', 8, 4, 2006, 4, 2006, 'Automation & Control Systems',
     ['Técnica Aplicada Internacional S.A. de C.V.'], 'biabG'),
    ('Módulos de Aleph V. 21', 'CURSO', 15, 2, 2016, 2, 2016, 'Automation & Control Systems',
     ['Dirección General de Bibiotecas (DGB)'], 'biabG'),
    ('Las artes escénicas en la divulgación científica', 'CURSO', 8, 10, 2015, 10, 2015, 'Theater',
     ['Coordinación de la Investigación Científica (CIC)'], 'Yrcbo'),
    ('Programación de Apps Móviles', 'CURSO', 40, 12, 2015, 12, 2015, 'Automation & Control Systems',
     ['Universidad Complutense Madrid'], 'n80rn'),
    ('Analítica Web', 'CURSO', 40, 12, 2015, 12, 2015, 'Automation & Control Systems',
     ['Escuela de Organización Industrial'], 'n80rn'),
    ('Introducción al Desarrollo Web (primera parte)', 'CURSO', 40, 12, 2015, 12, 2015, 'Telecommunications',
     ['Instituto de Economía Internacional'], 'n80rn'),
    ('Cloud Computing', 'CURSO', 40, 12, 2015, 12, 2015, 'Telecommunications', ['Escuela de Organización Industrial'],
     'n80rn'),
    ('Cómputo de Altas Prestaciones', 'CURSO', 30, 1, 2016, 1, 2016, 'Automation & Control Systems',
     ['Instituto de Investigaciones en Ecosistemas y Sustentabilidad (IIES)'], 'n80rn'),
    ('Administración de Fortianalyzer en la versión 5.2', 'CURSO', 40, 1, 2016, 1, 2016, 'Telecommunications',
     ['Centro de capacitación de alto rendimiento'], 'n80rn'),
    ('Administración de Fortigate en la versión 5.2.1', 'CURSO', 40, 1, 2016, 1, 2016, 'Telecommunications',
     ['Centro de capacitación de alto rendimiento'], 'n80rn'),
    ('Curso Básico de Marketing Digital', 'CURSO', 40, 3, 2016, 3, 2016, 'Telecommunications',
     ['Interactive Advertising Bureau (IAB)'], 'n80rn'),
    ('Reunión de la Conferencia de Geógrafos Latinoamericanistas CLAG Morelia 2005', 'OTRO', 40, 10, 2005, 10, 2005,
     'Physical Geography', ['Instituto de Geografía'], 'n80rn'),
    ('Sistema de Patentes Mexicano (IMPI)', 'OTRO', 40, 11, 2005, 11, 2005, 'Government & Law',
     ['Instituto Tecnológico de Morelia (ITM)'], 'n80rn'),
    (
        'Linux', 'OTRO', 40, 11, 2005, 11, 2005, 'Automation & Control Systems',
        ['Instituto Tecnológico de Morelia (ITM)'],
        'n80rn'),
    ('Manejo de Información y Productos Estadísticos del INEGI', 'OTRO', 40, 6, 2006, 6, 2006,
     'Information Science & Library Science', ['Universidad Don Vasco'], 'n80rn'),
    ('Programación Java Server Page', 'CURSO', 30, 6, 2006, 6, 2006, 'Automation & Control Systems',
     ['Instituto Tecnológico de Morelia (ITM)'], 'n80rn'),
    ('Programación y configuración de extensiones IP para conmutador NEAX2400 IPX', 'CURSO', 4, 11, 2006, 11, 2006,
     'Telecommunications', ['Universidad Nacional Autónoma de México, Campus Morelia (UNAM Morelia)'], 'n80rn'),
    ('Certified Packeteer Enginner Training Level I', 'CURSO', 20, 4, 2007, 4, 2007, 'Telecommunications',
     ['Universidad Nacional Autónoma de México, Campus Morelia (UNAM Morelia)'], 'n80rn'),
    ('StorageWorks Modular Smart Array Installation', 'CURSO', 20, 8, 2007, 8, 2007, 'Telecommunications',
     ['Unidad Académica de Geografía, Morelia (UNAM Morelia)'], 'n80rn'),
    ('Linux installation', 'CURSO', 8, 8, 2007, 8, 2007, 'Automation & Control Systems',
     ['Unidad Académica de Geografía, Morelia (UNAM Morelia)'], 'n80rn'),
    ('HP System Insight Manager Fundamentals', 'CURSO', 20, 7, 2007, 7, 2007, 'Telecommunications',
     ['Unidad Académica de Geografía, Morelia (UNAM Morelia)'], 'n80rn'),
    ('Integrating and Managing HP ProLiant Servers', 'CURSO', 20, 7, 2007, 7, 2007, 'Telecommunications',
     ['Unidad Académica de Geografía, Morelia (UNAM Morelia)'], 'n80rn'),
    ('Implementing HP ProLiant Servers', 'CURSO', 8, 8, 2007, 8, 2007, 'Telecommunications',
     ['Unidad Académica de Geografía, Morelia (UNAM Morelia)'], 'n80rn'),
    ('StorageWorks Modular Smart Array Administration', 'CURSO', 8, 8, 2007, 8, 2007, 'Telecommunications',
     ['Unidad Académica de Geografía, Morelia (UNAM Morelia)'], 'n80rn'),
    ('Introducción a Tecnologías de Videoconferencias', 'CURSO', 15, 11, 2007, 11, 2007, 'Telecommunications',
     ['Universidad Nacional Autónoma de México, Campus Morelia (UNAM Morelia)'], 'n80rn'),
    ('Actualización de Java y herramientas', 'CURSO', 30, 4, 2008, 5, 2008, 'Automation & Control Systems',
     ['Instituto de Investigaciones en Ecosistemas y Sustentabilidad (IIES)'], 'n80rn'),
    ('Fortimail v 3.0', 'CURSO', 30, 10, 2008, 10, 2008, 'Telecommunications',
     ['Centro de capacitación de alto rendimiento'], 'n80rn'),
    ('Implementando técnicas de seguridad en routers y switches CISCO', 'OTRO', 8, 6, 2009, 6, 2009,
     'Telecommunications', ['Centro de capacitación de alto rendimiento'], 'n80rn'),
    ('Primer Semestre Carrera Telecomunicaciones - Preparación CCNA', 'CURSO', 80, 8, 2009, 12, 2009,
     'Telecommunications', ['Centro de capacitación de alto rendimiento'], 'n80rn'),
    ('Reunión de Primavera, CUDI 2010', 'OTRO', 40, 4, 2010, 4, 2010, 'Telecommunications',
     ['Centro de capacitación de alto rendimiento'], 'n80rn'),
    ('Monitoreo de Redes', 'CURSO', 8, 4, 2010, 4, 2010, 'Telecommunications',
     ['Corporación Universitaria para el Desarrollo de Internet, A.C. (CUDI)'], 'n80rn'),
    (
        'Instalación, operación y mantenimiento de estaciones meteorológicas automáticas (EMA´s) Marca: FTS FOREST TECHNOLOGY SYSTEMS LTD., con sistema de comunicación satelital goes',
        'CURSO', 40, 5, 2010, 6, 2010, 'Telecommunications',
        ['Instituto de Investigaciones en Ecosistemas y Sustentabilidad (IIES)'], 'n80rn'),
    (
        'Tercer Encuentro Nacional sobre Ciencia, Tecnología en Innovación en México durante la última década: UNA VISIÓN CRITICA AL FUTURO y del 6to. Congreso Estatal de Ciencia y Tecnología',
        'OTRO', 30, 9, 2010, 9, 2010, 'Science & Technology Other Topics',
        ['Centro de capacitación de alto rendimiento'],
        'n80rn'),
    ('Administración y actualización de Fortimail en la versión 4.0', 'CURSO', 12, 5, 2012, 1, 2012,
     'Telecommunications', ['Centro de capacitación de alto rendimiento'], 'n80rn'),
    ('Administración de Sistemas de Almacenamiento en equipos Equallogic', 'CURSO', 40, 5, 2012, 5, 2012,
     'Telecommunications', ['Centro de capacitación de alto rendimiento'], 'n80rn'),
    ('Administración de Fortigate en la versión 4.0', 'CURSO', 21, 8, 2012, 8, 2012, 'Telecommunications',
     ['Centro de capacitación de alto rendimiento'], 'n80rn'),
    ('Taller de Análisis Forense', 'CURSO', 30, 8, 2013, 8, 2013, 'Telecommunications',
     ['Instituto de Investigaciones en Ecosistemas y Sustentabilidad (IIES)'], 'n80rn'),
    ('Análisis Forense de las Computadoras', 'CURSO', 30, 8, 2013, 8, 2013, 'Telecommunications',
     ['Universidad Nacional Autónoma de México, Campus Morelia (UNAM Morelia)'], 'n80rn'),
    ('Seminario Admin UNAM 2014', 'OTRO', 8, 6, 2014, 6, 2014, 'Public Administration',
     ['Universidad Nacional Autónoma de México (UNAM)'], 'n80rn'),
    ('Geografía Humana: Introducción a Yi Fu Tuan', 'CURSO', 20, 1, 2016, 1, 2016, 'Geography',
     ['Centro de Investigaciones en Geografía Ambiental (CIGA)'], 'prgh0'),
    ('Elementos para el seguimiento de Planes de Desarrollo', 'CURSO', 50, 4, 2016, 5, 2016, 'Public Administration',
     ['Universidad Nacional Autónoma de México (UNAM)'], '58Tln'),
    ('Geografía en la gestión y manejo de recursos naturales: experiencias vividas', 'CURSO', 25, 5, 2016, 5, 2016,
     'Environmental Sciences & Ecology', ['Centro de Investigaciones en Geografía Ambiental (CIGA)'], 'f4r8Q'),
    ('Desarrollo de Aplicaciones Web para visualización de Información Geográfica', 'CURSO', 40, 8, 2013, 9, 2013,
     'Telecommunications', ['Escuela Nacional de Estudios Superiores, Unidad Morelia (ENES Morelia)'], 'n80rn'),
    ('Redacción de textos científicos', 'CURSO', 30, 10, 2016, 10, 2016, 'Linguistics',
     ['Centro de Investigaciones en Geografía Ambiental (CIGA)'], 'f4r8Q'),
    ('Evaluación del Paisaje y Evaluación del Impacto Ambiental.', 'CURSO', 8, 11, 2016, 11, 2016,
     'Environmental Sciences & Ecology', ['Universidad Politécnica de Madrid'], 'df4ty'),
    ('Seminario Avances en Preparación de Muestras y Análisis de Materiales', 'OTRO', 8, 11, 2016, 11, 2016,
     'Instruments & Instrumentation', ['Escuela Nacional de Estudios Superiores, Unidad Morelia (ENES Morelia)'],
     'puYq7'),
    ('Movilidad y Urbanismo: Hacia una ciudad sostenible y humana', 'CURSO', 20, 2, 2016, 3, 2016,
     'Social Sciences Other Topics', ['Universidad Estatal de Sonora'], '9OzFa'),
    ('Curso-Taller Elaboración de mapas con ARGIS online para  servidores web', 'CURSO', 3, 11, 2016, 11, 2016,
     'Public Administration', ['Centro de Investigaciones en Geografía Ambiental (CIGA)'], 'c3fhV'),
    ('Taller Basico de edicion de textos con Latex', 'CURSO', 8, 5, 2016, 6, 2016, 'Education & Educational Research',
     ['Universidad Nacional Autónoma de México (UNAM)'], 'UiSNj'),
    ('Agrimonitor: Política agropecuaria, seguridad alimentaria y cambio climático', 'CURSO', 48, 8, 2016, 9, 2016,
     'Public Administration', ['Banco Interamericano de Desarrollo (BID)'], 'usmv1'),
    ('Drones como herramienta para Monitoreo y Manejo Territorial: Aplicaciones sociales y biofísicas', 'CURSO', 32, 11,
     2016, 11, 2016, 'Instruments & Instrumentation', ['Centro de Investigaciones en Geografía Ambiental (CIGA)'],
     'h8fvn'),
    ('Cartografia Del Paisaje', 'CURSO', 32, 3, 2016, 3, 2016, 'Physical Geography',
     ['Centro de Investigaciones en Geografía Ambiental (CIGA)'], 'h8fvn'),
    (
        '1° Curso Internacional de Geomorfología de Campo del Noroeste Argentino. Geoarqueología de los Valles Calchaquíes',
        'CURSO', 40, 8, 2016, 8, 2016, 'Geology',
        ['Laboratorio de Geoarqueología de la Facultad de Ciencias Naturales'],
        'h8fvn'),
    ('Introducción a la divulgación escrita', 'CURSO', 8, 8, 2016, 9, 2016, 'Education & Educational Research',
     ['Sociedad Mexicana para la Divulgación de la Ciencia y la Técnica, A.C.'], 'Yrcbo'),
    ('Taller de Herramientas para la Divulgación Científica', 'CURSO', 3, 8, 2016, 8, 2016,
     'Education & Educational Research', ['Centro de Investigación en Matemáticas (CIMAT)'], 'Yrcbo'),
    ('Jornada de Inducción para Académicos ENES Morelia 2017-1', 'OTRO', 4, 8, 2016, 8, 2016,
     'Education & Educational Research', ['Escuela Nacional de Estudios Superiores, Unidad Morelia (ENES Morelia)'],
     'Yrcbo'),
    ('Geoarqueología', 'CURSO', 30, 8, 2016, 8, 2016, 'Archaeology', ['Universidad Nacional de Tucumán'], '6ESlj'),
    ('Estrategias Lúdicas y Elaboración de Materiales para la Educación Ambiental', 'CURSO', 20, 8, 2016, 8, 2016,
     'Education & Educational Research', ['Universidad Michoacana de San Nicolás de Hidalgo (UMSNH)'], 'Yrcbo'),
    ('Introducción a R y sus aplicaciones a la Estadística básica', 'CURSO', 24, 8, 2016, 8, 2016, 'Computer Science',
     ['Escuela Nacional de Estudios Superiores, Unidad Morelia (ENES Morelia)'], 'd2BFg'),
    ('Taller Básico de edición de textos con Latex', 'CURSO', 12, 5, 2016, 6, 2016, 'Education & Educational Research',
     ['Centro de Investigaciones en Geografía Ambiental (CIGA)'], 'EeGJW'),
    ('Drones como herramienta para Monitoreo y Manejo Territorial: Aplicaciones Sociales y Biofísicas', 'CURSO', 32, 11,
     2016, 11, 2016, 'Instruments & Instrumentation', ['Centro de Investigaciones en Geografía Ambiental (CIGA)'],
     'EeGJW'),
    ('Curso de Construcción de Indicadores de Desempeño en Educación Superior', 'CURSO', 30, 10, 2016, 11, 2016,
     'Education & Educational Research', ['Secretaría de Desarrollo Institucional (SDI)'], '58Tln'),
    # 0                                                                        1      2   3   4     5    6                  7                                         8                               9
)

for i in CursosEspecializacion:
    c = CursoEspecializacion(nombre=i[0], tipo=i[1], horas=int(i[2]), fecha_inicio=datetime(int(i[4]), int(i[3]), 1),
                             fecha_fin=datetime(int(i[6]), int(i[5]), 28),
                             institucion=Dependencia.objects.get(nombre=i[8][0]).institucion,
                             dependencia=Dependencia.objects.get(nombre=i[8][0]), modalidad='PRESENCIAL',
                             area_conocimiento=AreaConocimiento.objects.get(nombre=i[7]),
                             usuario=User.objects.get(rfc=i[9]))
    c.save()
    print(c)

# GUKjy 	Septiembre 	1988 	Junio 	1989 	"Maîtrise" en biología 	Universidad Paul Sabatier 	Francia 	Junio 	1989 	- 	2015/11/13 18:23:47 	2015/11/13 18:23:47
# GUKjy 	Septiembre 	2015 	Septiembre 	1998 	Doctorado, Especialidad Percepción Remota / Ecolog... 	Universidad P. Sabatier 	Francia 	Enero 	2015 	Suivi de la déforestation dans le sudest du Mexique

Carreras = (
    ('Licenciatura en Geografía', 'Physical Geography'),
    ('Geografía', 'Physical Geography'),
    ('Ciencias del Mar', 'Environmental Sciences & Ecology'),
    ('Licenciatura en Biología', 'Environmental Sciences & Ecology'),
    ('Desarrollo Sustentable', 'Environmental Sciences & Ecology'),
    ('Agronomía', 'Agriculture'),
    ('Ingeniería en Agroecología', 'Geography'),
    ('Biología', 'Otra'),
    ('Licenciatura en Ciencias de la Comunicación', 'Communication'),
    ('Arqueología', 'Archaeology'),
    ('Ingeniería Técnica Agrícola', 'Automation & Control Systems'),
    ('Ingeniería Agrónoma', 'Physical Geography'),
    ('Historia', 'Geography'),
    ('Geography', 'Physical Geography'),
    ('Economía', 'Business & Economics'),
    ('Ciencias Ambientales', 'Environmental Sciences & Ecology'),
    ('Licenciatura en Ciencias Biológicas', 'Environmental Sciences & Ecology'),
    ('Geografia Economica', 'Geography'),
    ('Sociología', 'Sociology'),
    ('Licenciatura en Ciencias Antropológicas (orientación Arqueológica)', 'Anthropology'),
    ('Ingeniería en Sistemas Computacionales', 'Automation & Control Systems'),
    ('Medicina Veterinaria Zootecnista', 'Zoology'),
    ('Licenciatura en Economía', 'Business & Economics'),
    ('Licenciatura en Administración de Empresas Agropecuárias', 'Business & Economics'))

# ('Licenciatura en Biología', 'Agronomía', 'Arqueología', 'Biología', 'Ciencias Ambientales', 'Licenciatura en Ciencias Antropológicas (orientación Arqueológica)', 'Ciencias del Mar', 'Economía', 'Geografía', 'Geografia Economica', 'Geography', 'Historia', 'Ingeniería Agrónoma', 'Ingeniería en Sistemas Computacionales', 'Ingeniería en Agroecología', 'Ingeniería Técnica Agrícola', 'Licenciatura en Administración de Empresas Agropecuárias', 'Licenciatura en Economía', 'Licenciatura en Ciencias Biológicas', 'Medicina Veterinaria Zootecnista', 'Sociología')

for i in Carreras:
    c = ProgramaLicenciatura(nombre=i[0], area_conocimiento=AreaConocimiento.objects.get(nombre=i[1]))
    c.save()
    print(c)

Licenciaturas = (
    ('Licenciatura en Geografía', 'Physical Geography', ['Universidad de Guadalajara'],
     'Aportes de los Sistemas de Información Geográfica y de la Percepción Remota en la generación de cartografía forestal',
     1988, 8, 1992, 7, 1995, 3, 'Y9jOf'),
    ('Geografía', 'Physical Geography', ['Colegio de Geografia (Facultad de Filosofía y Letras)'],
     'Pronóstico del cambio de uso del suelo en áreas forestales del estado de Michoacán', 1984, 9, 1989, 6, 2007, 10,
     'J8YEd'),
    ('Ciencias del Mar', 'Environmental Sciences & Ecology', ['Universidad de Cádiz'], '-', 2000, 9, 2006, 9, 2006, 9,
     'hnSDn'),
    ('Licenciatura en Geografía', 'Physical Geography', ['Facultad de Geografía', 'Universidad de La Habana'],
     'Evaluación Edafo-Morfométrica para un Mejor Aprovechamiento del Recurso Tierra en el Municipio Los Palacios, Pinar del Río, Cuba.',
     1982, 9, 1987, 7, 1987, 7, '9hUCZ'),
    ('Ingeniería en Sistemas Computacionales', 'Physical Geography', ['Instituto Tecnológico de Morelia (ITM)'],
     'Sistema de Información Geográfica para el Ordenamiento Ecológico Territorial de la Región de la Mariposa Monarca (SIG-POETMM)',
     2001, 1, 2006, 6, 2007, 2, 'n80rn'),
    ('Licenciatura en Biología', 'Environmental Sciences & Ecology', ['Universidad Paul Sabatier'], '--', 1987, 9, 1988,
     6, 1988, 6, 'GUKjy'),
    ('Desarrollo Sustentable', 'Environmental Sciences & Ecology', ['UIIM Sede Pichátaro'],
     'Diagnóstico de la agricultura y sus perspectivas en la Comunidad San Francisco Uricho', 2014, 1, 2015, 3, 2015, 3,
     'sNeKu'),
    ('Agronomía', 'Agriculture', ['Universidad Politécnica de Valencia'],
     'Análisis de Ciclo de vida de la tortilla a base de maíz nativo Red Tsiri de la Cuenca del Lago de Pátzcuaro, Michoacán',
     2013, 6, 2015, 1, 2015, 1, 'sNeKu'),
    ('Ingeniería en Agroecología', 'Geography', ['Universidad Autónoma Chapingo'],
     'Estudio demográfico de Panicum miliacium en un cultivo de sorgo en Puruándiro, Michoacán', 1998, 8, 2002, 6, 2003,
     1, 'ubFaE'),
    ('Biología', 'Otra', ['Universidad Mayor se San Simón'], 'Graduación por excelencia Académica', 1998, 1, 2002, 9,
     2002, 9, 'Ersp5'),
    ('Licenciatura en Ciencias de la Comunicación', 'Communication',
     ['Universidad Autónoma del Estado de México (UAEMex)'], 'Mass Media Y Mercadotecnia Politica', 1991, 9, 1995, 5,
     1996, 1, 'Yl5I4'),
    ('Arqueología', 'Archaeology', ['Universidad París 1 Panteón-Sorbona'],
     'Las chinampas urbanas en Tenochitlan-Tlateloco', 2000, 9, 2004, 9, 2004, 9, '7Gs53'),
    ('Ingeniería Técnica Agrícola', 'Automation & Control Systems', ['Universidad Politécnica de Cataluña'],
     'Determinación del mercurio en la composta', 2001, 9, 2005, 7, 2005, 7, 'EeGJW'),
    ('Ingeniería Agrónoma', 'Physical Geography', ['Universidad de Lérida'],
     'Levantamiento de suelos y evaluación de la calidad del mapa de suelos en el Colegio de Postgraduados, Campus Montecillo, Estado de México, México',
     2006, 9, 2008, 7, 2008, 7, 'EeGJW'),
    ('Geografía', 'Physical Geography', ['Universidad de Brístol'],
     'Linear programming for optimal spatial allocation of hospital catchment areas, 	East Midlands', 1967, 9, 1970,
     7, 1970, 7, 'dNnfH'),
    ('Historia', 'Geography', ['Facultad de Filosofía y Letras'],
     'La montaña, el templo y la iglesia. Organización del espacio urbano de la Nueva España, siglo XVI. El caso de Tamuín en la Huasteca Potosina (',
     1998, 8, 2003, 7, 2004, 4, 'fEVor'),
    ('Geography', 'Physical Geography', ['Universidad de Brístol'], '-', 1967, 9, 1970, 6, 1970, 8, 'YxU7H'),
    ('Economía', 'Business & Economics',
     ['Facultad de Economía "Vasco de Quiroga"', 'Universidad Michoacana de San Nicolás de Hidalgo (UMSNH)'],
     '"Evaluación de los programas para el desarrollo local y alternativas para mejorar su impacto. El caso de La Huacana, Michoacán  en la administración 2005-2007"',
     2001, 9, 2006, 2, 2006, 9, 'usmv1'),
    ('Biología', 'Otra', ['Facultad de Ciencias'],
     'Diversidad y distribución de la familia Cactaceae en la región del Desierto Chihuahuense', 2001, 1, 2005, 7, 2006,
     2, '4th7o'),
    ('Ciencias Ambientales', 'Environmental Sciences & Ecology', ['Universidad Autónoma de Madrid'],
     'Programa de Ordenación de Embalses (POE) en la Comunidad de Madrid', 1994, 10, 1998, 9, 1998, 10, 'prgh0'),
    ('Licenciatura en Ciencias Biológicas', 'Environmental Sciences & Ecology',
     ['Universidad Nacional de Córdoba (UNC)'], 'Caracterización de volátiles en mieles del centro de Argentina', 1993,
     3, 2000, 3, 2000, 3, 'DgFdm'),
    ('Arqueología', 'Archaeology', ['Escuela Nacional de Antropología e Historia'],
     'Hacia el rescate y salvamento de la praxis arqueologica en México. Costa Azul, Baja California. Excavaciones arqueológicas a través de un salvamento arqueológico.',
     1999, 8, 2004, 7, 2006, 7, '6ESlj'),
    ('Geografia Economica', 'Geography', ['Universidad de Sinkiang (XinJiang University)'],
     'La importancia de Turismo para el desarrollo económico en la ciudad de Urumqi, XinJiang, China', 1994, 9, 1998, 7,
     1998, 7, 'UiSNj'),
    (
        'Sociología', 'Sociology', ['Facultad de Ciencias Políticas y Sociales'],
        'Arenas Políticas en la Meseta Purépecha',
        1975, 1, 1979, 1, 1995, 1, '88SSU'),
    ('Licenciatura en Geografía', 'Physical Geography', ['Colegio de Geografia (Facultad de Filosofía y Letras)'],
     'Estudio Geomorfológico de la Porción Sureste del Golfo de México', 1986, 9, 1991, 6, 1994, 10, 'wjZ8d'),
    ('Licenciatura en Ciencias Antropológicas (orientación Arqueológica)', 'Anthropology',
     ['Universidad de Buenos Aires (UBA)'],
     'Teledetección y análisis del uso del espacio en el sudeste del valle de Yocavil (Dpto. de Santa María, Prov. de Catamarca).',
     2001, 3, 2009, 4, 2009, 4, 'h8fvn'),
    ('Ingeniería en Sistemas Computacionales', 'Automation & Control Systems',
     ['Instituto Tecnológico de Morelia (ITM)'], 'Evaluación de Seguridad en Redes', 1998, 8, 2004, 6, 2009, 1,
     'biabG'),
    ('Medicina Veterinaria Zootecnista', 'Zoology',
     ['Facultad de Medicina Veterinaria y Zootecnia', 'Universidad Nacional Autónoma de México (UNAM)'],
     'Inducción de la Actividad Ovárica en Borregas Suffolk en Época de Anestro Mediante el Uso de Esponjas Intravaginales Impregnadas con Acetato de Fluorogestona.',
     1980, 1, 1990, 6, 1992, 6, '58Tln'),
    ('Ingeniería en Sistemas Computacionales', 'Automation & Control Systems',
     ['Instituto Tecnológico de Morelia (ITM)'],
     'Implementación del portal Web del CIEco usando un administrador de contenido', 2002, 8, 2007, 12, 2009, 3,
     'c3fhV'),
    ('Licenciatura en Economía', 'Business & Economics', ['Universidad de Sonora'],
     'La industria del bacanora: una oportunidad económica para el desarrollo de la región sierra de Sonora', 1996, 1,
     2000, 1, 2003, 1, 'gb4go'),
    ('Biología', 'Otra', ['Facultad de Ciencias'],
     'Evaluación del Deterioro de la Vegetación en el Sistema Estuarino Chantuto-Teculapa-Panzacola, Chiapas.', 1988, 8,
     1992, 6, 1995, 7, 'df4ty'),
    ('Geografía', 'Physical Geography', ['Colegio de Geografia (Facultad de Filosofía y Letras)'],
     'Los Métodos de Cálculo de Horas Frío: el Método Gómez-Morales', 1979, 8, 1984, 6, 1990, 3, 'ftTrS'),
    ('Licenciatura en Administración de Empresas Agropecuárias', 'Business & Economics',
     ['Escuela de Ciencias Agropecuarias'],
     'Eficiencia Biológica Y Económica Del Proceso De Producción De Papaya En El Trópico Seco De Michoacán', 1995, 9,
     1999, 7, 2000, 7, '16ymf'))

for i in Licenciaturas:
    if len(i[2]) > 1:
        dep_id = Dependencia.objects.filter(nombre=i[2][0], institucion=Institucion.objects.get(nombre=i[2][1]).id)[0].id
    else:
        dep_id = Dependencia.objects.get(nombre=i[2][0]).id
    c = Licenciatura(carrera=ProgramaLicenciatura.objects.get(nombre=i[0]),
                     institucion=Dependencia.objects.get(pk=dep_id).institucion,
                     dependencia=Dependencia.objects.get(pk=dep_id), titulo_tesis=i[3],
                     fecha_inicio=datetime(int(i[4]), int(i[5]), 1), fecha_fin=datetime(int(i[6]), int(i[7]), 28),
                     fecha_grado=datetime(int(i[8]), int(i[9]), 1), usuario=User.objects.get(rfc=i[10]))
    c.save()
    print(c)

ProgramasMaestria = (
    ('Física, Matemáticas y Ciencias de la Tierra', 'Paleontology'),
    ('Análisis y Manejo de Sistemas Ambientales', 'Environmental Sciences & Ecology'),
    ('Antropología Social', 'Anthropology'),
    ('Arqueologia', 'Archaeology'),
    ('Ciencias Agropecuarias y Recursos Naturales', 'Agriculture'),
    ('Ciencias Biológicas', 'Environmental Sciences & Ecology'),
    ('Ciencias de la Geo-información y observación de la Tierra', 'Mathematical & Computational Biology'),
    ('Ciencias de la Tierra', 'Physical Geography'),
    ('Ciencias en Ingeniería Eléctrica con opción en Sistemas Computacionales', 'Engineering'),
    ('Comercio Exterior', 'International Relations'),
    ('Conservación, Ecología y Manejo de Recursos Naturales', 'Environmental Sciences & Ecology'),
    ('Desarrollo Rural Regional', 'Agriculture'),
    ('Economía Aplicada', 'Business & Economics'),
    ('Estudio de Peligros Naturales', 'Imaging Science & Photographic Technology'),
    ('Filosofía', 'Agriculture'),
    ('Geoecología del Paisaje', 'Environmental Sciences & Ecology'),
    ('Geografía', 'Physical Geography'),
    ('Geomática', 'Computer Science'),
    ('Historia de México', 'History'),
    ('Industrial Engineering and management Sciences', 'Engineering'),
    ('Información de Suelos para el manejo de los Recursos Naturales', 'Environmental Sciences & Ecology'),
    ('Maestro en Tecnologías de Información', 'Automation & Control Systems'),
    ('Manejo de Ecosistemas de Zonas Áridas, Zonas Costeras y estudios sobre Biodiversidad.', 'Physical Geography'),
    ('Manejo Integral del Paisaje', 'Physical Geography'),
    ('Posgrado en Geografía', 'Physical Geography'),
    ('Sociologia Política', 'Public Administration'),
    ('Tecnologías de la Información', 'Automation & Control Systems')
)

for i in ProgramasMaestria:
    p = ProgramaMaestria(nombre=i[0], area_conocimiento=AreaConocimiento.objects.get(nombre=i[1]))
    p.save()
    print("agregado programa de maestria " + i[0].upper() + " en area " + i[1].upper())

Maestrias = (
    ('Estudio de Peligros Naturales', 'Imaging Science & Photographic Technology',
     'Faculty of Geo-Information Science and Earth Observation (ITC)',
     'Pixel based and object oriented image analysis in coal fire mapping', 2001, 9, 2003, 3, 2003, 3, 'UiSNj'),
    ('Geografía', 'Physical Geography', 'Colegio de Geografia (Facultad de Filosofía y Letras)',
     'Aplicación de un modelo espacial para la elaboración de escenarios de uso/cobertura del suelo en La Huacana, Michoacán',
     2005, 9, 2015, 1, 2008, 4, 'J8YEd'),
    ('Ciencias de la Geo-información y observación de la Tierra', 'Mathematical & Computational Biology',
     'International Institute for Geo-Information Sciences and Earth Observation (ITC)',
     'The applicability of a stochastic-dynamic model of land use change in a Mexican dry tropical region', 2005, 9,
     2007, 2, 2007, 3, 'J8YEd'),
    ('Manejo de Ecosistemas de Zonas Áridas, Zonas Costeras y estudios sobre Biodiversidad.', 'Physical Geography',
     'Universidad Autónoma de Baja California', 'Análisis de la ordenación del territorio en México y España', 2007, 8,
     2009, 6, 2009, 6, 'hnSDn'),
    ('Geoecología del Paisaje', 'Environmental Sciences & Ecology', 'Instituto de Ecología y Sistemática',
     'Diversidad de Ecosistemas en el Archipiélago de Camagüey, Cuba.', 1994, 9, 1996, 11, 1996, 11, '9hUCZ'),
    ('Maestro en Tecnologías de Información', 'Automation & Control Systems',
     'Universidad Interamericana para el Desarrollo, Morelia (UNID Morelia)',
     'Propuesta Estratégica y Análisis de Desempeño de Herramientas de Monitoreo y de Control para Redes Publicas en Institutos de Investigación',
     2007, 9, 2009, 7, 2009, 12, 'n80rn'),
    ('Manejo Integral del Paisaje', 'Physical Geography', 'Colegio de Geografia (Facultad de Filosofía y Letras)',
     'Transformación de los paisajes agrícolas durante últimos 20 años en la cuenca de Lago de Pátzcuaro y sus tendencias a la permanencia o desaparición.',
     2013, 1, 2015, 1, 2015, 1, 'sNeKu'),
    ('Ciencias Biológicas', 'Agriculture', 'Facultad de Ciencias',
     'El sistema alimentario del maiz en Pátzcuaro Michoacán', 2004, 8, 2006, 6, 2007, 3, 'ubFaE'),
    ('Información de Suelos para el manejo de los Recursos Naturales', 'Environmental Sciences & Ecology',
     'Universidad Mayor se San Simón',
     'La Ecología del Paisaje en Relación con los Sistemas de Producción en el Valle de Sacaba. Cochabamba- Bolivia',
     2002, 1, 2002, 12, 2002, 12, 'Ersp5'),
    ('Análisis y Manejo de Sistemas Ambientales', 'Environmental Sciences & Ecology',
     'International Institute for Geo-Information Sciences and Earth Observation (ITC)',
     'Polylepis Forest Condition Related with Two Threatening Factors', 2003, 1, 2004, 3, 2004, 3, 'Ersp5'),
    ('Sociologia Política', 'Public Administration', 'Universidad Autónoma de Querétaro',
     'La cultura politica de los estudiantes universitarios', 1995, 9, 1997, 8, 2001, 5, 'Yl5I4'),
    ('Arqueologia', 'Archaeology', 'Universidad París 1 Panteón-Sorbona',
     'Comparación entre los Pames y los Guamares según las fuentes arqueológicas y etnohistóricas.', 2004, 9, 2005, 6,
     2005, 6, '7Gs53'),
    ('Ciencias de la Tierra', 'Geology', 'Instituto de Geología',
     'Dinámica de la Erosión/Sedimentación en la Época Prehispánica y Periodo Colonial. Reconstrucción de las condiciones Paleoambientales en el Valle de Teotihuacán (Estado de México)',
     2009, 8, 2010, 7, 2014, 7, 'EeGJW'),
    ('Geografia', 'Physical Geography', 'Universidad Northwestern', '-', 1970, 9, 1971, 8, 1971, 9, 'dNnfH'),
    ('Historia de México', 'History', 'Instituto de Investigaciones Históricas',
     'Paisaje, territorio y paisaje ritual: La Huasteca potosina. Estudio de Geografía histórica.', 2006, 3, 2008, 3,
     2008, 8, 'fEVor'),
    ('Industrial Engineering and management Sciences', 'Engineering', 'Universidad Northwestern', 'Delphi Technique',
     1971, 1, 1972, 6, 1972, 6, 'YxU7H'),
    ('Comercio Exterior', 'International Relations', 'Instituto de Investigaciones Económicas y Empresariales (ININEE)',
     '"Competitividad de la industria electrónica de México y China en el mercado de Estados Unidos: 1993-2005"', 2007,
     3, 2009, 2, 2009, 8, 'usmv1'),
    ('Filosofía', 'Agriculture', 'Facultad de Filosofía "Samuel Ramos"',
     'Cultura del maíz: impacto a la soberanía alimentaria por la entrada del maíz genéticamente modificado en México',
     2013, 1, 2015, 6, 2015, 6, 'sNeKu'),
    ('Ciencias Biológicas', 'Environmental Sciences & Ecology', 'Facultad de Ciencias',
     'Estructura y composición de la selva baja caducifolia de Huautla, Morelos', 2006, 8, 2008, 7, 2009, 6, '4th7o'),
    ('Física, Matemáticas y Ciencias de la Tierra', 'Paleontology', 'Instituto de Geología',
     'Toposecuencia de paleosuelos volcánicos como herramienta para la reconstrucción paleoambiental del Cuaternario tardío en Tlaxcala',
     2007, 8, 2009, 7, 2010, 4, '6ESlj'),
    ('Antropología Social', 'Anthropology', 'El Colegio de Michoacán, A.C. (COLMICH)',
     'El dilema de los comunes. Un estudio de la crisis múltiple  en la  Meseta  Purepecha', 1982, 2, 1984, 2, 1996, 1,
     '88SSU'),
    ('Conservación, Ecología y Manejo de Recursos Naturales', 'Environmental Sciences & Ecology',
     'Instituto Tecnológico y de Estudios Superiores de Monterrey, Campus Guaymas (ITESM, Campus Guaymas)',
     'Regionalización Geomorfológica y de Paisajes de la Zona Costera entre Guaymas y Agiabampo, Sonora, México', 1994,
     1, 1996, 12, 1997, 1, 'wjZ8d'),
    ('Tecnologías de la Información', 'Automation & Control Systems',
     'Universidad Interamericana para el Desarrollo, Morelia (UNID Morelia)',
     'Gestión de proyectos mediante PMBok para el Desarrollo de software Kurhanguni  "Análisis de la participación comunitaria en proyectos para el desarrollo rural"',
     2011, 8, 2012, 12, 2013, 6, 'biabG'),
    ('Ciencias Agropecuarias y Recursos Naturales', 'Agriculture', 'Universidad de Queensland',
     'A multidimensional approach to poverty among farmers with small holdings', 1990, 1, 1995, 1, 2001, 12, '58Tln'),
    ('Economía Aplicada', 'Business & Economics', 'Universidad Autónoma de Barcelona (UAB)',
     'A contingent valuation exercise with a fix bid and varying environmental quality levels', 2004, 9, 2006, 9, 2007,
     1, 'gb4go'),
    ('Posgrado en Geografía', 'Physical Geography', 'Centro de Investigaciones en Geografía Ambiental (CIGA)',
     'Estado Ambiental de la Región Bajío, Michoacán en el periodo 1990, 2000 y 2010. México', 2012, 8, 2015, 12, 2016,
     5, 'zF8gk'),
    ('Ciencias en Ingeniería Eléctrica con opción en Sistemas Computacionales', 'Engineering',
     'Facultad de Ingeniería Eléctrica (FIE)', 'Compresión de Bases de Datos Métricas', 2011, 3, 2013, 1, 2013, 8,
     'c3fhV'),
    ('Geomática', 'Computer Science', 'Wageningen University and Research Centre',
     'Search and space theory as the foundations for the design of an object-oriented GIS', 1990, 10, 1992, 10, 1992,
     10, 'ftTrS'),
    ('Desarrollo Rural Regional', 'Agriculture', 'Universidad Autónoma Chapingo',
     'Estrategias Productivas, Comerciales Y De Vida De Los Productores De Mango En Apatzingán, Michoacán, México.',
     2002, 9, 2004, 7, 2005, 4, '16ymf'))
#             0                     1                     2                               3                                                                                             3       4   5    6   7    8   9     10


for i in Maestrias:
    m = Maestria(programa=ProgramaMaestria.objects.get(nombre=i[0]),
                 institucion=Dependencia.objects.get(nombre=i[2]).institucion,
                 dependencia=Dependencia.objects.get(nombre=i[2]),
                 titulo_tesis=i[3], fecha_inicio=datetime(int(i[4]), int(i[5]), 1),
                 fecha_fin=datetime(int(i[6]), int(i[7]), 28), fecha_grado=datetime(int(i[8]), int(i[9]), 1),
                 usuario=User.objects.get(rfc=i[10]))
    m.save()
    print(m)

ProgramasDoctorado = (
    ('Física, Matemáticas y Ciencias de la Tierra', 'Mathematical & Computational Biology'),
    ('Análisis Geográfico Regional y Geografía Física', 'Physical Geography'),
    ('Arqueología', 'Archaeology'),
    ('Ciencias Ambientales / Sociología Ambiental', 'Environmental Sciences & Ecology'),
    ('Ciencias Biológicas', 'Developmental Biology'),
    ('Ciencias de la Tierra', 'Physical Geography'),
    ('Ciencias en Planificación de Empresas y Desarrollo Regional', 'Business & Economics'),
    ('Desarrollo Regional', 'Business & Economics'),
    ('Doctorado en Agroecología', 'Agriculture'),
    ('Doctorado en Ciencias de la Tierra (Geología Ambiental)', 'Geology'),
    ('Doctorado en Ciencias Sociales, especialidad en Antropología Social', 'Anthropology'),
    ('Ecología', 'Environmental Sciences & Ecology'),
    ('Ecología y Manejo de Recursos Naturales', 'Environmental Sciences & Ecology'),
    ('Ecología y Manejo de Recursos Natutales', 'Environmental Sciences & Ecology'),
    ('Ecología y Medio Ambiente', 'Environmental Sciences & Ecology'),
    ('Economía Aplicada', 'Business & Economics'),
    ('Geografía', 'Physical Geography'),
    ('Ingeniería Agrícola y yso integral del agua', 'Agriculture'),
    ('Medio Ambiente y Desarrollo', 'Environmental Sciences & Ecology'),
    ('Posgrado en Ciencias Biológicas', 'Developmental Biology'),
    ('Segmentación de Imagenes y clasificación por objetos', 'Imaging Science & Photographic Technology'),
    ('Technology and Development', 'Science & Technology Other Topics'))

for i in ProgramasDoctorado:
    p = ProgramaDoctorado(nombre=i[0], area_conocimiento=AreaConocimiento.objects.get(nombre=i[1]))
    p.save()
    print("agregado programa de doctorado " + i[0].upper() + " en area " + i[1].upper())

Doctorados = (
    ('Análisis Geográfico Regional y Geografía Física', 'Universidad Complutense de Madrid',
     'Los espacios forestales de la Sierra de Angangueo (Michoacán-Estado de México), México. Una visión geográfica',
     1996, 1, 2001, 10, '2001', 10, 'Y9jOf'),
    ('Medio Ambiente y Desarrollo', 'Universidad Autónoma de Baja California',
     'Modelo de evaluación de la factibilidad para la Agenda Local 21 en países en desarrollo', 2009, 8, 2012, 9,
     '2012', 9, 'hnSDn'),
    ('Ecología y Manejo de Recursos Naturales', 'Instituto de Ecología, A.C. (INECOL)',
     'Relación entre la Heterogeneidad Geoecológica y la Biodiversidad en Ecosistemas Costeros Tropicales.', 1997, 1,
     2001, 1, '2004', 4, '9hUCZ'),
    ('Geografía', 'Universidad de California Davis',
     'Maize population structure and diversity related to ethnolinguistic variation', 2009, 9, 2014, 7, '2014', 9,
     'ubFaE'),
    ('Doctorado en Agroecología', 'Universidad de Antioquia',
     'Sustentabilidad y Sistemas de Manejo en Comunidades Indígenas en Chile', 2011, 3, 2015, 11, '2015', 11, 'sNeKu'),
    ('Ciencias Ambientales / Sociología Ambiental', 'University of East Anglia',
     'The socio-cultural dimension of flood vulnerability in a periurban community in central Mexico', 2006, 8, 2010,
     12, '2011', 3, 'Yl5I4'),
    ('Arqueología', 'Universidad París 1 Panteón-Sorbona',
     'La ocupación del territorio en la región de Acámbaro (Guanajuato- Michoacán) entre el Posclásico tardío  y el siglo XVI.',
     2005, 9, 2012, 12, '2012', 12, '7Gs53'),
    ('Ciencias de la Tierra', 'Instituto de Geología',
     'Dinámica de la Erosión/Sedimentación en la Época Prehispánica y Periodo Colonial. Reconstrucción de las condiciones Paleoambientales en el Valle de Teotihuacán (Estado de México)',
     2010, 8, 2014, 7, '2014', 7, 'EeGJW'),
    ('Geografía', 'Universidad Northwestern',
     'The Diffusion of Regional Underdevelop¬ment; Articulation of Capital and Peasantry in Sukumaland, Tanzania', 1971,
     9, 1980, 8, '1980', 8, 'dNnfH'),
    ('Geografía', 'Centro de Investigaciones en Geografía Ambiental (CIGA)',
     'Historia ambiental de paisajes latinoamericanos: abandono y reapropiación. Casos en México y Argentina', 2009, 8,
     2014, 7, '2015', 7, 'fEVor'),
    ('Technology and Development', 'University of Twente', 'Social Forestry as  Sustainable Development', 1989, 6, 1994,
     6, '1994', 6, 'YxU7H'),
    ('Desarrollo Regional', 'Instituto de Investigaciones Económicas y Empresariales (ININEE)',
     '"Sistemas de innovación y reservas de la biosfera: acciones para el desarrollo regional sustentable en Zicuirán-Infiernillo"',
     2010, 3, 2014, 2, '2014', 8, 'usmv1'),
    ('Ciencias Biológicas', 'Instituto de Investigaciones en Ecosistemas y Sustentabilidad (IIES)',
     'Sistemas agroforestales y conservación de biodiversidad en el Valle de Tehuacán, Cuicatlán', 2010, 1, 2014, 12,
     '2015', 2, '4th7o'),
    ('Ecología y Medio Ambiente', 'Universidad Autónoma de Madrid',
     'El paisaje en América Latina. Experiencia de valoración participada de paisajes visuales para la gestión ambiental en La Habana, Cuba',
     1999, 10, 2007, 4, '2007', 4, 'prgh0'),
    ('Posgrado en Ciencias Biológicas', 'Facultad de Ciencias',
     'Análisis multi-escalar de los patrones espaciales de oferta y demanda de leña para uso residencial en México',
     2003, 9, 2008, 7, '2008', 6, 'DgFdm'),
    ('Física, Matemáticas y Ciencias de la Tierra', 'Instituto de Geología',
     'Impacto Cultural Y Natural En Las Secuencias Edafosedimentarias Del Holoceno En La Región Suroriental De México. Un Estudio Geoarqueológico En Las Tierras Bajas Mayas',
     2010, 8, 2014, 7, '2014', 8, '6ESlj'),
    ('Segmentación de Imagenes y clasificación por objetos', 'Instituto de Geografía',
     'Object based image analysis with remote sensing images', 2004, 3, 2008, 9, '2015', 1, 'UiSNj'),
    ('Doctorado en Ciencias Sociales, especialidad en Antropología Social',
     'Centro de Investigaciones y Estudios Superiores en Antropología Social (CIESAS)',
     'La transformación corporativa del comunalismo forestal', 2000, 1, 2015, 2, '2005', 2, '88SSU'),
    ('Doctorado en Ciencias de la Tierra (Geología Ambiental)', 'Instituto de Geofísica',
     'Implicaciones del cambio de cobertura vegetal y uso del suelo en el balance hídrico a nivel regional. El caso de la cuenca del lago de Cuitzeo',
     1998, 9, 2002, 8, '2002', 12, 'wjZ8d'),
    ('Arqueología', 'Universidad de Buenos Aires (UBA)',
     'Habitar una región. Espacialidad arquitectónica y construcción de paisajes en Andalhuala, valle de Yocavil (Catamarca, Argentina).',
     2010, 3, 2015, 4, '2015', 4, 'h8fvn'),
    ('Ecología', 'Instituto de Ecología, A.C. (INECOL)',
     'Diversidad acústica de la Biofonía y degradación del bosque tropical: ¿Cómo los análisis del paisaje sonoro pueden complementar la evaluación de la integridad ecosistémica?',
     2016, 1, 3001, 1, 3001, 1, '9OzFa'),
    ('Ciencias en Planificación de Empresas y Desarrollo Regional', 'Universidad de Queensland',
     'Effects of urban growth in the process of impoverishment of campesinos´ households living in peri-urban areas: A case study in Mexico City.',
     1900, 1, 1900, 1, '2007', 7, '58Tln'),
    ('Economía Aplicada', 'Universidad Autónoma de Barcelona (UAB)',
     'Value equivalency analysis: quantity compensation, distance decay and time treatment', 2007, 2, 2010, 9, '2011',
     1, 'gb4go'),
    ('Ecología y Manejo de Recursos Natutales', 'Instituto de Ecología, A.C. (INECOL)',
     'Manejo de la zona riparia de la cuenca de río Cutizmala, Jal,', 2004, 8, 2014, 12, '2014', 12, 'df4ty'),
    ('Geografía', 'Colegio de Geografia (Facultad de Filosofía y Letras)',
     'Definition of a minimum set of spatial relations', 1996, 1, 2015, 11, '2015', 11, 'ftTrS'),
    ('Ingeniería Agrícola y yso integral del agua', 'Universidad Autónoma Chapingo',
     'Análisis Normativo Y Práctico De La Fertilidad Química Y Física Edáfica En La Agricultura Orgánica Y Convencional',
     2007, 9, 2010, 7, '2010', 12, '16ymf'))
#                              0                                1                                                                                          2                                            3   4   5    6     7     8     9

for i in Doctorados:
    m = Doctorado(programa=ProgramaDoctorado.objects.get(nombre=i[0]),
                  institucion=Dependencia.objects.get(nombre=i[1]).institucion,
                  dependencia=Dependencia.objects.get(nombre=i[1]), titulo_tesis=i[2],
                  fecha_inicio=datetime(int(i[3]), int(i[4]), 1), fecha_fin=datetime(int(i[5]), int(i[6]), 28),
                  fecha_grado=datetime(int(i[7]), int(i[8]), 1), usuario=User.objects.get(rfc=i[9]))
    m.save()
    print(m)

ningunproyecto = Proyecto(nombre='Ninguno', status='OTRO', clasificacion='OTRO', organizacion='INDIVIDUAL',
                          modalidad='OTRA', fecha_inicio=datetime(1900, 1, 1), fecha_fin=datetime(9900, 1, 1))
ningunproyecto.save()

postdoctorados = (
    ('Centro de Investigaciones en Geografía Ambiental (CIGA)', 2014, 3, 2015, 12, 'hnSDn'),
    ('Instituto de Geografía', 2004, 4, 2006, 4, '9hUCZ'),
    ('Centro de Investigaciones en Geografía Ambiental (CIGA)', 2012, 9, 2014, 8, 'Yl5I4'),
    ('Centro de Investigaciones en Geografía Ambiental (CIGA)', 2014, 9, 2015, 12, '7Gs53'),
    ('Centro de Investigaciones en Geografía Ambiental (CIGA)', 2014, 9, 2017, 8, 'EeGJW'),
    ('Universidad Nacional Autónoma de México (UNAM)', 2008, 9, 2010, 8, 'DgFdm'),
    ('Instituto de Investigaciones en Ecosistemas y Sustentabilidad (IIES)', 2008, 9, 2010, 8, 'UiSNj'),
    ('Universidad de Hokkaido', 2011, 1, 2013, 4, 'UiSNj'),
    ('Instituto de Geografía, Unidad Morelia (UNAM Morelia)', 2003, 2, 2006, 3, 'wjZ8d'),
    ('Universidad Nacional Autónoma de México (UNAM)', 2016, 3, 2017, 2, 'h8fvn'),
    ('Universidad Nacional Autónoma de México (UNAM)', 2011, 10, 2013, 12, 'gb4go'),
    ('Universidad Nacional Autónoma de México (UNAM)', 2014, 1, 2015, 12, 'gb4go'),
    ('Centro de Investigaciones en Geografía Ambiental (CIGA)', 2015, 3, 2017, 2, 'ubFaE'),
    ('Centro de Investigaciones en Geografía Ambiental (CIGA)', 2016, 8, 2017, 7, 'df4ty'),
    ('Universidad Michoacana de San Nicolás de Hidalgo (UMSNH)', 2013, 8, 2014, 7, '16ymf'),
    ('Universidad Nacional Autónoma de México (UNAM)', 2016, 8, 2016, 12, '16ymf'))

for i in postdoctorados:
    p = PostDoctorado(nombre=str(uuid.uuid1()), proyecto=Proyecto.objects.get(nombre='Ninguno'),
                      area_conocimiento=AreaConocimiento.objects.get(nombre='Otra'),
                      institucion=Dependencia.objects.get(nombre=i[0]).institucion,
                      dependencia=Dependencia.objects.get(nombre=i[0]),
                      fecha_inicio=datetime(i[1], i[2], 1), fecha_fin=datetime(i[3], i[4], 1),
                      usuario=User.objects.get(rfc=i[5]))
    p.save()
    print(p)

nombramientos = (
    ('N0000', 'Ninguno'),
    ('D0196', 'Profesor Extraordinario'),
    ('I0196', 'Investigador Extraordinario'),

    ('D1200', 'Ayudante de Profesor de Asignatura A'),
    ('D1300', 'Ayudante de Profesor de Asignatura B'),

    ('D2199', 'Profesor Emérito'),
    ('I2199', 'Investigador Emérito'),

    ('D3121', 'Ayudante de Profesor A, Medio tiempo'),
    ('D3227', 'Ayudante de Profesor B, Medio tiempo'),
    ('D3333', 'Ayudante de Profesor C, Medio tiempo'),
    ('D3446', 'Ayudante de Profesor A, Tiempo Completo'),
    ('D3558', 'Ayudante de Profesor B, Tiempo Completo'),
    ('D3667', 'Ayudante de Profesor C, Tiempo Completo'),

    ('I3121', 'Ayudante de Investigador A, Medio tiempo'),
    ('I3227', 'Ayudante de Investigador B, Medio tiempo'),
    ('I3333', 'Ayudante de Investigador C, Medio tiempo'),
    ('I3446', 'Ayudante de Investigador A, Tiempo Completo'),
    ('I3558', 'Ayudante de Investigador B, Tiempo Completo'),
    ('I3667', 'Ayudante de Investigador C, Tiempo Completo'),

    ('D4100', 'Profesor de Asignatura A'),
    ('D4200', 'Profesor de Asignatura B'),

    ('D4310', 'Profesor de Enseñanza Media Superior A'),
    ('D4420', 'Profesor de Enseñanza Media Superior B'),

    ('D5144', 'Profesor Asociado A, Medio tiempo'),
    ('D5251', 'Profesor Asociado B, Medio tiempo'),
    ('D5356', 'Profesor Asociado C, Medio tiempo'),
    ('D5480', 'Profesor Asociado A, Tiempo Completo'),
    ('D5584', 'Profesor Asociado B, Tiempo Completo'),
    ('D5686', 'Profesor Asociado C, Tiempo Completo'),

    ('I5144', 'Investigador Asociado A, Medio tiempo'),
    ('I5251', 'Investigador Asociado B, Medio tiempo'),
    ('I5356', 'Investigador Asociado C, Medio tiempo'),
    ('I5480', 'Investigador Asociado A, Tiempo Completo'),
    ('I5584', 'Investigador Asociado B, Tiempo Completo'),
    ('I5686', 'Investigador Asociado C, Tiempo Completo'),

    ('D6160', 'Profesor Titular A, Medio tiempo'),
    ('D6270', 'Profesor Titular B, Medio tiempo'),
    ('D6376', 'Profesor Titular C, Medio tiempo'),
    ('D6489', 'Profesor Titular A, Tiempo Completo'),
    ('D6593', 'Profesor Titular B, Tiempo Completo'),
    ('D6696', 'Profesor Titular C, Tiempo Completo'),

    ('I6160', 'Investigador Titular A, Medio tiempo'),
    ('I6270', 'Investigador Titular B, Medio tiempo'),
    ('I6376', 'Investigador Titular C, Medio tiempo'),
    ('I6489', 'Investigador Titular A, Tiempo Completo'),
    ('I6593', 'Investigador Titular B, Tiempo Completo'),
    ('I6696', 'Investigador Titular C, Tiempo Completo'),

    ('D7117', 'Técnico Académico Auxiliar (docencia) A, Medio tiempo'),
    ('D7220', 'Técnico Académico Auxiliar (docencia) B, Medio tiempo'),
    ('D7327', 'Técnico Académico Auxiliar (docencia) C, Medio tiempo'),
    ('D7439', 'Técnico Académico Auxiliar (docencia) A, Tiempo Completo'),
    ('D7544', 'Técnico Académico Auxiliar (docencia) B, Tiempo Completo'),
    ('D7658', 'Técnico Académico Auxiliar (docencia) C, Tiempo Completo'),

    ('D8133', 'Técnico Académico Asociado (docencia) A, Medio tiempo'),
    ('D8242', 'Técnico Académico Asociado (docencia) B, Medio tiempo'),
    ('D8346', 'Técnico Académico Asociado (docencia) C, Medio tiempo'),
    ('D8467', 'Técnico Académico Asociado (docencia) A, Tiempo Completo'),
    ('D8578', 'Técnico Académico Asociado (docencia) B, Tiempo Completo'),
    ('D8682', 'Técnico Académico Asociado (docencia) C, Tiempo Completo'),

    ('D9151', 'Técnico Académico Titular (docencia) A, Medio tiempo'),
    ('D9254', 'Técnico Académico Titular (docencia) B, Medio tiempo'),
    ('D9360', 'Técnico Académico Titular (docencia) C, Medio tiempo'),
    ('D9484', 'Técnico Académico Titular (docencia) A, Tiempo Completo'),
    ('D9585', 'Técnico Académico Titular (docencia) B, Tiempo Completo'),
    ('D9689', 'Técnico Académico Titular (docencia) C, Tiempo Completo'),

    ('I7117', 'Técnico Académico Auxiliar (investigación) A, Medio tiempo'),
    ('I7220', 'Técnico Académico Auxiliar (investigación) B, Medio tiempo'),
    ('I7327', 'Técnico Académico Auxiliar (investigación) C, Medio tiempo'),
    ('I7439', 'Técnico Académico Auxiliar (investigación) A, Tiempo Completo'),
    ('I7544', 'Técnico Académico Auxiliar (investigación) B, Tiempo Completo'),
    ('I7658', 'Técnico Académico Auxiliar (investigación) C, Tiempo Completo'),

    ('I8133', 'Técnico Académico Asociado (investigación) A, Medio tiempo'),
    ('I8242', 'Técnico Académico Asociado (investigación) B, Medio tiempo'),
    ('I8346', 'Técnico Académico Asociado (investigación) C, Medio tiempo'),
    ('I8467', 'Técnico Académico Asociado (investigación) A, Tiempo Completo'),
    ('I8578', 'Técnico Académico Asociado (investigación) B, Tiempo Completo'),
    ('I8682', 'Técnico Académico Asociado (investigación) C, Tiempo Completo'),

    ('I9151', 'Técnico Académico Titular (investigación) A, Medio tiempo'),
    ('I9254', 'Técnico Académico Titular (investigación) B, Medio tiempo'),
    ('I9360', 'Técnico Académico Titular (investigación) C, Medio tiempo'),
    ('I9484', 'Técnico Académico Titular (investigación) A, Tiempo Completo'),
    ('I9585', 'Técnico Académico Titular (investigación) B, Tiempo Completo'),
    ('I9689', 'Técnico Académico Titular (investigación) C, Tiempo Completo'))

for i in nombramientos:
    n = Nombramiento(clave=i[0], nombre=i[1])
    n.save()
    print(n)

cargos = (
    (False, 'Diseñador Instruccional Y Tutor Universidad Virtual Michoacán', False),
    (False, False, 'Otro'),
    (False, False, 'Pensionado Jubilado Pemex'),
    (False, False, 'Subdirectora de Sistemas de Información Geográfica'),
    (False, False, 'Jefe de Departamento de Migración Interna'),
    (False, False, 'Colaborador'),
    (False, False, 'Jefe de Departamento'),
    (False, False, 'Digitalizador'),
    (False, False, 'Analista'),
    (False, False, 'Técnico de investigación'),
    (False, False, 'Responsable de Computo'),
    ('Investigador Agregado', False, False),
    (False, 'Subdirector de Estudios del Medio Biofísico', False),
    ('Investigador Asociado', False, False),
    ('Investigador Titular', False, False),
    (False, False, 'Encargado del Área de Computación'),
    (False, False, 'Servicio Social'),
    ('Catedrático CONACYT', False, False),
    ('Investigador Postdoctoral', False, False),
    (False, False, 'Levantamiento y elaboración de mapas de suelos'),
    (False, False, 'Plan de mejora de los caminos rurales de Catalunya'),
    (False, 'Responsable de Calidad', False),
    (False, 'Secretaría Técnica', False),
    (False, False, 'Miembro de la Mesa Directiva del Colegio del Personal Académico'),
    (False, False, 'Representante de los técnicos académicos ante el Consejo Interno'),
    (False, False, 'Corresponsable del Proyecto de Creación de la Licenciatura en Geohistoria'),
    (False, False, 'Comisión para la elaboración del Nuevo Plan de la Licenciatura en Ciencias Ambientales'),
    (False, False, 'Representante del Director ante el Consejo Académico de Área en Ciencias Sociales'),
    (False, False,
     'Representante del personal académico del CIGA ante el Consejo Académico de la Licenciatura en Ciencias Ambientales'),
    (False, False, 'Miembro del Comité Académico Asesor de la Licenciatura en Ciencias Ambientales'),
    (False, False, 'Comisión para la Creación de la Licenciatura en Estudios Sociales y Gestión Local'),
    (False, False, 'Miembro de la Comisión para la Creación del Bachillerato Regional UNAM Michoacán'),
    (False, False, 'Miembro del Comité Académico Asesor de la Licenciatura en Geohistoria'),
    (False, False, 'Miembro del Comité Académico Asesor de la Licenciatura en Estudios Sociales y Gestión Local'),
    (False, False, 'Miembro del Comité de Publicaciones, representante del Área de Ciencias Sociales'),
    (False, False, 'Editor Académico del Comité Editorial'),
    (False, False, 'Representante académico ante el Comité Académico del Posgrado en Geografía'),
    (False, 'Coordinador de la Licenciatura en Geohistoria', False),
    (False, 'Jefe del Departamento de Docencia', False),
    (False, False, 'Lecturer'),
    (False, False, 'Unversitaire Hoog Docent'),
    ('Profesor', False, False),
    ('Profesor invitado', False, False),
    ('Profesor Investigador', False, False),
    (False, False, 'Administrador de Sistemas de información (SIGs)'),
    (False, False, 'Técico Superior'),
    (False, False, 'Encargada de Sistemas'),
    (False, False, 'Técnico Informático de Zona'),
    (False, False, 'Encargada del Área de Soporte Técnico'),
    (False, False, 'Residencia Profesional'),
    (False, False,
     'Conference Director. Miembro por invitación de la International Society for the Study of Religion, Nature and Culture (ISSRNC)'),
    (False, False,
     'Miembro fundador, por invitación, de la Asociación de Historiadores de las Ciencias y las Humanidades A.C. (HCyH). Asamblea General Constitutiva, celebrada en el Instituto de Geografía, UNAM, el 19 de abril de 2007.'),
    (False, False, 'Miembro regular de la Conference of Latin Americanist Geographers (CLAG).'),
    (False, 'Director de Cooperación Académica', False),
    (False, 'Subdirector de recursos genéticos', False),
    (False, False, 'Servicio Profesional en la Unidad de Cómputo'),
    (False, False, 'Pasante en desarrollo Web'),
    (False, False, 'Residente Profesional en desarrollo Web'),
    (False, False, 'Consultor Externo en Soporte Técnico'),
    (False, False, 'Servicio Profesional de apoyo a Control Escolar'),
    (False, False, 'Desarrollador Web'),
    (False, False, 'Jefe del Laboratorio de Cómputo'),
    (False, 'Jefe del Laboratorio de Sistemas de Información Geográfica y Percepción Remota', False),
    ('Coordinador del Laboratorio de Análisis Espacial', False, False),
    (False, 'Secretario Técnico', False),
    (False, False, 'Coordinador de Proyecto'),
    (False, False, 'Technical Officer'),
    ('Cátedras CONACYT', False, False),
    ('Investigador', False, False),
    (False, False, 'Profesor De Maestría En Derecho'),
    (False, False, 'Evaluador Del Proyecto')
)

for i in cargos:
    if not i[0] and not i[1] and i[2]:
        c = Cargo(nombre=i[2], tipo_cargo='OTRO')
        c.save()
        print(c)
    elif not i[0] and i[1] and not i[2]:
        c = Cargo(nombre=i[1], tipo_cargo='ADMINISTRATIVO')
        c.save()
        print(c)
    elif i[0] and not i[1] and not i[2]:
        c = Cargo(nombre=i[0], tipo_cargo='ACADEMICO')
        c.save()
        print(c)
    else:
        raise Exception

experiencias = (
    ('Ninguno', False, False, 'Diseñador Instruccional Y Tutor Universidad Virtual Michoacán', False,
     'Universidad Virtual del Estado de Michoacán (UNIVIM)', 2014, 1, 0, 0, '16ymf'),
    ('Investigador Titular B, Tiempo completo', True, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2014, 3, 0, 0, 'Y9jOf'),
    ('Ninguno', True, False, False, 'Pensionado Jubilado Pemex', 'Petróleos Mexicanos (PEMEX)', 1968, 6, 0, 0, '16ymf'),
    ('Técnico Académico Asociado (docencia) C, Tiempo Completo', False, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2011, 4, 2016, 3, 'J8YEd'),
    ('Profesor de Asignatura A', False, False, False, 'Otro',
     'Instituto de Investigaciones en Ecosistemas y Sustentabilidad (IIES)', 2010, 7, 2010, 12, 'J8YEd'),
    ('Ninguno', False, False, False, 'Subdirectora de Sistemas de Información Geográfica',
     'Instituto Nacional de Ecología y Cambio Climático (INECC)', 2000, 2, 2005, 9, 'J8YEd'),
    ('Ninguno', False, False, False, 'Jefe de Departamento de Migración Interna',
     'Consejo Nacional de Población (CONAPO)', 1999, 6, 2000, 1, 'J8YEd'),
    ('Ninguno', False, False, False, 'Colaborador', 'El Colegio de México, A.C.', 1998, 5, 1999, 7, 'J8YEd'),
    ('Ninguno', False, False, False, 'Colaborador', 'Instituto de Biología', 1997, 8, 1998, 4, 'J8YEd'),
    ('Ninguno', False, False, False, 'Colaborador', 'Instituto para el Desarrollo Sustentable en Mesoamérica, A.C.',
     1997, 5, 1997, 7, 'J8YEd'),
    ('Ninguno', False, False, False, 'Jefe de Departamento', 'Instituto Federal Electoral', 1994, 10, 1995, 1, 'J8YEd'),
    ('Ninguno', False, False, False, 'Colaborador', 'Instituto de Geografía', 1993, 1, 1994, 12, 'J8YEd'),
    ('Ninguno', False, False, False, 'Colaborador', 'Instituto de Ecología', 1991, 1, 1992, 12, 'J8YEd'),
    (
        'Ninguno', False, False, False, 'Digitalizador', 'Sistemas de Información Geográfica, S.A. de C.V.', 1989, 10,
        1990,
        12, 'J8YEd'),
    ('Ninguno', False, False, False, 'Analista', 'Instituto Nacional de Estadística y Geografía (INEGI)', 1989, 1, 1989,
     8, 'J8YEd'),
    ('Investigador Titular A, Medio tiempo', True, False, False, 'Otro',
     'Coordinación de la Investigación Científica (CIC)', 1995, 2, 0, 0, 'f4r8Q'),
    ('Ninguno', False, False, False, 'Técnico de investigación', 'Universidad Autónoma de Baja California', 2012, 10,
     2014, 2, 'hnSDn'),
    ('Investigador Asociado A, Tiempo Completo', False, 'Investigador Agregado', False, False,
     'Instituto de Ecología y Sistemática', 1988, 2, 2001, 11, '9hUCZ'),
    ('Ninguno', False, False, 'Subdirector de Estudios del Medio Biofísico', False,
     'Instituto Nacional de Ecología y Cambio Climático (INECC)', 2001, 11, 2004, 4, '9hUCZ'),
    ('Investigador Asociado C, Tiempo Completo', False, 'Investigador Asociado', False, False, 'Instituto de Geografía',
     2004, 4, 2006, 4, '9hUCZ'),
    ('Investigador Titular A, Tiempo Completo', True, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2007, 3, 0, 0, '9hUCZ'),
    ('Técnico Académico Titular (docencia) B, Tiempo Completo', True, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2014, 10, 0, 0, 'n80rn'),
    ('Técnico Académico Titular (docencia) A, Tiempo Completo', True, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2011, 6, 2014, 10, 'n80rn'),
    ('Técnico Académico Asociado (docencia) C, Tiempo Completo', False, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2007, 3, 2011, 6, 'n80rn'),
    (
        'Ninguno', False, False, False, 'Responsable de Computo',
        'Centro de Investigaciones en Geografía Ambiental (CIGA)',
        2006, 3, 2007, 2, 'n80rn'),
    ('Ninguno', False, False, False, 'Encargado del Área de Computación', 'Signos Diseño & Publicidad', 2001, 1, 2005,
     12, 'n80rn'),
    ('Ninguno', False, False, False, 'Servicio Social', 'Instituto Tecnológico de Morelia (ITM)', 2004, 6, 2004, 12,
     'n80rn'),
    ('Ninguno', False, False, False, 'Servicio Social',
     'Centro de Bachillerato Tecnológico Agropecuario #89 José Vasconcelos (CBTA 89)', 1999, 2, 1999, 8, 'n80rn'),
    (
        'Técnico Académico Auxiliar (investigación) A, Medio tiempo', False, False, False, 'Otro',
        'Instituto de Geografía',
        1994, 1, 1996, 2, 'GUKjy'),
    ('Investigador Asociado C, Medio tiempo', False, False, False, 'Otro', 'Universidad Autónoma de Campeche (UACAM)',
     1996, 2, 2000, 3, 'GUKjy'),
    ('Investigador Asociado C, Medio tiempo', False, False, False, 'Otro',
     'Instituto de Geografía, Unidad Morelia (UNAM Morelia)', 2000, 7, 2004, 7, 'GUKjy'),
    ('Investigador Titular A, Medio tiempo', False, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2007, 8, 2010, 2, 'GUKjy'),
    ('Investigador Titular B, Medio tiempo', True, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2010, 2, 2015, 5, 'GUKjy'),
    ('Investigador Titular C, Medio tiempo', True, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2015, 6, 0, 0, 'GUKjy'),
    ('Ninguno', False, 'Catedrático CONACYT', False, False, 'Centro de Investigaciones en Geografía Ambiental (CIGA)',
     2014, 10, 0, 0, 'Yl5I4'),
    ('Ninguno', False, 'Investigador Postdoctoral', False, False,
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2014, 9, 0, 0, 'EeGJW'),
    ('Ninguno', False, False, False, 'Levantamiento y elaboración de mapas de suelos',
     'Instituto Cartográfico y Geológico de Cataluña', 2008, 10, 2009, 7, 'EeGJW'),
    ('Ninguno', False, False, False, 'Plan de mejora de los caminos rurales de Catalunya',
     'Tecnologías y Servicios Agrarios, S.A (Tragsatec)', 2006, 4, 2006, 9, 'EeGJW'),
    ('Ninguno', False, False, False, 'Responsable de Calidad', 'Meneu Distribución, S.A.', 2005, 9, 2006, 2, 'EeGJW'),
    ('Técnico Académico Auxiliar (investigación) C, Tiempo Completo', False, False, False, 'Otro',
     'Instituto de Geografía', 1994, 12, 1997, 12, 'Yrcbo'),
    ('Técnico Académico Auxiliar (investigación) A, Tiempo Completo', False, False, False, 'Otro',
     'Instituto de Geografía', 1997, 12, 2001, 12, 'Yrcbo'),
    ('Técnico Académico Auxiliar (investigación) B, Tiempo Completo', True, False, False, 'Otro',
     'Instituto de Geografía', 2001, 12, 2006, 8, 'Yrcbo'),
    ('Técnico Académico Titular (docencia) B, Tiempo Completo', True, False, False, 'Otro', 'Instituto de Geografía',
     2006, 9, 2007, 7, 'Yrcbo'),
    ('Técnico Académico Titular (investigación) B, Tiempo Completo', True, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2006, 8, 2008, 12, 'Yrcbo'),
    ('Técnico Académico Titular (investigación) C, Tiempo Completo', True, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2015, 10, 0, 0, 'Yrcbo'),
    ('Técnico Académico Titular (investigación) B, Tiempo Completo', True, False, 'Secretaría Técnica', False,
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2009, 1, 2015, 9, 'Yrcbo'),
    ('Ninguno', False, False, False, 'Miembro de la Mesa Directiva del Colegio del Personal Académico',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2007, 11, 2011, 10, 'fEVor'),
    ('Ninguno', False, False, False, 'Representante de los técnicos académicos ante el Consejo Interno',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2007, 10, 2011, 10, 'fEVor'),
    ('Ninguno', False, False, False, 'Corresponsable del Proyecto de Creación de la Licenciatura en Geohistoria',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2011, 11, 2012, 4, 'fEVor'),
    ('Ninguno', False, False, False,
     'Comisión para la elaboración del Nuevo Plan de la Licenciatura en Ciencias Ambientales',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2010, 12, 2012, 4, 'fEVor'),
    (
        'Ninguno', False, False, False,
        'Representante del Director ante el Consejo Académico de Área en Ciencias Sociales',
        'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2008, 8, 2012, 6, 'fEVor'),
    ('Ninguno', False, False, False,
     'Representante del personal académico del CIGA ante el Consejo Académico de la Licenciatura en Ciencias Ambientales',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2011, 11, 2012, 6, 'fEVor'),
    ('Ninguno', False, False, False, 'Miembro del Comité Académico Asesor de la Licenciatura en Ciencias Ambientales',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2013, 10, 2014, 10, 'fEVor'),
    (
        'Ninguno', False, False, False,
        'Comisión para la Creación de la Licenciatura en Estudios Sociales y Gestión Local',
        'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2013, 2, 2014, 3, 'fEVor'),
    ('Ninguno', False, False, False, 'Miembro de la Comisión para la Creación del Bachillerato Regional UNAM Michoacán',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2014, 2, 2014, 12, 'fEVor'),
    ('Ninguno', False, False, False, 'Miembro del Comité Académico Asesor de la Licenciatura en Geohistoria',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2013, 10, 0, 0, 'fEVor'),
    ('Ninguno', False, False, False,
     'Miembro del Comité Académico Asesor de la Licenciatura en Estudios Sociales y Gestión Local',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2014, 10, 0, 0, 'fEVor'),
    ('Ninguno', False, False, False, 'Miembro del Comité de Publicaciones, representante del Área de Ciencias Sociales',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 1900, 1, 0, 0, 'fEVor'),
    ('Ninguno', False, False, False, 'Editor Académico del Comité Editorial',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 1900, 1, 0, 0, 'fEVor'),
    ('Ninguno', False, False, False, 'Representante académico ante el Comité Académico del Posgrado en Geografía',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2015, 10, 0, 0, 'fEVor'),
    ('Ninguno', False, False, 'Coordinador de la Licenciatura en Geohistoria', False,
     'Escuela Nacional de Estudios Superiores, Unidad Morelia (ENES Morelia)', 2012, 4, 2015, 2, 'fEVor'),
    ('Ninguno', False, False, 'Jefe del Departamento de Docencia', False,
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2015, 10, 0, 0, 'fEVor'),
    ('Investigador Asociado C, Tiempo Completo', False, False, False, 'Otro',
     'Instituto de Geografía, Unidad Morelia (UNAM Morelia)', 2004, 11, 2007, 8, 'fEVor'),
    ('Técnico Académico Asociado (docencia) C, Tiempo Completo', False, 'Otro', False, False,
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2007, 8, 2011, 2, 'fEVor'),
    ('Técnico Académico Titular (docencia) A, Tiempo Completo', True, 'Otro', False, False,
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2011, 2, 2015, 3, 'fEVor'),
    ('Técnico Académico Titular (docencia) B, Tiempo Completo', True, 'Otro', False, False,
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2015, 3, 0, 0, 'fEVor'),
    ('Ninguno', False, False, False, 'Lecturer', 'Universidad de Dar es-Salam', 1974, 1, 1982, 9, 'YxU7H'),
    ('Ninguno', True, False, False, 'Unversitaire Hoog Docent', 'University of Twente', 1982, 9, 2008, 6, 'YxU7H'),
    ('Profesor de Asignatura A', False, 'Profesor', False, False,
     'Escuela Nacional de Estudios Superiores, Unidad Morelia (ENES Morelia)', 2012, 8, 0, 0, '4th7o'),
    (
        'Ninguno', False, 'Profesor invitado', False, False, 'Universidad Autónoma de Tlaxcala', 2012, 7, 2012, 8,
        '4th7o'),
    ('Técnico Académico Titular (docencia) C, Tiempo Completo', True, 'Otro', False, False,
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2013, 6, 0, 0, 'zF8gk'),
    ('Investigador Asociado C, Tiempo Completo', True, 'Profesor Investigador', False, False,
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2009, 1, 2014, 10, 'prgh0'),
    ('Investigador Asociado C, Tiempo Completo', False, 'Profesor Investigador', False, False,
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2014, 11, 0, 0, 'prgh0'),
    ('Investigador Asociado C, Tiempo Completo', False, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2011, 4, 2016, 3, 'DgFdm'),
    ('Técnico Académico Titular (docencia) A, Tiempo Completo', True, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2016, 4, 0, 0, 'J8YEd'),
    ('Ninguno', False, False, False, 'Otro', 'Consejo Nacional de Investigaciones Científicas y Técnicas (CONICET)',
     2009, 4, 2014, 3, 'h8fvn'),
    ('Ninguno', False, False, False, 'Otro', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2010, 3, 2015,
     12, 'biabG'),
    ('Ninguno', False, False, False, 'Administrador de Sistemas de información (SIGs)',
     'Coordinación General de Gabinete y Planeación (CPLADE)', 2004, 8, 2004, 12, 'biabG'),
    (
        'Ninguno', False, False, False, 'Técico Superior', 'Instituto Nacional de Estadística y Geografía (INEGI)',
        2005, 7,
        2005, 12, 'biabG'),
    ('Ninguno', False, False, False, 'Encargada de Sistemas', 'Harlen Administrativo SA de CV', 2005, 6, 2007, 3,
     'biabG'),
    ('Ninguno', False, False, False, 'Técnico Informático de Zona',
     'Instituto Nacional de Estadística y Geografía (INEGI)', 2007, 3, 2007, 9, 'biabG'),
    ('Ninguno', False, False, False, 'Encargada del Área de Soporte Técnico', 'CodiNet S.A. DE C.V.', 2007, 9, 2010, 2,
     'biabG'),
    ('Ninguno', False, False, False, 'Residencia Profesional', 'Instituto de Geografía', 2006, 2, 2006, 5, 'n80rn'),
    ('Investigador Titular A, Tiempo Completo', True, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2016, 4, 0, 0, 'DgFdm'),
    ('Técnico Académico Titular (investigación) A, Medio tiempo', True, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2016, 4, 0, 0, 'puYq7'),
    ('Ninguno', False, False, False,
     'Conference Director. Miembro por invitación de la International Society for the Study of Religion, Nature and Culture (ISSRNC)',
     'International Society for the Study of Religion, Nature and Culture (ISSRNC)', 2006, 4, 2008, 12, 'fEVor'),
    ('Ninguno', True, False, False,
     'Miembro fundador, por invitación, de la Asociación de Historiadores de las Ciencias y las Humanidades A.C. (HCyH). Asamblea General Constitutiva, celebrada en el Instituto de Geografía, UNAM, el 19 de abril de 2007.',
     'Instituto de Geografía', 2007, 4, 0, 0, 'fEVor'),
    ('Ninguno', False, False, False, 'Miembro regular de la Conference of Latin Americanist Geographers (CLAG).',
     'Conference of Latin Americanist Geographers (CLAG)', 2011, 2, 0, 0, 'fEVor'),
    ('Ninguno', False, False, 'Director de Cooperación Académica', False,
     'Dirección General de Cooperación e Internacionalización (DGECI)', 2015, 9, 0, 0, 'rWKXd'),
    ('Profesor de Asignatura A', False, 'Profesor', False, False, 'Facultad de Economía', 2014, 1, 2016, 12, 'gb4go'),

    ('Ninguno', False, False, False, 'Subdirector de recursos genéticos',
     'Secretaría de Medio Ambiente y Recursos Naturales (SEMARNAT)', 2008, 8, 2009, 8, 'ubFaE'),
    ('Técnico Académico Titular (investigación) A, Medio tiempo', True, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2007, 3, 0, 0, '88SSU'),
    ('Técnico Académico Asociado (docencia) C, Tiempo Completo', False, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2016, 6, 0, 0, 'c3fhV'),
    ('Ninguno', False, False, False, 'Servicio Profesional en la Unidad de Cómputo',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 1900, 1, 0, 0, 'c3fhV'),
    ('Ninguno', False, False, False, 'Pasante en desarrollo Web',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2008, 8, 2008, 12, 'c3fhV'),
    ('Ninguno', False, False, False, 'Residente Profesional en desarrollo Web',
     'Instituto de Investigaciones en Ecosistemas y Sustentabilidad (IIES)', 2007, 8, 2007, 12, 'c3fhV'),
    ('Ninguno', False, False, False, 'Consultor Externo en Soporte Técnico', 'H. Ayuntamiento de Morelos', 2015, 10,
     2015, 12, 'c3fhV'),
    ('Ninguno', False, False, False, 'Servicio Profesional de apoyo a Control Escolar', 'Telebachillerato Michoacán',
     2013, 1, 2015, 1, 'c3fhV'),
    ('Ninguno', False, False, False, 'Servicio Profesional de apoyo a Control Escolar',
     'Universidad Michoacana de San Nicolás de Hidalgo (UMSNH)', 2009, 1, 2010, 12, 'c3fhV'),
    ('Ninguno', False, False, False, 'Desarrollador Web', 'TECIF', 2009, 1, 2009, 10, 'c3fhV'),
    (
        'Ninguno', False, False, False, 'Servicio Social',
        'Fideicomisos Instituidos en Relación con la Agrícultura (FIRA)',
        1900, 1, 0, 0, 'c3fhV'),
    ('Técnico Académico Auxiliar (docencia) B, Tiempo Completo', False, False, False, 'Otro', 'Facultad de Ingeniería',
     1984, 8, 1986, 10, 'ftTrS'),
    ('Técnico Académico Asociado (investigación) C, Tiempo Completo', False, False, False,
     'Jefe del Laboratorio de Cómputo', 'Instituto de Geografía', 1986, 11, 1990, 9, 'ftTrS'),
    ('Técnico Académico Asociado (investigación) B, Tiempo Completo', False, False, False, 'Otro',
     'Instituto de Geografía', 1992, 10, 1994, 4, 'ftTrS'),
    ('Técnico Académico Asociado (investigación) B, Tiempo Completo', False, False,
     'Jefe del Laboratorio de Sistemas de Información Geográfica y Percepción Remota', False, 'Instituto de Geografía',
     1998, 10, 2001, 10, 'ftTrS'),
    ('Técnico Académico Titular (docencia) C, Tiempo Completo', False, False,
     'Jefe del Laboratorio de Sistemas de Información Geográfica y Percepción Remota', False, 'Instituto de Geografía',
     2001, 11, 2004, 11, 'ftTrS'),
    ('Técnico Académico Titular (docencia) C, Tiempo Completo', False, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2004, 12, 2009, 12, 'ftTrS'),
    ('Técnico Académico Titular (investigación) C, Tiempo Completo', True,
     'Coordinador del Laboratorio de Análisis Espacial', False, False,
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2009, 1, 2015, 11, 'ftTrS'),
    ('Técnico Académico Titular (investigación) C, Tiempo Completo', True, False, 'Secretario Técnico', False,
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2015, 11, 0, 0, 'ftTrS'),
    ('Ninguno', False, False, False, 'Coordinador de Proyecto',
     'Instituto Nacional de Ecología y Cambio Climático (INECC)', 1995, 2, 1996, 2, 'ftTrS'),
    ('Ninguno', False, False, False, 'Technical Officer', 'Commission for Environmental Cooperation', 1996, 2, 1998, 10,
     'ftTrS'),
    ('Ninguno', False, 'Cátedras CONACYT', False, False, 'Consejo Nacional de Ciencia y Tecnología (CONACYT)', 2014, 10,
     2015, 12, 'Y6pdF'),
    ('Investigador Asociado C, Tiempo Completo', False, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2016, 1, 0, 0, 'Y6pdF'),
    ('Ninguno', False, False, False, 'Profesor De Maestría En Derecho', 'Universidad Vasco de Quiroga (UVAQ)', 2012, 1,
     0, 0, '16ymf'),
    ('Ninguno', False, False, False, 'Evaluador Del Proyecto',
     'Universidad Michoacana de San Nicolás de Hidalgo (UMSNH)', 2014, 6, 2015, 4, '16ymf')
)

for i in experiencias:

    if not i[2] and not i[3] and i[4]:
        c = i[4]
    elif not i[2] and i[3] and not i[4]:
        c = i[3]
    elif i[2] and not i[3] and not i[4]:
        c = i[2]
    else:
        raise Exception

    if int(i[8]) == 0 and int(i[9]) == 0:
        e = ExperienciaLaboral(institucion=Dependencia.objects.get(nombre=i[5]).institucion,
                               dependencia=Dependencia.objects.get(nombre=i[5]),
                               nombramiento=Nombramiento.objects.get(nombre=i[0]), es_nombramiento_definitivo=i[1],
                               cargo=Cargo.objects.get(nombre=c), fecha_inicio=date(int(i[6]), int(i[7]), 1),
                               usuario=User.objects.get(rfc=i[10]))
    else:
        e = ExperienciaLaboral(institucion=Dependencia.objects.get(nombre=i[5]).institucion,
                               dependencia=Dependencia.objects.get(nombre=i[5]),
                               nombramiento=Nombramiento.objects.get(nombre=i[0]), es_nombramiento_definitivo=i[1],
                               cargo=Cargo.objects.get(nombre=c), fecha_inicio=date(int(i[6]), int(i[7]), 28),
                               fecha_fin=date(int(i[8]), int(i[9]), 1), usuario=User.objects.get(rfc=i[10]))
    e.save()
    print(e)

capacidades = (
    ('Planificación del territorio', 2007, 'no', 'hnSDn'),
    ('Manejo de zona costera', 2007, 'no', 'hnSDn'),
    ('Gestión ambiental', 2007, 'no', 'hnSDn'),
    ('Gobernanza', 2009, 'no', 'hnSDn'),
    ('Ambientes urbanos y periurbanos', 2014, 'no', 'hnSDn'),
    ('Bases de datos: Visual FoxPro, MySQL, Access, Oracle, Excel. etc.', 2000, 'no', 'n80rn'),
    ('Diseño de imágenes: Photoshop, Corel Draw, Flash (Multimedia), Adobe Illustrator, Page Maker', 2000, 'no',
     'n80rn'),
    (
        'Programación: Visual Basic, Visual C++, JBuilder, Java, C++, PHP, HTML, JavaSever Page, Javascript, Servlets, etc.',
        2002, 'no', 'n80rn'),
    ('Levantamiento, clasificación y cartografía de paisajes físico-geográficos', 1987, 'no', '9hUCZ'),
    ('Heterogeneidad geoecológica y su relación con la distribución de la biodiversidad ', 1994, 'no', '9hUCZ'),
    ('Ordenamiento ecológico territorial ', 1987, 'no', '9hUCZ'),
    ('Mantenimiento: Preventivo y Correctivo de Microcomputadoras y Servidores.', 2001, 'no', 'n80rn'),
    ('Redes: Análisis, diseño e instalación de redes LAN y WAN (switches y ruteadores CISCO), Seguridad ', 2005, 'no',
     'n80rn'),
    (
        'Redes Internas conectadas a Internet (Firewall´s) (Packeeteer, CISCO, Fortinet, SonicWall), Instalación y configuración de Servidores Web, Correo, FTP, etc.',
        2005, 'no', 'n80rn'),
    ('Administración y configuración de terminales VOIP en un conmutador NEC NEAX IPX 2400', 2007, 'no', 'n80rn'),
    ('Uso y administración de videoconferencias utilizando el estándar H.323 (Polycom, Sony, Tandberg).', 2007, 'no',
     'n80rn'),
    ('Sistemas Operativos: Windows, Unix (Fedora, Suse, Red Hat, Debian), MacOS.', 2001, 'no', 'n80rn'),
    ('SIG Intranet: Arcview, ARCGIS, Ilwis, Idrisi, Envi, Erdas, etc.', 2007, 'no', 'n80rn'),
    ('SIG Internet: Map Server, Alov Map, etc.', 2009, 'no', 'n80rn'),
    ('Experiencia en modelado y análisis de procesos de cambio de uso y cubierta del suelo.', 1994, 'no', 'J8YEd'),
    (
        'Manejo especializado de los principales Sistemas de Información Geográfica: ArcGis 10x, ArcInfo 9.0, ArcView, Ilwis, QGis.',
        1989, 'no', 'J8YEd'),
    ('Monitoreo de la deforestación con base en imágenes de satélite', 1998, 'no', 'GUKjy'),
    ('Modelación de los cambios de cubierta/uso del suelo', 2000, 'no', 'GUKjy'),
    ('Cartografía de la vegetación con base en percepción remota y SIG', 2000, 'no', 'GUKjy'),
    ('territorialidad, cultura y politica', 2014, 'no', 'Yl5I4'),
    ('La perspectiva sociocultural de la vulnerabilidad a desastres', 2014, 'no', 'Yl5I4'),
    (
        'La perspectiva critica de los sistemas de informacion geografica y la integracion de las nuevas tecnologias de comunicacion',
        2014, 'no', 'Yl5I4'),
    ('Ciencia del suelo, clasificación y evaluación', 2008, 'no', 'EeGJW'),
    ('Geomorfología del paisaje y edafología', 2008, 'no', 'EeGJW'),
    ('Modelación de cuencas', 2010, 'no', 'EeGJW'),
    ('Evaluación y gestión del territorio asociado a cambios de uso de suelo y variabilidad climática', 2013, 'no',
     'EeGJW'),
    ('Influencia antrópica en los procesos geomórficos y erosión del suelo', 2010, 'no', 'EeGJW'),
    ('El manejo de forestería comunitaria ', 1978, 'no', 'YxU7H'),
    (
        'Implicaciones en política del cambio climático global. Deforestación, degradación, forestería comunitaria y fortalecimiento de capacidades institucionales locales; el mercado de carbono ',
        2000, 'no', 'YxU7H'),
    ('Bioenergía y biofuels; impactos sociales  ', 2007, '2012', 'YxU7H'),
    (
        'Género y energía. Perspectiva de género y herramientas de planeación en uso de la energía', 1995, '2003',
        'YxU7H'),
    ('Foresteria comunitaria y captura de carbono', 2003, 'no', 'YxU7H'),
    ('Políticas para promover el carbono forestal', 2007, 'no', 'YxU7H'),
    ('Gestión pública', 2005, 'no', 'usmv1'),
    ('Competitividad', 2007, 'no', 'usmv1'),
    ('Estructura económica', 2004, 'no', 'usmv1'),
    ('Innovación', 2009, 'no', 'usmv1'),
    ('Desarrollo sustentable', 2010, 'no', 'usmv1'),
    ('Manejo y Conservación de biodiversidad en socioecosistemas', 2010, 'no', '4th7o'),
    ('Complejidad y sistemas complejos para el estudio de problemas ambientales', 2012, 'no', '4th7o'),
    ('Valoración y percepción del paisaje', 2009, 'no', 'prgh0'),
    ('Conservación y desarrollo en ANP', 2009, 'no', 'prgh0'),
    (
        'Modelado espacio-temporal de los impactos ambientales por la extracción y producción de leña y carbón vegetal bajo patrones de aprovechamiento tradicional',
        2003, 'no', 'DgFdm'),
    (
        'Modelado prospectivo del potencial de los recursos dendroenergéticos bajo patrones de aprovechamiento tecnificado ',
        2006, 'no', 'DgFdm'),
    ('Seguridad energética de la población rural y urbana de bajos recursos', 2011, 'no', 'DgFdm'),
    ('Geografía del Paisaje', 2001, 'no', 'Y9jOf'),
    ('Uso del suelo', 2001, 'no', 'Y9jOf'),
    ('Análisis espacial', 2001, 'no', 'Y9jOf'),
    ('Manejo comunitario de recursos forestales', 2008, 'no', 'Y9jOf'),
    ('Política ambiental', 2008, 'no', 'Y9jOf'),
    ('Arqueología del paisaje', 2007, 'no', 'h8fvn'),
    ('Sensores remotos y teledetección', 2007, 'no', 'h8fvn'),
    ('Sistemas de Información geográfica participativos', 2016, 'no', 'h8fvn'),
    ('SIG y análisis espaciales', 2010, 'no', 'h8fvn'),
    (
        'historia ambiental, arqueogeografía, geohistoria, relación sociedad, medio ambiente, patrón de asentamiento, reconstrucción de las formas del paisaje...',
        2003, 'no', '7Gs53'),
    ('Historia y paisaje desde el cambio de uso de suelo y tenencia de la tierra', 2016, 'no', 'fEVor'),
    ('Teoría e historiografía de la geografía histórica e historia ambiental', 2016, 'no', 'fEVor'),
    ('Geografía cultural y paisajes históricos', 2016, 'no', 'fEVor'),
    ('Economía Ambiental. Instrumentos de Política Ambiental. Desarrollo Sustentable.', 2000, 'no', 'gb4go'),
    (
        'Especialización avanzada en el manejo de Sistemas de Información Geográfica aplicando diversos programas (ArcView, ArcGIS, Erdas, ILWIS).',
        2000, 'no', 'Ersp5'),
    ('Elaboración de modelos y análisis de cambio de coberturas y uso de suelo', 2000, 'no', 'Ersp5'),
    (
        'Aplicación de técnicas de análisis por criterios múltiples en relación a la caracterización, diagnóstico y priorización de sistemas ambientales con fines de conservación.',
        2000, 'no', 'Ersp5'),
    (
        'Aplicación de conceptos asociados a la Ecología del Paisaje con capacidad de determinar y recolectar el tipo de información necesaria en suelo y vegetación',
        2000, 'no', 'Ersp5'),
    ('Aplicación de Técnicas geoestadísticas en el análisis de datos espaciales', 2000, 'no', 'Ersp5'),
    ('Conocimiento avanzado en técnicas participativas de cartografía y realización de talleres', 2000, 'no', 'Ersp5'),
    ('Conocimiento sobre diseño y uso de cuestionarios y encuestas.', 2000, 'no', 'Ersp5'),
    ('Las ciencias sociales en la era de la globalización', 2011, 'no', 'vmh1r'),
    ('La cooperación científica internacional en el mundo contemporáneo', 2000, 'no', 'vmh1r'),
    ('Actividad científica en la Patagonia argentina y chilena', 2016, 'no', 'vmh1r'),
    ('La evaluación académica, gerencialismo  y la ilusión de lo cuantitativo', 2000, 'no', 'vmh1r'),
    ('Agrobiodiversidad y agroecología', 2003, 'no', 'ubFaE'),
    ('Recursos fitogenéticos', 2006, 'no', 'ubFaE'),
    ('Planeación y manejo de recursos naturales y desarrollo rural', 2002, '2008', 'ubFaE'),
    ('Erosión hídrica de suelos', 2010, 'no', 'EeGJW'),
    ('Paisajes mineros en México', 2007, 'no', '88SSU'),
    ('Manejo de zonas riparias', 2004, 'no', 'df4ty'),
    ('Monitoreo comunitario del agua', 2004, 'no', 'df4ty'),
    ('Sistemas socio-ecológicos', 2004, 'no', 'df4ty'),
    ('Sistemas de Información Geográfica (Geomática)', 2000, 'no', 'ftTrS'),
    ('Inventario de recurso naturales y evaluación de su calidad: suelos, polvos, clima y cuerpos de agua', 2000, 'no',
     '98big'),
    ('Valoración del conocimiento local sobre el ambiente, recursos naturales y formas de manejo', 2000, 'no', '98big'),
    ('Diseño de modelos de evaluación de la aptitud/calidad de los recursos naturales.', 2000, 'no', '98big'),
    (
        'Evaluación de tierras en sentido amplio, incluyendo ambientes urbanos, rurales, periurbanos, industriales y mineros, con las siguientes tres sublíneas',
        2000, 'no', '98big'),
    ('Percepción Remota (Teledetección)', 2000, 'no', 'ftTrS'),
    ('Análisis Espacial (Modelado)', 2000, 'no', 'ftTrS'),
    ('Drones (Operación y Aplicaciones Científicas)', 2000, 'no', 'ftTrS'),
    ('Riesgo, Peligro y Vulnerabilidad (Modelado)', 2000, 'no', 'ftTrS'),
    ('Ecología Política', 2012, 'no', 'Y6pdF'),
    ('Cubiertas y Usos del Territorio', 2005, 'no', 'Y6pdF'),
    ('Etnoecología', 2010, 'no', 'Y6pdF'),
    ('Innovación Comunitaria', 2016, 'no', 'Y6pdF')
)

for i in capacidades:
    if i[2] == 'no':
        c = CapacidadPotencialidad(nombre=i[0], fecha_inicio=date(int(i[1]), 1, 1), usuario=User.objects.get(rfc=i[3]))
    else:
        c = CapacidadPotencialidad(nombre=i[0], fecha_inicio=date(int(i[1]), 1, 1), fecha_fin=date(int(i[2]), 12, 28),
                                   usuario=User.objects.get(rfc=i[3]))
    c.save()
    print(c)

ed = Editorial(nombre='Otra', pais=Pais.objects.get(nombre='México'), estado=Estado.objects.get(nombre='Michoacán de Ocampo'), ciudad=Ciudad.objects.get(nombre='Morelia'))
ed.save()
print("Agregada Editorial 'Otra'")

revistas = (
    ('Environmental Modelling & Software', ' Env. Model. & Soft.', 'Otra', 'México', 4.54),
    ('Espacio Abierto', None, 'Otra', 'México', None),
    ('The Cartographic Journal', 'Cartog', 'Otra', 'México', None),
    ('ACME An International E-Journal for Critical Geographies', 'ACME', 'Otra', 'México', 2.22),
    ('Agriculture and Human Values', 'J Agric Hum Values', 'Otra', 'México', 2.22),
    ('Agrociencia', None, 'Otra', 'México', 0.30),
    ('Agroecology and Sustainable Food Systems', None, 'Otra', 'México', 1.13),
    ('Agroecología', None, 'Otra', 'México', None),
    ('Agroforestry Systems', 'Agrofor. Syst.', 'Otra', 'México', 1.21),
    ('American Entomologist', 'Am. Entomol.', 'Otra', 'México', None),
    ('Andamios, Revista de Investigación Social', 'Andamios', 'Otra', 'México', 0.02),
    ('Annals of the American Association of Geographers', None, 'Otra', 'México', 2.56),
    ('Andean Past', None, 'Otra', 'México', None),
    ('Annual Review of Environment and Resources', 'An. Amn. Ass. Geog.', 'Otra', 'México', 5.89),
    ('Applied Geography', None, 'Otra', 'México', 2.85),
    ('Arqueología', None, 'Otra', 'México', None),
    ('Atmosfera', None, 'Otra', 'México', 0.87),
    ('Atmospheric Environment', None, 'Otra', 'México', 3.06),
    ('Biblio 3W. Revista bibliográfica de Geografía y Ciencias Sociales', None, 'Otra', 'México', None),
    ('Biotropica', None, 'Otra', 'México', 2.08),
    ('Boletín de la Sociedad Geológica Mexicana', None, 'Otra', 'México', 0.24),
    ('Boletín del Instituto de Geografía', None, 'Otra', 'México', None),
    ('Boletín del Museo Chileno de Arte Precolombino', None, 'Otra', 'México', None),
    ('Botanical Sciences', None, 'Otra', 'México', 0.62),
    ('Capitalism Nature Socialism', 'CNS', 'Otra', 'México', 7.10),
    ('CATENA', None, 'Otra', 'México', 2.82),
    ('CECTI Michoacán', 'CECTI', 'Otra', 'México', None),
    ('Children, Youth and Environments', 'CYE', 'Otra', 'México', None),
    ('Ciencia Nicolaita', None, 'Otra', 'México', None),
    ('City and Community', 'CC', 'Otra', 'México', 1.00),
    ('Climatic Change', None, 'Otra', 'México', None),
    ('Cogent Environmental Science', 'COG ENV SCI', 'Otra', 'México', 2.49),
    ('Comechingonia, Revista de Arqueología', 'Comechingonia', 'Otra', 'México', None),
    ('Conference Montpellier France', None, 'Otra', 'México', None),
    ('Congreso del Estado de Michoacán', None, 'Otra', 'México', None),
    ('Conservation and Society', 'Conservat. Soc.', 'Otra', 'México', 1.64),
    ('Coordinación General de Estudios de Posgrado', 'CGEP UMSNH', 'Otra', 'México', None),
    ('Cuadernos de Geografía', None, 'Otra', 'México', None),
    ('Cuadernos Geográficos', None, 'Otra', 'México', None),
    ('Dendrochronologia', None, 'Otra', 'México', 1.79),
    ('Desacatos, Revista de Antropología Social', 'Desacatos', 'Otra', 'México', None),
    ('Development in Practice', 'DiP', 'Otra', 'México', 0.75),
    ('Disasters', None, 'Otra', 'México', 0.72),
    ('Ecological Economics', 'Ecolecon', 'Otra', 'México', 2.57),
    ('Ecological Indicators', None, 'Otra', 'México', 3.44),
    ('Ecology and Society', 'E&S', 'Otra', 'México', 4.36),
    ('Economic Botany', ' ECON BOT', 'Otra', 'México', 1.10),
    ('Economía, Sociedad y Territorio', 'EST', 'Otra', 'México', None),
    ('Ecosistemas y Recursos Agropecuarios', None, 'Otra', 'México', None),
    ('Ecosphere Journal', 'Ecosphere', 'Otra', 'México', 2.25),
    ('Energy for Sustainable Development', None, 'Otra', 'México', 2.38),
    ('Environmental Earth Science', 'Environ Earth Sci,', 'Otra', 'México', 1.76),
    ('Environmental Management', None, 'Otra', 'México', None),
    ('Environmental Modelling and Software', None, 'Otra', 'México', None),
    ('Environmental Research Letters', 'Env. Res. Let.', 'Otra', 'México', 4.13),
    ('Environmental Science && Policy', 'Env. Sci. Pol.', 'Otra', 'México', 2.97),
    ('Espacio y tiempo, Revista latinoamericana de Ciencias Sociales y humanidades', None, 'Otra', 'México', None),
    ('Fontqueria', None, 'Otra', 'México', None),
    ('Forest Policy and Economics', None, 'Otra', 'México', 1.97),
    ('Forests', None, 'Otra', 'México', 1.58),
    ('Frontiers in Earth Science', None, 'Otra', 'México', 0.88),
    ('Gaceta Ecológica, Nueva Época', None, 'Otra', 'México', None),
    ('Genetic Resources and Crop Evolution', None, 'Otra', 'México', 1.25),
    ('Geoarchaeology', None, 'Otra', 'México', 1.77),
    ('Geocarto International', None, 'Otra', 'México', 1.37),
    ('Geoforum', 'Geoforum', 'Otra', 'México', 2.39),
    ('Geofísica Internacional', None, 'Otra', 'México', None),
    ('Geografía y Sistema de Información Geográfica', None, 'Otra', 'México', None),
    ('Geomorphology', None, 'Otra', 'México', 2.78),
    ('Geotrópico', None, 'Otra', 'México', None),
    ('GIM International', None, 'Otra', 'México', None),
    ('Global Change Biology', 'GCB', 'Otra', 'México', 8.44),
    ('Global Environmental Change', 'Glob. Environ. Chang.', 'Otra', 'México', 9.05),
    ('Heredity', 'Heredity', 'Otra', 'México', 3.80),
    ('Hidrobiológica', None, 'Otra', 'México', 0.10),
    ('Human Ecology', None, 'Otra', 'México', 1.89),
    ('Interciencia, Revista de Ciencia y Tecnología de América Latina', None, 'Otra', 'México', 0.37),
    ('International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences - ISPRS Archives',
     None, 'Otra', 'México', None),
    ('International Encyclopedia of Anthropology', None, 'Otra', 'México', None),
    ('International Forestry Review', None, 'Otra', 'México', 1.73),
    ('International Journal of Geosciences', 'IJGeosci', 'Otra', 'México', 0.78),
    ('International Journal of Wildland Fire', 'IntlJWildlandFire', 'Otra', 'México', 2.08),
    ('International Review of Forestry', 'IntRevFor', 'Otra', 'México', None),
    ('Intersticios Sociales', 'Intersticios', 'Otra', 'México', None),
    ('Investigaciones Geográficas, Boletín del Instituto de Geografía', None, 'Otra', 'Chile', 0.13),
    ('Investigación Ambiental', None, 'Otra', 'México', None),
    ('ISPRS International Journal of Geo-Information', None, 'Otra', 'México', 0.65),
    ('Journal of Applied Research and technology', 'J App R T', 'Otra', 'México', 0.81),
    ('Journal of Cave and Karst Studies', None, 'Otra', 'México', 1.32),
    ('Journal of Environmental Management', None, 'Otra', 'México', 2.72),
    ('Journal of Ethnobiology and Ethnomedicine', 'J Ethnobiol Ethnmed', 'Otra', 'México', 2.41),
    ('Journal of Forests and Livelihoods', None, 'Otra', 'México', None),
    ('Journal Of Geographic Information System', 'JGIS', 'Otra', 'México', 1.03),
    ('Journal of Latin American Geography', 'JLAG', 'Otra', 'México', None),
    ('Journal of Maps', None, 'Otra', 'México', 0.62),
    ('Journal of Rural Studies', None, 'Otra', 'México', 2.20),
    ('La Revue d´ethnoécologie', None, 'Otra', 'México', None),
    ('La Zaranda de Ideas', None, 'Otra', 'México', None),
    ('Land Degradation and Development', None, 'Otra', 'México', 8.14),
    ('Land Use Policy', None, 'Otra', 'México', 3.13),
    ('Landscape Research', 'Landsc. Res.', 'Otra', 'México', 1.08),
    ('LANIA Newsletter', None, 'Otra', 'México', None),
    ('Latimag Letters', 'Latinmag', 'Otra', 'Brasil', None),
    ('Latinmag Letters', None, 'Otra', 'México', None),
    ('Les Cahiers des Amériques Latines', 'Les Cahiers des Amériques Latines', 'Otra', 'México', None),
    ('Madera y Bosque', None, 'Otra', 'México', 0.29),
    ('Mercator', None, 'Otra', 'México', None),
    ('Nature & Resources', None, 'Otra', 'México', None),
    ('Nature Climate Change', None, 'Otra', 'México', 15.30),
    ('Open Journal of Forestry', 'OJFor', 'Otra', 'México', 0.81),
    ('Perspectiva Geográfica', 'Perspectiva Geográfica', 'Otra', 'México', None),
    ('Photogrammetric Engineering and Remote Sensing', None, 'Otra', 'México', 1.80),
    ('Physical Geography', None, 'Otra', 'México', None),
    ('Plant Ecology', None, 'Otra', 'México', None),
    ('Plos One', 'Plos1', 'Otra', 'México', 3.23),
    ('Polibotánica', 'Polibotánica', 'Otra', 'México', None),
    ('Polígonos, Revista de Geografía', None, 'Otra', 'México', None),
    ('Procedia Engineering', None, 'Otra', 'México', 0.73),
    ('Proceedings of National Academy of Sciences of USA', None, 'Otra', 'México', None),
    ('Proceedings of the 8th International Congress on Environmental Modelling and Software (iEMSs)', None, 'Otra',
     'México', None),
    ('Programmnye produkty i sistemy', None, 'Otra', 'México', None),
    ('Progress in Development Studies Journal', None, 'Otra', 'México', 0.79),
    ('Progress in Physical Geography', None, 'Otra', 'México', 2.78),
    ('Quaternary International', None, 'Otra', 'México', 2.48),
    ('Región y Sociedad', None, 'Otra', 'México', None),
    ('Relaciones', None, 'Otra', 'México', None),
    ('Remote Sensing Journal by MDPI', None, 'Otra', 'México', None),
    ('Remote Sensing', 'Rem. Sens.', 'Otra', 'México', 3.03),
    ('Renewable and Sustainable Energy Reviews', 'RENEW SUST ENERG REV', 'Otra', 'México', 5.51),
    ('Revista Mexicana de Ingeniería Química', 'RMIQ', 'Otra', 'México', 0.92),
    ('Revista Agricultura Familiar', None, 'Otra', 'México', None),
    ('Revista Cartográfica', None, 'Otra', 'México', None),
    ('Revista Catalana de Geografía', None, 'Otra', 'España', None),
    ('Revista Chapingo Serie Ciencias Forestales y del Ambiente', 'RCSFA', 'Otra', 'México', 0.11),
    ('Revista Chapingo Serie Horticultura', None, 'Otra', 'México', 0.12),
    ('Revista de Agroecología', None, 'Otra', 'México', None),
    ('Revista de Ciencia y Tecnología de América', None, 'Otra', 'México', 0.30),
    ('Revista De Investigación En Ciencias De La Administración', 'INCEPTUM', 'Otra', 'México', None),
    ('Revista Del Jardín Botánico Nacional De Cuba', None, 'Otra', 'Cuba', None),
    ('Revista del Museo de Antropología', 'RMA', 'Otra', 'México', None),
    ('Revista Española de Antropología Americana', 'REAA', 'Otra', 'México', None),
    ('Revista Geográfica De América Central', None, 'Otra', 'México', None),
    ('Revista Internacional de Contaminación Ambiental', 'Rev. Int. Cont. Amb.', 'Otra', 'México', 0.17),
    ('Revista INVI', None, 'Otra', 'México', 0.12),
    ('Revista Mexicana de Biodiversidad', None, 'Otra', 'México', 0.50),
    ('Revista Mexicana de Ciencias Geológicas', 'Rev Mex C Geol', 'Otra', 'México', 0.57),
    ('Revista Mexicana de Sociología', None, 'Otra', 'México', None),
    ('Revue Anthropologie des Connaissances', None, 'Otra', 'México', None),
    ('Science Technology and Human Values', 'SCI TECHNOL HUM VAL', 'Otra', 'México', 2.19),
    ('Singapore Journal Of Tropical Geography', 'TROPICAL GEOGRAPHY ', 'Otra', 'Singapur', 0.87),
    ('Sociedad Española de Agricultura Ecológica (SEAE)', 'SEAE', 'Otra', 'España', None),
    ('Society & Natural Resources', None, 'Otra', 'México', 1.06),
    ('Spanish Journal of Soil Science', 'sjss', 'Otra', 'España', None),
    ('Tecnología en Marcha', 'Tec. en Marcha', 'Otra', 'México', None),
    ('Teknokultura. Revista de Cultura Digital y Movimientos Sociales', 'Teknokultura', 'Otra', 'México', 0.50),
    ('The Geographical Journal', 'TGJ', 'Otra', 'México', 1.93),
    ('The International Forestry Review', 'Int. For. Rev.', 'Otra', 'México', None),
    ('Tourism Geographies', None, 'Otra', 'México', 1.69),
    ('World Development', 'worlddev', 'Otra', 'México', 3.10),
    ('World Landslide Forum', None, 'Otra', 'México', None),
    ('Ñawpa Pacha. Journal of Andean Archaeology', 'Ñawpa Pacha', 'Otra', 'México', None)
)

for i in revistas:
    r = Revista(nombre=i[0], nombre_abreviado_wos=i[1], pais=Pais.objects.get(nombre=i[3]), factor_impacto=i[4])
    r.save()
    print(r)

indices = ('Web of Science: SCI/SSCI/SCI-EX', 'Latindex', 'Scopus', 'SciELO', 'Clase', 'Revistas CONACYT', 'RedALyC',
           'Otros Indices')

for i in indices:
    I = Indice(nombre=i)
    I.save()
    print('Agregado indice ' + I.nombre)

problemas = ['Gestión integral del agua, seguridad hídrica y derecho del agua',
             'Mitigación y adaptación al cambio climático', 'Resiliencia frente a desastres naturales y tecnológicos',
             'Aprovechamiento y protección de ecosistemas y de la biodiversidad', 'Los océanos y su aprovechamiento',
             'Alimentos y su producción', 'Ciudades y desarrollo urbano',
             'Conectividad informática y desarrollo de las tecnologías de la información, la comunicación y las telecomunicaciones',
             'Manufactura de alta tecnología', 'Consumo sustentable de energía',
             'Desarrollo y aprovechamiento de energías renovables limpias  onducta humana y prevención de adicciones',
             'Enfermedades emergentes y de importancia nacional', 'Combate a la pobreza y seguridad alimentaria',
             'Migraciones y asentamientos humanos', 'Seguridad ciudadana', 'Economía y gestión del conocimiento',
             'Prevención de riesgos naturales', ]

for i in problemas:
    p = ProblemaNacionalConacyt(nombre=i)
    p.save()
    print('Agregado problema conacyt: ', p)

t = TipoEvento(nombre='Otro')
t.save()
print("agregado tipo evento", t)

e = Evento(nombre='Otro', fecha_inicio=date(2010, 10, 10), fecha_fin=date(2010, 10, 10), tipo=TipoEvento.objects.get(nombre='Otro'))
e.save()
print("agregado evento", e)




adscritos = (
    ('maria.ramirez', 2007, 10, 1),
    ('rosaura.paez',  2007, 11, 1),
    ('yadira.mendez', 2011, 4, 1),
    ('maria.carmona', 2007, 8, 1),
    ('hugo.zavala', 2007, 3, 1),
    ('luis.morales', 2007, 1, 1),
    ('gabriela.cuevas', 2011, 4, 1),
    ('manuel.mendoza', 2007, 4, 1),
    ('gerardo.bocco', 2007, 1, 1),
    ('lourdes.gonzalez', 2014, 8, 1),
    ('lorena.poncela', 2010, 1, 1),
    ('jean.mas', 2001, 7, 1),
    ('quetzalcoatl.orozco', 2015, 3, 1),
    ('alejandra.larrazabal', 2007, 8, 1),
    ('frida.guiza', 2014, 10, 1),
    ('berenice.solis', 2016, 1, 1),
    ('keith.mccall', 2008, 10, 1),
    ('pedro.urquijo', 2007, 8, 1),
    ('sara.barrasa', 2014, 11, 1),
    ('saray.bucio', 2015, 9, 1),
    ('mariana.vallejo', 2015, 3, 1),
    ('yan.gao', 2013, 4, 1),
    ('adrian.ghilardi', 2011, 4, 1),
    ('hilda.rivas', 2007, 9, 1),
    ('claudio.garibay', 2007, 3, 1),
    ('raquel.gonzalez', 2010, 3, 1),
    ('antonio.vieyra', 2007, 1, 1),
    ('fabiola.velazquez', 2016, 1, 1),
    ('karine.lefebvre', 2014, 9, 1),
    ('mario.figueroa', 2016, 1, 1),
    ('adriana.flores', 2016, 2, 1),
    ('angel.priego', 2007, 2, 1),
    ('alina.alvarez', 2016, 3, 1),
    ('francisco.bautista', 2007, 3, 1),
    ('jaime.paneque', 2016, 1, 1),
)

for i in adscritos:
    u = User.objects.get(username=i[0])
    u.ingreso_entidad = datetime(i[1], i[2], i[3])
    u.save()
