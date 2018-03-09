import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SIA.settings")

django.setup()

from datetime import datetime, date
from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.conf import settings


from nucleo.models import *

from formacion_academica.models import CursoEspecializacion, Licenciatura, Maestria, Doctorado, PostDoctorado
from experiencia_laboral.models import *

from investigacion.models import ArticuloCientifico, ProyectoInvestigacion

import uuid

print("Borrando financciamientos")
Financiamiento.objects.all().delete()

print("Borrando articulos")
ArticuloCientifico.objects.all().delete()

print("Borrando libros")
Libro.objects.all().delete()

print("Borrando revistas")
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
ProyectoInvestigacion.objects.all().delete()
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
    ('Universidad Nacional Autónoma de México (UNAM)', Pais.objects.get(nombre='México').id, Estado.objects.get(nombre='Ciudad de México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
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
         ('Colegio de Geografia (Facultad de Filosofía y Letras)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
     ]
     ),

    ('Universidad Michoacana de San Nicolás de Hidalgo (UMSNH)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado.id, Ciudad.objects.get(nombre='Morelia').id,
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

    ('Universidad de Camerino', Pais.objects.get(nombre='Italia').id, Ciudad.objects.get(nombre='Camerino').estado_id, Ciudad.objects.get(nombre='Camerino').id,
     [
         ('Departamento de Geobotánica', Ciudad.objects.get(nombre='Camerino').id),
         ('Braun Blanquetia', Ciudad.objects.get(nombre='Camerino').id)
     ]
     ),

    ('Universidad Nacional de Colombia', Pais.objects.get(nombre='Colombia').id, Ciudad.objects.get(nombre='Bogotá D.C.').estado_id, Ciudad.objects.get(nombre='Bogotá D.C.').id,
     [
         ('Universidad Nacional de Colombia', Ciudad.objects.get(nombre='Bogotá D.C.').id),
         ('Universidad Nacional de Colombia Sede Medellín', Ciudad.objects.get(nombre='Medellín').id),
         ('Instituto de Ciencias Naturales', Ciudad.objects.get(nombre='Bogotá D.C.').id),
         ('Caldasia', Ciudad.objects.get(nombre='Bogotá D.C.').id),
         ('Facultad de Minas', Ciudad.objects.get(nombre='Bogotá D.C.').id)
     ]
     ),

    ('Universidad Intercultural Indígena de Michoacán (UIIM)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Pátzcuaro').estado_id, Ciudad.objects.get(nombre='Pátzcuaro').id,
     [
         ('UIIM Sede Pichátaro', Ciudad.objects.get(nombre='Pichátaro').id),
         ('UIIM Unidad Académica Purépecha', Ciudad.objects.get(nombre='Pátzcuaro').id)
     ]
     ),

    ('University of Bern', Pais.objects.get(nombre='Suiza').id, Ciudad.objects.get(nombre='Bern').estado_id, Ciudad.objects.get(nombre='Bern').id,
     [('Mountain Research and Development', Ciudad.objects.get(nombre='Bern').id)]),

    ('Universidad de León', Pais.objects.get(nombre='España').id, Ciudad.objects.filter(nombre='León', estado=Estado.objects.get(nombre='Provincia de León'))[0].estado_id, Ciudad.objects.filter(nombre='León', estado=Estado.objects.get(nombre='Provincia de León'))[0].id,
     [
         ('Universidad de León',
          Ciudad.objects.filter(nombre='León', estado=Estado.objects.get(nombre='Provincia de León'))[0].id)
     ]
     ),

    ('Universidad Complutense de Madrid', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Madrid').estado_id, Ciudad.objects.get(nombre='Madrid').id,
     [('Universidad Complutense de Madrid', Ciudad.objects.get(nombre='Madrid').id)]),

    ('Consejo Nacional de Ciencia y Tecnología (CONACYT)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [
         ('Consejo Nacional de Ciencia y Tecnología (CONACYT)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Fomento Regional para el Desarrollo Científico, Tecnológico y de Innovación (FORDECYT)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Innovate UK - CONACYT', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)
     ]
     ),

    ('Gobierno de la República Mexicana', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
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

    ('Gobierno del Estado de Michoacán de Ocampo', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado_id, Ciudad.objects.get(nombre='Morelia').id,
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
     Pais.objects.get(nombre='Francia').id, Ciudad.objects.get(nombre='París').estado_id, Ciudad.objects.get(nombre='París').id,
     [('Organización de las Naciones Unidas para la Educación, la Ciencia y la Cultura (UNESCO)',
        Ciudad.objects.get(nombre='París').id)]),

    ('El Colegio de Michoacán, A.C. (COLMICH)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='La Piedad de Cabadas').estado_id, Ciudad.objects.get(nombre='La Piedad de Cabadas').id,
     [('El Colegio de Michoacán, A.C. (COLMICH)', Ciudad.objects.get(nombre='La Piedad de Cabadas').id)]),

    ('Interciencia, Revista de Ciencia y Tecnología de América Latina', Pais.objects.get(nombre='Venezuela').id, Ciudad.objects.get(nombre='Caracas').estado_id, Ciudad.objects.get(nombre='Caracas').id,
     [('Interciencia, Revista de Ciencia y Tecnología de América Latina', Ciudad.objects.get(nombre='Caracas').id)]),

    ('Hindawi Publishing Corporation', Pais.objects.get(nombre='Reino Unido').id, Ciudad.objects.get(nombre='Londres').estado_id, Ciudad.objects.get(nombre='Londres').id,
     [('Advances in Meteorology', Ciudad.objects.get(nombre='Londres').id)]),

    ('Universidad Autónoma de Ciudad Juárez', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad Juárez').estado_id, Ciudad.objects.get(nombre='Ciudad Juárez').id,
     (
         ('Instituto de Arquitectura, Diseño y Arte', Ciudad.objects.get(nombre='Ciudad Juárez').id),
         ('Departamento. de Arquitectura', Ciudad.objects.get(nombre='Ciudad Juárez').id),
         ('Programa Académico de Geoinformática', Ciudad.objects.get(nombre='Ciudad Juárez').id)
     )
     ),

    ('Universidad Valladolid', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado_id, Ciudad.objects.get(nombre='Morelia').id,
     [('Instituto Valladolid Preparatoria', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Instituto Tecnológico de Morelia (ITM)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado_id, Ciudad.objects.get(nombre='Morelia').id,
     (
         ('Instituto Tecnológico de Morelia (ITM)', Ciudad.objects.get(nombre='Morelia').id),
         ('Departamento de Sistemas y Computación', Ciudad.objects.get(nombre='Morelia').id)
     )
     ),

    ('Universidad Autónoma de San Luis Potosí', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='San Luis Potosí').estado_id, Ciudad.objects.get(nombre='San Luis Potosí').id,
     [('Universidad Autónoma de San Luis Potosí', Ciudad.objects.get(nombre='San Luis Potosí').id)]),

    ('Pontificia Universidad Católica de Chile', Pais.objects.get(nombre='Chile').id, Ciudad.objects.get(nombre='Santiago').estado_id, Ciudad.objects.get(nombre='Santiago').id,
     (
         ('Pontificia Universidad Católica de Chile', Ciudad.objects.get(nombre='Santiago').id),
         ('Comisión Nacional de Acreditación', Ciudad.objects.get(nombre='Santiago').id)
     )
     ),

    ('Instituto de Ecología, A.C. (INECOL)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Xalapa').estado_id, Ciudad.objects.get(nombre='Xalapa').id,
     [('Instituto de Ecología, A.C. (INECOL)', Ciudad.objects.get(nombre='Xalapa').id)]),

    ('Red Mexicana de Cuencas Hidrográficas', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Red Mexicana de Cuencas Hidrográficas', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Universidad Agraria de la Selva', Pais.objects.get(nombre='Perú').id, Ciudad.objects.get(nombre='Tingo María').estado_id, Ciudad.objects.get(nombre='Tingo María').id,
     [('Revista Investigación y Amazonía', Ciudad.objects.get(nombre='Tingo María').id)]),

    ('Instituto de Investigaciones de la Amazonía Peruana', Pais.objects.get(nombre='Perú').id, Ciudad.objects.get(nombre='Lima').estado_id, Ciudad.objects.get(nombre='Lima').id,
     [('Instituto de Investigaciones de la Amazonía Peruana', Ciudad.objects.get(nombre='Lima').id)]),

    ('Asociación Española de Fitosociología (AEFA)', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Madrid').estado_id, Ciudad.objects.get(nombre='Madrid').id,
     (
         ('Global Geobotany', Ciudad.objects.get(nombre='Madrid').id),
         ('International Journal of Geobotanical Research', Ciudad.objects.get(nombre='Madrid').id)
     )
     ),

    ('Austrian Development Cooperation (ADC)', Pais.objects.get(nombre='Austria').id, Ciudad.objects.get(nombre='Viena').estado_id, Ciudad.objects.get(nombre='Viena').id,
     [('APPEAR', Ciudad.objects.get(nombre='Viena').id)]),

    ('National Geographic Society (NGS)', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Washington, D.C.').estado_id, Ciudad.objects.get(nombre='Washington, D.C.').id,
     [('National Geographic Society (NGS)', Ciudad.objects.get(nombre='Washington, D.C.').id)]),

    ('National Science Foundation (NSF)', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Arlington').estado_id, Ciudad.objects.get(nombre='Arlington').id,
     [('National Science Foundation (NSF)', Ciudad.objects.get(nombre='Arlington').id)]),

    ('National Environmental Research Council (NERC)', Pais.objects.get(nombre='Reino Unido').id, Ciudad.objects.get(nombre='Swindon').estado_id, Ciudad.objects.get(nombre='Swindon').id,
     [('National Environmental Research Council (NERC)', Ciudad.objects.get(nombre='Swindon').id)]),

    ('Gobierno del Estado de Yucatán', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Mérida').estado_id, Ciudad.objects.get(nombre='Mérida').id,
     [('Fondo Mixto Conacyt-Gobierno del Estado de Yucatán (FOMIX)', Ciudad.objects.get(nombre='Mérida').id)]),

    ('Universidad Autónoma de Tamaulipas', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad Victoria').estado_id, Ciudad.objects.get(nombre='Ciudad Victoria').id,
     (
         ('Universidad Autonoma de Tamaulipas', Ciudad.objects.get(nombre='Ciudad Victoria').id),
         ('Instituto de Ecología Aplicada', Ciudad.objects.get(nombre='Ciudad Victoria').id)
     )
     ),

    ('Agencia Nacional de Investigación e Innovación de Uruguay (ANII)', Pais.objects.get(nombre='Uruguay').id, Ciudad.objects.get(nombre='Montevideo').estado_id, Ciudad.objects.get(nombre='Montevideo').id,
     [('Fondo María Viñas', Ciudad.objects.get(nombre='Montevideo').id)]),

    ('Universidad Autónoma de Baja California', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Mexicali').estado_id, Ciudad.objects.get(nombre='Mexicali').id,
     [('Universidad Autónoma de Baja California', Ciudad.objects.get(nombre='Mexicali').id)]),

    ('Universidad de California Davis', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Davis').estado_id, Ciudad.objects.get(nombre='Davis').id,
     [('Universidad de California Davis', Ciudad.objects.get(nombre='Davis').id)]),

    ('Universidad de Antioquia', Pais.objects.get(nombre='Colombia').id, Ciudad.objects.get(nombre='Medellín').estado_id, Ciudad.objects.get(nombre='Medellín').id,
     [('Universidad de Antioquia', Ciudad.objects.get(nombre='Medellín').id)]),

    ('University of East Anglia', Pais.objects.get(nombre='Reino Unido').id, Ciudad.objects.get(nombre='Norfolk').estado_id, Ciudad.objects.get(nombre='Norfolk').id,
     [('University of East Anglia', Ciudad.objects.get(nombre='Norfolk').id)]),

    ('Universidad París 1 Panteón-Sorbona', Pais.objects.get(nombre='Francia').id, Ciudad.objects.get(nombre='París').estado_id, Ciudad.objects.get(nombre='París').id,
     [('Universidad París 1 Panteón-Sorbona', Ciudad.objects.get(nombre='París').id)]),

    ('Universidad Northwestern', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Evanston').estado_id, Ciudad.objects.get(nombre='Evanston').id,
     [('Universidad Northwestern', Ciudad.objects.get(nombre='Evanston').id)]),

    ('University of Twente', Pais.objects.get(nombre='Países Bajos / Holanda').id, Ciudad.objects.get(nombre='Enschede').estado_id, Ciudad.objects.get(nombre='Enschede').id,
     (
         ('University of Twente', Ciudad.objects.get(nombre='Enschede').id),
         ('International Institute for Geo-Information Sciences and Earth Observation (ITC)',
          Ciudad.objects.get(nombre='Enschede').id),
         ('Faculty of Geo-Information Science and Earth Observation (ITC)', Ciudad.objects.get(nombre='Enschede').id),
         ('Department of Governance and Technology for Sustainability (CSTM)', Ciudad.objects.get(nombre='Enschede').id)
     )
     ),

    ('Universidad Autónoma de Madrid', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Madrid').estado_id, Ciudad.objects.get(nombre='Madrid').id,
     [('Universidad Autónoma de Madrid', Ciudad.objects.get(nombre='Madrid').id)]),

    ('Universidad de Buenos Aires (UBA)', Pais.objects.get(nombre='Argentina').id, Ciudad.objects.get(nombre='Buenos Aires').estado_id, Ciudad.objects.get(nombre='Buenos Aires').id,
     (
         ('Universidad de Buenos Aires (UBA)', Ciudad.objects.get(nombre='Buenos Aires').id),
         ('Proyecto Arqueológico Yocavil', Ciudad.objects.get(nombre='Buenos Aires').id)
     )
     ),

    ('Universidad de Queensland', Pais.objects.get(nombre='Australia').id, Ciudad.objects.get(nombre='Brisbane').estado_id, Ciudad.objects.get(nombre='Brisbane').id,
     [('Universidad de Queensland', Ciudad.objects.get(nombre='Brisbane').id)]),

    ('Universidad Autónoma de Barcelona (UAB)', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Barcelona').estado_id, Ciudad.objects.get(nombre='Barcelona').id,
     (
         ('Universidad Autónoma de Barcelona (UAB)', Ciudad.objects.get(nombre='Barcelona').id),
         ('Instituto Catalán de Tecnología Ambiental (ICTA)', Ciudad.objects.get(nombre='Barcelona').id)
     )
     ),

    ('El Colegio de México, A.C.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('El Colegio de México, A.C.', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('LEAD International', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('LEAD International', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Instituto Nacional de Estadística y Geografía (INEGI)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Aguascalientes').estado_id, Ciudad.objects.get(nombre='Aguascalientes').id,
     [('Instituto Nacional de Estadística y Geografía (INEGI)', Ciudad.objects.get(nombre='Aguascalientes').id)]),

    ('Sociedad Latinoamericana de Percepción Remota y Sistemas de Información Espacial (SELPER México)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Sociedad Latinoamericana de Percepción Remota y Sistemas de Información Espacial (SELPER México)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Universidad Autónoma del Estado de México (UAEMex)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Toluca').estado_id, Ciudad.objects.get(nombre='Toluca').id,
     (
         ('Universidad Autónoma del Estado de México (UAEMex)', Ciudad.objects.get(nombre='Toluca').id),
         ('Facultad de Geografía', Ciudad.objects.get(nombre='Toluca').id)
     )
     ),

    ('Open Geospatial Consortium (OGC)', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Wayland').estado_id, Ciudad.objects.get(nombre='Wayland').id,
     [('Open Geospatial Consortium (OGC)', Ciudad.objects.get(nombre='Wayland').id)]),

    ('Gtt Imaging, S.A. de C.V.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Guadalajara').estado_id, Ciudad.objects.get(nombre='Guadalajara').id,
     [('Gtt Imaging, S.A. de C.V.', Ciudad.objects.get(nombre='Guadalajara').id)]),

    ('Instituto Nacional para el Federalismo y el Desarrollo Municipal (INAFED)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Instituto Nacional para el Federalismo y el Desarrollo Municipal (INAFED)',
       Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Secretaría de Medio Ambiente y Recursos Naturales (SEMARNAT)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     (
         ('Secretaría de Medio Ambiente y Recursos Naturales (SEMARNAT)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Instituto Nacional de Ecología y Cambio Climático (INECC)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)
     )
     ),

    ('Universidad Iberoamericana (UIA)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [
         ('Ibero OnLine', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)
     ]
     ),

    ('Centro de Capacitación en Calidad Sanitaria S.A. DE C.V.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Monterrey').estado_id, Ciudad.objects.get(nombre='Monterrey').id,
     [('Centro de Capacitación en Calidad Sanitaria S.A. DE C.V.', Ciudad.objects.get(nombre='Monterrey').id)]),

    ('Instituto Nacional de Antropología e Historia (INAH)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     (
         ('Centro de Investigaciones y Estudios Superiores en Antropología Social (CIESAS)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Coordinación de Antropología', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Escuela Nacional de Antropología e Historia', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)
     )
     ),

    ('Universidad Autónoma Chapingo', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Texcoco de Mora').estado_id, Ciudad.objects.get(nombre='Texcoco de Mora').id,
     [('Universidad Autónoma Chapingo', Ciudad.objects.get(nombre='Texcoco de Mora').id)]),

    ('Sistema de la Integración Centroamericana (SICA)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Comisión Centroamericana de Ambiente y Desarrollo (CCAD)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('National Aeronautics and Space Administration (NASA)', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Washington, D.C.').estado_id, Ciudad.objects.get(nombre='Washington, D.C.').id,
     [('National Aeronautics and Space Administration (NASA)', Ciudad.objects.get(nombre='Washington, D.C.').id)]),

    ('Organización de las Naciones Unidas (ONU)', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Washington, D.C.').estado_id, Ciudad.objects.get(nombre='Washington, D.C.').id,
     (
         ('Banco Mundial (The World Bank)', Ciudad.objects.get(nombre='Washington, D.C.').id),
         ('Organización de las Naciones Unidas para la Alimentación y la Agricultura (FAO)',
          Ciudad.objects.get(nombre='Roma').id)
     )
     ),

    ('Environmental Systems Research Institute (ESRI)', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Redlands').estado_id, Ciudad.objects.get(nombre='Redlands').id,
     [('Environmental Systems Research Institute (ESRI)', Ciudad.objects.get(nombre='Redlands').id)]),

    ('Hexagon Geospatial', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Norcross').estado_id, Ciudad.objects.get(nombre='Norcross').id,
     [('ERDAS Imagine', Ciudad.objects.get(nombre='Norcross').id)]),

    ('Sistemas de Información Geográfica, S.A. de C.V.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Sistemas de Información Geográfica, S.A. de C.V.', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Centro de Información y Comunicación Ambiental de Norte América, A.C. (CICEANA)',
     Pais.objects.get(nombre='México').id,  Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [(
        'Centro de Información y Comunicación Ambiental de Norte América, A.C. (CICEANA)',
        Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Sociedad Mexicana de Geografía y Estadística, A.C.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Sociedad Mexicana de Geografía y Estadística, A.C.', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Dirección General de Geografía y Medio Ambiente', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Dirección General de Geografía y Medio Ambiente', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Universidad Autónoma de Nayarit', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Tepic').estado_id, Ciudad.objects.get(nombre='Tepic').id,
     [('Universidad Autónoma de Nayarit', Ciudad.objects.get(nombre='Tepic').id)]),

    ('El Colegio de Jalisco A.C.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Guadalajara').estado_id, Ciudad.objects.get(nombre='Guadalajara').id,
     [('El Colegio de Jalisco A.C.', Ciudad.objects.get(nombre='Guadalajara').id)]),

    ('Fundación Premio Nacional de Tecnología A.C.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Fundación Premio Nacional de Tecnología A.C.', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Universidad de Harvard', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Boston').estado_id, Ciudad.objects.get(nombre='Boston').id,
     [
         ('Harvard Business Publishing', Ciudad.objects.get(nombre='Boston').id)
     ]
     ),

    ('Instituto Mexicano de la Propiedad Industrial (IMPI)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Instituto Mexicano de la Propiedad Industrial (IMPI)',
        Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Universidad Tecmilenio', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     (
         ('Universidad Tecmilenio', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Buzan Latin America', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)
     )
     ),

    ('La Universidad de Indiana Bloomington', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Bloomington').estado_id, Ciudad.objects.get(nombre='Bloomington').id,
     (
         ('Department of Political Science and Workshop in Political Theory and Policy Analysis',
          Ciudad.objects.get(nombre='Bloomington').id),
         ('Workshop in Political Theory and Policy Analysis', Ciudad.objects.get(nombre='Bloomington').id),
         ('Vincent and Elinor Ostrom Workshop in Political Theory and Policy Analysis',
          Ciudad.objects.get(nombre='Bloomington').id)
     )
     ),

    ('Universidad Mayor se San Simón', Pais.objects.get(nombre='Bolivia').id, Ciudad.objects.get(nombre='Cochabamba').estado_id, Ciudad.objects.get(nombre='Cochabamba').id,
     (
         ('Universidad Mayor se San Simón', Ciudad.objects.get(nombre='Cochabamba').id),
         (
             'Centro de Levantamientos Aeroespaciales y Aplicaciones SIG para el Desarrollo Sostenible de los Recursos Naturales (CLAS)',
             Ciudad.objects.get(nombre='Cochabamba').id)
     )
     ),

    ('Escuela Politécnica Federal de Zúrich (ETHZ)', Pais.objects.get(nombre='Suiza').id, Ciudad.objects.get(nombre='Zúrich').estado_id, Ciudad.objects.get(nombre='Zúrich').id,
     [('Institute of Hydromechanics and Water Management', Ciudad.objects.get(nombre='Zúrich').id)]),

    ('Universidad de Míchigan', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Ann Arbor').estado_id, Ciudad.objects.get(nombre='Ann Arbor').id,
     [('Universidad de Míchigan', Ciudad.objects.get(nombre='Ann Arbor').id)]),

    ('ASPEL', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Guadalajara').estado_id, Ciudad.objects.get(nombre='Guadalajara').id,
     [('ASPEL', Ciudad.objects.get(nombre='Guadalajara').id)]),

    ('Técnica Aplicada Internacional S.A. de C.V.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Naucalpan de Juárez').estado_id, Ciudad.objects.get(nombre='Naucalpan de Juárez').id,
     [('Técnica Aplicada Internacional S.A. de C.V.', Ciudad.objects.get(nombre='Naucalpan de Juárez').id)]),

    ('Universidad de Wurzburgo', Pais.objects.get(nombre='Alemania').id, Ciudad.objects.get(nombre='Wurzburgo').estado_id, Ciudad.objects.get(nombre='Wurzburgo').id,
     [('Universidad de Wurzburgo', Ciudad.objects.get(nombre='Wurzburgo').id)]),

    ('The Big Van Theory: científicos sobre ruedas', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Madrid').estado_id, Ciudad.objects.get(nombre='Madrid').id,
     [('The Big Van Theory: científicos sobre ruedas', Ciudad.objects.get(nombre='Madrid').id)]),

    ('Universidad Complutense Madrid', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Madrid').estado_id, Ciudad.objects.get(nombre='Madrid').id,
     [('Universidad Complutense Madrid', Ciudad.objects.get(nombre='Madrid').id)]),

    ('Escuela de Organización Industrial', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Madrid').estado_id, Ciudad.objects.get(nombre='Madrid').id,
     [('Escuela de Organización Industrial', Ciudad.objects.get(nombre='Madrid').id)]),

    ('Gobierno de España', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Madrid').estado_id, Ciudad.objects.get(nombre='Madrid').id,
     [('Gobierno de España', Ciudad.objects.get(nombre='Madrid').id)]),

    ('Universidad de Alicante', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='San Vicente del Raspeig').estado_id, Ciudad.objects.get(nombre='San Vicente del Raspeig').id,
     [('Instituto de Economía Internacional', Ciudad.objects.get(nombre='San Vicente del Raspeig').id)]),

    ('Interactive Advertising Bureau (IAB)', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Nueva York').estado_id, Ciudad.objects.get(nombre='Nueva York').id,
     [('Interactive Advertising Bureau (IAB)', Ciudad.objects.get(nombre='Nueva York').id)]),

    ('Universidad Don Vasco', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Uruapan').estado_id, Ciudad.objects.get(nombre='Uruapan').id,
     [('Universidad Don Vasco', Ciudad.objects.get(nombre='Uruapan').id)]),

    ('Arkinet, S.A. De C.V.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado_id, Ciudad.objects.get(nombre='Morelia').id,
     [('Centro de capacitación de alto rendimiento', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Corporación Universitaria para el Desarrollo de Internet, A.C. (CUDI)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Corporación Universitaria para el Desarrollo de Internet, A.C. (CUDI)',
        Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Universidad Politécnica de Madrid', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Madrid').estado_id, Ciudad.objects.get(nombre='Madrid').id,
     [('Universidad Politécnica de Madrid', Ciudad.objects.get(nombre='Madrid').id)]),

    ('Academia Mexicana de Impacto Ambiental, A.C.(AMIA, A.C.)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Academia Mexicana de Impacto Ambiental, A.C.(AMIA, A.C.)',
        Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Advanced Analytical Systems, S.A. de C.V.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Advanced Analytical Systems, S.A. de C.V.', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Universidad de Sonora', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Hermosillo').estado_id, Ciudad.objects.get(nombre='Hermosillo').id,
     [('Universidad de Sonora', Ciudad.objects.get(nombre='Hermosillo').id)]),

    ('Universidad Estatal de Sonora', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Hermosillo').estado_id, Ciudad.objects.get(nombre='Hermosillo').id,
     [('Universidad Estatal de Sonora', Ciudad.objects.get(nombre='Hermosillo').id)]),

    ('Banco Interamericano de Desarrollo (BID)', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Washington, D.C.').estado_id, Ciudad.objects.get(nombre='Washington, D.C.').id,
     [('Banco Interamericano de Desarrollo (BID)', Ciudad.objects.get(nombre='Washington, D.C.').id)]),

    ('Universidad Nacional de Tucumán', Pais.objects.get(nombre='Argentina').id, Ciudad.objects.get(nombre='San Miguel de Tucumán').estado_id, Ciudad.objects.get(nombre='San Miguel de Tucumán').id,
     (
         ('Universidad Nacional de Tucumán', Ciudad.objects.get(nombre='San Miguel de Tucumán').id),
         ('Facultad de Ciencias Naturales', Ciudad.objects.get(nombre='San Miguel de Tucumán').id),
         ('Laboratorio de Geoarqueología de la Facultad de Ciencias Naturales',
          Ciudad.objects.get(nombre='San Miguel de Tucumán').id)
     )
     ),

    ('Sociedad Mexicana para la Divulgación de la Ciencia y la Técnica, A.C.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Sociedad Mexicana para la Divulgación de la Ciencia y la Técnica, A.C.',
        Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Centro de Investigación en Matemáticas (CIMAT)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Guanajuato').estado_id, Ciudad.objects.get(nombre='Guanajuato').id,
     [('Centro de Investigación en Matemáticas (CIMAT)', Ciudad.objects.get(nombre='Guanajuato').id)]),

    ('Universidad de Guadalajara', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Guadalajara').estado_id, Ciudad.objects.get(nombre='Guadalajara').id,
     (
         ('Universidad de Guadalajara', Ciudad.objects.get(nombre='Guadalajara').id),
         ('Centro Universitario de Ciencias Sociales y Humanidades', Ciudad.objects.get(nombre='Guadalajara').id)
     )
     ),

    ('Universidad de Cádiz', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Cádiz').estado_id, Ciudad.objects.get(nombre='Cádiz').id,
     [('Universidad de Cádiz', Ciudad.objects.get(nombre='Cádiz').id)]),

    ('Universidad de La Habana', Pais.objects.get(nombre='Cuba').id, Ciudad.objects.get(nombre='La Habana').estado_id, Ciudad.objects.get(nombre='La Habana').id,
     [('Facultad de Geografía', Ciudad.objects.get(nombre='La Habana').id)]),

    ('Universidad Paul Sabatier', Pais.objects.get(nombre='Francia').id, Ciudad.objects.get(nombre='Toulouse').estado_id, Ciudad.objects.get(nombre='Toulouse').id,
     [('Universidad Paul Sabatier', Ciudad.objects.get(nombre='Toulouse').id)]),

    ('Universidad Politécnica de Valencia', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Valencia').estado_id, Ciudad.objects.get(nombre='Valencia').id,
     [('Universidad Politécnica de Valencia', Ciudad.objects.get(nombre='Valencia').id)]),

    ('International Social Science Council (ISSC)', Pais.objects.get(nombre='Francia').id, Ciudad.objects.get(nombre='París').estado_id, Ciudad.objects.get(nombre='París').id,
     [('International Social Science Council (ISSC)', Ciudad.objects.get(nombre='París').id)]),

    ('Universidad de París I Panthéon-Sorbonne', Pais.objects.get(nombre='Francia').id, Ciudad.objects.get(nombre='París').estado_id, Ciudad.objects.get(nombre='París').id,
     [('Universidad de París I Panthéon-Sorbonne', Ciudad.objects.get(nombre='París').id)]),

    ('Universidad Politécnica de Cataluña', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Barcelona').estado_id, Ciudad.objects.get(nombre='Barcelona').id,
     [('Universidad Politécnica de Cataluña', Ciudad.objects.get(nombre='Barcelona').id)]),

    ('Universidad de Lérida', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Lérida').estado_id, Ciudad.objects.get(nombre='Lérida').id,
     [('Universidad de Lérida', Ciudad.objects.get(nombre='Lérida').id)]),

    ('Universidad de Brístol', Pais.objects.get(nombre='Reino Unido').id, Ciudad.objects.get(nombre='Brístol').estado_id, Ciudad.objects.get(nombre='Brístol').id,
     [('Universidad de Brístol', Ciudad.objects.get(nombre='Brístol').id)]),

    ('Universidad Nacional de Córdoba (UNC)', Pais.objects.get(nombre='Argentina').id, Ciudad.objects.get(nombre='Córdoba').estado_id, Ciudad.objects.get(nombre='Córdoba').id,
     [('Universidad Nacional de Córdoba (UNC)', Ciudad.objects.get(nombre='Córdoba').id)]),

    ('Universidad de Sinkiang (XinJiang University)', Pais.objects.get(nombre='China').id, Ciudad.objects.get(nombre='Urumchi').estado_id, Ciudad.objects.get(nombre='Urumchi').id,
     [('Universidad de Sinkiang (XinJiang University)', Ciudad.objects.get(nombre='Urumchi').id)]),

    ('Universidad Autónoma de Baja California Sur (UABCS)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='La Paz').estado_id, Ciudad.objects.get(nombre='La Paz').id,
     [('Universidad Autónoma de Baja California Sur (UABCS)', Ciudad.objects.get(nombre='La Paz').id)]),

    ('Academia de Ciencias de Cuba', Pais.objects.get(nombre='Cuba').id, Ciudad.objects.get(nombre='La Habana').estado_id, Ciudad.objects.get(nombre='La Habana').id,
     [('Instituto de Ecología y Sistemática', Ciudad.objects.get(nombre='La Habana').id)]),

    ('Universidad Interamericana para el Desarrollo (UNID)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado_id, Ciudad.objects.get(nombre='Morelia').id,
     [
         ('Universidad Interamericana para el Desarrollo, Morelia (UNID Morelia)',
          Ciudad.objects.get(nombre='Morelia').id)
     ]
     ),

    ('Universidad Autónoma de Querétaro', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Santiago de Querétaro').estado_id, Ciudad.objects.get(nombre='Santiago de Querétaro').id,
     [('Universidad Autónoma de Querétaro', Ciudad.objects.get(nombre='Santiago de Querétaro').id)]),

    ('Instituto Tecnológico y de Estudios Superiores de Monterrey (ITESM)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Monterrey').estado_id, Ciudad.objects.get(nombre='Monterrey').id,
     (
         ('Instituto Tecnológico y de Estudios Superiores de Monterrey (ITESM)',
          Ciudad.objects.get(nombre='Monterrey').id),
         ('Instituto Tecnológico y de Estudios Superiores de Monterrey, Campus Guaymas (ITESM, Campus Guaymas)',
          Ciudad.objects.get(nombre='Heroica Guaymas de Zaragoza').id)
     )
     ),

    ('Universidad de Wageningen (WUR)', Pais.objects.get(nombre='Países Bajos / Holanda').id, Ciudad.objects.get(nombre='Wageningen').estado_id, Ciudad.objects.get(nombre='Wageningen').id,
     [('Wageningen University and Research Centre', Ciudad.objects.get(nombre='Wageningen').id)]),

    ('Universidad de Hokkaido', Pais.objects.get(nombre='Japón').id, Ciudad.objects.get(nombre='Sapporo').estado_id, Ciudad.objects.get(nombre='Sapporo').id,
     [('Universidad de Hokkaido', Ciudad.objects.get(nombre='Sapporo').id)]),

    ('Biocenosis, A.C.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Biocenosis, A.C.', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Alternare, A.C.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Áporo').estado_id, Ciudad.objects.get(nombre='Áporo').id,
     [('Alternare, A.C.', Ciudad.objects.get(nombre='Áporo').id)]),

    ('Espacio Autónomo, A.C.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Espacio Autónomo, A.C.', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('H. Ayuntamiento de Morelia', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado_id, Ciudad.objects.get(nombre='Morelia').id,
     (
         ('H. Ayuntamiento de Morelia', Ciudad.objects.get(nombre='Morelia').id),
         ('Instituto Municipal de Planeación Morelia (IMPLAN)', Ciudad.objects.get(nombre='Morelia').id)
     )
     ),

    ('H. Ayuntamiento de Morelos', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelos').estado_id, Ciudad.objects.get(nombre='Morelos').id,
     [
         ('H. Ayuntamiento de Morelos', Ciudad.objects.get(nombre='Morelos').id)
     ]
     ),

    ('Universidad de Santiago de Compostela', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Santiago de Compostela').estado_id, Ciudad.objects.get(nombre='Santiago de Compostela').id,
     (
         ('Universidad de Santiago de Compostela', Ciudad.objects.get(nombre='Santiago de Compostela').id),
         ('Departamento de Farmacia y Tecnología Farmacéutica', Ciudad.objects.get(nombre='Santiago de Compostela').id)
     )
     ),

    ('Universidad de Columbia Británica (University of British Columbia (UBC))', Pais.objects.get(nombre='Canadá').id, Ciudad.objects.get(nombre='West Point Grey').estado_id, Ciudad.objects.get(nombre='West Point Grey').id,
     [('Universidad de Columbia Británica (University of British Columbia (UBC))',
         Ciudad.objects.get(nombre='West Point Grey').id)]),

    ('Universidad de Illinois en Urbana-Champaign', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Urbana-Champaign').estado_id, Ciudad.objects.get(nombre='Urbana-Champaign').id,
     [('Universidad de Illinois en Urbana-Champaign', Ciudad.objects.get(nombre='Urbana-Champaign').id)]),

    ('Universidad Autónoma de Campeche (UACAM)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Campeche').estado_id, Ciudad.objects.get(nombre='Campeche').id,
     (
         ('Universidad Autónoma de Campeche (UACAM)', Ciudad.objects.get(nombre='Campeche').id),
         ('Instituto de Ecología, Pesquerías y Oceanografía del Golfo de México (EPOMEX)',
          Ciudad.objects.get(nombre='Campeche').id)
     )
     ),

    ('El Colegio de la Frontera Sur Unidad San Cristóbal (ECOSUR)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Campeche').estado_id, Ciudad.objects.get(nombre='Campeche').id,
     [('El Colegio de la Frontera Sur Unidad San Cristóbal (ECOSUR)',
        Ciudad.objects.get(nombre='Campeche').id)]),

    ('Universidad Federal de Minas Gerais', Pais.objects.get(nombre='Brasil').id, Ciudad.objects.get(nombre='Belo Horizonte').estado_id, Ciudad.objects.get(nombre='Belo Horizonte').id,
     [('Universidad Federal de Minas Gerais', Ciudad.objects.get(nombre='Belo Horizonte').id)]),

    ('Universidad Estatal de Feira de Santana', Pais.objects.get(nombre='Brasil').id, Ciudad.objects.get(nombre='Feira de Santana').estado_id, Ciudad.objects.get(nombre='Feira de Santana').id,
     [('Universidad Estatal de Feira de Santana', Ciudad.objects.get(nombre='Feira de Santana').id)]),

    ('Universidad de Toulouse', Pais.objects.get(nombre='Francia').id, Ciudad.objects.get(nombre='Toulouse').estado_id, Ciudad.objects.get(nombre='Toulouse').id,
     [('Universidad de Toulouse', Ciudad.objects.get(nombre='Toulouse').id)]),

    ('Universidad de Granada', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Granada').estado_id, Ciudad.objects.get(nombre='Granada').id,
     [('Universidad de Granada', Ciudad.objects.get(nombre='Granada').id)]),

    ('Centro de Investigación en Alimentación y Desarrollo, A.C. (CIAD)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Culiacán Rosales').estado_id, Ciudad.objects.get(nombre='Culiacán Rosales').id,
     [('Centro de Investigación en Alimentación y Desarrollo, A.C. (CIAD)',
        Ciudad.objects.get(nombre='Culiacán Rosales').id)]),

    ('Instituto Nacional de Investigaciones Forestles, Agrícolas y Pecuarias (INIFAP)',
     Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado_id, Ciudad.objects.get(nombre='Morelia').id,
     [('Instituto Nacional de Investigaciones Forestles, Agrícolas y Pecuarias (INIFAP)',
        Ciudad.objects.get(nombre='Morelia').id)]),

    ('Universidad de Guanajuato', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Guanajuato').estado_id, Ciudad.objects.get(nombre='Guanajuato').id,
     (
         ('Universidad de Guanajuato', Ciudad.objects.get(nombre='Guanajuato').id),
         ('Departamento de Geomática e Hidráulica', Ciudad.objects.get(nombre='Guanajuato').id)
     )
     ),

    ('Instituto Tecnológico del Valle de Morelia', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado_id, Ciudad.objects.get(nombre='Morelia').id,
     [('Instituto Tecnológico del Valle de Morelia', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Universidad de Trento', Pais.objects.get(nombre='Italia').id, Ciudad.objects.get(nombre='Trento').estado_id, Ciudad.objects.get(nombre='Trento').id,
     [('Universidad de Trento', Ciudad.objects.get(nombre='Trento').id)]),

    ('Diputación Provincial de Barcelona', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Barcelona').estado_id, Ciudad.objects.get(nombre='Barcelona').id,
     [('Diputación Provincial de Barcelona', Ciudad.objects.get(nombre='Barcelona').id)]),

    ('Netherlands Organization for Scientific Research (NWO)', Pais.objects.get(nombre='Países Bajos / Holanda').id, Ciudad.objects.get(nombre='Ámsterdam').estado_id, Ciudad.objects.get(nombre='Ámsterdam').id,
     (
         ('Netherlands Organization for Scientific Research (NWO)', Ciudad.objects.get(nombre='Ámsterdam').id),
         ('Netherlands Organization for Scientific Research (WOTRO)', Ciudad.objects.get(nombre='Ámsterdam').id)
     )
     ),

    ('Alianza México REDD+', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Alianza México REDD+', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Reserva de la Biosfera de la Mariposa Monarca', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='El Rosario').estado_id, Ciudad.objects.get(nombre='El Rosario').id,
     [('Reserva de la Biosfera de la Mariposa Monarca', Ciudad.objects.get(nombre='El Rosario').id)]),

    ('Fondo Mexicano para la Conservación de la Naturaleza, A.C. (FMCN)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Fondo Mexicano para la Conservación de la Naturaleza, A.C. (FMCN)',
        Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Agencia Nacional de Promoción Científica y Tecnológica', Pais.objects.get(nombre='Argentina').id, Ciudad.objects.get(nombre='Buenos Aires').estado_id, Ciudad.objects.get(nombre='Buenos Aires').id,
     [('Agencia Nacional de Promoción Científica y Tecnológica', Ciudad.objects.get(nombre='Buenos Aires').id)]),

    ('Consejo Nacional de Investigaciones Científicas y Técnicas (CONICET)', Pais.objects.get(nombre='Argentina').id, Ciudad.objects.get(nombre='Buenos Aires').estado_id, Ciudad.objects.get(nombre='Buenos Aires').id,
     [('Consejo Nacional de Investigaciones Científicas y Técnicas (CONICET)',
        Ciudad.objects.get(nombre='Buenos Aires').id)]),

    ('Global Water Watch México', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Global Water Watch México', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Grupo Balsas para Estudio y Manejo de Ecosistemas, A.C.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado_id, Ciudad.objects.get(nombre='Morelia').id,
     [('Grupo Balsas para Estudio y Manejo de Ecosistemas, A.C.', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Fundación Produce Michoacán, A.C.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado_id, Ciudad.objects.get(nombre='Morelia').id,
     [('Fundación Produce Michoacán, A.C.', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Fundación Gonzalo Río Arronte I.A.P.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Fundación Gonzalo Río Arronte I.A.P.', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Inter-American Institute for Global Change Research', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Montevideo').estado_id, Ciudad.objects.get(nombre='Montevideo').id,
     [('Inter-American Institute for Global Change Research', Ciudad.objects.get(nombre='Montevideo').id)]),

    ('Gobierno del Estado de Jalisco', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Guadalajara').estado_id, Ciudad.objects.get(nombre='Guadalajara').id,
     (
         ('Gobierno del Estado de Jalisco', Ciudad.objects.get(nombre='Guadalajara').id),
         ('Secretaria de Medio Ambiente', Ciudad.objects.get(nombre='Guadalajara').id),
         ('Secretaría de Medio Ambiente y Desarrollo Territorial (SEMADET Jalisco)',
          Ciudad.objects.get(nombre='Guadalajara').id)
     )
     ),

    ('Universidad de Murcia', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Murcia').estado_id, Ciudad.objects.get(nombre='Murcia').id,
     [('Universidad de Murcia', Ciudad.objects.get(nombre='Murcia').id)]),

    ('Universidad Nacional de la Patagonia San Juan Bosco', Pais.objects.get(nombre='Argentina').id, Ciudad.objects.get(nombre='Comodoro Rivadavia').estado_id, Ciudad.objects.get(nombre='Comodoro Rivadavia').id,
     [('Universidad Nacional de la Patagonia San Juan Bosco', Ciudad.objects.get(nombre='Comodoro Rivadavia').id)]),

    ('Centro de Estudios Patagonia', Pais.objects.get(nombre='Argentina').id, Ciudad.objects.get(nombre='Viedma').estado_id, Ciudad.objects.get(nombre='Viedma').id,
     [('Centro de Estudios Patagonia', Ciudad.objects.get(nombre='Viedma').id)]),

    ('Colegio de Postgraduados (COLPOS)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Colegio de Postgraduados (COLPOS)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Centro Nacional para la Investigación Científica (Centre National de la Recherche Scientifique CNRS)',
     Pais.objects.get(nombre='Francia').id, Ciudad.objects.get(nombre='París').estado_id, Ciudad.objects.get(nombre='París').id,
     [('Centro Nacional para la Investigación Científica (Centre National de la Recherche Scientifique CNRS)',
        Ciudad.objects.get(nombre='París').id)]),

    ('Ministerio de Asuntos Exteriores y Desarrollo Internacional francés', Pais.objects.get(nombre='Francia').id, Ciudad.objects.get(nombre='París').estado_id, Ciudad.objects.get(nombre='París').id,
     [('Ministerio de Asuntos Exteriores y Desarrollo Internacional francés', Ciudad.objects.get(nombre='París').id)]),

    ('Universidad Autónoma de Chiapas (UNACH)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Tuxtla Gutiérrez').estado_id, Ciudad.objects.get(nombre='Tuxtla Gutiérrez').id,
     [('Universidad Autónoma de Chiapas (UNACH)', Ciudad.objects.get(nombre='Tuxtla Gutiérrez').id)]),

    ('Universidad de Texas en Austin', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Austin').estado_id, Ciudad.objects.get(nombre='Austin').id,
     [('Universidad de Texas en Austin', Ciudad.objects.get(nombre='Austin').id)]),

    ('WWF México', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('WWF México', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('International Union for Conservation of Nature (IUCN)', Pais.objects.get(nombre='Suiza').id, Ciudad.objects.get(nombre='Gland').estado_id, Ciudad.objects.get(nombre='Gland').id,
     [('International Union for Conservation of Nature (IUCN)', Ciudad.objects.get(nombre='Gland').id)]),

    ('Universidad de Toulouse-Jean Jaurès', Pais.objects.get(nombre='Francia').id, Ciudad.objects.get(nombre='Toulouse').estado_id, Ciudad.objects.get(nombre='Toulouse').id,
     [('Universidad de Toulouse-Jean Jaurès', Ciudad.objects.get(nombre='Toulouse').id)]),

    ('Instituto Politécnico Nacional (IPN)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     (
         ('Instituto Politécnico Nacional (IPN)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Centro de Investigación y de Estudios Avanzados (CINVESTAV)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)
     )
     ),

    ('Instituto Politécnico y Universidad Estatal de Virginia (Virginia Tech, VT)',
     Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Blacksburg').estado_id, Ciudad.objects.get(nombre='Blacksburg').id,
     [('Department of Biological Systems Engineering (BSE)', Ciudad.objects.get(nombre='Blacksburg').id)]),

    ('Universidad Estatal de Washington', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Pullman').estado_id, Ciudad.objects.get(nombre='Pullman').id,
     [('Universidad Estatal', Ciudad.objects.get(nombre='Pullman').id)]),

    ('Consejo Superior de Investigaciones Científicas (CSIC)', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Murcia').estado_id, Ciudad.objects.get(nombre='Murcia').id,
     [('Centro de Edafología y Biología Aplicada del Segura (CEBAS)', Ciudad.objects.get(nombre='Murcia').id)]),

    ('Universidad Pablo de Olavide (UPO)', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Sevilla').estado_id, Ciudad.objects.get(nombre='Sevilla').id,
     [('Universidad Pablo de Olavide (UPO)', Ciudad.objects.get(nombre='Sevilla').id)]),

    ('Unión Geográfica Internacional (UGI)', Pais.objects.get(nombre='Sudáfrica').id, Ciudad.objects.get(nombre='Ciudad del Cabo').estado_id, Ciudad.objects.get(nombre='Ciudad del Cabo').id,
     [('Unión Geográfica Internacional (UGI)', Ciudad.objects.get(nombre='Ciudad del Cabo').id)]),

    ('Consejo Latinoamericano de Ciencias Sociales (CLACSO)', Pais.objects.get(nombre='Argentina').id, Ciudad.objects.get(nombre='Buenos Aires').estado_id, Ciudad.objects.get(nombre='Buenos Aires').id,
     [('Consejo Latinoamericano de Ciencias Sociales (CLACSO)', Ciudad.objects.get(nombre='Buenos Aires').id)]),

    ('La Universidad de Texas A&M', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='College Station').estado_id, Ciudad.objects.get(nombre='College Station').id,
     [('La Universidad de Texas A&M', Ciudad.objects.get(nombre='College Station').id)]),

    ('Universidad de Montreal', Pais.objects.get(nombre='Canadá').id, Ciudad.objects.get(nombre='Quebec').estado_id, Ciudad.objects.get(nombre='Quebec').id,
     [('HEC Montreal', Ciudad.objects.get(nombre='Quebec').id)]),

    ('Universidad Tulane', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Nueva Orleans').estado_id, Ciudad.objects.get(nombre='Nueva Orleans').id,
     [('Universidad Tulane', Ciudad.objects.get(nombre='Nueva Orleans').id)]),

    ('Universidad Nacional de General Sarmiento (UNGS)', Pais.objects.get(nombre='Argentina').id, Ciudad.objects.get(nombre='Buenos Aires').estado_id, Ciudad.objects.get(nombre='Buenos Aires').id,
     [
         ('Instituto del Conurbano (ICO)', Ciudad.objects.get(nombre='Buenos Aires').id)
     ]
     ),

    ('Universidad de Cabo Verde', Pais.objects.get(nombre='Cabo Verde').id, Ciudad.objects.get(nombre='Praia').estado_id, Ciudad.objects.get(nombre='Praia').id,
     [('Universidad de Cabo Verde', Ciudad.objects.get(nombre='Praia').id)]),

    ('Centro di Ricerca, Sviluppo e Studi Superiori in Sardegna (CRS4)', Pais.objects.get(nombre='Italia').id, Ciudad.objects.get(nombre='Pula').estado_id, Ciudad.objects.get(nombre='Pula').id,
     [('Centro di Ricerca, Sviluppo e Studi Superiori in Sardegna (CRS4)', Ciudad.objects.get(nombre='Pula').id)]),

    ('Universidad de Ciencias de Vida de Noruega (NMBU)', Pais.objects.get(nombre='Noruega').id, Ciudad.objects.get(nombre='Oslo').estado_id, Ciudad.objects.get(nombre='Oslo').id,
     [('International Environment and Development Studies', Ciudad.objects.get(nombre='Oslo').id)]),

    ('Gobierno de Cataluña (Generalitat de Catalunya)', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Barcelona').estado_id, Ciudad.objects.get(nombre='Barcelona').id,
     [('Gobierno de Cataluña (Generalitat de Catalunya)', Ciudad.objects.get(nombre='Barcelona').id)]),

    ('Sociedad Científica Latinoamericana de Agroecología (SOCLA)', Pais.objects.get(nombre='Argentina').id, Ciudad.objects.get(nombre='Buenos Aires').estado_id, Ciudad.objects.get(nombre='Buenos Aires').id,
     [('Sociedad Científica Latinoamericana de Agroecología (SOCLA)', Ciudad.objects.get(nombre='Buenos Aires').id)]),

    ('Partido de La Costa', Pais.objects.get(nombre='Argentina').id, Ciudad.objects.get(nombre='Buenos Aires').estado_id, Ciudad.objects.get(nombre='Buenos Aires').id,
     [('Honorable Concejo Deliberante', Ciudad.objects.get(nombre='Buenos Aires').id)]),

    ('Asociación Etnobiológica Mexicana, A.C.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Asociación Etnobiológica Mexicana, A.C.', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Universidad Autónoma de Guerrero', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Chilpancingo de los Bravo').estado_id, Ciudad.objects.get(nombre='Chilpancingo de los Bravo').id,
     [
         ('Universidad Autónoma de Guerrero', Ciudad.objects.get(nombre='Chilpancingo de los Bravo').id),
         ('Unidad de Ciencias de la Tierra', Ciudad.objects.get(nombre='Chilpancingo de los Bravo').id)
     ]
     ),

    ('Academia Mexicana de Ciencias', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Academia Mexicana de Ciencias', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Instituto Tecnológico Superior de Huetamo', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Huetamo').estado_id, Ciudad.objects.get(nombre='Huetamo').id,
     [('Instituto Tecnológico Superior de Huetamo', Ciudad.objects.get(nombre='Huetamo').id)]),

    ('Universidad Pedagógica Nacional', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     (
         ('Universidad Pedagógica Nacional', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Unidad 161 Morelia', Ciudad.objects.get(nombre='Morelia').id)
     )
     ),

    ('Grupo Interdisciplinario de Tecnología Rural Apropiada, A.C. (GIRA)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Pátzcuaro').estado_id, Ciudad.objects.get(nombre='Pátzcuaro').id,
     [('Grupo Interdisciplinario de Tecnología Rural Apropiada, A.C. (GIRA)',
        Ciudad.objects.get(nombre='Pátzcuaro').id)]),

    ('International Maize and Wheat Improvement Center (CIMMYT)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='El Batán').estado_id, Ciudad.objects.get(nombre='El Batán').id,
     [('International Maize and Wheat Improvement Center (CIMMYT)', Ciudad.objects.get(nombre='El Batán').id)]),

    ('Cooperación Alemana al Desarrollo GIZ', Pais.objects.get(nombre='Alemania').id, Ciudad.objects.get(nombre='Bonn').estado_id, Ciudad.objects.get(nombre='Bonn').id,
     [('Cooperación Alemana al Desarrollo GIZ', Ciudad.objects.get(nombre='Bonn').id)]),

    ('Universidad de Florida', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Gainesville').estado_id, Ciudad.objects.get(nombre='Gainesville').id,
     (
         ('Universidad de Florida', Ciudad.objects.get(nombre='Gainesville').id),
         ('Center for Latin American Studies', Ciudad.objects.get(nombre='Gainesville').id)
     )
     ),

    ('Instituto Tecnológico Superior de Tacámbaro', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Tacámbaro').estado_id, Ciudad.objects.get(nombre='Tacámbaro').id,
     (
         ('Instituto Tecnológico Superior de Tacámbaro', Ciudad.objects.get(nombre='Tacámbaro').id),
         ('Departamento de Geociencias', Ciudad.objects.get(nombre='Tacámbaro').id)
     )
     ),

    ('Universidad Católica de Honduras (UNICAH)', Pais.objects.get(nombre='Honduras').id, Ciudad.objects.get(nombre='Tegucigalpa').estado_id, Ciudad.objects.get(nombre='Tegucigalpa').id,
     [('Universidad Católica de Honduras (UNICAH)', Ciudad.objects.get(nombre='Tegucigalpa').id)]),

    ('Universidad Autónoma Metropolitana (UAM)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     (
         ('Universidad Autónoma Metropolitana (UAM)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Universidad Autónoma Metropolitana, Unidad Xochimilco (UAM)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)
     )
     ),

    ('Instituto Tecnológico Superior de Ciudad Hidalgo', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad Hidalgo').estado_id, Ciudad.objects.get(nombre='Ciudad Hidalgo').id,
     [('Instituto Tecnológico Superior de Ciudad Hidalgo', Ciudad.objects.get(nombre='Ciudad Hidalgo').id)]),

    ('Universidad de Morelia (UDEM)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado_id, Ciudad.objects.get(nombre='Morelia').id,
     (
         ('Universidad de Morelia (UDEM)', Ciudad.objects.get(nombre='Morelia').id),
         ('Escuela de Tecnologías de la Información', Ciudad.objects.get(nombre='Morelia').id)
     )
     ),

    ('Instituto Tecnológico Superior de Puruándiro (ITESP)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Puruándiro').estado_id, Ciudad.objects.get(nombre='Puruándiro').id,
     [('Instituto Tecnológico Superior de Puruándiro (ITESP)', Ciudad.objects.get(nombre='Puruándiro').id)]),

    ('Benemérita Universidad Autónoma de Puebla (BUAP)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Puebla de Zaragoza').estado_id, Ciudad.objects.get(nombre='Puebla de Zaragoza').id,
     (
         ('Benemérita Universidad Autónoma de Puebla (BUAP)', Ciudad.objects.get(nombre='Puebla de Zaragoza').id),
         ('Instituto de Ciencias', Ciudad.objects.get(nombre='Puebla de Zaragoza').id)
     )
     ),

    ('Universidad de Zaragoza', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Zaragoza').estado_id, Ciudad.objects.get(nombre='Zaragoza').id,
     [('Departamento de Geografía y Ordenación del Territorio', Ciudad.objects.get(nombre='Zaragoza').id)]),

    ('Universidad Internacional de Andalucía (UNIA)', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Sevilla').estado_id, Ciudad.objects.get(nombre='Sevilla').id,
     [('Universidad Internacional de Andalucía (UNIA)', Ciudad.objects.get(nombre='Sevilla').id)]),

    ('Universidad de los Llanos (UNILLANOS)', Pais.objects.get(nombre='Colombia').id, Ciudad.objects.get(nombre='Villavicencio').estado_id, Ciudad.objects.get(nombre='Villavicencio').id,
     [('Facultad de Ciencias Agropecuarias y Recursos Naturales (FCARN)',
        Ciudad.objects.get(nombre='Villavicencio').id)]),

    ('Universidad Nacional de La Plata (UNLP)', Pais.objects.get(nombre='Argentina').id, Ciudad.objects.get(nombre='La Plata').estado_id, Ciudad.objects.get(nombre='La Plata').id,
     [('Facultad de Humanidades y Ciencias de la Educación', Ciudad.objects.get(nombre='La Plata').id)]),

    ('Universidad Nacional de Cuyo (UNCUYO)', Pais.objects.get(nombre='Argentina').id, Ciudad.objects.get(nombre='Mendoza').estado_id, Ciudad.objects.get(nombre='Mendoza').id,
     [('Universidad Nacional de Cuyo (UNCUYO)', Ciudad.objects.get(nombre='Mendoza').id)]),

    ('Facultad Latinoamericana de Ciencias Sociales (FLACSO)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Facultad Latinoamericana de Ciencias Sociales (FLACSO)',
        Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Universidad Autónoma del Estado de Morelos', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Cuernavaca').estado_id, Ciudad.objects.get(nombre='Cuernavaca').id,
     [('Universidad Autónoma del Estado de Morelos', Ciudad.objects.get(nombre='Cuernavaca').id)]),

    ('Universidad de Quintana Roo', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Chetumal').estado_id, Ciudad.objects.get(nombre='Chetumal').id,
     (
         ('Universidad de Quintana Roo', Ciudad.objects.get(nombre='Chetumal').id),
         ('Universidad de Quintana Roo, Campus Cozumel', Ciudad.objects.get(nombre='Cozumel').id)
     )
     ),

    ('Universidad Tecnológica de Madrid', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Madrid').estado_id, Ciudad.objects.get(nombre='Madrid').id,
     [('Universidad Tecnológica de Madrid', Ciudad.objects.get(nombre='Madrid').id)]),

    ('Universidad Internacional Jefferson', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado_id, Ciudad.objects.get(nombre='Morelia').id,
     [('Universidad Internacional Jefferson', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Universidad Federal de Espírito Santo (UFES)', Pais.objects.get(nombre='Brasil').id, Ciudad.objects.get(nombre='Vitória').estado_id, Ciudad.objects.get(nombre='Vitória').id,
     [('Universidad Federal de Espírito Santo (UFES)', Ciudad.objects.get(nombre='Vitória').id)]),

    ('Universidad del Minho', Pais.objects.get(nombre='Portugal').id, Ciudad.objects.get(nombre='Braga').estado_id, Ciudad.objects.get(nombre='Braga').id,
     [('Universidad del Minho', Ciudad.objects.get(nombre='Braga').id)]),

    ('Universidad de San Carlos de Guatemala', Pais.objects.get(nombre='Guatemala').id, Ciudad.objects.get(nombre='Ciudad de Guatemala').estado_id, Ciudad.objects.get(nombre='Ciudad de Guatemala').id,
     (
         ('Universidad de San Carlos de Guatemala', Ciudad.objects.get(nombre='Ciudad de Guatemala').id),
         ('Escuela de Biología', Ciudad.objects.get(nombre='Ciudad de Guatemala').id),
         ('Facultad de Ciencias Químicas y Farmacia', Ciudad.objects.get(nombre='Ciudad de Guatemala').id)
     )
     ),

    ('Universidad Veracruzana (UV)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Xalapa').estado_id, Ciudad.objects.get(nombre='Xalapa').id,
     (
         ('Universidad Veracruzana (UV)', Ciudad.objects.get(nombre='Xalapa').id),
         ('Facultad de Biología', Ciudad.objects.get(nombre='Xalapa').id)
     )
     ),

    ('Pontificia Universidad Javeriana', Pais.objects.get(nombre='Colombia').id, Ciudad.objects.get(nombre='Bogotá D.C.').estado_id, Ciudad.objects.get(nombre='Bogotá D.C.').id,
     [('Pontificia Universidad Javeriana', Ciudad.objects.get(nombre='Bogotá D.C.').id)]),

    ('Universidad de Ámsterdam', Pais.objects.get(nombre='Países Bajos / Holanda').id, Ciudad.objects.get(nombre='Ámsterdam').estado_id, Ciudad.objects.get(nombre='Ámsterdam').id,
     (
         ('Universidad de Ámsterdam', Ciudad.objects.get(nombre='Ámsterdam').id),
         ('Amsterdam Institute for Social Science Research (AISSR)', Ciudad.objects.get(nombre='Ámsterdam').id)
     )
     ),

    ('Instituto Federal Electoral', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Instituto Federal Electoral', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Centro de Bachillerato Tecnológico Agropecuario (CBTA)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     (
         ('Centro de Bachillerato Tecnológico Agropecuario (CBTA)',
          Ciudad.objects.get(nombre='Ciudad de México, CDMX').id),
         ('Centro de Bachillerato Tecnológico Agropecuario #89 José Vasconcelos (CBTA 89)',
          Ciudad.objects.get(nombre='Taretan').id)
     )
     ),

    ('Tecnológico Nacional de México (TecNM)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Tecnológico Nacional de México (TecNM)', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Instituto Venezolano de Investigaciones Científicas (IVIC)', Pais.objects.get(nombre='Venezuela').id, Ciudad.objects.get(nombre='Los Salias').estado_id, Ciudad.objects.get(nombre='Los Salias').id,
     [('Instituto Venezolano de Investigaciones Científicas (IVIC)', Ciudad.objects.get(nombre='Los Salias').id)]),

    ('Instituto para el Desarrollo Sustentable en Mesoamérica, A.C.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='San Cristóbal de las Casas').estado_id, Ciudad.objects.get(nombre='San Cristóbal de las Casas').id,
     [('Instituto para el Desarrollo Sustentable en Mesoamérica, A.C.',
        Ciudad.objects.get(nombre='San Cristóbal de las Casas').id)]),

    ('Signos Diseño & Publicidad', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado_id, Ciudad.objects.get(nombre='Morelia').id,
     [('Signos Diseño & Publicidad', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Tecnologías y Servicios Agrarios, S.A (Tragsatec)', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Lérida').estado_id, Ciudad.objects.get(nombre='Lérida').id,
     [('Tecnologías y Servicios Agrarios, S.A (Tragsatec)', Ciudad.objects.get(nombre='Lérida').id)]),

    ('Meneu Distribución, S.A.', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Albuixech').estado_id, Ciudad.objects.get(nombre='Albuixech').id,
     [('Meneu Distribución, S.A.', Ciudad.objects.get(nombre='Albuixech').id)]),

    ('Instituto Cartográfico y Geológico de Cataluña (ICGC)', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Barcelona').estado_id, Ciudad.objects.get(nombre='Barcelona').id,
     [('Instituto Cartográfico y Geológico de Cataluña', Ciudad.objects.get(nombre='Barcelona').id)]),

    ('Universidad de Dar es-Salam', Pais.objects.get(nombre='Tanzania').id, Ciudad.objects.get(nombre='Dar es-Salam').estado_id, Ciudad.objects.get(nombre='Dar es-Salam').id,
     [('Universidad de Dar es-Salam', Ciudad.objects.get(nombre='Dar es-Salam').id)]),

    ('Universidad Autónoma de Tlaxcala', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Tlaxcala de Xicohténcatl').estado_id, Ciudad.objects.get(nombre='Tlaxcala de Xicohténcatl').id,
     [('Universidad Autónoma de Tlaxcala', Ciudad.objects.get(nombre='Tlaxcala de Xicohténcatl').id)]),

    ('Harlen Administrativo SA de CV', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado_id, Ciudad.objects.get(nombre='Morelia').id,
     [('Harlen Administrativo SA de CV', Ciudad.objects.get(nombre='Morelia').id)]),

    ('CodiNet S.A. DE C.V.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado_id,  Ciudad.objects.get(nombre='Morelia').id,
     [('CodiNet S.A. DE C.V.', Ciudad.objects.get(nombre='Morelia').id)]),

    ('International Society for the Study of Religion, Nature and Culture (ISSRNC)',
     Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Gainesville').estado_id, Ciudad.objects.get(nombre='Gainesville').id,
     [('International Society for the Study of Religion, Nature and Culture (ISSRNC)',
        Ciudad.objects.get(nombre='Gainesville').id)]),

    ('Conference of Latin Americanist Geographers (CLAG)', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Gainesville').estado_id, Ciudad.objects.get(nombre='Gainesville').id,
     [('Conference of Latin Americanist Geographers (CLAG)', Ciudad.objects.get(nombre='Gainesville').id)]),

    ('Ayuntamiento de Cuernavaca', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Cuernavaca').estado_id, Ciudad.objects.get(nombre='Cuernavaca').id,
     [('Ayuntamiento de Cuernavaca', Ciudad.objects.get(nombre='Cuernavaca').id)]),

    ('Gobierno del Estado de Morelos', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Cuernavaca').estado_id, Ciudad.objects.get(nombre='Cuernavaca').id,
     [('Gobierno del Estado de Morelos', Ciudad.objects.get(nombre='Cuernavaca').id)]),

    ('TECIF', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado_id, Ciudad.objects.get(nombre='Morelia').id,
     [('TECIF', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Fideicomisos Instituidos en Relación con la Agrícultura (FIRA)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado_id, Ciudad.objects.get(nombre='Morelia').id,
     [('Fideicomisos Instituidos en Relación con la Agrícultura (FIRA)', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Commission for Environmental Cooperation', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').estado_id, Ciudad.objects.get(nombre='Ciudad de México, CDMX').id,
     [('Commission for Environmental Cooperation', Ciudad.objects.get(nombre='Ciudad de México, CDMX').id)]),

    ('Universidad Vasco de Quiroga (UVAQ)', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado_id, Ciudad.objects.get(nombre='Morelia').id,
     [('Universidad Vasco de Quiroga (UVAQ)', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Ministerio de Infraestructura, Provincia de Buenos Aires', Pais.objects.get(nombre='Argentina').id, Ciudad.objects.get(nombre='Buenos Aires').estado_id, Ciudad.objects.get(nombre='Buenos Aires').id,
     [('Ministerio de Infraestructura', Ciudad.objects.get(nombre='Buenos Aires').id)]),

    ('Fondo Monarca, A.C.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado_id, Ciudad.objects.get(nombre='Morelia').id,
     [('Fondo Monarca, A.C.', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Universidad de California en Berkeley', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Berkeley').estado_id, Ciudad.objects.get(nombre='Berkeley').id,
     (
         ('Universidad de California en Berkeley', Ciudad.objects.get(nombre='Berkeley').id),
         ('Center for Latin American Studies (CLAS)', Ciudad.objects.get(nombre='Berkeley').id)
     )
     ),

    ('EcoLogic Development Fund', Pais.objects.get(nombre='Estados Unidos de América').id, Ciudad.objects.get(nombre='Cambridge').estado_id, Ciudad.objects.get(nombre='Cambridge').id,
     [('EcoLogic Development Fund', Ciudad.objects.get(nombre='Cambridge').id)]),

    ('Ecotecnologías, A.C.', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').estado_id, Ciudad.objects.get(nombre='Morelia').id,
     [('Ecotecnologías, A.C.', Ciudad.objects.get(nombre='Morelia').id)]),

    ('Universidad Nacional Agraria La Molina (UNALM)', Pais.objects.get(nombre='Perú').id, Ciudad.objects.get(nombre='Lima').estado_id, Ciudad.objects.get(nombre='Lima').id,
     [('Universidad Nacional Agraria La Molina (UNALM)', Ciudad.objects.get(nombre='Lima').id)]),
)

for i in Instituciones:
    e = Institucion(nombre=i[0], pais=Pais(pk=i[1]), estado=Estado(pk=i[2]), ciudad=Ciudad(pk=i[3]))
    e.save()
    print("Agregada la Institución " + i[0].upper() + " para el país " + str(Pais.objects.get(pk=i[1]).nombre))

    for j in i[4]:
        f = Dependencia(nombre=j[0], ciudad=Ciudad.objects.get(pk=j[1]), estado=Ciudad.objects.get(pk=j[1]).estado, pais=Ciudad.objects.get(pk=j[1]).estado.pais, institucion=Institucion(pk=e.pk))
        f.save()
        print(" --- Agregada la Dependencia " + j[0].upper() + " para la institución " + str(
            Institucion.objects.get(pk=e.pk).nombre))

User.objects.create_superuser(username='admin', email='cesar.benjamin@enesmorelia.unam.mx', password='ciga2017',
                              pais_origen=Pais.objects.get(nombre='México'),
                              pais=Pais.objects.get(nombre='México'),
                              estado=Estado.objects.get(nombre='Michoacán de Ocampo'),
                              ciudad=Ciudad.objects.get(nombre='Morelia'), genero='M')

Usuarios = (
    ('usr_st', 'usr_st', 'usr_st', 'OTRO', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').id,
        '-', 'Aso3U', 'M'),
    ('mario.figueroa', 'Figueroa Cárdenas', 'Mario', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '16ymf', 'M'),
    ('yunsh', 'yunsh', 'yunsh', 'OTRO', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').id,
     '-', 'yunsh', 'F'),

    ('berenice.solis', 'Berenice', 'Solis Castillo', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '6ESlj', 'F'),
    ('saray.bucio', 'Saray', 'Bucio Mendoza', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'usmv1', 'F'),
    ('quetzalcoatl.orozco', 'Quetzalcoatl', 'Orozco Ramirez', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ubFaE', 'M'),
    ('lourdes.gonzalez', 'Maria Lourdes', 'González Arqueros', 'OTRO', Pais.objects.get(nombre='España').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'EeGJW', 'F'),
    ('karine.lefebvre', 'Karine', 'Lefebvre', 'INVESTIGADOR', Pais.objects.get(nombre='Francia').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '7Gs53', 'F'),
    ('lorena.poncela', 'Lorena', 'Poncela Rodríguez', 'OTRO', Pais.objects.get(nombre='España').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'hnSDn', 'F'),
    ('pedro.urquijo', 'Pedro Sergio', 'Urquijo Torres', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'D', 'fEVor', 'M'),
    ('hilda.rivas', 'Hilda', 'Rivas', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'C', 'OH7fq', 'F'),
    ('jose.navarrete', 'José Antonio', 'Navarrete Pacheco', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'd2BFg', 'M'),
    ('luis.morales', 'Luis Miguel', 'Morales Manilla', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'C', 'ftTrS', 'M'),
    ('alejandra.larrazabal', 'Alejandra Patricia', 'Larrazábal De la Via', 'TECNICO',
     Pais.objects.get(nombre='Bolivia').id, Ciudad.objects.get(nombre='Morelia').id, 'C', 'Ersp5', 'F'),
    ('maria.carmona', 'María Estela', 'Carmona Jiménez', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'C', 'Yrcbo', 'F'),
    ('manuel.bollo', 'Manuel', 'Bollo Manent', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'D', 'zF8gk', 'M'),
    ('yan.gao', 'Yan', 'Gao', 'INVESTIGADOR', Pais.objects.get(nombre='China').id,
     Ciudad.objects.get(nombre='Morelia').id, 'B', 'UiSNj', 'F'),
    ('gabriela.cuevas', 'Gabriela', 'Cuevas García', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'B', 'J8YEd', 'F'),
    ('margaret.skutsch', 'Margaret', 'Skutsch', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'YxU7H', 'F'),
    ('angel.priego', 'Angel Guadalupe', 'Priego Santander', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'C', '9hUCZ', 'M'),
    ('brian.napoletano', 'Brian', 'Napoletano', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'B', '9OzFa', 'M'),
    ('manuel.mendoza', 'Manuel Eduardo', 'Mendoza Cantú', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'D', 'wjZ8d', 'M'),
    ('keith.mccall', 'Keith Michael', 'McCall', 'INVESTIGADOR', Pais.objects.get(nombre='Reino Unido').id,
     Ciudad.objects.get(nombre='Morelia').id, 'D', 'dNnfH', 'M'),
    ('jean.mas', 'Jean Francois', 'Mas', 'INVESTIGADOR', Pais.objects.get(nombre='Francia').id,
     Ciudad.objects.get(nombre='Morelia').id, 'D', 'GUKjy', 'M'),
    ('adrian.ghilardi', 'Adrián', 'Ghilardi', 'INVESTIGADOR', Pais.objects.get(nombre='Italia').id,
     Ciudad.objects.get(nombre='Morelia').id, 'B', 'DgFdm', 'M'),
    ('claudio.garibay', 'Claudio', 'Garibay Orozco', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'C', '88SSU', 'M'),
    ('ana.burgos', 'Ana Laura', 'Burgos Tornadú', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jEvFg', 'F'),
    ('gerardo.bocco', 'Gerardo Héctor Rubén', 'Bocco Verdinelli', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'D', 'f4r8Q', 'M'),
    ('francisco.bautista', 'Francisco', 'Bautista Zúñiga', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'C', '98big', 'M'),
    ('sara.barrasa', 'Sara', 'Barrasa García', 'INVESTIGADOR', Pais.objects.get(nombre='España').id,
     Ciudad.objects.get(nombre='Morelia').id, 'B', 'prgh0', 'F'),
    ('marta.astier', 'Marta', 'Astier', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'sNeKu', 'F'),
    ('antonio.vieyra', 'Jose Antonio', 'Vieyra Medrano', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'C', 'fs3S7', 'M'),
    ('hugo.zavala', 'Hugo Alejandro', 'Zavala Vaca', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'C', 'n80rn', 'M'),
    ('rosaura.paez', 'Rosaura', 'Páez Bistrain', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'C', 'puYq7', 'F'),
    ('yadira.mendez', 'Yadira Mireya', 'Méndez Lemus', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'B', '58Tln', 'F'),
    ('gabriela.lemus', 'Gabriela', 'Lemus', 'ADMINISTRATIVO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'B', 'Hj7Jx', 'F'),
    ('fabiola.velazquez', 'Fabiola Araceli', 'Velázquez Ayala', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'c3fhV', 'F'),
    ('alejandro.velazquez', 'Alejandro', 'Velázquez Montes', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'rWKXd', 'M'),
    ('alina.alvarez', 'Alina', 'Alvarez Larrain', 'POSTDOCTORADO', Pais.objects.get(nombre='Argentina').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'h8fvn', 'F'),
    ('arturo.muniz', 'Arturo', 'Muñiz Jauregui', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '10002', 'M'),
    ('maria.ramirez', 'María Isabel', 'Ramírez Ramírez', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, 'D', 'Y9jOf', 'F'),
    ('jaime.paneque', 'Jaime', 'Paneque Gálvez', 'INVESTIGADOR', Pais.objects.get(nombre='España').id, Ciudad.objects.get(nombre='Morelia').id, 'B', 'Y6pdF', 'M'),
    ('cinthia.ruiz', 'Cinthia', 'Ruiz López', 'INVESTIGADOR', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').id, '-', 'cinthia.ruiz', 'F'),
    ('frida.guiza', 'Frida Nadiezda', 'Güiza Valverde', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'Yl5I4', 'F'),
    ('mariana.vallejo', 'Mariana', 'Vallejo Ramos', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '4th7o', 'F'),
    ('hebe.vessuri', 'Hebe', 'Vessuri', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'vmh1r', 'F'),
    ('rosa.rivas', 'Rosa', 'Rivas', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00002', 'F'),
    ('manuel.zavala', 'Manuel', 'Zavala', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00003', 'M'),
    ('raquel.gonzalez', 'Raquel', 'González García', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'biabG', 'F'),
    ('omar.montano', 'Omar', 'Montaño', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00004', 'M'),
    ('arturo.balderas', 'Arturo', 'Balderas Torres', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00005', 'M'),
    ('adriana.flores', 'Adriana Carolina', 'Flores Díaz', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'df4ty', 'F'),
    ('armonia.borrego', 'Armonía', 'Borrego', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'gb4go', 'F'),
    ('hernando.rodriguez', 'Hernando', 'Rodriguez', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00006', 'M'),
    ('sara.ortiz', 'Sara', 'Ortiz', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00007', 'F'),
    ('roser.manejo', 'Roser', 'Manejo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00008', 'F'),
    ('pablo.argueta', 'Pablo', 'Argueta', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00009', 'M'),
    ('beatriz.tejera', 'Beatriz', 'de la Tejera', 'INVESTIGADOR', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00010', 'F'),
    ('ana.moreno', 'Ana Isabel', 'Moreno Calles', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00011', 'F'),
    ('marcela.morales', 'Marcela', 'Morales', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00012', 'F'),
    ('jorge.gonzalez', 'Jorge', 'Gonzalez', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00013', 'M'),
    ('dante.ayala', 'Dante Ariel ', 'Ayala Ortiz', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00014', 'M'),
    ('jose.pimentel', 'Jose', 'Pimentel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00015', 'M'),
    ('martha.velazquez', 'Martha', 'Velazquez', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00016', 'F'),
    ('rocio.aguirre', 'Rocío', 'Aguirre', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00017', 'F'),
    ('margarita.alvarado', 'Margarita', 'Alvarado', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00018', 'F'),
    ('carina.grajales', 'Carina', 'Grajales', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00019', 'F'),
    ('luis.garcia', 'Luis', 'García', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00020', 'M'),
    ('luz.garcia', 'Luz Elena', 'García Martínez', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00021', 'F'),
    ('luis.ramirez', 'Luis', 'Ramírez', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00022', 'M'),
    ('maria.vizcaino', 'María', 'Vizcaíno', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00023', 'F'),
    ('andrew.boni', 'Andrew', 'Boni', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00024', 'M'),
    ('john.healey', 'John', 'Healey', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00025', 'M'),
    ('eduardo.frapolli', 'Eduardo', 'Frapolli', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00026', 'M'),
    ('miguel.martinez', 'Miguel', 'Martínez', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00027', 'M'),
    ('g.legorreta.paulin', 'G', 'Legorreta Paulin', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00028', 'M'),
    ('j.tiburio', 'J', 'Tiburio', 'OTRO', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').id,
     '-', '00029', 'F'),
    ('lucia.almeida', 'Lucia', 'Almeida', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00030', 'F'),
    ('roberto.lindig', 'Roberto', 'Lindig', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00031', 'M'),
    ('enrique.ojeda', 'Enrique', 'Ojeda', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00032', 'M'),
    ('jose.farina', 'José', 'Fariña', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00033', 'M'),
    ('jesus.fuentes', 'Jesús', 'Fuentes', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00034', 'M'),
    ('sophie.avila', 'Sophie', 'Avila', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00035', 'F'),
    ('guillermo.salas', 'Guillermo', 'Salas', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00036', 'M'),
    ('gian.delgado', 'Gian', 'Delgado', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00037', 'M'),
    ('octavio.gonzalez', 'Octavio', 'González', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00038', 'M'),
    ('jose.hernandez', 'José', 'Hernández', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00039', 'M'),
    ('leticia.merino', 'Leticia', 'Merino', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', '00040', 'F'),
    ('luis.macias', 'José Luis', 'Macías', 'OTRO', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').id, '-', '00041', 'M'),
    ('jovanka.spiric', 'Jovanka', 'Spiric', 'POSTDOCTORADO', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').id, '-', 'jovanka.spiric', 'F'),
    ('rafael.garcia', 'Rafael', 'García Ruíz', 'POSTDOCTORADO', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').id, '-', 'rafael.garcia', 'M'),
    ('montserrat.serrano', 'Montserrat', 'Serrano Medrano', 'POSTDOCTORADO', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').id, '-', 'montserrat.serrano', 'F'),
)


for i in Usuarios:
    u = User.objects.create_user(username=i[0], first_name=i[1], last_name=i[2], tipo=i[3], pais_origen=Pais(pk=i[4]),
                                 pais=Pais.objects.get(nombre='México'),
                                 estado=Estado.objects.get(nombre='Michoacán de Ocampo'),
                                 ciudad=Ciudad(pk=i[5]), pride=i[6], rfc=i[7], direccion=i[0], password=i[7],
                                 email=i[0] + '@ciga.unam.mx', genero=i[8])
    print(u)

Usuarios = (
    ('yameli.aguilar', 'Aguilar Duarte', 'Yameli', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'yameli.aguilar', 'F'),
    ('luis.cancer', 'Cancer Pomar', 'Luis', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'luis.cancer', 'M'),
    ('r.aguilar.romero', 'Aguilar Romero', 'R.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'r.aguilar.romero', 'M'),
    ('raul.aguirre', 'Aguirre Gómez', 'Raúl', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'raul.aguirre', 'M'),
    ('eduardo.alanis', 'Alanís Rodríguez', 'Eduardo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'eduardo.alanis', 'M'),
    ('israde.alcantara', 'Alcántara', 'Israde', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'israde.alcantara', 'F'),
    ('j.alcantar.mejía', 'Alcántar Mejía', 'J.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'j.alcantar.mejía', 'M'),
    ('sonia.altizer', 'Altizer', 'Sonia', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'sonia.altizer', 'F'),
    ('fernando.alvarado', 'Alvarado Ramos', 'Fernando', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'fernando.alvarado', 'M'),
    ('alfredo.amador', 'Amador García', 'Alfredo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alfredo.amador', 'M'),
    ('mirna.ambrosio', 'Ambrosio', 'Mirna', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'Mirna.ambrosio', 'F'),
    ('jose.anaya', 'Anaya Gomez', 'José Eduardo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jose.anaya', 'M'),
    ('carlos.anaya', 'Anaya Merchant', 'Carlos Antonio', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'carlos.anaya', 'M'),
    ('a.andablo.reyes', 'Andablo Reyes', 'A.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'a.andablo.reyes', 'F'),
    ('rene.arzuffi', 'Arzuffi Barrera', 'René', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'rene.arzuffi', 'M'),
    ('patricia.balvanera', 'Balvanera', 'Patricia', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'patricia.balvanera', 'F'),
    ('rc.barrientos.medina', 'Barrientos Medina', 'R. C.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'rc.barrientos.medina', ';'),
    ('m.boada.junca', 'Boada Juncá', 'M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'm.boada.junca', 'M'),
    ('encarnacion.bobadilla', 'Bobadilla Soto', 'Encarnación Ernesto', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'enc.bobadilla', 'F'),
    ('nayda.bravo', 'Bravo Hernández', 'Nayda Luz', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'nayda.bravo', 'F'),
    ('miguel.bravo', 'Bravo', 'Miguel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'miguel.bravo', 'M'),
    ('lincoln.brwoer', 'Brower', 'Lincoln P.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'lincoln.brwoer', 'M'),
    ('stephen.brush', 'Brush', 'Stephen', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'stephen.brush', 'M'),
    ('bryan.pijanowski', 'Pijanowski', 'Bryan C.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'bryan.pijanowski', 'M'),
    ('matthias.bucker', 'Bücker', 'Matthias', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'matthias.bucker', 'M'),
    ('hector.cabadas', 'Cabadas Báez', 'Héctor Víctor', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'hector.cabadas', 'M'),
    ('cecilia.caballero', 'Caballero Miranda', 'Cecilia I.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'cecilia.caballero', 'F'),
    ('martin.cardena', 'Cadena Salgado', 'Martin', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'martin.cardenas', 'M'),
    ('nadia.campos', 'Campos Salas', 'Nadia', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'nadia.campos', 'F'),
    ('m.campos.sanchez', 'Campos Sánchez', 'M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'a.campos.sanchez', 'M'),
    ('jp.carbonelli', 'Carbonelli', 'J. P.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jp.carbonelli', 'M'),
    ('v.palamarczuk', 'Palamarczuk', 'V.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'v.palamarczuk', 'F'),
    ('t.carlon.allende', 'Carlón Allende', 'T.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 't.carlon.allende', 'M'),
    ('angel.carrancho', 'Carrancho', 'Ángel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'angel.carrancho', 'M'),
    ('oswaldo.carrillo', 'Carrillo', 'Oswaldo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'oswaldo.carrillo', 'M'),
    ('alejandro.casas', 'Casas Fernández', 'Alejandro', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alejandro.casas', 'M'),
    ('miguel.castillo', 'Castillo Santiago', 'Miguel Angel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'miguel.castillo', 'M'),
    ('alicia.castillo', 'Castillo', 'Alicia', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alicia.castillo', 'F'),
    ('federico.castrejon', 'Castrejón Ayala', 'Federico', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'federico.castrejon', 'M'),
    ('raul.cejudo', 'Cejudo Ruiz', 'Raul', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'raul.cejudo', 'M'),
    ('laura.chang', 'Chang Martínez', 'Laura', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'laura.chang', 'F'),
    ('noah.chutz', 'Chutz', 'Noah', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'noah.chutz', 'M'),
    ('alejandro.collantes', 'Collantes', 'Alejandro', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alejandro.collantes', 'M'),
    ('camilo.correa', 'Correa Ayram', 'Camilo A.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'camilo.correa', 'M'),
    ('stephane.couturier', 'Couturier', 'Stéphane', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'stephane.couturier', 'F'),
    ('zoila.cardenas', 'Cárdenas Mendoza', 'Zoila', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'zoila.cardenas', 'F'),
    ('o.delgado.carranza', 'Delgado Carranza', 'O.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'o.delgado.carranza', 'M'),
    ('luis.dourado', 'Dourado', 'Luís', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'luis,dourado', 'M'),
    ('inna.dubrovina', 'Dubrovina', 'Inna', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'inna.dubrovina', 'F'),
    ('ek.del.val', 'de Gortari', 'Ek del Val', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ek.del.val', 'F'),
    ('miguel.escalona', 'Escalona', 'Miguel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'miguel.escalona', 'M'),
    ('ileana.espejel', 'Espejel', 'Ileana', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ileana.espejel.', 'F'),
    ('lm.espinosa.rodriguez', 'Espinosa Rodríguez', 'L. M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'e.rodriguez', 'M'),
    ('a.espinoza.maya', 'Espinoza Maya', 'A.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'a.espinoza.maya', 'F'),
    ('bailis.espinoza', 'Espinoza Medrano', 'Bailis', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'bailis.Espinoza', 'F'),
    ('fabricio.espinoza', 'Espinoza Medrano', 'Fabricio', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'fabricio.espinoza', 'M'),
    ('osvaldo.esquivel', 'Esquivel Lucatero', 'Osvaldo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'osvaldo.esquivel', 'M'),
    ('andres.etter', 'Etter', 'Andrés', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'andres.etter', 'M'),
    ('b.figueroa.rangel', 'Figueroa Rangel', 'B.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'figueroa.rangel', 'M'),
    ('linda.fink', 'Fink', 'Linda S.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'linda.fink', 'F'),
    ('roberto.fisher', 'Fisher Ortíz', 'Roberto Alexander', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'roberto.fisher', 'M'),
    ('a.flamenco.sandoval', 'Flamenco Sandoval', 'A.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'flamenco.sandoval', 'M'),
    ('angel.flores', 'Flores Domínguez', 'Angel David', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'angel.flores', 'M'),
    ('ivan.franch', 'Franch Pardo', 'Iván', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ivan.franch', 'M'),
    ('oscar.frausto', 'Frausto', 'Oscar', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'oscar.frausto', 'M'),
    ('mario.freitas', 'Freitas', 'Mário', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'mario.freitas', 'M'),
    ('gabriel.vazquez', 'Vázquez', 'C. Gabriel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'gabriel.vazquez', 'M'),
    ('artemio.gallegos', 'Gallegos García', 'Artemio', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'artemio.gallegos', 'M'),
    ('angeles.gallegos', 'Gallegos A.', 'Angeles', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'angeles.gallegos', 'F'),
    ('victoria.reyes', 'Reyes García', 'Victoria', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'victoria.reyes', 'F'),
    ('manuel.macia', 'J. Macía', 'Manuel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'manuel.macia', 'M'),
    ('m.farfan.gutierez', 'Farfán Gutiérrez', 'M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'm.farfan.gutierez', 'M'),
    ('jorge.gama', 'Gama Castro', 'Jorge E.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jorge.gama', 'M'),
    ('andres.garcia', 'Garcia', 'Andres', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'andres.garcia', 'M'),
    ('ana.garcia', 'García de Fuentes', 'Ana', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ana.garcia', 'F'),
    ('eduardo.garcia', 'García', 'Eduardo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'eduardo.garcia', 'M'),
    ('f.gavi.reyes', 'Gavi Reyes', 'F.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'f.gavi.reyes', 'F'),
    ('mayra.gavito', 'Gavito', 'Mayra', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'mayra.gavito', 'F'),
    ('gilberto.gaxiola', 'Gaxiola Castro', 'Gilberto', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'gilberto.gaxiola', 'M'),
    ('d.geissert.kientz', 'Geissert Kientz', 'D.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'd.geissert.kientz', 'M'),
    ('peter.gerritsen', 'W. Gerritsen', 'Peter R.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'peter.gerritsen', 'M'),
    ('joaquin.gimenez', 'Giménez de Azcarate', 'Joaquin', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'joaquin.gimenez', 'M'),
    ('pierre.glynn', 'Glynn', 'Pierre', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'pierre.glynn', 'M'),
    ('avto.gogichaishvili', 'Gogichaishvili', 'Avto', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'gogichaishvili', 'M'),
    ('j.gonzález.areu', 'González Areu', 'J.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'gonzález.areu', 'M'),
    ('claudio.gonzalez', 'González Arqueros', 'Claudio', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'claudio.gonzalez', 'M'),
    ('carlos.gonzalez', 'González Esquivel', 'Carlos', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'carlos.gonzalez', 'M'),
    ('gaspar.gonzalez', 'González Sansón', 'Gaspar', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'gaspar.gonzalez', 'M'),
    ('maria.gonzalez', 'González Santiago', 'María Virginia', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'maria.gonzalez', 'M'),
    ('luis.gopar', 'Gopar Merino', 'Luis Fernando', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'luis.gopar', 'M'),
    ('solange.grimoldi', 'Grimoldi', 'Solange', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'solange.grimoldi', 'M'),
    ('maximilien.gueze', 'Gueze', 'Maximilien', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'maximilien.gueze', 'M'),
    ('francisco.gurri', 'Gurri', 'Francisco', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'francisco.gurri', 'M'),
    ('gemma.gomez', 'Gómez Castillo', 'Gemma', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'gemma.gomez', 'F'),
    ('enrique.gomez', 'Gómez Pech', 'Enrique', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'enrique.gomez', 'M'),
    ('ernest.williams', 'H. Williams', 'Ernest', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ernest.williams', 'M'),
    ('muki.haklay', 'Haklay', 'Muki', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'muki.haklay', 'M'),
    ('vm.hernandez.madrigal', 'Hernández Madrigal', 'V. M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'vm.hernandez', 'M'),
    ('aldo.hernandez', 'Hernández  Magaña', 'Aldo I.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'aldo.hernandez', 'M'),
    ('benigno.hernandez', 'Hernández de la Torre', 'Benigno', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'benigno.hernandez', 'M'),
    ('ruben.hernandez', 'Hernández Morales', 'Ruben', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ruben.hernandez', 'M'),
    ('keith.hobson', 'Hobson', 'Keith A.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'hobson.keith', 'M'),
    ('isabel.ramirez', 'Ramirez', 'M. Isabel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'isabel.ramirez', 'F'),
    ('e.vera.isunza', 'Isunza Vera', 'E.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'e.vera.isunza', 'M'),
    ('daniel.iura', 'Iura Gonzalez', 'Daniel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'daniel.iura', 'M'),
    ('thomas.j.ihl', 'J. Ihl', 'Thomas', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'thomas.j.ihl', 'M'),
    ('jaime.urrutia', 'Urrutia Fucugauchi', 'Jaime', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jaime.urrutia', 'M'),
    ('pablo.jaramillo', 'Jaramillo López', 'Pablo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'pablo.jaramillo', 'M'),
    ('ramon.jarquin', 'Jarquin Gálvez', 'Ramón', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ramon.jarquin', 'M'),
    ('adrian.mas', 'Jean François', 'Adrián Mas', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'adrian.mas', 'M'),
    ('r.jimenez.ramirez', 'Jiménez Ramírez', 'R.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'r.jimenez', 'M'),
    ('erik.juarez', 'Juarez Blanquet', 'Erik', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'erik.juarez', 'M'),
    ('elias.ucakuwun', 'K. Ucakuwun', 'Elias', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'elias.ucakuwun', 'M'),
    ('ken.oyama', 'Oyama', 'Alberto Ken', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ken.oyama', 'M'),
    ('maxime.kieffer', 'Kieffer', 'Maxime', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'maxime.kieffer', 'M'),
    ('nagesh.kolagani', 'Kolagani', 'Nagesh', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'nagesh.kolagani', 'M'),
    ('marit.kraagt', 'Kraagt', 'Marit', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'marit.kraagt', 'M'),
    ('rosario.langrave', 'Langrave', 'Rosario', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'rosario.langrave', 'F'),
    ('Lemoine,rodríguez', 'Lemoine Rodríguez', 'R.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'Lemoine,rodríguez', 'F'),
    ('rodrigo.liendo', 'Liendo', 'Rodrigo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'rodrigo.liendo', 'M'),
    ('a.lomelí.jimenez', 'Lomelí Jiménez', 'A.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'a.lomelí', 'F'),
    ('lourdes,gonzalez', 'González Arqueros', 'M. Lourdes', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'lourdes,gonzalez', 'F'),
    ('jesus.luna', 'Luna Béjar', 'Jesús Alonso', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jesus.luna', 'M'),
    ('cruz.lopez', 'López Contreras', 'Cruz', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'cruz.lopez', 'M'),
    ('erna.lopez', 'López Granados', 'Erna M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'erna.lopez', 'F'),
    ('gilbert.nduru', 'M. Nduru', 'Gilbert', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'gilbert.nduru', 'M'),
    ('miguel.maass', 'Maass Moreno', 'Miguel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'miguel.maass', 'M'),
    ('javier.martinez', 'Martínez', 'Javier', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'javier.martinez', 'M'),
    ('y.martinez.ruiz', 'Martínez Ruíz', 'Y.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'y.martinez.ruiz', 'M'),
    ('tomas.martinez', 'Martínez Saldaña', 'Tomás', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'tomas.martinez', 'M'),
    ('ayesa.martinez', 'Martínez Serrano', 'Ayesa', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ayesa.martinez', 'F'),
    ('leonardo.martinez', 'Martínez Torres', 'H. Leonardo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'leonardo.martinez', 'M'),
    ('emily.mcclung', 'McClung de Tapia', 'Emily', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'emily.mcclung', 'M'),
    ('paula.melic', 'Melic', 'Paula', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'paula.melic', 'F'),
    ('josemaria.michel', 'Michel Fuentes', 'Jose Maria', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'josemaria.michel', 'M'),
    ('rosa.molina', 'Molina Rojas', 'Rosa María', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'rosa.molina', 'F'),
    ('jc.mora.chaparro', 'Mora Chaparro', 'J. C.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jc.mora.chaparro', 'M'),
    ('j.morales.contreras', 'Morales Contreras', 'J.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'j.morales.contreras', 'M'),
    ('jaime.morales', 'Morales Hernández', 'Jaime', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jaime.morales', 'M'),
    ('helda.morales', 'Morales Iglesias', 'Helda', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'h.morales.iglesias', 'M'),
    ('juan.morales', 'Morales', 'Juan J.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'juan.morales', 'M'),
    ('wendy.morales', 'Morales', 'Wendy', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'wendy.morales', 'F'),
    ('julius.muchemi', 'Muchemi', 'Julius G.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'julius.muchemi', 'M'),
    ('antonio.mendez', 'Méndez Lemus', 'Antonio', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'antonio.mendez', 'M'),
    ('alfred.gichu', 'N. Gichu', 'Alfred', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alfred.gichu', 'M'),
    ('francis.wegulo', 'N. Wegulo', 'Francis', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'francis.wegulo', 'M'),
    ('alejandro.nene', 'Nené Preciado', 'Alejandro Jalmacin', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alejandro.nene', 'M'),
    ('julie.noriega', 'Noriega', 'Julie', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'julie.noriega', 'M'),
    ('ricardo.napoles', 'Nápoles', 'Ricardo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ricardo.napoles', 'M'),
    ('karen.oberhauser', 'Oberhauser', 'Karen S.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'karen.oberhauser', 'F'),
    ('luis.olivares', 'Olivares Martínez', 'Luis Daniel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'luis.olivares', 'M'),
    ('eduardo.orihuela', 'Orihuela Estefan', 'Eduardo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'eduardo.orihuela', 'M'),
    ('alberto.orozco', 'Orozco Moreno', 'Alberto', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alberto.orozco', 'M'),
    ('marti.orta', 'Orta Martínez', 'Martí', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'marti.orta', 'M'),
    ('beatriz.ortega', 'Ortega', 'Beatriz', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'beatriz.ortega', 'F'),
    ('s.ortiz.garcia', 'Ortiz García', 'S.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 's.ortiz.garcia', 'F'),
    ('laura.osorio', 'Osorio', 'Laura P.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'laura.osorio', 'F'),
    ('frank.ostermann', 'Ostermann', 'Frank', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'frank.ostermann', 'M'),
    ('d.palma.lopez', 'Palma López', 'D.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'd.palma.lopez', 'M'),
    ('hugo.perales', 'Perales', 'Hugo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'hugo.perales', 'M'),
    ('sol.perez', 'Perez Jimenez', 'Sol', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'sol.perez', 'F'),
    ('suzanne.pierce', 'Pierce', 'Suzanne', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'suzanne.pierce', 'F'),
    ('jose.plancarte', 'Plancarte Trujillo', 'José Aldo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jose.plancarte', 'M'),
    ('sandra.pola', 'Pola Villaseñor', 'Sandra', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'sandra.pola', 'F'),
    ('juan.pulido', 'Pulido', 'Juan', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'juan.pulido', 'M'),
    ('irene.perez', 'Pérez Llorente', 'Irene', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'irene.perez', 'F'),
    ('diego.perez', 'Pérez Salicrup', 'Diego Raúl', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'diego.perez', 'M'),
    ('azucena.perez', 'Pérez Vega', 'Azucena', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'azucena.perez', 'F'),
    ('jorge.quetzal', 'Quetzal Argueta', 'Jorge', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jorge.quetzal', 'M'),
    ('giacomo.gambaldi', 'Rambaldi', 'Giacomo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'giacomo.gambaldi', 'M'),
    ('palaniappan.ramu', 'Ramu', 'Palaniappan', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'palaniappan.ramu', 'F'),
    ('diana.ramirez', 'Ramírez Mejía', 'Diana', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'diana.ramirez', 'F'),
    ('lg.ramirez.sanchez', 'Ramírez Sanchez', 'L. G.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'lg.ramirez.sanchez', 'M'),
    ('hugo.ramirez', 'Ramírez Tobías', 'Hugo Magdaleno', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'hugo.ramirez', 'M'),
    ('f.garcía.oliva', 'García Oliva', 'F.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'f.garcía.oliva', 'F'),
    ('f.pineda.garcia', 'Pineda-García', 'F.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'f.pineda.garcia', 'M'),
    ('i.torres.garcia', 'Torres-García', 'I.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'i.torres.garcia', 'M'),
    ('f.pena.vega', 'Peña Vega', 'F.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'f.pena.vega', 'M'),
    ('saul.alvarez', 'Álvarez Borrego', 'Saúl', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'saul.alvarez', 'M'),

    ('selene.rangel', 'Rangel Landa', 'Selene', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'selene.rangel', 'F'),
    ('omar.masera', 'Masera', 'Omar Raul', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'omar.masera', 'M'),
    ('j.reyez.lopez', 'Reyes López', 'J.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'j.reyez.lopez', 'M'),
    ('mercedes.rivera', 'Rivera León', 'Mercedes', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'mercedes.rivera', 'F'),
    ('alexis.rivero', 'Rivero Romero', 'Alexis Daniela', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alexis.rivero', 'M'),
    ('yesenia.rodriguez', 'Rodríguez López', 'Yesenia', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'yesenia.rodriguez', 'F'),
    ('g.rodriguez.tapia', 'Rodríguez Tapia', 'G.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'g.rodriguez.tapia', 'M'),
    ('paul.roge', 'Roge', 'Paul', 'OTRO', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').id,
     '-', 'paul.roge', 'M'),
    ('yessica.romero', 'Romero Bautista', 'Yessica Angélica', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'yessica.romero', 'F'),
    ('fernando.rosete', 'Rosete Vergés', 'Fernando', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'fernando.rosete', 'M'),
    ('jeffrey.ross', 'Ross Ibarra', 'Jeffrey', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jeffrey.ross', 'M'),
    ('peter.rosset', 'Rosset', 'Peter', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'peter.rosset', 'M'),
    ('andrew.roth', 'Roth', 'Andrew', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'andrew.roth', 'M'),
    ('ryan.morris', 'Ryan Norris', 'D.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ryan.morris', 'M'),
    ('amalio.santacruz', 'Santacruz Varela', 'Amalio', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'amalio.santacruz', 'M'),
    ('ge.santana.huicochea', 'Santana Huicochea', 'G. E.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ge.santana.huicochea', 'M'),
    ('laura.santillan', 'Santillán Hernández', 'Laura Alicia', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'laura.santillan', 'F'),
    ('didac.santos', 'Santos Fita', 'Didac', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'didac.santos', 'M'),
    ('daniel.schwindt', 'Schwindt', 'Daniel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'dalien.schwindt', 'M'),
    ('sergey.sedov', 'Sedov', 'Sergey', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'sergey.sedov', 'M'),
    ('paola.segundo', 'Segundo Métay', 'Paola', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'pola.segundo', 'F'),
    ('itzi.segundo', 'Segundo', 'Itzi', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'itzi.segundo', 'F'),
    ('tzitzi.sharhi', 'Sharhi Delgado', 'Tzitzi', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'tzitzi.sharhi', 'F'),
    ('francisco.silva', 'Silva Bátiz', 'Francisco de Asís', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'francisco.silva', 'M'),
    ('peter.simmons', 'Simmons', 'Peter', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'peter.simmons', 'M'),
    ('m.solange.grimoldi', 'Solange Grimoldi', 'M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'm.solange.grimoldi', 'M'),
    ('ana.soler', 'Soler Arechalde', 'Ana M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ana.soler', 'F'),
    ('jose.solis', 'Solis Navarrete', 'José Alberto', 'TECNICO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jose.solis', 'M'),
    ('elizabeth.solleiro', 'Solleiro Rebolledo', 'Elizabeth', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'elizabeth.solleiro', 'M'),
    ('f.solis.dominguez', 'Solís Domínguez', 'F.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'f.solis.dominguez', 'M'),
    ('roger.guevara', 'Guevara Hernández', 'Roger', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'roger.guevara', 'M'),
    ('jl.palacio.prieto', 'Palacio Prieto', 'J. L.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jl.palacio.prieto', 'M'),
    ('p.moreno.casasola', 'Moreno Casasola', 'P.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'p.moreno.casasola', 'M'),
    ('ja.lopez.portillo', 'López Portillo', 'J. A.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ja.lopez.portillo', 'M'),
    ('h.hernandez.trejo', 'Hernández Trejo', 'H.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'h.hernandez.trejo', 'M'),
    ('m.vargas.sandoval', 'Vargas Sandoval', 'M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'm.vargas.sandoval', 'M'),
    ('v.rico.gray', 'Zamora Crescencio', 'V.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'v.rico.gray', 'M'),
    ('c.gutierrez.baez', 'Gutiérrez Báez', 'C.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'c.gutierrez.baez', 'M'),
    ('m.domínguez.c', 'Domìnguez Carrasco', 'M. R.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'm.domínguez.c', 'M'),
    ('mt.camacho.olmedo', 'Camacho Olmedo', 'M. T.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'mt.camacho.olmedo', 'M'),
    ('teresa.ramirez', 'Ramírez Herrera', 'María Teresa', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'teresa.ramirez', 'F'),
    ('y.calvillo.garcía', 'Calvillo García', 'Y.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'y.calvillo.garcía', 'M'),
    ('c.delgado.trejo', 'Delgado Trejo', 'C.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'c.delgado.trejo', 'M'),
    ('claudia.uberhuaga', 'Uberhuaga', 'Claudia', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'claudia.uberhuaga', 'F'),
    ('jacquie.burgess', 'Burgess', 'Jacquie', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jacquie.burgess', 'F'),
    ('m.kinyanjui', 'Kinyanjui', 'M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'm.kinyanjui', 'M'),
    ('ricardo.saucedo', 'Saucedo', 'Ricardo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ricardo.saucedo', 'M'),
    ('l.morales.barquero', 'Morales Barquero', 'L.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'l.morales.barquero', 'M'),
    ('daniel.slayback', 'A. Slayback', 'Daniel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'daniel.slayback', 'M'),
    ('guillermo.figueroa', 'Figueroa Béjar', 'Guillermo Iván', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'guillermo.figueroa', 'M'),
    ('monica.figueroa', 'Figueroa Béjar', 'Mónica Adriana', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'monica.figueroa', 'F'),
    ('maria.figueroa', 'Figueroa Béjar', 'María del Socorro', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'maria.figueroa', 'F'),
    ('yair.merlin', 'Merlín Uribe', 'Yair', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'yair.merlin', 'M'),
    ('robert.hijmans', 'Hijmans', 'Hijmans', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'robert.hijmans', 'M'),
    ('ramon.mariaca', 'Mariaca Méndez', 'Ramón', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ramon.mariaca', 'M'),
    ('bruce.ferguson', 'Ferguson', 'Bruce', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'bruce.ferguson', 'M'),
    ('jorge.morfin', 'Morfin Rios', 'Jorge', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jorge.morfin', 'M'),
    ('citlalli.lopez', 'López Binqüist', 'Citlalli', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'citlalli.lopez', 'F'),
    ('neyra.sosa', 'Sosa Gutiérrez', 'Neyra', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'neyra.sosa', 'F'),
    ('lorena.soto', 'Soto Pinto', 'Lorena', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'lorena.soto', 'F'),
    ('romina.spano', 'Spano', 'Romina C.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'romina.spano', 'F'),
    ('a.sanchez.duque', 'Sánchez Duque', 'A.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'a.sanchez.duque', 'M'),
    ('julio.sanchez', 'Sánchez Escudero', 'Julio', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'julio.sanchez', 'M'),
    ('jm.sanchez.nunez', 'Sánchez Núñez', 'J. M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jm.sanchez', 'M'),
    ('cristobal.sanchez', 'Sánchez Sánchez', 'Cristóbal Daniel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'cristobal.sanchez', 'M'),
    ('hind.taud', 'Taud', 'Hind', 'OTRO', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').id,
     '-', 'hind.taud', 'M'),
    ('keiko.tatanisho', 'Teranisho Castillo', 'Keiko', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'keiko.tatanisho', 'M'),
    ('birgit.terhorst', 'Terhorst', 'Birgit', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'birgit.terhorst', 'M'),
    ('diego.torres', 'Torres Huerta', 'Diego', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'diego.torres', 'M'),
    ('jf.torrescano.valle', 'Torrescano Valle', 'J. F.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jf.torrescano.valle', 'M'),
    ('tyler.flockhart', 'Tyler Flockhart', 'D. T.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'tyler.flockhart', 'M'),
    ('nicolas.vargas', 'Vargas Ramírez', 'Nicolás', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'nicolas.vargas', 'M'),
    ('jeroen.verplanke', 'Verplanke', 'Jeroen', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jeroen.verplanke', 'M'),
    ('laura.villamil', 'Villamil Echeverri', 'Laura', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'laura.villamil', 'F'),
    ('alexey.voinov', 'Voinov', 'Alexey', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alexey.voinov', 'F'),
    ('lorenzo.vazquez', 'Vázquez Selem', 'Lorenzo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'lorenzo.vazquez', 'M'),
    ('leonard.wassenaar', 'Wassenaar', 'Leonard I.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'leonard.wassenaar', 'M'),
    ('martina.wilde', 'Wilde', 'Martina', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'martina.wilde', 'F'),
    ('antoinette.winklerprins', 'WinklerPrins', 'Antoinette', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'winklerprins', 'F'),
    ('j.zavala.cruz', 'Zavala Cruz', 'J.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'j.zavala.cruz', 'M'),
    ('isela.zarmeno', 'Zermeño', 'Isela', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'isela.zarmeño', 'F'),
    ('zirion.martinez', 'Zirión Martínez', 'M.', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'zirion.martinez', 'M'),
    ('n.aguila.carrasco', 'Águila Carrasco', 'N', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'aguila.carrasco', 'M'),
    ('pablo.alvarez', 'Álvarez', 'Pablo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'pablo.alvarez', 'M'),
    ('l.menéndez.carrera', 'Menéndez Carrera', 'L', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'l.menéndez.carrera', 'M'),
    ('georges.seingier', 'Seingier', 'Georges', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'l.menéndez.carrera', 'M'),
    ('dalma.albarracin', 'Dalma', 'Albarracín', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'dalma.albarracin', 'F'),
    ('gabriela.alvarez', 'Alvarez Gamboa', 'Gabriela', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'gabriela.alvarez', 'F'),
    ('fabiana.bekerman', 'Bekerman', 'Fabiana', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'fabiana.bekerman', 'F'),
    ('ana.cinti', 'Cinti', 'Ana', 'OTRO', Pais.objects.get(nombre='México').id, Ciudad.objects.get(nombre='Morelia').id,
     '-', 'ana.cinti', 'F'),
    ('leticia.curti', 'Curti', 'Leticia', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'leticia.curti', 'F'),
    ('cristina.flores', 'Flores', 'Cristina', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'cristina.flores', 'F'),
    ('rosana.guber', 'Guber', 'Rosana', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'rosana.guber', 'F'),
    ('sergio.kaminker', 'Kaminker', 'Sergio Andres', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'sergio.kaminker', 'M'),
    ('carolina.laztra', 'Laztra', 'Carolina', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'carolina.laztra', 'F'),
    ('isabelle.sanchez', 'Sanchez Rose', 'Isabelle', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'isabelle.sanchez', 'F'),
    ('javier.serrano', 'Serrano', 'Javier', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'javier.serrano', 'M'),
    ('marcos.sourrouille', 'Sourrouille', 'Marcos', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'marcos.sourrouille', 'M'),
    ('damian.taire', 'Taire', 'Damián Leonardo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'damian.taire', 'M'),
    ('julio.vezub', 'Vezub', 'Julio', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'julio.vezub', 'M'),
    ('joaquin.sosa', 'Sosa Ramírez', 'Joaquín', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'joaquin.sosa', 'M'),
    ('donald.brand', 'Brand', 'Donald. D', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'donald.brand', 'M'),
    ('victor.toledo', 'Toledo', 'Victor M.','OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'victor.toledo', 'M'),
    ('alfred.zinck', 'Zinck', 'Joseph Alfred', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alfred.zinck', 'M'),
    ('hector.delvalle', 'Del Valle', 'Héctor Francisco', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'hector.delvalle', 'M'),
    ('carlos.paredes', 'Paredes Martínez', 'Carlos', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'carlos.paredes', 'M'),
    ('victoria.canino', 'Canino', 'Ma Victoria', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'victoria.canino', 'F'),
    ('rosa.bolivar', 'Bolivar', 'Rosa', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'rosa.bolivar', 'F'),
    ('ana.castellanos', 'Ana', 'Castellanos', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ana.castellanos', 'F'),
    ('alejandra.aray', 'Aray', 'Maria Alejandra', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alejandra.aray', 'F'),
    ('alberto.ortiz', 'Ortiz Rivera', 'Alberto', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alberto.ortiz', 'M'),
    ('michael.kuhn', 'Kuhn', 'Michael', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'michael.kuhn', 'M'),
    ('juan.vazquez', 'Vazquez Gutierrez', 'Juan Pablo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'juan.vazquez', 'M'),
    ('pablo.reyna', 'Reyna Estévez', 'Pablo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'pablo.reyna', 'M'),
    ('leon.nkolo', 'Nkolo Njodo', 'Léon Marie', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'leon.nkolo', 'M'),
    ('christiane.hartnack', 'Hartnack', 'Christiane', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'christiane.hartnack', 'F'),
    ('roger.magazine', 'Magazine', 'Roger', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'roger.magazine', 'M'),
    ('claudia.magallanes', 'Magallanes Blanco', 'Claudia', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'claudia.magallanes', 'F'),
    ('leandro.rodriguez', 'Rodriguez Medina', 'Leandro', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'leandro.rodriguez', 'M'),
    ('ivan.costa', 'da Costa Marquez', 'Ivan', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ivan.costa', 'M'),
    ('michel.christie', 'Christie', 'Michel', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'michel.christie', 'M'),
    ('kumaran.rajagopal', 'Rajagopal', 'Kumaran', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'kumaran.rajagopal', 'M'),
    ('quodratullah.qorbani', 'Qorbani', 'Quodratullah', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'quodratullah.qorbani', 'M'),
    ('consuelo.medina', 'Medina García', 'Consuelo', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'consuelo.medina', 'F'),
    ('elvira.duran', 'Durán Medina', 'Elvira', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'elvira.duran', 'F'),
    ('carmen.bueno', 'Bueno Castellanos', 'Carmen', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'carmen.bueno', 'F'),
    ('kwang.yeong', 'Yeong Shin', 'Kwang', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'kwang.yeong', 'M'),
    ('huri.islamoglu', 'Islamoglu', 'Huri', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'huri.islamoglu', 'M'),
    ('doris.weidermann', 'Weidermann', 'Doris', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'doris.weidermann', 'F'),
    ('mauricio.nieto', 'Nieto Olarte', 'Mauricio', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'mauricio.nieto', 'M'),
    ('reinerg.grundmann', 'Grundmann', 'Reiner', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'reinerg.grundmann', 'M'),
    ('sujata.patel', 'Patel', 'Sujata', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'sujata.patel', 'F'),
    ('igor.yegorov', 'Yegorov', 'Igor', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'igor.yegorov', 'M'),
    ('pal.tamas', 'Tamas', 'Pal', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'pal.tamas', 'M'),
    ('kazumi.okamoto', 'Okamoto', 'Kazumi', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'kazumi.okamoto', 'F'),
    ('ramon.hernandez', 'Hernández Santana', 'José Ramón', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'ramon.hernandez', 'M'),
    ('rigel.zaragoza', 'Zaragoza', 'Rigel Alfonso', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'rigel.zaragoza', 'F'),
    ('oscar.leal', 'Leal Nares', 'Oscar Adrián', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'oscar.leal', 'M'),
    ('laura.villaseñor', 'Villaseñor Gómez', 'Laura', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'oscar.leal', 'M'),
    ('felipe.hernandez', 'Hernández', 'Felipe', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'felipe.hernandez', 'M'),
    ('jose.moncada', 'Moncada Maya', 'José Omar', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jose.moncada', 'M'),
    ('alvaro.lopez', 'López López', 'Álvaro', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alvaro.lopez', 'M'),
    ('alberto.alvarez', 'Álvarez', 'Alberto', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'alberto.alvarez', 'M'),
    ('juan.ortiz', 'Ortiz Escamilla', 'Juan', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'juan.ortiz', 'M'),
    ('isolda.lunavega', 'Luna Vega', 'Isolda', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'isolda.lunavega', 'F'),
    ('rafael.camaraartigas', 'Cámara Artigas', 'Rafael', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'rafael.camaraartigas', 'M'),
    ('jesus.ruizcareaga', 'Ruiz Careaga', 'Jesús', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'jesus.ruizcareaga', 'M'),
    ('mauricio.perea', 'Perea Peña', 'Mauricio', 'OTRO', Pais.objects.get(nombre='México').id,
     Ciudad.objects.get(nombre='Morelia').id, '-', 'mauricio.perea', 'M'),

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
     ['Escuela Nacional de Estudios Superiores, Unidad Morelia (ENES Morelia)'], 'fEVor'),
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
    ('Ciencias de la Tierra', 'Physical Geography', 'Instituto de Geología',
     'Dinámica de la Erosión/Sedimentación en la Época Prehispánica y Periodo Colonial. Reconstrucción de las condiciones Paleoambientales en el Valle de Teotihuacán (Estado de México)',
     2009, 8, 2010, 7, 2014, 7, 'EeGJW'),
    ('Geografía', 'Physical Geography', 'Universidad Northwestern', '-', 1970, 9, 1971, 8, 1971, 9, 'dNnfH'),
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

ningunproyecto = ProyectoInvestigacion(nombre='Ninguno', status='OTRO', clasificacion='OTRO', organizacion='INDIVIDUAL',
                                       modalidad='OTRA', fecha_inicio=datetime(1900, 1, 1), fecha_fin=datetime(9900, 1, 1),
                                       institucion=Institucion.objects.get(nombre='Universidad Nacional Autónoma de México (UNAM)'),
                                       dependencia=Dependencia.objects.get(nombre='Universidad Nacional Autónoma de México (UNAM)'))
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
    p = PostDoctorado(nombre=str(uuid.uuid1()), proyecto=ProyectoInvestigacion.objects.get(nombre='Ninguno'),
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

    ('D6160', 'Profesor Titular A, Medio tiempo'),
    ('D6270', 'Profesor Titular B, Medio tiempo'),
    ('D6376', 'Profesor Titular C, Medio tiempo'),
    ('D6489', 'Profesor Titular A, Tiempo Completo'),
    ('D6593', 'Profesor Titular B, Tiempo Completo'),
    ('D6696', 'Profesor Titular C, Tiempo Completo'),


    ('I5144', 'Investigador Asociado A, Medio tiempo'),
    ('I5251', 'Investigador Asociado B, Medio tiempo'),
    ('I5356', 'Investigador Asociado C, Medio tiempo'),
    ('I5480', 'Investigador Asociado A, Tiempo Completo'),
    ('I5584', 'Investigador Asociado B, Tiempo Completo'),
    ('I5686', 'Investigador Asociado C, Tiempo Completo'),

    ('I6160', 'Investigador Titular A, Medio tiempo'),
    ('I6270', 'Investigador Titular B, Medio tiempo'),
    ('I6376', 'Investigador Titular C, Medio tiempo'),
    ('I6489', 'Investigador Titular A, Tiempo Completo'),
    ('I6593', 'Investigador Titular B, Tiempo Completo'),
    ('I6696', 'Investigador Titular C, Tiempo Completo'),

    ('I7117', 'Técnico Académico Auxiliar A, Medio tiempo'),
    ('I7220', 'Técnico Académico Auxiliar B, Medio tiempo'),
    ('I7327', 'Técnico Académico Auxiliar C, Medio tiempo'),
    ('I7439', 'Técnico Académico Auxiliar A, Tiempo Completo'),
    ('I7544', 'Técnico Académico Auxiliar B, Tiempo Completo'),
    ('I7658', 'Técnico Académico Auxiliar C, Tiempo Completo'),

    ('I8133', 'Técnico Académico Asociado A, Medio tiempo'),
    ('I8242', 'Técnico Académico Asociado B, Medio tiempo'),
    ('I8346', 'Técnico Académico Asociado C, Medio tiempo'),
    ('I8467', 'Técnico Académico Asociado A, Tiempo Completo'),
    ('I8578', 'Técnico Académico Asociado B, Tiempo Completo'),
    ('I8682', 'Técnico Académico Asociado C, Tiempo Completo'),

    ('I9151', 'Técnico Académico Titular A, Medio tiempo'),
    ('I9254', 'Técnico Académico Titular B, Medio tiempo'),
    ('I9360', 'Técnico Académico Titular C, Medio tiempo'),
    ('I9484', 'Técnico Académico Titular A, Tiempo Completo'),
    ('I9585', 'Técnico Académico Titular B, Tiempo Completo'),
    ('I9689', 'Técnico Académico Titular C, Tiempo Completo')

    #('D7117', 'Técnico Académico Auxiliar A, Medio tiempo'),
    #('D7220', 'Técnico Académico Auxiliar B, Medio tiempo'),
    #('D7327', 'Técnico Académico Auxiliar C, Medio tiempo'),
    #('D7439', 'Técnico Académico Auxiliar A, Tiempo Completo'),
    #('D7544', 'Técnico Académico Auxiliar B, Tiempo Completo'),
    #('D7658', 'Técnico Académico Auxiliar C, Tiempo Completo'),
#
    #('D8133', 'Técnico Académico Asociado A, Medio tiempo'),
    #('D8242', 'Técnico Académico Asociado B, Medio tiempo'),
    #('D8346', 'Técnico Académico Asociado C, Medio tiempo'),
    #('D8467', 'Técnico Académico Asociado A, Tiempo Completo'),
    #('D8578', 'Técnico Académico Asociado B, Tiempo Completo'),
    #('D8682', 'Técnico Académico Asociado C, Tiempo Completo'),
#
    #('D9151', 'Técnico Académico Titular A, Medio tiempo'),
    #('D9254', 'Técnico Académico Titular B, Medio tiempo'),
    #('D9360', 'Técnico Académico Titular C, Medio tiempo'),
    #('D9484', 'Técnico Académico Titular A, Tiempo Completo'),
    #('D9585', 'Técnico Académico Titular B, Tiempo Completo'),
    #('D9689', 'Técnico Académico Titular C, Tiempo Completo'),
#
    #('I7117', 'Técnico Académico Auxiliar A, Medio tiempo'),
    #('I7220', 'Técnico Académico Auxiliar B, Medio tiempo'),
    #('I7327', 'Técnico Académico Auxiliar C, Medio tiempo'),
    #('I7439', 'Técnico Académico Auxiliar A, Tiempo Completo'),
    #('I7544', 'Técnico Académico Auxiliar B, Tiempo Completo'),
    #('I7658', 'Técnico Académico Auxiliar C, Tiempo Completo'),
#
    #('I8133', 'Técnico Académico Asociado A, Medio tiempo'),
    #('I8242', 'Técnico Académico Asociado B, Medio tiempo'),
    #('I8346', 'Técnico Académico Asociado C, Medio tiempo'),
    #('I8467', 'Técnico Académico Asociado A, Tiempo Completo'),
    #('I8578', 'Técnico Académico Asociado B, Tiempo Completo'),
    #('I8682', 'Técnico Académico Asociado C, Tiempo Completo'),
#
    #('I9151', 'Técnico Académico Titular A, Medio tiempo'),
    #('I9254', 'Técnico Académico Titular B, Medio tiempo'),
    #('I9360', 'Técnico Académico Titular C, Medio tiempo'),
    #('I9484', 'Técnico Académico Titular A, Tiempo Completo'),
    #('I9585', 'Técnico Académico Titular B, Tiempo Completo'),
    #('I9689', 'Técnico Académico Titular C, Tiempo Completo')

    )

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
    (False, False, 'Profesor De Maestría En Derecho'),
    (False, False, 'Evaluador Del Proyecto'),
    ('Investigador', False, False),
    ('Investigador UNAM', False, False),
    ('Investigador CONACYT', False, False),
    ('Investigador Invitado', False, False),
    ('Cátedras CONACYT', False, False),
    ('Investigador Postdoctoral', False, False),
    ('Investigador por convenio', False, False),
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
    ('Investigador Titular B, Tiempo Completo', True, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2014, 3, 0, 0, 'Y9jOf'),
    ('Ninguno', True, False, False, 'Pensionado Jubilado Pemex', 'Petróleos Mexicanos (PEMEX)', 1968, 6, 0, 0, '16ymf'),
    ('Técnico Académico Asociado C, Tiempo Completo', False, False, False, 'Otro',
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
    ('Técnico Académico Titular B, Tiempo Completo', True, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2014, 10, 0, 0, 'n80rn'),
    ('Técnico Académico Titular A, Tiempo Completo', True, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2011, 6, 2014, 10, 'n80rn'),
    ('Técnico Académico Asociado C, Tiempo Completo', False, False, False, 'Otro',
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
        'Técnico Académico Auxiliar A, Medio tiempo', False, False, False, 'Otro',
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
    ('Ninguno', False, 'Cátedras CONACYT', False, False, 'Centro de Investigaciones en Geografía Ambiental (CIGA)',
     2014, 10, 0, 0, 'Yl5I4'),
    ('Ninguno', False, 'Investigador Postdoctoral', False, False,
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2014, 9, 0, 0, 'EeGJW'),
    ('Ninguno', False, False, False, 'Levantamiento y elaboración de mapas de suelos',
     'Instituto Cartográfico y Geológico de Cataluña', 2008, 10, 2009, 7, 'EeGJW'),
    ('Ninguno', False, False, False, 'Plan de mejora de los caminos rurales de Catalunya',
     'Tecnologías y Servicios Agrarios, S.A (Tragsatec)', 2006, 4, 2006, 9, 'EeGJW'),
    ('Ninguno', False, False, False, 'Responsable de Calidad', 'Meneu Distribución, S.A.', 2005, 9, 2006, 2, 'EeGJW'),
    ('Técnico Académico Auxiliar C, Tiempo Completo', False, False, False, 'Otro',
     'Instituto de Geografía', 1994, 12, 1997, 12, 'Yrcbo'),
    ('Técnico Académico Auxiliar A, Tiempo Completo', False, False, False, 'Otro',
     'Instituto de Geografía', 1997, 12, 2001, 12, 'Yrcbo'),
    ('Técnico Académico Auxiliar B, Tiempo Completo', True, False, False, 'Otro',
     'Instituto de Geografía', 2001, 12, 2006, 8, 'Yrcbo'),
    ('Técnico Académico Titular B, Tiempo Completo', True, False, False, 'Otro', 'Instituto de Geografía',
     2006, 9, 2007, 7, 'Yrcbo'),
    ('Técnico Académico Titular B, Tiempo Completo', True, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2006, 8, 2008, 12, 'Yrcbo'),
    ('Técnico Académico Titular C, Tiempo Completo', True, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2015, 10, 0, 0, 'Yrcbo'),
    ('Técnico Académico Titular B, Tiempo Completo', True, False, 'Secretaría Técnica', False,
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
    ('Técnico Académico Asociado C, Tiempo Completo', False, 'Otro', False, False,
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2007, 8, 2011, 2, 'fEVor'),
    ('Técnico Académico Titular A, Tiempo Completo', True, 'Otro', False, False,
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2011, 2, 2015, 3, 'fEVor'),
    ('Técnico Académico Titular B, Tiempo Completo', True, 'Otro', False, False,
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2015, 3, 0, 0, 'fEVor'),
    ('Ninguno', False, False, False, 'Lecturer', 'Universidad de Dar es-Salam', 1974, 1, 1982, 9, 'YxU7H'),
    ('Ninguno', True, False, False, 'Unversitaire Hoog Docent', 'University of Twente', 1982, 9, 2008, 6, 'YxU7H'),
    ('Profesor de Asignatura A', False, 'Profesor', False, False,
     'Escuela Nacional de Estudios Superiores, Unidad Morelia (ENES Morelia)', 2012, 8, 0, 0, '4th7o'),
    ('Ninguno', False, 'Profesor invitado', False, False, 'Universidad Autónoma de Tlaxcala', 2012, 7, 2012, 8, '4th7o'),
    ('Técnico Académico Titular C, Tiempo Completo', True, 'Otro', False, False,
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2013, 6, 0, 0, 'zF8gk'),
    ('Investigador Asociado C, Tiempo Completo', True, 'Profesor Investigador', False, False,
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2009, 1, 2014, 10, 'prgh0'),
    ('Investigador Asociado C, Tiempo Completo', False, 'Profesor Investigador', False, False,
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2014, 11, 0, 0, 'prgh0'),
    ('Investigador Asociado C, Tiempo Completo', False, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2011, 4, 2016, 3, 'DgFdm'),
    ('Técnico Académico Titular A, Tiempo Completo', True, False, False, 'Otro',
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
    ('Técnico Académico Titular A, Medio tiempo', True, False, False, 'Otro',
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
    ('Técnico Académico Titular A, Medio tiempo', True, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2007, 3, 0, 0, '88SSU'),
    ('Técnico Académico Asociado C, Tiempo Completo', False, False, False, 'Otro',
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
    ('Técnico Académico Auxiliar B, Tiempo Completo', False, False, False, 'Otro', 'Facultad de Ingeniería',
     1984, 8, 1986, 10, 'ftTrS'),
    ('Técnico Académico Asociado C, Tiempo Completo', False, False, False,
     'Jefe del Laboratorio de Cómputo', 'Instituto de Geografía', 1986, 11, 1990, 9, 'ftTrS'),
    ('Técnico Académico Asociado B, Tiempo Completo', False, False, False, 'Otro',
     'Instituto de Geografía', 1992, 10, 1994, 4, 'ftTrS'),
    ('Técnico Académico Asociado B, Tiempo Completo', False, False,
     'Jefe del Laboratorio de Sistemas de Información Geográfica y Percepción Remota', False, 'Instituto de Geografía',
     1998, 10, 2001, 10, 'ftTrS'),
    ('Técnico Académico Titular C, Tiempo Completo', False, False,
     'Jefe del Laboratorio de Sistemas de Información Geográfica y Percepción Remota', False, 'Instituto de Geografía',
     2001, 11, 2004, 11, 'ftTrS'),
    ('Técnico Académico Titular C, Tiempo Completo', False, False, False, 'Otro',
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2004, 12, 2009, 12, 'ftTrS'),
    ('Técnico Académico Titular C, Tiempo Completo', True,
     'Coordinador del Laboratorio de Análisis Espacial', False, False,
     'Centro de Investigaciones en Geografía Ambiental (CIGA)', 2009, 1, 2015, 11, 'ftTrS'),
    ('Técnico Académico Titular C, Tiempo Completo', True, False, 'Secretario Técnico', False,
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

editoriales = (
('CIGA-UNAM', 'Morelia', 'Michoacán de Ocampo', 'México'),
('UNAM', 'Ciudad de México, CDMX', 'Ciudad de México', 'México'),
('UNPA', 'Río Gallegos', 'Santa Cruz', 'Argentina'),
('INECOL', 'Xalapa', 'Veracruz de Ignacio de la Llave', 'México'),
('Skiu', 'Ciudad de México, CDMX', 'Ciudad de México', 'México'),
('FAO', 'Roma', 'Ciudad metropolitana de Roma Capital', 'Italia'),
('Lovell-Johns', 'Long Hanborough', 'Witney', 'Reino Unido'),
('Morevalladolid', 'Morelia', 'Michoacán de Ocampo', 'México'),
('CIDEM', 'Morelia', 'Michoacán de Ocampo', 'México'),
('ENES Unidad Morelia', 'Morelia', 'Michoacán de Ocampo', 'México'),
('Fundación Escuela Editorial El perro y la rana', 'Caracas', 'Caracas', 'Venezuela'),
('Ibidem Sociedad Editorial De Formacion Juridica Y Economica S. L.', 'Madrid', 'Comunidad de Madrid', 'España'),
('Springer', 'Luxemburgo', 'Luxemburgo', 'Luxemburgo'),
('UNESCO', 'París', 'Isla de Francia', 'Francia'),
('Centro Nacional de Biodiversidad del Instituto de Ecología y Sistemática', 'La Habana', 'La Habana', 'Cuba'),
)

for i in editoriales:
    e = Editorial(nombre=i[0], ciudad=Ciudad.objects.get(nombre=i[1]), estado=Estado.objects.get(nombre=i[2]), pais=Pais.objects.get(nombre=i[3]))
    e.save()
    print("Guardada la editorial", e)


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
           'Otros índices')

for i in indices:
    I = Indice(nombre=i)
    I.save()
    print('Agregado indice ' + I.nombre)

problemas = ['Gestión integral del agua, \n\r<br >seguridad hídrica y derecho del agua',
             'Mitigación y adaptación al cambio climático',
             'Resiliencia frente a desastres naturales y tecnológicos',
             'Aprovechamiento y protección de ecosistemas y de la biodiversidad',
             'Los océanos y su aprovechamiento',
             'Alimentos y su producción',
             'Ciudades y desarrollo urbano',
             'Conectividad informática y desarrollo de las tecnologías de la información, la comunicación y las telecomunicaciones',
             'Manufactura de alta tecnología',
             'Consumo sustentable de energía',
             'Desarrollo y aprovechamiento de energías renovables limpias, conducta humana y prevención de adicciones',
             'Enfermedades emergentes y de importancia nacional',
             'Combate a la pobreza y seguridad alimentaria',
             'Migraciones y asentamientos humanos',
             'Seguridad ciudadana',
             'Economía y gestión del conocimiento',
             'Prevención de riesgos naturales']

for i in problemas:
    p = ProblemaNacionalConacyt(nombre=i)
    p.save()
    print('Agregado problema conacyt: ', p)

t = TipoEvento(nombre='Otro')
t.save()
print("agregado tipo evento", t)

e = Evento(nombre='Otro', fecha_inicio=date(2010, 10, 10), fecha_fin=date(2010, 10, 10),
           tipo=TipoEvento.objects.get(nombre='Otro'), pais=Pais.objects.get(nombre='México'),
           estado=Estado.objects.get(nombre='Michoacán de Ocampo'), ciudad=Ciudad.objects.get(nombre='Morelia'))
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


articulos = (
    ['Charcoal contribution accumulation at different scales of production among the rural population of Mutomo District in Kenya', 'Energy for Sustainable Development', '33', '', 2016, '0973-0826', 'PUBLICADO', 'No', 'adrian.ghilardi', 'Web of Science: SCI/SSCI/SCI-EX', 167, 175, '10.1016/j.esd.2016.05.002'],
    ['Spatiotemporal modeling of fuelwood environmental impacts: towards improved accounting for non-renewable biomass', 'Environmental Modelling & Software', '82', '', 2016, '1364-8152', 'PUBLICADO', 'No', 'adrian.ghilardi^bailis.espinoza^jean.mas^margaret.skutsch^omar.masera', 'Web of Science: SCI/SSCI/SCI-EX', 241, 254, '10.1016/j.envsoft.2016.04.023'],
    ['Análisis de la producción de carbón vegetal en la Cuenca del Lago de Cuitzeo, Michoacán, México: implicaciones para una producción sustentable', 'Investigación Ambiental', '6', '2', 2014, '2007-4492', 'PUBLICADO', 'No', 'adrian.ghilardi^ken.oyama^omar.masera', 'Otros índices', 127, 138, ''],
    ['Sustainable bioenergy options for Mexico: GHG mitigation and costs', 'Renewable and Sustainable Energy Reviews', '43', '', 2015, '1364-0321', 'PUBLICADO', 'No', 'adrian.ghilardi^margaret.skutsch^omar.masera', 'Web of Science: SCI/SSCI/SCI-EX', 545, 552, '10.1016/j.rser.2014.11.062'],
    ['The carbon footprint of traditional woodfuels', 'Nature Climate Change', '5', '', 2015, '1758-678X', 'PUBLICADO', 'No', 'adrian.ghilardi^omar.masera^bailis.espinoza', 'Web of Science: SCI/SSCI/SCI-EX', 266, 272, '10.1038/nclimate2491'],
    ['Environmental Burden of Traditional Bioenergy Use', 'Annual Review of Environment and Resources', '40', '', 2015, '1543-5938', 'PUBLICADO', 'No', 'adrian.ghilardi^omar.masera^bailis.espinoza', 'Web of Science: SCI/SSCI/SCI-EX', 121, 150, '10.1146/annurev-environ-102014-021318'],
    ['Evaluation of annual modis PTC data for deforestation and forest degradation analysis', 'International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences - ISPRS Archives', '', '', 2016, '', 'PUBLICADO', 'Si', 'adrian.ghilardi^yan.gao^jean.mas^jaime.paneque^margaret.skutsch', 'Scopus', 9, 13, '10.5194/isprsarchives-XLI-B2-9-2016'],
    ['Management-sensitive hierarchical typology for riparian zones based on biophysical features: a procedure', 'Physical Geography', '', '', 2017, '', 'ENVIADO', 'No', 'adriana.flores^roger.guevara^manuel.mendoza^rosario.langrave^miguel.maass', 'Web of Science: SCI/SSCI/SCI-EX; Otros índices', 0, 0, ''],
    ['Componentes del paisaje como predictores de cubiertas de vegetación: estudio de caso del estado de Michoacán, México', 'Investigaciones Geográficas, Boletín del Instituto de Geografía', '90', '', 2016, '0188-4611', 'PUBLICADO', 'No', 'luis.gopar', 'Web of Science: SCI/SSCI/SCI-EX; Latindex', 75, 88, 'dx.doi.org/10.14350'],
    ['Elementos del paisaje como predictores de tipos de cubiertas de vegetación', 'Investigaciones Geográficas, Boletín del Instituto de Geografía', '', '', 2015, '', 'EN_PRENSA', 'No', 'luis.gopar^alejandro.velazquez', 'Otros índices', 1, 10, 'http://dx.doi.org/10.14350/rig.46688'],
    ['Bioclimatic mapping as a new method to assess effects of climatic change', 'Ecosphere Journal', '6', '1', 2015, '', 'PUBLICADO', 'Si', 'luis.gopar^alejandro.velazquez^joaquin.gimenez', 'Otros índices', 1, 12, '10.1890/ES14-00138.1'],
    ['Implementación del Índice de Condición Forestal (ICF), Como un insumo para el diseño de políticas públicas de corte forestal en México', 'Investigaciones Geográficas, Boletín del Instituto de Geografía', '', '', 2016, '0188-4611', 'ACEPTADO', 'No', 'neyra.sosa^alejandro.velazquez^dante.ayala^gerardo.bocco^luis.gopar', 'Revistas CONACYT; Web of Science: SCI/SSCI/SCI-EX', 0, 0, 'dx.doi.org/10.14350'],
    ['Diseño de las políticas públicas de corte forestal en México: implicaciones para la gestión de la vulnerabilidad social y el territorio', 'Investigaciones Geográficas, Boletín del Instituto de Geografía', '', '', 2016, ' 0188-4611', 'EN_PRENSA', 'Si', 'neyra.sosa^alejandro.velazquez^dante.ayala^gerardo.bocco^luis.gopar', 'SciELO; Revistas CONACYT; Scopus; Latindex; RedALyC', 1, 13, '10.14350/rig.53915'],
    ['Habitar una región. Espacialidad arquitectónica y construcción de paisajes en Andalhuala, valle de Yocavil (Catamarca, Argentina)', 'Arqueología', '22', '', 2016, '0327-5159', 'EN_PRENSA', 'No', 'alina.alvarez', 'Scopus; SciELO; Latindex', 0, 0, ''],
    ['Paisajes agroalfareros del primer y segundo milenio DC en la Mesada de Andalhuala Banda (Yocavil, Noroeste argentino)', 'Ñawpa Pacha. Journal of Andean Archaeology', '36', '2', 2016, '0077-6297', 'PUBLICADO', 'No', 'alina.alvarez', 'Otros índices', 161, 184, 'http://www.instituteofandeanstudies.org/publications.html'],
    ['Don Mateo-El Cerro, a Newly Rediscovered Late Period Settlement in Yocavil (Catamarca, Argentina)', 'Andean Past', '12', '', 2016, '1055-8756', 'PUBLICADO', 'No', 'alina.alvarez', 'Otros índices', 0, 0, ''],
    ['El arte rupestre como geosigno del paisaje (valle de Yocavil, Catamarca, Argentina)', 'Comechingonia, Revista de Arqueología', '16', '2', 2012, '0326-7911', 'PUBLICADO', 'No', 'alina.alvarez', 'Latindex; SciELO', 55, 74, 'http://www.comechingonia.com/'],
    ['Somos en el mundo: seres, materialidad y paisajes', 'La Zaranda de Ideas', '8', '', 2012, '1853-1296', 'PUBLICADO', 'No', 'alina.alvarez', 'SciELO; Latindex; Scopus; Otros índices', 10, 31, 'http://lazaranda.wix.com/lazarandadeideas'],
    ['Arquitectura y paisajes en la localidad arqueológica de Andalhuala (valle de Yocavil, Catamarca)', 'Revista del Museo de Antropología', '3', '', 2010, '1852-O6OX', 'PUBLICADO', 'No', 'alina.alvarez', 'Latindex; SciELO; RedALyC', 33, 48, 'http://revistas.unc.edu.ar/index.php/antropologia'],
    ['Gran Gruta Grabada de Chiquimí. Noticia acerca de su hallazgo y redescubrimiento, 100 años después', 'Boletín del Museo Chileno de Arte Precolombino', '16', '1', 2011, '0716-1530', 'PUBLICADO', 'No', 'alina.alvarez^jp.carbonelli', 'SciELO; Latindex', 23, 46, 'http://www.precolombino.cl/biblioteca/boletin-del-museo/'],
    ['Soria 3. Nuevas evidencias de la ocupación aldeana temprana en Yocavil, Noroeste argentino', 'Revista Española de Antropología Americana', '', '', 2016, '0556-6533', 'ENVIADO', 'Si', 'alina.alvarez^romina.spano^solange.grimoldi', 'Latindex; Scopus; RedALyC', 0, 0, 'http://revistas.ucm.es/index.php/REAA'],
    ['Repensando una época. Aproximación semiótica a los estilos alfareros de inicios del período Tardío en Yocavil por medio del caso Lorohuasi', 'Boletín del Museo Chileno de Arte Precolombino', '20', '2', 2015, '0716-1530', 'PUBLICADO', 'No', 'alina.alvarez^solange.grimoldi', 'Latindex; SciELO; RedALyC', 23, 55, 'http://boletinmuseoprecolombino.cl/wp/wp-content/uploads/2016/01/02-PALAMARCZUK-PRECOLOMBINO-202.pdf'],
    ['Ollas como urnas, casas como tumbas: reflexiones en torno a las prácticas de entierro de niños en tiempos tempranos (Andalhuala Banda, sur de Yocavil)', 'Comechingonia, Revista de Arqueología', '', '', 2016, '0326-7911', 'ENVIADO', 'No', 'alina.alvarez^solange.grimoldi^romina.spano', 'SciELO; Latindex', 1, 1, ''],
    ['Un hallazgo funerario en Shiquimil, Provincia de Catamarca. Bioarqueología y estilos alfareros de inicios del período Tardío en Yocavil', 'Arqueología', '18', '', 2012, '0327-5159', 'PUBLICADO', 'No', 'alina.alvarez^solange.grimoldi^v.palamarczuk', 'Latindex; Scopus; SciELO', 11, 37, 'http://revistascientificas.filo.uba.ar/index.php/Arqueologia/about/submissions#onlineSubmissions'],
    ['La alfarería de inicios del segundo milenio en Yocavil. El problema "San José" y las tipologías cerámicas', 'Arqueología', '20', 'Dossier', 2014, '0327-5159', 'PUBLICADO', 'Si', 'alina.alvarez^v.palamarczuk^solange.grimoldi', 'RedALyC; Latindex; Scopus', 107, 134, 'https://sites.google.com/site/revistaarqueologia/'],
    ['Consumo de energía en el manejo de huertas de aguacate en  Michoacán, México', 'Revista Chapingo Serie Horticultura', '21', '1', 2015, '1027-152X', 'PUBLICADO', 'No', 'ana.burgos^carlos.anaya', 'Otros índices', 5, 20, '10.5154/r.rchsh.2014.01.002 '],
    ['Patrones espacio-temporales en la condición microbiológica del agua de fuentes comunitarias y amenazas a la salud familiar en cuencas estacionales del Bajo Balsas (México)', 'Revista Internacional de Contaminación Ambiental', '2', '33', 2017, '', 'EN_PRENSA', 'No', 'ana.burgos^margarita.alvarado^rosaura.paez^ruben.hernandez', 'Otros índices', 0, 0, ''],
    ['Productive identities and community conditions for rural tourism in Mexican tropical drylands', 'Tourism Geographies', '17', '4', 2015, '', 'PUBLICADO', 'No', 'ana.burgos^maxime.kieffer', '', 561, 585, 'http://dx.doi.org/10.1080/14616688.2015.1043576'],
    ['Ecotechnologies for the sustainable management of tropical forest diversity', 'Nature & Resources', '33', '1', 1997, '0028-0844', 'PUBLICADO', 'No', 'angel.priego', 'Otros índices', 2, 17, ''],
    ['Determinación de zonas prioritarias para la eco-rehabilitación de la cuenca Lerma-Chapala, México', 'Gaceta Ecológica, Nueva Época', '', '71', 2004, '1405-2849', 'PUBLICADO', 'No', 'angel.priego', 'Latindex; Otros índices', 79, 92, ''],
    ['Biophysical landscapes of a coastal area of Michoacán state in Mexico', 'Journal of Maps', '', '6', 2011, '1744-5647', 'PUBLICADO', 'No', 'angel.priego', 'Web of Science: SCI/SSCI/SCI-EX; Otros índices', 42, 47, ''],
    ['La dinámica ambiental de la cuenca Lerma-Chapala, México', 'Gaceta Ecológica, Nueva Época', '', '71', 2004, '1405-2849', 'PUBLICADO', 'No', 'angel.priego', 'Latindex; Otros índices', 23, 77, ''],
    ['Vegetación original y actual de un sector de las playas del Este de Ciudad de La Habana, Cuba', 'Fontqueria', '', '36', 1993, '0212-0623', 'PUBLICADO', 'No', 'angel.priego', 'Latindex; Otros índices', 429, 437, ''],
    ['Zonificación funcional ecoturística de la zona costera de Michoacán, México a escala 1:250 000', 'Revista Geográfica De América Central', '', 'Número Especial EGAL 2011', 2011, '2115-2563', 'PUBLICADO', 'No', 'angel.priego^angel.flores', 'Latindex; Otros índices', 1, 15, ''],
    ['The contribution of physical geography to environmental public policy in México', 'Singapore Journal Of Tropical Geography', '', '31', 2010, '0129-7619', 'PUBLICADO', 'No', 'angel.priego^gerardo.bocco', 'Web of Science: SCI/SSCI/SCI-EX; Otros índices', 215, 223, ''],
    ['La Geografía Física y el Ordenamiento Ecológico del Territorio. Experiencias en México', 'Gaceta Ecológica, Nueva Época', '', '76', 2005, '1405-2849', 'PUBLICADO', 'No', 'angel.priego^gerardo.bocco', 'Latindex; Otros índices', 23, 34, ''],
    ['Relationship between landscape heterogeneity and plant species richness in the Mexican Pacific coast', 'Applied Geography', '', '40', 2013, '0143-6228', 'PUBLICADO', 'No', 'angel.priego^gerardo.bocco^lg.ramirez.sanchez', 'Web of Science: SCI/SSCI/SCI-EX; Scopus; Otros índices', 171, 178, ''],
    ['Paisajes físico-geográficos de los manglares de la laguna de La Mancha, Veracruz, México', 'Interciencia, Revista de Ciencia y Tecnología de América Latina', '31', '3', 2006, '0378-1844', 'PUBLICADO', 'No', 'angel.priego^h.hernandez.trejo^ja.lopez.portillo^ja.lopez.portillo^e.vera.isunza', 'Web of Science: SCI/SSCI/SCI-EX; Latindex; Otros índices', 211, 219, ''],
    ['Paisajes físico-geográficos de la cuenca Lerma-Chapala, México', 'Gaceta Ecológica, Nueva Época', '', '71', 2004, '1405-2849', 'PUBLICADO', 'No', 'angel.priego^helda.morales', 'Latindex; Otros índices', 11, 22, ''],
    ['Aplicación de los paisajes físico-geográficos en un sector de la cordillera Ibérica: La cuenca del río Martín (Aragón, España)', 'Interciencia, Revista de Ciencia y Tecnología de América Latina', '40', '6', 2015, '0378-1844', 'PUBLICADO', 'No', 'angel.priego^ivan.franch^manuel.bollo^luis.cancer', 'Web of Science: SCI/SSCI/SCI-EX; Latindex; SciELO; Otros índices', 381, 389, ''],
    ['Paisajes físico-geográficos de Cayo Guillermo, Ciego de Ávila, Cuba', 'Revista Del Jardín Botánico Nacional De Cuba', '', '20', 1999, '0253-5696', 'PUBLICADO', 'No', 'angel.priego^j.gonzález.areu^l.menéndez.carrera', 'Latindex; Otros índices', 159, 166, ''],
    ['Heterogeneidad del paisaje y riqueza de flora: Su relación en el archipiélago de Camagüey, Cuba', 'Interciencia, Revista de Ciencia y Tecnología de América Latina', '29', '3', 2004, '0378-1844', 'PUBLICADO', 'No', 'angel.priego^jl.palacio.prieto^p.moreno.casasola^ja.lopez.portillo^d.geissert.kientz', 'Web of Science: SCI/SSCI/SCI-EX; Latindex; Otros índices', 138, 144, ''],
    ['Potencial para la conservación de la geodiversidad de los paisajes del Estado de Michoacán, México', 'Perspectiva Geográfica', '', '', 2017, '0123-3769', 'ACEPTADO', 'No', 'angel.priego^luis.ramirez^manuel.bollo', 'Clase; Latindex; Otros índices', 1, 15, ''],
    ['An interdisciplinary approach to depict landscape change drivers: A case study of the Ticuiz agrarian community in Michoacan, Mexico', 'Applied Geography', '', '32', 2012, '0143-6228', 'PUBLICADO', 'No', 'angel.priego^m.campos.sanchez^alejandro.velazquez^gerardo.bocco^margaret.skutsch^m.boada.junca', 'Web of Science: SCI/SSCI/SCI-EX; Scopus; Otros índices', 409, 419, ''],
    ['Rural people\'s knowledge and perception of landscape: A case study from the Mexican Pacific coast', 'Society & Natural Resources', '', '25', 2012, '0894-1920', 'PUBLICADO', 'No', 'angel.priego^m.campos.sanchez^gerardo.bocco^alejandro.velazquez^m.boada.junca', 'Otros índices', 759, 774, ''],
    ['Defining environmental management units based upon integrated landscape principles at the Pacific coast in Mexico', 'Interciencia, Revista de Ciencia y Tecnología de América Latina', '35', '1', 2010, '0378-1844', 'PUBLICADO', 'No', 'angel.priego^m.campos.sanchez^gerardo.bocco^alejandro.velazquez^m.boada.junca', 'Web of Science: SCI/SSCI/SCI-EX; Latindex; Revistas CONACYT; RedALyC; Otros índices', 33, 40, ''],
    ['Potential Species Distribution and Richness of Ixodidae Ticks Associated with Wild Vertebrates from Michoacán, Mexico', 'Journal Of Geographic Information System', '', '6', 2014, '2151 1969', 'PUBLICADO', 'No', 'angel.priego^m.vargas.sandoval^alejandra.larrazabal', 'Web of Science: SCI/SSCI/SCI-EX; Otros índices', 467, 477, 'http://dx.doi.org/10.4236/jgis.2014.65040'],
    ['Relación entre la heterogeneidad del paisaje y la riqueza de especies de flora en cuencas costeras del estado de Veracruz, México', 'Investigaciones Geográficas, Boletín del Instituto de Geografía', '', '52', 2003, '0188-4611', 'PUBLICADO', 'No', 'angel.priego^p.moreno.casasola^jl.palacio.prieto^ja.lopez.portillo^d.geissert.kientz', 'Latindex; Scopus; SciELO; Revistas CONACYT; RedALyC; Otros índices', 31, 51, ''],
    ['Spatial fix and metabolic rift as conceptual tools in land-change science', 'Capitalism Nature Socialism', '26', '4', 2015, '1045-5752', 'PUBLICADO', 'No', 'antonio.vieyra^brian.napoletano^jaime.paneque', '', 198, 214, 'DOI: 10.1080/10455752.2015.1104706'],
    ['Narrativas sobre el lugar. Habitar una vivienda de interés social en la periferia urbana', 'Revista INVI', '30', '84', 2015, '0718-1299', 'PUBLICADO', 'No', 'antonio.vieyra^claudio.garibay', '', 59, 72, ''],
    ['Procesos participativos intramunicipales como pasos hacia la  gobernanza local en territorios periurbanos. La experiencia en el municipio de Tarímbaro, Michoacán, México', 'Journal of Latin American Geography', '14', '2', 2015, '1545-2476', 'PUBLICADO', 'No', 'antonio.vieyra^lorena.poncela^yadira.mendez', '', 129, 157, 'DOI: 10.1353/lag.2015.0027'],
    ['Acceso al suelo ejidal en la periferia urbana mexicana: Análisis desde el Capital Social', 'Economía, Sociedad y Territorio', '', '', 2016, '1405-8421', 'ACEPTADO', 'Si', 'yadira.mendez^sandra.pola^antonio.vieyra', '', 0, 0, ''],
    ['How social capital enables/restricts the  livelihoods of poor peri-urban farmers in Mexico', 'Development in Practice', '', '', 2016, '0961-4524', 'ACEPTADO', 'No', 'antonio.vieyra^yadira.mendez', '', 0, 0, ''],
    ['Peri-urban local governance? Intra-government relationships and social capital in a peripheral municipality of Michoacán, Mexico', 'Progress in Development Studies Journal', '0', '0', 2016, '1464-9934', 'ACEPTADO', 'No', 'antonio.vieyra^yadira.mendez^lorena.poncela', '', 0, 0, '0'],
    ['A detailed paleomagnetic and rock-magnetic investigation of the Matuyama-Brunhes geomagnetic reversal recorded in the tephra-paleosol sequence of Tlaxcala (Central Mexico)', 'Frontiers in Earth Science', '3', '', 2015, '2296-6463', 'PUBLICADO', 'No', 'berenice.solis^ana.soler^avto.gogichaishvili^angel.carrancho^sergey.sedov^cecilia.caballero^beatriz.ortega^juan.morales^jaime.urrutia^francisco.bautista', 'Otros índices', 1, 24, 'http://dx.doi.org/10.3389/feart.2015.00011'],
    ['Mineral magnetic properties of an alluvial paleosol sequence in the Maya Lowlands: Late Pleistocene-Holocene paleoclimatic implications', 'Quaternary International', '', '', 2015, '1040-6182', 'ACEPTADO', 'Si', 'berenice.solis^gabriel.vazquez^elizabeth.solleiro^avto.gogichaishvili^juan.morales', 'Otros índices', 0, 1, ''],
    ['Volcaniclastic reworked sediments in the Usumacinta River, Mexico: the serendipitous source of volcanic glass for Maya ceramics', 'Geoarchaeology', '', '', 2016, '1520-6548', 'EN_PRENSA', 'Si', 'berenice.solis^hector.cabadas^elizabeth.solleiro^sergey.sedov^keiko.tatanisho^rodrigo.liendo', '', 0, 0, ''],
    ['Landslides in the tropical mountain range of Veracruz (Mexico) - A case-study of the large El Capulin landslide', 'World Landslide Forum', '', '', 2016, '', 'EN_PRENSA', 'Si', 'berenice.solis^martina.wilde^wendy.morales^daniel.schwindt^matthias.bucker^birgit.terhorst', '', 0, 0, ''],
    ['Horizontal and vertical landscape-complexity influence avian species-richness patterns across the conterminous USA', 'Cogent Environmental Science', '', '', 2015, '0143-6228', 'ENVIADO', 'No', 'brian.napoletano^bryan.pijanowski', '', 0, 0, ''],
    ['Visibility analysis and landscape evaluation in Martin River Cultural Park (Aragon, Spain) integrating biophysical and visual units', 'Journal of Maps', '', '', 1900, '', 'PUBLICADO', 'Si', 'brian.napoletano^ivan.franch^luis.cancer', '', 0, 0, ''],
    ['Small Drones for Community-Based Forest Monitoring: An Assessment of Their Feasibility and Potential in Tropical Areas', 'Forests', '5', '6', 2014, '1999-4907', 'PUBLICADO', 'Si', 'brian.napoletano^jaime.paneque^keith.mccall', '', 1481, 1507, '10.3390/f5061481'],
    ['Recuento nacional de los conflictos mineros territoriales en México', 'Les Cahiers des Amériques Latines', '', '', 2016, '', 'ACEPTADO', 'No', 'claudio.garibay', '', 1, 2, ''],
    ['A. Brigitte Nellie Luisa Boehm Shchoendube (1938-2005)', 'International Encyclopedia of Anthropology', '', '', 2016, '', 'EN_PRENSA', 'No', 'claudio.garibay^andrew.roth', '', 0, 1, ''],
    ['Evaluación de la contaminación ambiental a partir del aumento magnético en polvos urbanos - Caso de estudio para la ciudad de Mexicali, México', 'Revista Mexicana de Ciencias Geológicas', '32', '3', 2016, '1026-8774', 'PUBLICADO', 'Si', 'francisco.bautista^a.sanchez.duque^avto.gogichaishvili^raul.cejudo^j.reyez.lopez^f.solis.dominguez^j.morales.contreras', '', 501, 513, 'http://satori.geociencias.unam.mx/32-3/(09)SanchezDuque.pdf'],
    ['Soil & Environment as a tool for soil environmental functions evaluation', 'Programmnye produkty i sistemy', '2', '3', 2016, '2311-2735', 'PUBLICADO', 'Si', 'francisco.bautista^angeles.gallegos^inna.dubrovina', 'Otros índices', 195, 200, '10.15827/0236-235X.114.195-200'],
    ['El color del polvo urbano como indicador de contaminación por elementos potencialmente tóxicos: El caso de Ensenada, Baja California', 'Revista Chapingo Serie Ciencias Forestales y del Ambiente', '21', '3', 2015, '', 'PUBLICADO', 'No', 'francisco.bautista^avto.gogichaishvili', '', 255, 266, ''],
    ['Propiedades magnéticas y color de polvos urbanos como indicadores proxy de contaminación por metales pesados', 'Latimag Letters', '3', '', 2015, '', 'PUBLICADO', 'Si', 'francisco.bautista^avto.gogichaishvili^o.delgado.carranza^raul.cejudo^jaime.morales', '', 0, 0, ''],
    ['The App SOC + a tool to estimate or/and calculate organic carbon in the soil profile', 'Journal of Applied Research and technology', '14', '2', 2016, '1665-6423', 'PUBLICADO', 'Si', 'francisco.bautista^eduardo.garcia^angeles.gallegos', '', 135, 139, 'doi.org/10.1016/j.jart.2016.03.002'],
    ['Application of the physico-geographic landscapes in a sector of the Iberian Mountain Range: The Martin River Basin (Aragon, Spain)', 'Interciencia, Revista de Ciencia y Tecnología de América Latina', '40', '', 2015, '', 'PUBLICADO', 'No', 'francisco.bautista^ivan.franch^angel.priego^manuel.bollo^luis.cancer', '', 381, 389, ''],
    ['Paisajes geomorfológicos: base para el levantamiento de suelos en Tabasco, México', 'Ecosistemas y Recursos Agropecuarios', '3', '8', 2016, '2007-901X', 'PUBLICADO', 'Si', 'francisco.bautista^j.zavala.cruz^r.jimenez.ramirez^d.palma.lopez^f.gavi.reyes', '', 161, 171, '358645282002'],
    ['Further evidence for magnetic susceptability as a proxy for the evaluation of heavy metals in mining waste: case study of Thalpujahua and El Oro mining districts', 'Environmental Earth Science', '75', '', 2016, '', 'PUBLICADO', 'No', 'francisco.bautista^jaime.morales^avto.gogichaishvili', '', 309, 318, '10.1007/s12665-015-5187-8'],
    ['Diagnóstico agroecológico de la microcuenca periurbana Río Platanitos, Guatemala', 'Tecnología en Marcha', '28', '', 2015, '', 'PUBLICADO', 'Si', 'francisco.bautista^luis.morales', '', 169, 178, ''],
    ['Actualización del mapa de suelos de Yucatán utilizando un enfoque geomorfopedológico y WRB', 'Ecosistemas y Recursos Agropecuarios', '2', '', 2015, '', 'PUBLICADO', 'Si', 'francisco.bautista^oscar.frausto^thomas.j.ihl^yadira.mendez', '', 303, 3015, ''],
    ['Análisis espacial de susceptibilidad magnética en la zona metropolitana de la ciudad de Guadalajara', 'Latimag Letters', '3', '', 2015, '', 'PUBLICADO', 'Si', 'francisco.bautista^raul.cejudo^avto.gogichaishvili^jaime.morales', '', 0, 0, ''],
    ['Estudio de propiedades magnéticas en riñon e hígado de Mus musculus para la detección de elementos tóxicos', 'Latimag Letters', '6', '', 2016, '2007-9656', 'PUBLICADO', 'Si', 'francisco.bautista^raul.cejudo^o.delgado.carranza^avto.gogichaishvili^jaime.morales', '', 1, 6, ''],
    ['Identificación de zonas presumiblemente contaminadas por elementos tóxicos por técnicas no convencionales en la ciudad de Morelia, Michoacán', 'Latimag Letters', '6', '', 2016, '2007-9656', 'PUBLICADO', 'Si', 'francisco.bautista^raul.cejudo^o.delgado.carranza^israde.alcantara^avto.gogichaishvili^jaime.morales', '', 1, 5, ''],
    ['Caracterización magnética del polvo urbano de calles y plantas por uso de suelo en la Zona Metropolitana del Valle de México', 'Latimag Letters', '3', '', 2015, '', 'PUBLICADO', 'Si', 'francisco.bautista^raul.cejudo^o.delgado.carranza^israde.alcantara^avto.gogichaishvili^jaime.morales^ana.soler', '', 0, 0, ''],
    ['Estudio magnético y geoquímico de lodos lixiviados de sitios de disposición final de residuos urbanos', 'Latimag Letters', '6', '', 2016, '2007-9656', 'PUBLICADO', 'Si', 'francisco.bautista^raul.cejudo^o.delgado.carranza^israde.alcantara^avto.gogichaishvili^jaime.morales^ana.soler', '', 1, 5, ''],
    ['El potencial del magnetismo en la clasificación de suelos: una revisión', 'Boletín de la Sociedad Geológica Mexicana', '66', '', 2015, '', 'PUBLICADO', 'No', 'francisco.bautista^raul.cejudo^yameli.aguilar^avto.gogichaishvili', '', 123, 134, ''],
    ['Concentration of toxic elements in topsoils of Metropolitan area of Mexico City: A spatial analysis using Ordinary Kriging and Indicator Kriging', 'Revista Internacional de Contaminación Ambiental', '31', '', 2015, '', 'PUBLICADO', 'Si', 'francisco.bautista^thomas.j.ihl^raul.cejudo^o.delgado.carranza^avto.gogichaishvili', '', 42, 62, ''],
    ['Entre la utopía y la distopía. La construcción social de la experiencia de la ciudad en un espacio excluido de la ciudad de Morelia, Michoacán', 'Revista Mexicana de Sociología', '', '', 2016, '', 'ENVIADO', 'No', 'frida.guiza', '', 0, 0, ''],
    ['Información geográfica voluntaria (IGV), estado del arte en Latinoamérica', 'Revista Cartográfica', '', '', 2016, '', 'ACEPTADO', 'No', 'frida.guiza^aldo.hernandez', '', 0, 0, ''],
    ['The networked agency of flash flood\'s materiality and its socioenvironmental processes, exhibit power performances and inequalities', 'Geoforum', '', '', 2015, '0016-7185', 'ACEPTADO', 'No', 'frida.guiza^peter.simmons', '', 0, 0, ''],
    ['Politics of material agency in vulnerable places', 'Science Technology and Human Values', '', '', 2016, '', 'ENVIADO', 'No', 'frida.guiza^peter.simmons', '', 0, 0, ''],
    ['Chronic institutional failure and enhanced vulnerability to flash-floods in the Cuenca Altadel Río Lerma, Mexico', 'Disasters', '', '', 2015, '1467-7717', 'PUBLICADO', 'No', 'frida.guiza^peter.simmons^keith.mccall', '', 0, 0, '10.1111/disa.12134'],
    ['Urbanscapes of disaster. The sociopolitical and environmental factors underpinning a disaster processes within a vulnerable slum in Mexico', 'City and Community', '', '', 2015, '1540-6040', 'ACEPTADO', 'No', 'frida.guiza^yadira.mendez^keith.mccall', '', 0, 0, ''],
    ['Sex Ratio and Sex-Specific Latitudinal Variation in Floral Characteristics of Gynodioecious Kallstroemia grandiflora (Zygophyllaceae) in Mexico', 'Biotropica', '43', '3', 2010, '1744-7429', 'PUBLICADO', 'No', 'gabriela.cuevas', '', 317, 323, '10.1111/j.1744-7429.2010.00692.x.'],
    ['Si no comemos tortilla, no vivimos: women, climate change, and food security in central Mexico', 'Agriculture and Human Values', '31', '4', 2014, '0889-048X', 'PUBLICADO', 'No', 'gabriela.cuevas', '', 607, 620, '10.1007/s10460-014-9503-9'],
    ['Health impacts from power plant emissions in Mexico', 'Atmospheric Environment', '39', '7', 2005, '', 'PUBLICADO', 'No', 'gabriela.cuevas', '', 1199, 1209, '10.1016/j.atmosenv.2004.10.035'],
    ['Energy consumption in the management of avocado orchards in Michoacán, Mexico', 'Revista Chapingo Serie Horticultura', '21', '1', 2015, '', 'PUBLICADO', 'No', 'gabriela.cuevas^carlos.anaya^ana.burgos', '', 5, 20, '10.5154/r.rchsh. 2014.01.002'],
    ['Contenido de Carbono orgánico y retención de agua en los suelos de un bosque de niebla en Michoacán, México', 'Agrociencia', '50', '2', 2016, '1405-3195', 'PUBLICADO', 'No', 'gabriela.cuevas^carlos.anaya^manuel.mendoza^rosaura.paez^luis.olivares', 'Revistas CONACYT; Web of Science: SCI/SSCI/SCI-EX; SciELO; RedALyC', 251, 269, ''],
    ['Land use and cover change scenarios in the Mesoamerican Biological Corridor-Chiapas, México', 'Botanical Sciences', '', '', 2016, '', 'ACEPTADO', 'No', 'gabriela.cuevas^diana.ramirez^paula.melic^manuel.mendoza', '', 0, 0, ''],
    ['Supporting environmental and Natural Resources Management. The National Institute of Ecology of Mexico', 'GIM International', '18', '4', 2004, '', 'PUBLICADO', 'No', 'gabriela.cuevas^gerardo.bocco', '', 69, 71, ''],
    ['Distribución geográfica y ecológica de Ipomoea (Convolvulaceae) en el estado de Michoacán, México', 'Revista Mexicana de Biodiversidad', '83', '', 2012, '1870-3453', 'PUBLICADO', 'No', 'gabriela.cuevas^j.alcantar.mejía', '', 731, 741, ''],
    ['Assessing Modifiable Areal Unit Problem (MAUP) Effects in the Analysis of Deforestaion Drivers Using Local Models', 'Proceedings of the 8th International Congress on Environmental Modelling and Software (iEMSs)', '', '', 2016, '', 'PUBLICADO', 'Si', 'gabriela.cuevas^jean.mas^azucena.perez^a.andablo.reyes^miguel.castillo^a.flamenco.sandoval', '', 1313, 1318, ''],
    ['Deforestation and land tenure in Mexico: A response to Bonilla-Moheno et al', 'Land Use Policy', '39', '', 2014, '0264-8377', 'PUBLICADO', 'No', 'gabriela.cuevas^margaret.skutsch^jean.mas^gerardo.bocco^yan.gao', '', 390, 396, '10.1016/j.landusepol.2013.11.013'],
    ['Absence of detectable transgenes in local landraces of maize in Oaxaca, Mexico (2003-2004)', 'Proceedings of National Academy of Sciences of USA', '102', '35', 2015, '1091-6490', 'PUBLICADO', 'No', 'gabriela.cuevas^s.ortiz.garcia', '', 12338, 12343, '10.1073/pnas.0503356102'],
    ['An Accuracy Index with Positional and Thematic Fuzzy Bounds for Land-use/Land-cover Maps', 'Photogrammetric Engineering and Remote Sensing', '75', '7', 2009, '0099-1112', 'PUBLICADO', 'No', 'gabriela.cuevas^stephane.couturier^jean.mas', '', 789, 805, '10.14358/PERS.75.7.789'],
    ['Remoteness and remote places. A geographic perspective', 'Geoforum', '', '', 2016, '', 'ACEPTADO', 'No', 'gerardo.bocco', 'Scopus; Otros índices', 0, 0, ''],
    ['General principles behind traditional environmental knowledge: the local dimension in land management', 'The Geographical Journal', '', '', 2015, '', 'PUBLICADO', 'No', 'gerardo.bocco^antoinette.winklerprins', '', 0, 0, 'DOI: 10.1111/geoj.12147'],
    ['Ordenamiento Ecológico Marino en el Pacífico Norte mexicano: propuesta metodológica', 'Hidrobiológica', '', '', 2015, '0188-8897', 'EN_PRENSA', 'No', 'gerardo.bocco^benigno.hernandez^raul.aguirre^gilberto.gaxiola^raul.aguirre^gilberto.gaxiola^saul.alvarez^artemio.gallegos^fernando.rosete', '', 0, 0, ''],
    ['Vulnerable and invisible: impact of hurricane activity on a peasant population in a mountainous region on the Mexican Pacific coast', 'Journal of Latin American Geography', '14', '2', 2015, '', 'PUBLICADO', 'No', 'gerardo.bocco^itzi.segundo', '', 159, 179, ''],
    ['Conocimiento tradicional del paisaje en una comunidad indígena: caso de estudio en la región purépecha, occidente de México', 'Investigaciones Geográficas, Boletín del Instituto de Geografía', '', '', 2015, '0188-4611', 'PUBLICADO', 'No', 'gerardo.bocco^juan.pulido', 'Revistas CONACYT; Scopus; SciELO; RedALyC; Latindex', 0, 0, 'dx.doi.org/10.14350/rig.45590 ISI'],
    ['Regional Landscape Change in Fishing Communities of the Mexican North Pacific', 'Landscape Research', '40', '7', 2015, '', 'PUBLICADO', 'No', 'gerardo.bocco^pablo.alvarez^georges.seingier^ileana.espejel^julie.noriega', '', 855, 874, '10.1080/01426397.2015.1031095'],
    ['Pensamiento geográfico en América Latina: retrospectiva y balances generales', 'Investigaciones Geográficas, Boletín del Instituto de Geografía', '', '90', 2016, '0188-4611', 'EN_PRENSA', 'No', 'gerardo.bocco^pedro.urquijo', 'Scopus; Revistas CONACYT; RedALyC', 0, 0, ''],
    ['Metales pesados en suelos urbanos de Morelia, Michoacán: influencia de los usos de suelo y tipos de viabilidad', 'Ciencia Nicolaita', '65', '', 2015, '2007-7068', 'PUBLICADO', 'No', 'hilda.rivas^o.delgado.carranza^israde.alcantara^francisco.bautista^avto.gogichaishvili^raul.cejudo^jaime.morales', '', 120, 138, ''],
    ['Impacts of Bokashi on survival and growth rates of Pinus pseudostrobus in community reforestation projects', 'Journal of Environmental Management', '150', '', 2015, '', 'PUBLICADO', 'No', 'hilda.rivas^pablo.jaramillo^maria.ramirez^diego.perez', '', 48, 56, ''],
    ['Three approaches to the assessment of spatio-temporal distribution of the water balance: the case of the Cuitzeo basin, Michoacán, Mexico.', 'Boletín del Instituto de Geografía', '76', '', 2011, '0188-4611', 'PUBLICADO', 'No', 'hugo.zavala^alfredo.amador^erna.lopez^manuel.mendoza', '', 34, 55, ''],
    ['Monitoring Deforestation With MODIS, Proceedings of the ForestSat 07 Conference, Montpellier France', 'Conference Montpellier France', '', '', 2007, '', 'PUBLICADO', 'No', 'hugo.zavala^jean.mas^yan.gao', '', 0, 0, ''],
    ['Tendencias recientes de las superficies ocupadas por el lago de Cuitzeo. Un enfoque basado  en percepción remota, sistemas de información geográfica y análisis estadístico', 'Boletín del Instituto de Geografía', '64', '64', 2007, '0188-4611', 'PUBLICADO', 'No', 'hugo.zavala^manuel.mendoza^gerardo.bocco^erna.lopez^miguel.bravo', '', 43, 62, ''],
    ['Exploring indigenous landscape classification across different dimensions: a case study from the Bolivian Amazon', 'Landscape Research', '40', '3', 2015, '0142-6397', 'PUBLICADO', 'No', 'jaime.paneque', '', 318, 337, '10.1080/01426397.2013.829810'],
    ['Opportunities, constraints and perceptions of smallholders regarding their potential to contribute to forest landscape transitions under REDD+: Case studies from Mexico', 'The International Forestry Review', '17', 'S1', 2015, '1465-5489', 'PUBLICADO', 'No', 'jaime.paneque^margaret.skutsch^armonia.borrego^diego.perez^yan.gao', '', 65, 84, '10.1505/146554815814669025'],
    ['State formation and territorialization in forest lands: historical and geographical evolution of forest conflicts in the state of Michoacán, Mexico', 'Annals of the American Association of Geographers', '', '', 2016, '1467-8306', 'ENVIADO', 'No', 'jaime.paneque^irene.perez^irene.perez^maria.ramirez^claudio.garibay^pedro.urquijo', '', 0, 0, ''],
    ['Traditional ecological knowledge and tropical forest conservation. A spatial analysis among Tsimane Amerindians (Bolivian Amazon)', 'Global Environmental Change', '', '', 2016, '', 'ENVIADO', 'No', 'jaime.paneque^irene.perez^maximilien.gueze^jean.mas^manuel.macia^marti.orta^victoria.reyes', '', 0, 0, ''],
    ['How does cultural change affect indigenous peoples\' hunting activity? An empirical study among the Tsimane\' in the Bolivian Amazon', 'Conservation and Society', '13', '4', 2015, '', 'PUBLICADO', 'No', 'jaime.paneque^marti.orta^victoria.reyes', '', 382, 394, '10.4103/0972-4923.179879'],
    ['Uso comunitario de pequeños vehículos aéreos no tripulados (drones) en conflictos ambientales: ¿un factor innovador desequilibrante?', 'Teknokultura. Revista de Cultura Digital y Movimientos Sociales', '13', '2', 2016, '', 'EN_PRENSA', 'Si', 'jaime.paneque^nicolas.vargas^marcela.morales', '', 0, 0, ''],
    ['Validation of MODIS Vegetation Continuos Fields for monitoring deforestation and forest degradation: two cases in Mexico', 'Geocarto International', '31', '9', 2016, '', 'PUBLICADO', 'No', 'jaime.paneque^yan.gao^adrian.ghilardi^margaret.skutsch^jean.mas', '', 1019, 1031, '10.1080/10106049.2015.1110205'],
    ['Modeling Historical Land Cover and Land Use: A Review from Contemporary Modeling', 'ISPRS International Journal of Geo-Information', '4', '4', 2015, '2220-9964', 'PUBLICADO', 'No', 'jean.mas^laura.chang^jf.torrescano.valle^pedro.urquijo', '', 1791, 1812, '10.3390/ijgi4041791'],
    ['Toward a near-real time forest monitoring system (Technical note)', 'Investigaciones Geográficas, Boletín del Instituto de Geografía', '', '91', 2016, '0188-4611', 'PUBLICADO', 'Si', 'jean.mas^Lemoine,rodríguez^hind.taud', 'Latindex; Revistas CONACYT', 168, 175, '10.14350/rig.48600'],
    ['Análisis jerárquico de la intensidad de cambio de cobertutra/uso de suelo y deforestación (2000-2008) en la Reserva de la Biosfera Sierra de Manantlán, México', 'Investigaciones Geográficas, Boletín del Instituto de Geografía', '88', '', 2016, '0188-4611', 'PUBLICADO', 'No', 'jean.mas^m.farfan.gutierez^g.rodriguez.tapia', 'Latindex; Revistas CONACYT', 75, 90, 'dx.doi.org/10.14350/rig.48600'],
    ['Análisis y modelación de los procesos de deforestación: un caso de estudio en la cuenca  del río Coyuquilla, Guerrero, México', 'Investigaciones Geográficas, Boletín del Instituto de Geografía', '88', '', 2015, '0188-4611', 'PUBLICADO', 'No', 'jean.mas^miguel.maass^laura.osorio', 'Latindex', 75, 90, '10.14350/rig.44603'],
    ['Comparison of simulation models in terms of quantity and allocation of land change', 'Environmental Modelling & Software', '69', '', 2015, '1364-8152', 'PUBLICADO', 'No', 'jean.mas^mt.camacho.olmedo', '', 214, 221, '10.1016/j.envsoft.2015.03.003'],
    ['Composición y estructura de la vegetación arbórea de petenes en la reserva de la biosfera de los petenes, Campeche, México', 'Polibotánica', '39', '', 2015, '1405-2768', 'PUBLICADO', 'Si', 'jean.mas', 'Latindex', 1, 19, ''],
    ['Comment on Gebhardt et al. MAD-MEX: Automatic Wall-to-Wall Land Cover Monitoring for the Mexican REDD-MRV Program Using All Landsat Data', 'Remote Sensing', '8', '533', 2016, '2072-4292', 'PUBLICADO', 'Si', 'jean.mas^stephane.couturier^jaime.paneque^margaret.skutsch^azucena.perez^gerardo.bocco^miguel.castillo', 'Web of Science: SCI/SSCI/SCI-EX', 1, 14, '10.3390/rs8070533 '],
    ['Ubicación de los sitios de muestreo, generos de bacterias identificadas y fuentes de origen de las muestras en la CASPJ', 'Ciencia Nicolaita', '', '', 2015, '', 'ENVIADO', 'No', 'jose.navarrete^maria.carmona', '', 1, 1, ''],
    ['Modeling sea-level change, inundation scenarios and their effect on the Colola Beach Reserve - a nesting - habitat of the black sea turtle, Michoacán, México', 'Geofísica Internacional', '54', '2', 2015, '', 'PUBLICADO', 'No', 'jose.navarrete^y.calvillo.garcía^teresa.ramirez^c.delgado.trejo^g.legorreta.paulin', '', 179, 190, ''],
    ['De lo efímero a lo perdurable, el sello de la religión cristina en el paisaje: el sistema constructivo de los edificios religiosos primitivos', 'Relaciones', '', '', 2016, '', 'ENVIADO', 'No', 'karine.lefebvre', '', 0, 0, ''],
    ['Beyond "Landscape" in REDD+: The imperative for "Territory"', 'World Development', '85', '', 2016, '0305-750X', 'PUBLICADO', 'No', 'keith.mccall', '', 58, 72, '10.1016/j.worlddev.2016.05.001'],
    ['Participatory methods in the Georgian Caucasus: Understanding vulnerability and response to debrisflow hazards', 'International Journal of Geosciences', '6', '', 2015, '2156-8359', 'PUBLICADO', 'No', 'keith.mccall', '', 666, 674, '0.4236/ijg.2015.67054'],
    ['Recognized but not supported: Assessing the incorporation of non-timber forest products into Mexican forest policy', 'Forest Policy and Economics', '71', '', 2016, '1389-9341', 'PUBLICADO', 'No', 'keith.mccall^tzitzi.sharhi^citlalli.lopez', '', 36, 42, ''],
    ['Preface to this Virtual Thematic Issue: Modelling with Stakeholders II', 'Environmental Modelling & Software', '77', '', 2016, '1364-8152', 'PUBLICADO', 'Si', 'keith.mccall^alexey.voinov^nagesh.kolagani', '', 153, 155, 'DOI: 10.1016/j.envsoft.2016.01.006'],
    ['Modelling with Stakeholders - Next Generation', 'Environmental Modelling & Software', '77', '00', 2016, '1364-8152', 'PUBLICADO', 'No', 'keith.mccall^alexey.voinov^nagesh.kolagani^pierre.glynn^marit.kraagt^frank.ostermann^palaniappan.ramu^suzanne.pierce', '', 196, 220, 'doi.org/10.1016/j.envsoft.2015.11.016'],
    ['Urbanscapes of disaster. The sociopolitical and spatial processes underpinning vulnerability within a slum in Mexico', 'City and Community', '00', '', 2016, '1540-6040', 'PUBLICADO', 'No', 'keith.mccall^frida.guiza^yadira.mendez', '', 0, 0, ''],
    ['Shifting Boundaries of Volunteered Geographic Information Systems and Modalities: Learning from PGIS', 'ACME An International E-Journal for Critical Geographies', '14', '3', 2015, '1492-9732', 'PUBLICADO', 'Si', 'keith.mccall^javier.martinez^jeroen.verplanke', '', 791, 826, ''],
    ['A shared perspective for PGIS and VGI', 'The Cartographic Journal', '53', '', 2016, '0008-7041', 'PUBLICADO', 'No', 'keith.mccall^jeroen.verplanke^claudia.uberhuaga^giacomo.gambaldi^muki.haklay', '', 0, 0, 'DOI:  10.1080/00087041.2016.1227552'],
    ['Conceptualizing community monitoring of forest carbon stocks and tracking of safeguards in Kenya', 'Open Journal of Forestry', '5', '4', 2015, '1999-4907', 'PUBLICADO', 'No', 'keith.mccall^julius.muchemi^francis.wegulo^m.kinyanjui^alfred.gichu^elias.ucakuwun^gilbert.nduru', '', 0, 0, '10.4236/ojf.2015.54040'],
    ['Participatory Mapping of the Geography of Risk: Risk Perceptions of Children and Adolescents in Two Portuguese Towns', 'Children, Youth and Environments', '26', '1', 2016, '', 'PUBLICADO', 'No', 'keith.mccall^mario.freitas^luis.dourado', '', 85, 110, 'www.jstor.org/action/showPublication?journalCode=chilyoutenv'],
    ['Moving from Measuring, Reporting, Verification (MRV) of Forest Carbon to Community Mapping, Measuring, Monitoring (MMM): a case in Mexico', 'Plos One', '11', '6', 2016, '1932-6203', 'PUBLICADO', 'Si', 'keith.mccall^noah.chutz^margaret.skutsch', '', 0, 0, 'doi:10.1371/journal.pone.0146038'],
    ['History of pedogenesis and geomorphic processes in the Valley of Teotihuacán, Mexico: micromorphological evidence from soil catena', 'Spanish Journal of Soil Science', '3', '3', 2013, '', 'PUBLICADO', 'No', 'lourdes.gonzalez^emily.mcclung^jorge.gama^sergey.sedov^lorenzo.vazquez', '', 201, 216, '10.3232/SJSS.2013.V3.N3.05'],
    ['Late Holocene erosion events in the Valley of Teotihuacan, central Mexico: insights from a soil-geomorphic analysis of catenas', 'CATENA', '', '', 2016, '', 'ACEPTADO', 'No', 'lourdes.gonzalez^emily.mcclung^jorge.gama^sergey.sedov^lorenzo.vazquez', '', 1, 2, ''],
    ['Effects of biophysical properties on soil erosion within a catchment approach: modeling through WEPP over the last 2000 years', 'Land Degradation and Development', '', '', 2017, '', 'ENVIADO', 'No', 'lourdes.gonzalez^manuel.mendoza^jose.navarrete', '', 1, 1, ''],
    ['Human impact on natural systems modeled through soil erosion in GeoWEPP: a comparison between pre-Hispanic periods and modern times in the Teotihuacan Valley (central Mexico)', 'CATENA', '', '', 2016, '', 'PUBLICADO', 'No', 'lourdes.gonzalez^manuel.mendoza^lorenzo.vazquez', '', 0, 0, ''],
    ['Zonificación geoecológica del paisaje urbano', 'Mercator', 'v.15,', '2', 2016, '1676-8329', 'PUBLICADO', 'No', 'manuel.bollo^ayesa.martinez', 'Latindex; SciELO; RedALyC', 117, 136, '10.4215/RM2016.1502. 0008'],
    ['Mapa de paisajes físico-geográficos del Parque Cultural del río Martín (Teruel, Aragón) escala 1:50.000', 'Revista Catalana de Geografía', '. IV época / volumen XXI /', 'núm. 53', 2016, '1988-2459', 'PUBLICADO', 'Si', 'manuel.bollo^ivan.franch^a.espinoza.maya^luis.cancer', '', 1, 15, ''],
    ['Panorama contemporáneo del ordenamiento ecológico territorial en México', 'Polígonos, Revista de Geografía', '1', '26', 2014, '1132-1202', 'PUBLICADO', 'No', 'manuel.bollo^lm.espinosa.rodriguez', 'Latindex', 111, 146, ''],
    ['Potential distribution of mountain cloud forest in Michoacan, Mexico: prioritization for conservation in the context of landscape connectivity', 'Environmental Management', '', '', 2016, '', 'ENVIADO', 'No', 'manuel.mendoza^camilo.correa^andres.etter^diego.perez', '', 0, 0, ''],
    ['Modelación espacial del tiempo de intervención antrópica sobre el paisaje: un caso de estudio en el sistema volcánico transversal de Michoacán, México', 'Geografía y Sistema de Información Geográfica', '8', '8', 2016, '1852-8031', 'PUBLICADO', 'Si', 'manuel.mendoza^camilo.correa^andres.etter^diego.perez', '', 183, 205, ''],
    ['Habitat connectivity in biodiversity conservation: a review of recent studies and applications', 'Progress in Physical Geography', '40', '1', 2016, '1477-0296', 'PUBLICADO', 'No', 'manuel.mendoza^camilo.correa^andres.etter^diego.perez', '', 7, 37, 'DOI: 10.1177/0309133315598713'],
    ['Evaluation of anthropogenic impact of habitat connectivity through a multidimensional spatial human footprint index in a highly biodiverse ladscape of central Mexico', 'Ecological Indicators', '72', '1', 2016, '1470-160X', 'EN_PRENSA', 'No', 'manuel.mendoza^camilo.correa^andres.etter^diego.perez', '', 895, 909, '10.1016/j.ecolind.2016.09.007'],
    ['Riesgo volcánico: Estado del arte y desafíos de trabajo', 'Boletín de la Sociedad Geológica Mexicana', '', '', 2016, '', 'ENVIADO', 'No', 'manuel.mendoza^gemma.gomez^luis.macias^erna.lopez', '', 0, 0, ''],
    ['An exploratory analysis of land abandonment drivers in areas prone to desertification', 'CATENA', '128', '', 2015, '0341-8162', 'PUBLICADO', 'No', 'manuel.mendoza', '', 252, 261, 'http://dx.doi.org/10.1016/j.catena.2014.02.006'],
    ['Is canopy-cover recovery associated to vegetation attributes and diversity recovery in tropical shrubland?', 'Plant Ecology', '', '', 2015, '', 'ENVIADO', 'No', 'manuel.mendoza^a.lomelí.jimenez^diego.perez^b.figueroa.rangel', '', 0, 0, ''],
    ['Dinámica espacio-temporal del bosque nublado y su estado sucesional en el Estado de Michoacán, México', 'Geografía y Sistema de Información Geográfica', '8', '8', 2016, '1852-8031', 'PUBLICADO', 'Si', 'manuel.mendoza^y.martinez.ruiz^ge.santana.huicochea^erna.lopez', '', 233, 247, ''],
    ['Statistical spatial model for multifactorial analyisis of landslides: the case of the municipality of Francisco León, Chiapas', 'Geomorphology', '', '', 2015, '', 'ENVIADO', 'No', 'manuel.mendoza^arturo.muniz^jc.mora.chaparro', '', 0, 0, ''],
    ['Procesos de cambio de cobertura y uso de suelo en cuencas tropicales costeras del pacifico central mexicano', 'Investigaciones Geográficas, Boletín del Instituto de Geografía', '', '', 2016, '', 'ENVIADO', 'No', 'manuel.mendoza^alejandro.nene^gaspar.gonzalez^francisco.silva', '', 0, 0, ''],
    ['Effect of the landscape matrix condition for prioritizing Multi-Species Connectivity Conservation in a Highly Biodiverse Landscape of Central Mexico', 'Environmental Management', '', '', 2016, '', 'ENVIADO', 'No', 'manuel.mendoza^camilo.correa^andres.etter^diego.perez', '', 0, 0, ''],
    ['Análisis espacial del paisaje como base para muestreos dendrocronológicos: El caso de la reserva de la Biosfera de la Mariposa Monarca, México', 'Madera y Bosque', '22', '2', 2015, '', 'PUBLICADO', 'No', 'manuel.mendoza^t.carlon.allende^diego.perez', '', 11, 22, ''],
    ['Geomorpology, internal structure and evolution of alluvial fans at Motozintla, Chiapas, Mexico', 'Geomorphology', '230', '', 2015, '', 'PUBLICADO', 'No', 'manuel.mendoza^jm.sanchez.nunez^luis.macias^ricardo.saucedo', '', 1, 12, 'http://dx.doi.org/10.1016/j.geomorph.2014.10.003'],
    ['Climatic responses of Pinus pseudostrobus and Abies religiosa in the Monarch Butterfly Biosphere Reserve', 'Dendrochronologia', '38', '', 2016, '1125-7865', 'PUBLICADO', 'No', 'manuel.mendoza^t.carlon.allende^diego.perez', '', 103, 116, 'http://dx.doi.org/10.1016/j.dendro.2016.04.002'],
    ['Identifying future climatic change patterns at basin level in Baja California', 'Atmosfera', '', '', 2016, '', 'ENVIADO', 'No', 'manuel.mendoza^t.carlon.allende^yan.gao', '', 0, 0, ''],
    ['Policy for pro-poor distribution of REDD+ benefits in Mexico: how the legal and technical challenges are being addressed', 'Forest Policy and Economics', '', '', 2017, '1389-9341', 'ACEPTADO', 'No', 'margaret.skutsch^arturo.balderas', '', 0, 0, ''],
    ['Impacts of Finnish cooperation in the Mexican policy making process: from community forest management to the liberalisation of forest services', 'Forest Policy and Economics', '73', '', 2016, '', 'PUBLICADO', 'No', 'margaret.skutsch', '', 229, 2380, 'http://dx.doi.org/10.1016/j.forpol.2016.09.011 1389-9341/'],
    ['Editorial for Special Issue: The Potential Role for Community Monitoring in MRV and in Benefit Sharing in REDD+', 'Forests', '6', '1', 2015, '1999-4907', 'PUBLICADO', 'No', 'margaret.skutsch^arturo.balderas', '', 244, 251, 'doi:10.3390/f6010244'],
    ['Yes-in-my-backyard: spatial differences in the valuation of forest services and local co-benefits for carbon markets in México', 'Ecological Economics', '109', '', 2015, '', 'PUBLICADO', 'No', 'margaret.skutsch^arturo.balderas', '', 130, 141, 'doi:10.1016/j.ecolecon.2014.11.008'],
    ['Carbon measurement: an overview of carbon estimation methods and the role of GIS and remote sensing techniques for REDD+ implementation', 'Journal of Forests and Livelihoods', '13', '', 2015, '', 'PUBLICADO', 'No', 'margaret.skutsch', '', 1, 15, ''],
    ['Moving from MRV to community MMM: a case in Mexico', 'Plos One', '0000000', '', 2015, '', 'EN_PRENSA', 'No', 'margaret.skutsch', '', 0, 0, ''],
    ['Identification and quantification of drivers of forest degradation in tropical dry forests: a case study in Western Mexico', 'Land Use Policy', '69', '', 2015, '0264-8377', 'PUBLICADO', 'No', 'margaret.skutsch^l.morales.barquero^armonia.borrego^john.healey', '', 296, 309, 'doi:10.1016/j.landusepol.2015.07.006'],
    ['The Place of Community Forest Management in the REDD+ Landscape', 'Forests', '7', '170', 2016, '', 'PUBLICADO', 'No', 'margaret.skutsch', '', 0, 0, 'doi:10.3390/f7080170'],
    ['Distribución de bacterias patógenas en el agua para consumo humano en una cuenca rural y sus afectaciones potenciales en la saludo pública', 'Ciencia Nicolaita', '', '66', 2015, '2007-7068', 'PUBLICADO', 'Si', 'maria.carmona^yesenia.rodriguez^ruben.hernandez', '', 25, 40, 'http://www.cic.cn.umich.mx/index.php/cn/issue/view/14'],
    ['Regional climate on the breeding grounds predicts variation in the natal origin of monarch butterflies overwintering in Mexico over 38 years', 'Global Change Biology', '', '', 1900, '1365-2486', 'ACEPTADO', 'No', 'maria.ramirez^tyler.flockhart^lincoln.brwoer^keith.hobson^leonard.wassenaar^sonia.altizer^ryan.morris', 'Web of Science: SCI/SSCI/SCI-EX', 0, 0, ''],
    ['The importance of the traditional fire knowledge system in a subtropical montane socio-ecosystem in a protected natural area', 'International Journal of Wildland Fire', '25', '9', 2016, '1049-8001', 'PUBLICADO', 'No', 'maria.ramirez^leonardo.martinez^alicia.castillo^diego.perez', 'Web of Science: SCI/SSCI/SCI-EX; Scopus', 911, 921, 'http://dx.doi.org/10.1071/WF15181'],
    ['Illegal Logging of 10 Hectares of Forest in the Sierra Chincua Monarch Butterfly Overwintering Area in Mexico', 'American Entomologist', '62', '2', 2016, '1046-2821', 'PUBLICADO', 'No', 'maria.ramirez^lincoln.brwoer^daniel.slayback^pablo.jaramillo^karen.oberhauser^ernest.williams^linda.fink', 'Web of Science: SCI/SSCI/SCI-EX', 92, 97, 'http://dx.doi.org/10.1093/ae/tmw040 '],
    ['Ethnoagroforestry: Integration of biocultural diversity for food sovereignty in México', 'Journal of Ethnobiology and Ethnomedicine', '12', '54', 2016, '', 'PUBLICADO', 'No', 'mariana.vallejo^ana.moreno^alejandro.casas^alexis.rivero^yessica.romero^selene.rangel^roberto.fisher^fernando.alvarado^didac.santos', '', 1, 21, '10.1186/s13002-016-0127-6'],
    ['TEK and biodiversity management in agroforestry systems of different socio-ecological contexts of the Tehuacán Valley', 'Journal of Ethnobiology and Ethnomedicine', '', '', 2016, '1746-4269', 'ACEPTADO', 'No', 'mariana.vallejo^ana.moreno^alejandro.casas', '', 0, 0, '10.1186/s13002-016-0102-2'],
    ['Agroforestry systems in the highlands of the Tehuacán Valley, Mexico: indigenous cultures and biodiversity conservation', 'Agroforestry Systems', '88', '', 2014, '', 'PUBLICADO', 'No', 'mariana.vallejo^ana.moreno^alejandro.casas^selene.rangel', '', 125, 140, 'DOI 10.1007/s10457-013-9660-7'],
    ['Agroforestry systems of the lowland alluvial valleys of the Tehuacan-Cuicatlan biosphere reserve: an evaluation of their biocultural capacity', 'Journal of Ethnobiology and Ethnomedicine', '11', '8', 2015, '1746-4269', 'PUBLICADO', 'Si', 'mariana.vallejo^alejandro.casas^ana.moreno', '', 1, 18, 'DOI:10.1186/1746-4269-11-8 '],
    ['Plant management in agroforestry systems of rosetophyllous forests in the Tehuacán Valley, Mexico', 'Economic Botany', '', '', 2016, '0013-0001', 'ACEPTADO', 'No', 'mariana.vallejo^nadia.campos^alejandro.casas^ana.moreno', '', 0, 0, 'DOI:10.1007/s12231-016-9352-0'],
    ['Ixcatec ethnoecology: plant management and biocultural heritage in Oaxaca, Mexico', 'Journal of Ethnobiology and Ethnomedicine', '12', '30', 2016, '', 'PUBLICADO', 'No', 'mariana.vallejo^selene.rangel^alejandro.casas', '', 0, 83, '10.1186/s13002-016-0101-3'],
    ['Fundamentos agronómicos para reformar la ley de desarrollo rural integral sustentable en el estado de Michoacán de Ocampo, México', 'CECTI Michoacán', '', '', 2016, '', 'PUBLICADO', 'No', 'mario.figueroa', '', 1706, 1713, ''],
    ['Estudio del metabolismo social del aguacate en Michoacán, México. Una aproximación agroecológica encaminada al entendimiento y recuperación de sistemas de cultivo tradicionales', 'Sociedad Española de Agricultura Ecológica (SEAE)', '', '', 2016, '', 'PUBLICADO', 'No', 'mario.figueroa^zirion.martinez^marta.astier', '', 1, 6, ''],
    ['Análisis comparativo de lixiviados obtenidos de tiraderos abieirtos y rastrojo de maíz utilizados como fertilizantes en la microcuenta Morelia-Tarimbaro, Michoacán, México', 'CECTI Michoacán', '.', '', 2015, '', 'PUBLICADO', 'No', 'mario.figueroa^guillermo.figueroa^diego.torres^jose.plancarte', '', 21, 5, ''],
    ['Introducción: el MESMIS en Brasil y en el mundo', 'Revista Cartográfica', '', '', 2016, '1729-7419', 'ENVIADO', 'No', 'marta.astier^carlos.gonzalez^omar.masera', '', 0, 0, ''],
    ['Historia de la agroecología en México', 'Revista de Agroecología', '10', '2', 2015, '1989-4686', 'PUBLICADO', 'No', 'marta.astier^pablo.argueta^quetzalcoatl.orozco^peter.gerritsen^miguel.escalona^julio.sanchez^cristobal.sanchez^rene.arzuffi^federico.castrejon^lorena.soto^jaime.morales^peter.rosset^teresa.ramirez^ramon.jarquin^carlos.gonzalez', '', 9, 18, ''],
    ['Participatory evaluation of food and nutritional security through sustainability indicators in a highland peasant system in Guatemala', 'Journal of Rural Studies', '', '', 2016, '0743-0167', 'ENVIADO', 'No', 'marta.astier', '', 0, 0, ''],
    ['Socio-economic and environmental changes related to maize richness in Mexico\'s central highlands', 'Agriculture and Human Values', '', '', 2016, '1572-8366', 'PUBLICADO', 'Si', 'marta.astier^quetzalcoatl.orozco', '', 0, 0, '10.1007/s10460-016-9720-5'],
    ['La distribución de la diversidad de maíces en la región de Pátzcuaro y sus asociación con factores ambientales y sociales', 'Agrociencia', '', '', 2016, '1405-3195', 'ENVIADO', 'No', 'marta.astier^quetzalcoatl.orozco', '', 0, 0, ''],
    ['Changes in climate, crops, and tradition: Cajete maize and the rainfed farming systems of Oaxaca, Mexico', 'Human Ecology', '46', '5', 2015, '0300-7839', 'PUBLICADO', 'No', 'marta.astier^paul.roge', '', 639, 653, '10.1007/s10745-015-9780-y'],
    ['Promoting local sustainable development and mitigating climate change in indigenous communities of México', 'Climatic Change', '', '', 2015, '1573-1480', 'PUBLICADO', 'No', 'marta.astier^ayesa.martinez^omar.masera', '', 1, 15, '10.?1007/?s10584-015-1523-y'],
    ['Ecosystem service trade-offs, perceived drivers and sustainability in contrasting agroecosystems in Central Mexico', 'Ecology and Society', '20', '1', 2015, '1708-3087', 'PUBLICADO', 'No', 'marta.astier^carlos.gonzalez^mayra.gavito^martin.cardena^ek.del.val^laura.villamil^yair.merlin^patricia.balvanera', '', 38, 52, 'http://dx.doi.org/10.5751/ES-06875-200138 '],
    ['Resiliencia, vulnerabilidad y sustentabilidad de sistemas socioecológicos en México', 'Revista Mexicana de Biodiversidad', '', '', 2016, '1870-3453', 'ACEPTADO', 'No', 'marta.astier^patricia.balvanera^francisco.gurri^isela.zarmeno', '', 1, 3, ''],
    ['Management practices and plant and flower visitor biodiversity in conventional and organic avocado orchards of Michoacán, México', 'Agroecology and Sustainable Food Systems', '', '', 2016, '2168-3565', 'ENVIADO', 'No', 'marta.astier^laura.villamil^yair.merlin^mayra.gavito', '', 0, 0, ''],
    ['Back to the roots: understanding current agroecological movement, science and practice in Mexico', 'Agroecology and Sustainable Food Systems', '', '', 2016, '2168-3573', 'ENVIADO', 'No', 'marta.astier^quetzalcoatl.orozco^peter.gerritsen^miguel.escalona^julio.sanchez^rene.arzuffi^federico.castrejon^ruben.hernandez^lorena.soto^peter.rosset^carlos.gonzalez^mirna.ambrosio', '', 0, 0, ''],
    ['Quantifying the Mexican forest carbon sink', 'Environmental Research Letters', '', '', 2016, '1748-9326', 'ENVIADO', 'Si', 'jaime.paneque^margaret.skutsch^adrian.ghilardi^arturo.balderas', '', 0, 0, ''],
    ['La estación ecológica de Majana: Su vegetación y flora', 'Fontqueria', '', '39', 1994, '0212-0623', 'PUBLICADO', 'No', 'n.aguila.carrasco^l.menéndez.carrera^ricardo.napoles^angel.priego', 'Latindex; Otros índices', 251, 261, ''],
    ['El paisaje en su connotación ritual. Un caso en la Huasteca Potosina, México', 'Geotrópico', '', '2', 2010, '1692-0791', 'PUBLICADO', 'Si', 'pedro.urquijo', 'Latindex', 1, 1, ''],
    ['Religión y naturaleza en la construcción de la identidad de los teenek potosinos', 'Espacio y tiempo, Revista latinoamericana de Ciencias Sociales y humanidades', '', '1', 2008, '', 'PUBLICADO', 'No', 'pedro.urquijo', '', 19, 30, ''],
    ['Los estudios de paisaje y su importancia en México, 1970-2010', 'Journal of Latin American Geography', '10', '2', 2011, '1545-2476', 'PUBLICADO', 'No', 'pedro.urquijo^gerardo.bocco', '', 37, 63, ''],
    ['Los espacios del pueblo de indios tras el proceso de congregación, 1550-1625', 'Investigaciones Geográficas, Boletín del Instituto de Geografía', '', '60', 2006, '', 'PUBLICADO', 'No', 'pedro.urquijo', 'Otros índices; Scopus; Revistas CONACYT', 145, 158, ''],
    ['Historia y paisaje : Explorando un concepto geográfico monista', 'Andamios, Revista de Investigación Social', '5', '10', 2009, '1870-0063', 'PUBLICADO', 'No', 'pedro.urquijo', 'Otros índices; Web of Science: SCI/SSCI/SCI-EX; Revistas CONACYT', 227, 252, ''],
    ['Geografía ambiental : Reflexiones teóricas y práctica institucional', 'Región y Sociedad', '25', '44', 2013, '1405-9274', 'PUBLICADO', 'No', 'pedro.urquijo^gerardo.bocco', 'Revistas CONACYT; Clase; RedALyC; Latindex; Otros índices', 75, 101, ''],
    ['Construcción social del paisaje en comunidades de pescadores artesanales. El caso de la Península de Valdés, Provincia de Chubut, Argentina', 'Biblio 3W. Revista bibliográfica de Geografía y Ciencias Sociales', '18', '1012', 2013, '1138-9796', 'PUBLICADO', 'Si', 'pedro.urquijo^gerardo.bocco', 'Otros índices', 1, 1, ''],
    ['Corporación minera, colusión gubernamental y deposeción campesina. El caso de Goldcorp Inc en Mazapil , Zacatecas', 'Desacatos, Revista de Antropología Social', '', '44', 2014, '1405-9274', 'PUBLICADO', 'No', 'pedro.urquijo^claudio.garibay^andrew.boni', 'Revistas CONACYT; RedALyC; SciELO; Latindex', 113, 142, ''],
    ['Unequal Partners, Unequal Exchange: Goldcorp, the Mexican State and Campesino Dispossession at the Peñasquito goldmine', 'Journal of Latin American Geography', '10', '2', 2011, '1545-2476', 'PUBLICADO', 'No', 'pedro.urquijo^claudio.garibay^andrew.boni', '', 153, 176, ''],
    ['Geographical distribution and diversity of maize (Zea mays L. subsp. mays) races in Mexico', 'Genetic Resources and Crop Evolution', '', '', 2016, '', 'PUBLICADO', 'No', 'quetzalcoatl.orozco^hugo.perales^robert.hijmans', '', 0, 0, 'doi:10.1007/s10722-016-0405-0'],
    ['Maize diversity associated with social origin and environmental variation in Southern Mexico', 'Heredity', '116', '', 2016, '0018-067X', 'PUBLICADO', 'No', 'quetzalcoatl.orozco^jeffrey.ross^amalio.santacruz^stephen.brush', '', 477, 484, '10.1038/hdy.2016.10'],
    ['Diversidad de maíces en Pátzcuaro, Michoacán, México y su relación con factores ambientales y sociales', 'Agrociencia', '', '', 2016, '', 'ENVIADO', 'No', 'quetzalcoatl.orozco^marta.astier', '', 0, 0, ''],
    ['Patterns of distribution along environmental gradients of nine Quercus species in central Mexico', 'Botanical Sciences', '94', '3', 2016, '2007-4476', 'PUBLICADO', 'No', 'r.aguilar.romero^f.garcía.oliva^f.pineda.garcia^i.torres.garcia^f.pena.vega^adrian.ghilardi^ken.oyama', 'Web of Science: SCI/SSCI/SCI-EX', 471, 482, '10.17129/botsci.620'],
    ['Correlación entre los elementos potencialmente tóxicos y propiedades magnéticas en suelos de la Ciudad de México para la determinación de sitios contaminados: definición de umbrales magnéticos', 'Revista Mexicana de Ciencias Geológicas', '32', '', 2015, '', 'PUBLICADO', 'Si', 'raul.cejudo^francisco.bautista^o.delgado.carranza^avto.gogichaishvili^j.morales.contreras', '', 50, 61, ''],
    ['De montaña, milpa y cañaveral. Transformaciones percibidas de los paisajes en la costa de Chiapas', 'Investigaciones Geográficas, Boletín del Instituto de Geografía', '', '', 2016, '0188-4611', 'ACEPTADO', 'No', 'sara.barrasa', 'Otros índices', 0, 30, ''],
    ['Percepción del cambio climático en comunidades campesinas de la Reserva de la Biosfera La Encrucijada, Chiapas, México', 'Cuadernos de Geografía', '', '', 2016, '0210-5462', 'ENVIADO', 'No', 'sara.barrasa', 'Web of Science: SCI/SSCI/SCI-EX; Scopus; RedALyC', 1, 24, ''],
    ['Métodos para la evaluación visual del paisaje: entre la estética y la ecología', 'Agrociencia', '', '', 2015, '1405-3195', 'ENVIADO', 'No', 'sara.barrasa^cruz.lopez^alejandro.collantes^eduardo.alanis', '', 0, 15, ''],
    ['Paisaje urbano a orillas de la Laguna de Bacalar (Quintana Roo, México): ocupación del suelo y producción del imaginario por el turismo', 'Cuadernos de Geografía', '', '', 2016, '0121-215X', 'PUBLICADO', 'No', 'sara.barrasa^enrique.gomez^ana.garcia', 'RedALyC; Latindex; SciELO', 1, 25, ''],
    ['A thematic transition in STS studies?', 'Revue Anthropologie des Connaissances', '', '4', 2016, '1760-5393', 'EN_PRENSA', 'No', 'saray.bucio^hebe.vessuri', '', 0, 0, ''],
    ['La comunicación científica en contextos de complejidad: el acceso abierto', 'LANIA Newsletter', '17', '57/58', 2016, '', 'PUBLICADO', 'Si', 'saray.bucio^hebe.vessuri', '', 0, 0, ''],
    ['La evolución del campo de los estudios sociales de la ciencia y la tecnología en Venezuela: notas de memoria', 'Espacio Abierto', '25', '4', 2016, '1315-0006', 'EN_PRENSA', 'No', 'saray.bucio^hebe.vessuri', 'Web of Science: SCI/SSCI/SCI-EX; SciELO', 0, 0, ''],
    ['The science and policy of REDD+ in a sink: Case of Mexico', 'Environmental Science && Policy', '', '', 2016, '1462-9011', 'ENVIADO', 'No', 'margaret.skutsch^jaime.paneque^adrian.ghilardi^jorge.morfin^josemaria.michel^oswaldo.carrillo', '', 0, 0, ''],
    ['How social capital enables/restricts the livelihoods of poor peri-urban farmers in Mexico', 'Development in Practice', '', '', 2016, '0961-4524', 'ACEPTADO', 'No', 'yadira.mendez^antonio.vieyra', '', 0, 0, ''],
    ['Periurbanization, agricultural livelihoods and ejidatarios´ social capital: Lessons from a periphery municipality in Michoacán, Mexico', 'Procedia Engineering', '', '', 2016, '1877-7058', 'ENVIADO', 'No', 'yadira.mendez^antonio.vieyra^lorena.poncela', 'Scopus', 0, 0, ''],
    ['IVAKY: Índice de la vulnerabilidad del acuífero kárstico yucateco a la contaminación', 'Revista Mexicana de Ingeniería Química', '15', '3', 2016, '2395-8472', 'PUBLICADO', 'No', 'yameli.aguilar^francisco.bautista^manuel.mendoza^oscar.frausto^thomas.j.ihl^o.delgado.carranza', 'Web of Science: SCI/SSCI/SCI-EX', 913, 930, 'http://rmiq.org/iqfvp/Pdfs/Vol.%2015,%20No.%203/IA1/RMIQTemplate.pdf'],
    ['Abundance and hábitat use of the lizard Sceloporus utiformis (Squamata: Phrynosomatidae) during seasonal transitional in a tropical environment', 'Revista Mexicana de Biodiversidad', '87', '4', 2016, '', 'PUBLICADO', 'No', 'yan.gao', 'RedALyC; Latindex; Otros índices', 1301, 1307, 'http://dx.doi.org/10.1016/j.rmb.2016.10.011']
)

for i in articulos:
    if i[2] == '':
        i[2] = 0
    if i[3] == '':
        i[3] = 0

    if i[7] == 'Si':
        i[7]=True
    else:
        i[7]=False

    if i[9] == '':
        i[9] = None


    if i[12] == '':
        i[12] = None

    a = ArticuloCientifico(titulo=i[0], tipo='ARTICULO', revista=Revista.objects.get(nombre=i[1]), volumen=i[2], numero=i[3], fecha=datetime(i[4], 1, 1), issn_impreso=i[5], status=i[6], solo_electronico=i[7], pagina_inicio=i[10], pagina_fin=i[11], id_doi=i[12])
    a.save()
    print("Agregado", a)

    for j in i[8].split('^'):
        print("       ", j)
        a.usuarios.add(User.objects.get(username=j))

    if i[9]:
        for j in i[9].split('; '):
            print("       ", j)
            a.indices.add(Indice.objects.get(nombre=j))


libros_inv = (
    ['Dimensiones Sociales en el Manejo de Cuencas', 'Morelia', 'CIGA-UNAM', 'PUBLICADO', 2015, 1, 320, '978-607-02-6883-0', '', 'ana.burgos^gerardo.bocco^joaquin.sosa'],
    ['Morelia y sus ríos. Relaciones entre los procesos históricos, biofísicos y sociales en el contexto urbano', 'Morelia', 'CIGA-UNAM', 'ACEPTADO', 2017, 1, 1, '', '', 'frida.guiza^manuel.mendoza^pedro.urquijo'],
    ['Tres niveles de análisis en la Sierra-Costa michoacana (insumos para el ordenamiento ecológico)', 'Morelia', 'CIGA-UNAM', 'PUBLICADO', 2015, 1, 223, '978-607-02-6530-3', 'http://www.ciga.unam.mx/publicaciones/', 'gerardo.bocco^angel.priego'],
    ['Conocimiento, paisaje, territorio. Procesos de cambio individual y colectivo', 'Comodoro Rivadavia', 'UNPA', 'PUBLICADO', 2015, 1, 400, '978-987-3714-06-1', '', 'hebe.vessuri^gerardo.bocco'],
    ['XIX Reunión Nacional SELPER México. Memorias', 'Morelia', 'CIGA-UNAM', 'PUBLICADO', 2012, 1, 420, '978-607-02-3172-8', 'http://www.ciga.unam.mx/publicaciones/', 'gabriela.cuevas^jean.mas'],
    ['La regionalización físico-geográfica del estado de Guerrero, México', 'Morelia', 'CIGA-UNAM', 'PUBLICADO', 2015, 1, 157, '978-607-02-6706-2', 'http://www.ciga.unam.mx/publicaciones/images/abook_file/9786070267062.pdf', 'angel.priego^manuel.bollo^angel.priego^alberto.ortiz'],
    ['Una propuesta de regionalización físico-geográfica de México', 'Morelia', 'CIGA-UNAM', 'PUBLICADO', 2015, 1, 59, '978-607-02-6527-3', 'http://www.ciga.unam.mx/publicaciones/images/abook_file/PropuestadelaRFGdeMexico.pdf', 'angel.priego^manuel.bollo^ramon.hernandez^rigel.zaragoza'],
    ['Propuesta para la generación de unidades de paisajes de manera semi-automatizada. Fundamentos y método', 'Ciudad de México, CDMX', 'CIGA-UNAM', 'PUBLICADO', 2010, 1, 104, '978-968-817-923-9', 'http://www2.inecc.gob.mx/publicaciones/descarga.html?cv_pub=633&tipo_file=pdf&filename=633', 'angel.priego^gerardo.bocco^manuel.mendoza'],
    ['La cartografía de sistemas naturales como base geográfica para la planeación territorial. Una revisión de la bibliografía', 'Ciudad de México, CDMX', 'CIGA-UNAM', 'PUBLICADO', 2010, 1, 72, '978-968-817-920-8', 'http://www.ciga.unam.mx/publicaciones/index.php?option=com_abook&view=book&catid=12%3Acoleccionesciga&id=15&Itemid=16', 'angel.priego^gerardo.bocco^manuel.mendoza^ana.burgos'],
    ['30 Años en el Paisaje Costero Veracruzano: Central Nucleoeléctrica Laguna Verde', 'Xalapa', 'INECOL', 'PUBLICADO', 2008, 1, 239, '970-709-106-1', '', 'angel.priego^p.moreno.casasola^e.vera.isunza'],
    ['Procesos Urbanos, Pobreza y Ambiente. Experiencias en Megaciudades y Ciudades Medias', 'Morelia', 'CIGA-UNAM', 'PUBLICADO', 2016, 1, 179, '978-607-02-8098-6', '', 'yadira.mendez^antonio.vieyra^alejandra.larrazabal'],
    ['Consejos a los jóvenes con vocación científica o de cómo perderle el miedo al estudio de las ciencias', 'Ciudad de México, CDMX', 'Skiu', 'PUBLICADO', 2015, 2, 227, '978-607-96883-0-1', '', 'francisco.bautista'],
    ['La evaluación automatizada de las funciones ambientales del suelo con base en datos de perfiles', 'Morelia', 'CIGA-UNAM', 'PUBLICADO', 2015, 1, 109, '978-607-02-6600-3', '', 'francisco.bautista'],
    ['Atlas de Solos da América Latina e Caribe', 'Morelia', 'FAO', 'PUBLICADO', 2015, 1, 1, '', '', 'francisco.bautista'],
    ['Soil Atlas of Latin America and Caribbean', 'Ciudad de México, CDMX', 'Lovell-Johns', 'PUBLICADO', 2015, 1, 1, '978-92-79-25599-1', '', 'francisco.bautista'],
    ['La Región como categoría geográfica', 'Morelia', 'Morevalladolid', 'PUBLICADO', 2016, 2, 108, '978-607-02-7872-3. ', 'http://www.ciga.unam.mx/publicaciones/', 'manuel.bollo'],
    ['Humboldt y el Jorullo. Historia de una exploración', 'Morelia', 'CIDEM', 'PUBLICADO', 2008, 1, 103, '978-703-475-0', '', 'pedro.urquijo'],
    ['Proyectos de educación en México. Perspectivas históricas', 'Morelia', 'ENES Unidad Morelia', 'PUBLICADO', 2014, 1, 494, '978-607-02-6251-7', '', 'pedro.urquijo'],
    ['Estudio costero del suroccidente de México', 'Morelia', 'CIGA-UNAM', 'PUBLICADO', 2013, 1, 264, '978-607-02-4149-9', '', 'donald.brand'],
    ['Corografía y escala local. Enfoques desde la geografía humana. ', 'Morelia', 'CIGA-UNAM', 'PUBLICADO', 2012, 1, 116, '978-607-02-3152-0', 'http://www.ciga.unam.mx/publicaciones/', 'pedro.urquijo'],
    ['Cocula contra Coatepec de los Costales: un conflicto territorial, 1802-1804. Archivo Dr. Fructuoso Martínez Román', 'Morelia', 'CIGA-UNAM', 'PUBLICADO', 2011, 1, 30, '978-607-02-2497-3', 'http://www.ciga.unam.mx/publicaciones/', 'claudio.garibay^pedro.urquijo'],
    ['Geografía y ambiente en América Latina', 'Morelia', 'CIGA-UNAM', 'PUBLICADO', 2011, 1, 355, '978-607-02-2496-6', 'http://www2.ine.gob.mx/publicaciones/index.html', 'gerardo.bocco^pedro.urquijo^antonio.vieyra'],
    ['Temas de geografía latinoamericana', 'Morelia', 'CIGA-UNAM', 'PUBLICADO', 2009, 1, 443, '978-968-9529-12-5', '', 'pedro.urquijo'],
    ['Science for Sustainable Development (Agenda 2030', 'París', 'UNESCO', 'PUBLICADO', 2016, 1, 16, '', 'http://creative commons/licenses/by-sa/3.0/igo/', 'hebe.vessuri'],
    ['Etonoagroforestería en México', 'Morelia', 'ENES Unidad Morelia', 'PUBLICADO', 2015, 1, 432, '978-607-02-8164-8', '', 'mariana.vallejo^ana.moreno^alejandro.casas^victor.toledo'],
    ['Standardized Hierarchical, Vegetation, Classification, Mexican and Global Patterns', 'Ciudad de México, CDMX', 'Springer', 'PUBLICADO', 2016, 1, 143, '978-3-319-41221-4', 'https://scholar.google.es/scholar?q=Standardized+Hierarchical+Vegetation+Classification+Mexican+and+Global+Patterns&&&&btnG=&&&&hl=es&&&&as_sdt=0%2C5&&&&as_vis=1', 'alejandro.velazquez^consuelo.medina^elvira.duran^alfredo.amador'],
    ['La memoria de los nombres: la toponimia en la conformación histórica del territorio. De Mesoamerica a México', 'Morelia', 'CIGA-UNAM', 'EN_PRENSA', 2015, 1, 475, '', '', 'karine.lefebvre^carlos.paredes'],
    ['The global social science world - Under and beyond Western universalism', 'Morelia', 'Ibidem Sociedad Editorial De Formacion Juridica Y Economica S. L.', 'PUBLICADO', 2016, 1, 278, '978-3-8382-0893-0', '', 'hebe.vessuri^michael.kuhn^hebe.vessuri^kwang.yeong^huri.islamoglu^doris.weidermann^mauricio.nieto^reinerg.grundmann^sujata.patel^igor.yegorov^pal.tamas^kumaran.rajagopal^kazumi.okamoto'],
    ['Some Contributions to Alternative Concepts of Knowledge', 'Morelia', 'Ibidem Sociedad Editorial De Formacion Juridica Y Economica S. L.', 'PUBLICADO', 2016, 1, 272, '978-3-8382-0894-7', '', 'hebe.vessuri^michael.kuhn^juan.vazquez^pablo.reyna^leon.nkolo^christiane.hartnack^roger.magazine^claudia.magallanes^leandro.rodriguez^ivan.costa^michel.christie^kumaran.rajagopal^quodratullah.qorbani'],
    ['Conocimiento, Paisaje y Territorio. Procesos de cambio individual y colectivo', 'Buenos Aires', 'UNPA', 'PUBLICADO', 2016, 1, 400, '978-987-3714-0', '', 'dalma.albarracin^gabriela.alvarez^fabiana.bekerman^gerardo.bocco^ana.cinti^leticia.curti^cristina.flores^rosana.guber^sergio.kaminker^carolina.laztra^javier.serrano^marcos.sourrouille^damian.taire^pedro.urquijo^hebe.vessuri'],
    ['La Otra, El Mismo. Mujeres en la ciencia y la tecnología en Venezuela', 'Caracas', 'Fundación Escuela Editorial El perro y la rana', 'EN_PRENSA', 2016, 1, 1, '', '', 'hebe.vessuri^victoria.canino^rosa.bolivar^ana.castellanos^alejandra.aray'],
    ['Procesos Urbanos, Pobreza y Ambiente. Implicaciones en Ciudades Medias y Megaciudades', 'Morelia', 'CIGA-UNAM', 'PUBLICADO', 2016, 1, 1, '978-607-02-8100-6 ', '', 'yadira.mendez^antonio.vieyra^alejandra.larrazabal'],
    ['Procesos periurbanos: Desequilibrios territoriales, desigualdades sociales, ambientales y pobreza', 'Morelia', 'CIGA-UNAM', 'EN_PRENSA', 2016, 1, 1, '', '', 'yadira.mendez^antonio.vieyra^alejandra.larrazabal'],
)

for i in libros_inv:
    if i[8] == '':
        i[8] = None
    if i[7] == '':
        i[7] = None

    l = Libro(nombre=i[0], tipo='INVESTIGACION',
              pais=Pais.objects.get(nombre=Ciudad.objects.get(nombre=i[1]).estado.pais),
              estado=Estado.objects.get(nombre=Ciudad.objects.get(nombre=i[1]).estado),
              ciudad=Ciudad.objects.get(nombre=Ciudad.objects.get(nombre=i[1])),
              editorial=Editorial.objects.get(nombre=Editorial.objects.get(nombre=i[2])),
              status=i[3],
              fecha=datetime(i[4], 1, 1),
              numero_edicion=i[5],
              numero_paginas=i[6],
              isbn=i[7],
              url=i[8],
              )
    l.save()
    print(l)

    for j in i[9].split('^'):
        print("       ", j)
        l.usuarios.add(User.objects.get(username=j))


libros_cap = (
    ['Geopedology. An integration of Geomorphology and Pedology for Soil and Landscape Studies', 'Nueva York', 'Springer', 'PUBLICADO', 2015, 1, 556, '978-3-319-19158-4', 'http://www.doi.org/10.1007/978-3-319-19159-1', 'gerardo.bocco^alfred.zinck^hector.delvalle'],
    ['La biodiversidad en Michoacán. Estudio de Estado', 'Morelia', 'CONABIO', 'OTRO', 2005, 1, 1, '970-900-028-4', 'https://doi.org/10.5962/bhl.title.118635', 'oscar.leal^laura.villaseñor^manuel.mendoza^francisco.bautista'],
    ['Informality: Re-Viewing Latin American Cities', 'Cambridge', 'Department of Architecture, Cambridge', 'OTRO', 2011, 1, 4, '', 'http://www.crassh.cam.ac.uk/events/1324/', 'felipe.hernandez^brian.napoletano^antonio.vieyra^jaime.paneque'],
    ['70 años del Instituto de Geografía: Historia, actualidad y perspectiva', 'Ciudad de México, CDMX', 'UNAM', 'OTRO', 2015, 1, 1, '978-607-02-7321-6', 'http://www.publicaciones.igg.unam.mx/index.php/ig/catalog/book/75', 'admin'],
    ['Estudio Nacional sobre la Diversidad Biológica en la República de Cuba', 'La Habana', 'Centro Nacional de Biodiversidad del Instituto de Ecología y Sistemática', 'OTRO', 1998, 1, 429, '', 'ftp://169.158.189.34/pub/PROYECTOS/Cambio%20Climatico/libros/Estudio%20de%20Pais%20DB%201998.pdf', 'alberto.alvarez^angel.priego'],
    ['Atlas del Patrimonio Natural, Histórico y Cultural de Veracruz, Tomo I: Patrimonio Natural', 'Xalapa', 'UNAM', 'OTRO', 2010, 1, 1, '978-607-951-315-3', 'https://www.sev.gob.mx/', 'juan.ortiz^angel.priego'],
    ['Atzala de la Asunción, Guerrero Agua entre rocas', 'Ciudad de México, CDMX', 'UNAM', 'OTRO', 2000, 1, 1, '', '', 'admin'],
    ['Biodiversidad de la Sierra Madre del Sur', 'Ciudad de México, CDMX', 'UNAM', 'OTRO', 2000, 1, 1, '978-607-027906-5', '', 'isolda.lunavega^alejandro.velazquez'],
    ['Biogeografía de Sistemas Litorales. Dinámica y Conservación', 'Sevilla', 'Asociación de Geógrafos Españoles', 'OTRO', 2014, 1, 408, ' 978-84-617-1068-3',  'http://digibuo.uniovi.es/dspace/bitstream/10651/30573/1/Din%C3%A1mica_Bosques_Aramo.pdf', 'rafael.camaraartigas^angel.priego'],
    ['Ciencias Ambientales: Temáticas para el Desarrollo', 'Puebla de Zaragoza', 'BUAP', 'OTRO', 2004, 1, 1, '978-968-863-987-0', '', 'jesus.ruizcareaga^angel.priego'],
    ['Conflictos Ambientales en Latinoamérica', 'Buenos Aires', 'UNGS', 'OTRO', 2017, 1, 1, '', '', 'jaime.paneque^maria.ramirez^claudio.garibay^pedro.urquijo'],
    ['Conocimiento, ambiente y poder. Perspectivas desde la ecología política', 'San Luis Potosí', 'El Colegio de San Luis', 'OTRO', 2017, 1, 1, '', '', 'claudio.garibay'],
    #['Conocimiento, paisaje, territorio. Procesos de cambio individual y colectivo', 'Río Gallegos', 'UNPA', 'OTRO', 2015, 1, 1, '978-987-3714-06-1', 'http://www.ub.es/geocrit/b3w-1012.htm', 'gerardo.bocco^pedro.urquijo'],
    ['Continuidades y rupturas: una historia tensa de la ciencia en México', 'Morelia', 'UAEH', 'OTRO', 2010, 1, 1, '978-607-424-196-7', '', 'pedro.urquijo'],
    ['Contributions to Alternative Concepts of Knowledge', 'Stuttgart', 'Ibidem Sociedad Editorial De Formacion Juridica Y Economica S. L.', 'OTRO', 2016, 1, 1, '978-3-8382-0894-7', '', 'michael.kuhn^hebe.vessuri'],
    ['Convergencias teóricas y empíricas en el espacio-tiempo', 'Morelia', 'CIGA-UNAM', 'OTRO', 2010, 1, 1, '', '', 'sara.barrasa'],
    ['Corografía y escala local. Enfoques desde la geografía humana', 'Morelia', 'CIGA-UNAM', 'OTRO', 2012, 1, 1, '978-607-02-3152-0', 'http://www.ciga.unam.mx/publicaciones', 'pedro.urquijo^claudio.garibay^gerardo.bocco'],
    ['Cosmos. Enciclopedia de las ciencias y la tecnología en México. Geografía', 'Ciudad de México, CDMX', 'UAM', 'OTRO', 2011, 1, 1, '978-607-477-137-4', '', 'pedro.urquijo^gerardo.bocco'],
    ['Cubierta y Uso del Territorio. Conceptos, enfoques y métodos de análisis', 'Morelia', 'CIGA-UNAM', 'OTRO', 2010, 1, 1, '', '', 'maria.ramirez^brian.napoletano^frida.guiza'],
    ['Cultural Dynamics and Production Activities in Ancient Western Mexico', 'Oxford', 'BAR', 'OTRO', 2016, 1, 1, '', '', 'karine.lefebvre^jean.mas'],
    ['Desarrollo desde lo local y dinámicas territoriales', 'Ciudad de México, CDMX', 'Editorial Fontamara', 'OTRO', 2016, 1, 1, '978-607-736-265-4', '', 'ana.burgos^gerardo.bocco'],
    ['Diálogos en la diversidad. Investigaciones postdoctorales 2015', 'Morelia', 'UMSNH', 'OTRO', 2015, 1, 1, '', '', 'mario.figueroa^mauricio.perea^encarnacion.bobadilla^alberto.orozco^jesus.luna'],
    ['Diálogos sobre la relación entre arqueología, antropología, e historia', 'Zamora', 'El Colegio de Michoacán', 'OTRO', 2016, 1, 1, '', '', 'sara.barrasa'],
    #['Dimensiones Sociales en el Manejo de Cuencas', 'Morelia', 'UNAM', 'OTRO', 2015, 1, 1, '978-607-02-6883-0', '', 'ana.burgos^gerardo.bocco'],
    ['Ecosistema de Manglar en el Archipiélago Cubano', 'La Habana', 'Editorial Academia', 'OTRO', 2006, 1, 1, '959- 270-090-7', '', 'angel.priego'],
    ['El análisis geoespacial en los estudios urbanos', 'Morelia', 'SELPER', 'OTRO', 2015, 1, 1, '', '', 'frida.guiza^keith.mccall^jean.mas'],
    ['El ecosistema de manglar en América Latina y la cuenca del Caribe: Su manejo y conservación', 'Nueva York', 'Rossentiel School of Marine and Atmospheric Science', 'OTRO', 1994, 1, 1, '0-9642315-0-6', '', 'angel.priego'],
    ['El Manejo Integral de Cuencas en México', 'Ciudad de México, CDMX', 'INE-SEMARNAT', 'OTRO', 2007, 1, 1, '978-968-817-861-4', '', 'angel.priego'],
    ['Els Sòls de Catalunya: Conca Dellà (Pallars Jussà). Monografies tècniques', 'Barcelona', 'Institut Geològic de Catalunya', 'OTRO', 2011, 1, 1, '978-843-938-586-8', '', 'lourdes.gonzalez'],
    ['Energía, Ambiente y Sociedad', 'Morelia', 'UNAM', 'OTRO', 2016, 1, 1, '', '', 'omar.masera^marta.astier'],
    ['Entomología Mexicana', 'Xalapa', 'Sociedad Mexicana de Entomoogía', 'OTRO', 2009, 1, 1, '968-839-559-2', '', 'alejandro.velazquez^angel.priego'],
    ['Entre Pasados y Presentes II. Estudios contemporáneos en Ciencias Antropológicas', 'Buenos Aires', 'Vázquez Mazzini Editores', 'OTRO', 2009, 1, 1, '978-987-23545-1-0', '', 'alina.alvarez^jp.carbonelli^v.palamarczuk'],
    ['Entre Pasados y Presentes III. Estudios contemporáneos en Ciencias Antropológicas', 'Buenos Aires', 'Editorial Mnemosyne', 'OTRO', 2012, 1, 1, '978-987-1829-21-7', '', 'alina.alvarez'],
    ['Environmental Management of River Basin Ecosystems', 'Estocolmo', 'Springer', 'OTRO', 2015, 1, 1, '978-3-319-13425-3', '', 'yan.gao'],
    ['Estudio de los grupos insulares y zonas litorales del archipiélago cubano con fines turísticos', 'La Habana', 'Editorial Científico-Técnica', 'OTRO', 1990, 1, 1, '', '', 'angel.priego'],
)


for i in libros_cap:
    try:
        te = Editorial.objects.get(nombre=i[2])
        te = None
        pass
    except:
        e = Editorial(nombre=i[2], pais=Pais.objects.get(nombre=Ciudad.objects.get(nombre=i[1]).estado.pais),
                      estado=Estado.objects.get(nombre=Ciudad.objects.get(nombre=i[1]).estado),
                      ciudad=Ciudad.objects.get(nombre=i[1]))
        e.save()
        print(e)

for i in libros_cap:
    l = Libro(nombre=i[0], tipo='INVESTIGACION',
              pais=Pais.objects.get(nombre=Ciudad.objects.get(nombre=i[1]).estado.pais),
              estado=Estado.objects.get(nombre=Ciudad.objects.get(nombre=i[1]).estado),
              ciudad=Ciudad.objects.get(nombre=i[1]),
              editorial=Editorial.objects.get(nombre=Editorial.objects.get(nombre=i[2])),
              status=i[3],
              fecha=datetime(i[4], 1, 1),
              numero_edicion=i[5],
              numero_paginas=i[6],
              isbn=i[7],
              url=i[8],
              es_libro_completo=False)
    l.save()

    print(l)

    for j in i[9].split('^'):
        print("       ", j)
        l.usuarios.add(User.objects.get(username=j))


investigadores_unam = [
['Dra', 'marta.astier', 'mastier@ciga.unam.mx', '(443) 322-3876'],
['Dra', 'sara.barrasa', 'sbarrasa@ciga.unam.mx', '(443) 322-3846'],
['Dr', 'francisco.bautista', 'leptosol@ciga.unam.mx', '(443) 322-3869'],
['Dr', 'gerardo.bocco', 'gbocco@ciga.unam.mx', '(443) 322-3834'],
['Dra', 'ana.burgos', 'aburgos@ciga.unam.mx', '(443) 322-3833'],
['Dra', 'yan.gao', 'ygao@ciga.unam.mx', '(443) 322-2777'],
['Dr', 'claudio.garibay', 'claudio.garibay@gmail.com', '(443) 322-3864'],
['Dr', 'adrian.ghilardi', 'aghilardi@ciga.unam.mx', '(443) 322-3854'],
['Dra', 'karine.lefebvre', 'klefebvre@ciga.unam.mx', '(443) 322-3865'],
['Dr', 'jean.mas', 'jfmas@ciga.unam.mx', '(443) 322-3835'],
['Dr', 'keith.mccall', 'mccall@ciga.unam.mx', '(443) 322-3879'],
['Dra', 'yadira.mendez', 'ymendez@ciga.unam.mx', '(443) 322-2777'],
['Dr', 'manuel.mendoza', 'mmendoza@ciga.unam.mx', '(443) 322-3839'],
['Dr', 'brian.napoletano', 'brian@ciga.unam.mx', '(443) 322-2777'],
['Dr', 'jaime.paneque', 'jpanequegalvez@ciga.unam.mx', '(443) 322-2777'],
['Dr', 'angel.priego', 'apriego@ciga.unam.mx', '(443) 322-3874'],
['Dra', 'maria.ramirez', 'isabelrr@ciga.unam.mx', '(443) 322-3841'],
['Dra', 'cinthia.ruiz', 'cruiz@ciga.unam.mx', '(443) 322-3880'],
['Dra', 'margaret.skutsch', 'mskutsch@ciga.unam.mx', '(443) 322-3849'],
['Dr', 'pedro.urquijo', 'psurquijo@ciga.unam.mx', '(443) 322-2777'],
['Dr', 'alejandro.velazquez', 'alex@ciga.unam.mx', '(443) 322-3842'],
['Dr', 'antonio.vieyra', 'avieyra@ciga.unam.mx', '(443) 322-3844'],
]

investigadores_conacyt = [
['Dra', 'armonia.borrego', 'aborrego@ciga.unam.mx', '(443) 322-2777'],
['Dra', 'frida.guiza', 'fguiza@ciga.unam.mx', '(443) 322-2777'],
['Dra', 'berenice.solis', 'solis@ciga.unam.mx', '(443) 322-3880'],
]

investigadores_invitados = [
['Dra', 'beatriz.tejera', 'bdelatejera@ciga.unam.mx', '(443) 322-2777'],
['Dra', 'hebe.vessuri', 'hvessuri@gmail.com', '(443) 323-5651']
]



for i in investigadores_unam:
    a = User.objects.get(username=i[1])
    a.titulo = i[0]
    a.email = i[2]
    a.telefono = i[3]
    a.save()

for i in investigadores_unam:
    e = ExperienciaLaboral(institucion=Institucion.objects.get(nombre='Universidad Nacional Autónoma de México (UNAM)'),
                           dependencia=Dependencia.objects.get(
                               nombre='Centro de Investigaciones en Geografía Ambiental (CIGA)'),
                           cargo=Cargo.objects.get(nombre='Investigador UNAM'), fecha_inicio=date(2015, 1, 1),
                           usuario=User.objects.get(username=i[1]))
    e.save()
    print(i)
    print(e)


for i in investigadores_conacyt:
    a = User.objects.get(username=i[1])
    a.titulo = i[0]
    a.email = i[2]
    a.telefono = i[3]
    a.save()

for i in investigadores_conacyt:
    e = ExperienciaLaboral(institucion=Institucion.objects.get(nombre='Universidad Nacional Autónoma de México (UNAM)'),
                           dependencia=Dependencia.objects.get(
                               nombre='Centro de Investigaciones en Geografía Ambiental (CIGA)'),
                           cargo=Cargo.objects.get(nombre='Investigador CONACYT'), fecha_inicio=date(2015, 1, 1),
                           usuario=User.objects.get(username=i[1]))
    e.save()
    print(i)
    print(e)


for i in investigadores_invitados:
    a = User.objects.get(username=i[1])
    a.titulo = i[0]
    a.email = i[2]
    a.telefono = i[3]
    a.save()

for i in investigadores_invitados:
    e = ExperienciaLaboral(institucion=Institucion.objects.get(nombre='Universidad Nacional Autónoma de México (UNAM)'),
                           dependencia=Dependencia.objects.get(
                               nombre='Centro de Investigaciones en Geografía Ambiental (CIGA)'),
                           cargo=Cargo.objects.get(nombre='Investigador Invitado'), fecha_inicio=date(2015, 1, 1),
                           usuario=User.objects.get(username=i[1]))
    e.save()
    print(i)
    print(e)