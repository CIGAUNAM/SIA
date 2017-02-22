import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SIC.settings")

django.setup()

from datetime import datetime, date
from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.conf import settings

#from autoslug import AutoSlugField

from formacion_academica.models import CursoEspecializacion, Licenciatura, Maestria, Doctorado, PostDoctorado
from experiencia_laboral.models import *

import uuid


from nucleo.models import Tag, ZonaPais, Pais, Estado, Ciudad, Region, Ubicacion, Institucion, Dependencia, User, Revista, Indice
from investigacion.models import *


import pymysql
#conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='cigacurricula')
#cur = conn.cursor()
#cur.execute("SELECT curso, tipo, horas, mes_ini, anio_ini, mes_fin, anio_fin, area, instituciones, idu FROM fa_especializacion")
#cur.execute("SELECT DISTINCT area FROM `fa_especializacion` ORDER BY `fa_especializacion`.`area` ASC ")
#cur.execute("SELECT carrera, area, institucion, tesis, anio_ini, mes_ini, anio_fin, mes_fin, grado_fin, grado_ini, idu FROM fa_licenciatura")
#cur.execute("SELECT area, area_wos, institucion, tesis, anio_ini, mes_ini, anio_fin, mes_fin, grado_fin, grado_ini, idu FROM fa_maestria")
#cur.execute("SELECT DISTINCT area, area_wos FROM fa_maestria ORDER BY area")
#cur.execute("SELECT DISTINCT area, area_wos FROM fa_doctorado ORDER BY area")
#cur.execute("SELECT area, institucion, tesis, anio_ini, mes_ini, anio_fin, mes_fin, grado_fin, grado_ini, idu FROM fa_doctorado")
#cur.execute("SELECT institucion, anio_ini, mes_ini, anio_fin, mes_fin, idu FROM fa_posdoctorado")


#                     0            1          2          3         4         5         6        7         8        9       10
#cur.execute("SELECT nombre, definitividad, cargo_aca, cargo_adm, otro, institucion, anio_ini, mes_ini, anio_fin, mes_fin, idu FROM uk_experiencia")

#cur.execute("SELECT titulo, revista, becarios, electronica, autores_iimas, alumnos, indices, abreviado, anio, volumen, numeros, issn, pagina_i, pagina_f, doi, isiut from ir_articuloscientificos")
#meses = [0, 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

"""
for i in cur:
    l = "('"
    l += i[0]
    l += "', '"
    l += i[1]
    l += "', '"
    l += i[2]
    l += "', "
    l += i[3]
    l += ", "
    l += str(meses.index(i[4]))
    l += ", "
    l += i[5]
    l += ", "
    l += str(meses.index(i[6]))
    l += ", '"
    l += i[7]
    l += "', "
    l += str(meses.index(i[8]))
    l += ", '"
    l += i[9]
    l += "'"
    l += "),"
    print(l)


for i in cur:
    #print(row)
    l = "('"

    l += i[0]

    l += "', "

    if i[1] == '0000' or i[1] == 'N/A':
        l += '2000'
    else:
        l += i[1]

    l += ", '"

    l += i[2]

    l += "', '"
    l += i[3]


    l += "'),"
    print(l)
"""

"""
for i in cur:
    #print(row)
    l = "('"
    if i[0] == 'no':
        l += 'Ningúno'
    else:
        l += i[0]
    l += "', "

    if i[1] == 'Si':
        l += 'True'
    else:
        l += 'False'
    l += ", "
    if i[2] == 'no':
        l += 'False'
    else:
        l += "'" + i[2] + "'"
    l += ", "
    if i[3] == 'no':
        l += 'False'
    else:
        l += "'" + i[3] + "'"

    l += ", "

    if i[4] == 'no':
        l += 'False'
    else:
        l += "'" + i[4] + "'"

    l += ", '"
    l += i[5]
    l += "', "
    l += i[6]
    l += ", "
    l += str(meses.index(i[7]))
    l += ", "
    if i[9] == 'A la fecha':
        l += '0'
    else:
        l += i[8]
    l += ", "
    if i[9] == 'A la fecha':
        l += '0'
    else:
        l += str(meses.index(i[9]))
    l += ", '"
    l += i[10]
    l += "'),"
    print(l)
"""

#for i in cur:
#    print(i)
#cur.close()
#conn.close()


"""

Gestión integral del agua, seguridad hídrica y derecho del agua
Mitigación y adaptación al cambio climático
Resiliencia frente a desastres naturales y tecnológicos
Aprovechamiento y protección de ecosistemas y de la biodiversidad
Los océanos y su aprovechamiento
Alimentos y su producción
Ciudades y desarrollo urbano
Conectividad informática y desarrollo de las tecnologías de la información, la comunicación y las telecomunicaciones
Manufactura de alta tecnología
Consumo sustentable de energía
Desarrollo y aprovechamiento de energías renovables limpias
Conducta humana y prevención de adicciones
Enfermedades emergentes y de importancia nacional
Combate a la pobreza y seguridad alimentaria
Migraciones y asentamientos humanos
Seguridad ciudadana
Economía y gestión del conocimiento
Prevención de riesgos naturales


"""




articulos = (
('A detailed paleomagnetic and rock-magnetic investigation of the Matuyama-Brunhes geomagnetic reversal recorded in the tephra-paleosol sequence of Tlaxcala (Central Mexico)', 'Frontiers in Earth Science', 'Publicado', 'No', 'berenice.solis^ana.soler^avto.gogichaishvili^angel.carrancho^sergey.sedov^cecilia.caballero^beatriz.ortega^juan.morales^jaime.urrutia^francisco.bautista', '', 'Otros indices', '', '2015', '3', 'N/A', '2296-6463', '1', '24', 'http://dx.doi.org/10.3389/feart.2015.00011', ''),
('A shared perspective for PGIS and VGI.\t ', 'The Cartographic Journal', 'Publicado', 'No', 'keith.mccall^jeroen.verplanke^claudia.uberhuaga^giacomo.gambaldi^muki.haklay', '', '', 'Cartog', '2016', '53', 'N/A', '0008-7041', '0', '0', 'DOI:  10.1080/00087041.2016.1227552', ''),
('A thematic transition in STS studies?  ', 'Revue Anthropologie des Connaissances', 'En prensa', 'No', 'saray.bucio^hebe.vessuri', '', '', '', '2016', 'vol. X', '4', '1760-5393', '0', '0', '', ''),
('A. Brigitte Nellie Luisa Boehm Shchoendube (1938-2005) ', 'International Encyclopedia of Anthropology', 'En prensa', 'No', 'claudio.garibay^andrew.roth', '', '', '', '2016', 'N/A', 'N/A', '', '0', '1', '', ''),
('Absence of detectable transgenes in local landraces of maize in Oaxaca, Mexico (2003\x962004)', 'Proceedings of National Academy of Sciences of USA', 'Publicado', 'No', 'gabriela.cuevas^s.ortiz.garcia', '', '', '', '2015', '102', '35', '1091-6490', '12338', '12343', '10.1073/pnas.0503356102', ''),
('Abundance and hábitat use of the lizard Sceloporus utiformis (Squamata: Phrynosomatidae) during seasonal transitional in a tropical environment', 'Revista Mexicana de Biodiversidad', 'Publicado', 'No', 'yan.gao^andres.garcia', '', 'RedALyC; Latindex; Otros indices', '', '2016', '87', '4', '', '1301', '1307', 'http://dx.doi.org/10.1016/j.rmb.2016.10.011', ''),
('Acceso al suelo ejidal en la periferia urbana mexicana: Análisis desde el Capital Social', 'Economía, Sociedad y Territorio', 'Aceptado', 'No', 'antonio.vieyra^sandra.pola^yadira.mendez', 'sandra.pola', '', '', '2016', 'N/A', 'N/A', '', '0', '0', '', ''),
('Actualización del mapa de suelos de Yucatán utilizando un enfoque geomorfopedológico y WRB', 'Ecosistemas y Recursos Agropecuarios', 'Publicado', 'Si', 'francisco.bautista^oscar.frausto^thomas.j.ihl^yadira.mendez', '', '', 'Ecosistemas y Recursos Agropecuarios', '2015', '2', 'N/A', '', '303', '3015', '', ''),
('Agroforestry systems in the highlands of the Tehuacán Valley, Mexico: indigenous cultures and biodiversity conservation. ', 'Agroforestry Systems ', 'Publicado', 'No', 'mariana.vallejo^ana.moreno^alejandro.casas^selene.rangel', '', '', 'Agrofor. Syst.', '2014', '88', 'N/A', '', '125', '140', 'DOI 10.1007/s10457-013-9660-7', ''),
('Agroforestry systems of the lowland alluvial valleys of the Tehuacan-Cuicatlan biosphere reserve: an evaluation of their biocultural capacity. ', 'Journal of Ethnobiology and Ethnomedicine ', 'Publicado', 'Si', 'mariana.vallejo^alejandro.casas^ana.moreno', '', '', 'J Ethnobiol Ethnomed', '2015', '11', '8', '1746-4269.', '1', '18', 'DOI:10.1186/1746-4269-11-8 ', ''),
('An Accuracy Index with Positional and Thematic Fuzzy Bounds for Land-use/Land-cover Maps', 'Photogrammetric Engineering and Remote Sensing', 'Publicado', 'No', 'gabriela.cuevas^stephane.couturier^jean.mas', '', '', '', '2009', '75', '7', '0099-1112', '789', '805', '10.14358/PERS.75.7.789', ''),
('An exploratory analysis of land abandonment drivers in areas prone to desertification', 'CATENA', 'Publicado', 'No', 'manuel.mendoza', 'daniel.iura', '', '', '2015', '128', 'N/A', '0341-8162', '252', '261', 'http://dx.doi.org/10.1016/j.catena.2014.02.006', ''),
('An interdisciplinary approach to depict landscape change drivers: A case study of the Ticuiz agrarian community in Michoacan, Mexico. ', 'Applied Geography', 'Publicado', 'No', 'angel.priego^m.campos.sanchez^alejandro.velazquez^gerardo.bocco^margaret.skutsch^m.boada.junca', '', 'WOS: SCI/SSCI/SCI-EX; Scopus; Otros indices', '', '2012', 'N/A', '32', '0143-6228', '409', '419', '', ''),
('Análisis Comparativo De Lixiviados Obtenidos De Tiraderos Abiertos Y Rastrojo De Maíz Utilizados Como Fertilizantes En La Microcuenca Morelia-Tarímbaro, Michoacán, México', 'CECTI Michoacán', 'Publicado', 'No', 'mario.figueroa^maria.figueroa^guillermo.figueroa^diego.torres^jose.plancarte', 'maria.figueroa^guillermo.figueroa^diego.torres^jose.plancarte', '', '.', '2015', '.', 'N/A', '', '21', '5', '', ''),
('Análisis de la producción de carbón vegetal en la Cuenca del Lago de Cuitzeo, Michoacán, México: implicaciones para una producción sustentable', 'Investigación Ambiental ', 'Publicado', 'No', 'adrian.ghilardi^ken.oyama^omar.masera', '', '', '', '2014', '6', '2', '2007-4492', '127', '138', '', ''),
('Análisis espacial de susceptibilidad magnética en la zona metropolitana de la ciudad de Guadalajara', 'Latinmag Letters', 'Publicado', 'Si', 'francisco.bautista^raul.cejudo^avto.gogichaishvili^jaime.morales', '', '', 'Latinmag Letters', '2015', '3', 'N/A', '', '0', '0', '', ''),
('Análisis espacial del paisaje como base para muestreos dendrocronológicos: El caso de la reserva de la Biosfera de la Mariposa Monarca, México', 'Madera y Bosque', 'Publicado', 'No', 'manuel.mendoza^t.carlon.allende^diego.perez', 't.carlon.allende', '', '', '2015', '22', '2', '', '11', '22', '', ''),
('Análisis jerárquico de la intensidad de cambio de cobertutra/uso de suelo y deforestación (2000-2008) en la Reserva de la Biosfera Sierra de Manantlán, México', 'Investigaciones Geográficas', 'Publicado', 'No', 'jean.mas^m.farfan.gutierez^g.rodriguez.tapia', 'm.farfan.gutierez', 'Latindex; Revistas CONACYT', '', '2016', '88', 'N/A', '0188-4611', '75', '90', 'dx.doi.org/10.14350/rig.48600', ''),
('Análisis y modelación de los procesos de deforestación: un caso de estudio en la cuenca  del río Coyuquilla, Guerrero, México', 'Investigaciones Geográficas', 'Publicado', 'No', 'jean.mas^manuel.maass^laura.osorio', 'laura.osorio', 'Latindex', 'Investigaciones Geográficas', '2015', '88', 'N/A', '0188-4611', '75', '90', '10.14350/rig.44603', ''),
('Aplicación de los paisajes físico-geográficos en un sector de la cordillera Ibérica: La cuenca del río Martín (Aragón, España)', 'Revista de Ciencia y Tecnología de América', 'Publicado', 'No', 'angel.priego^ivan.franch^manuel.bollo^luis.cancer^f.bautista.zuniga', 'ivan.franch', '  WOS: SCI/SSCI/SCI-EX; Latindex; SciELO; Otros indices', 'Interciencia', '2015', '40', '6', '0378-1844', '381', '389', '', ''),
('Aplicación de los paisajes físico-geográficos en un sector de la Cordillera Ibérica: la Cuenca del río Martín (Aragón, España)', 'Interciencia', 'Publicado', 'Si', 'ivan.franch^angel.priego^manuel.bollo^luis.cancer^francisco.bautista', '', 'ISI Web of Knowledge', '', '2015', '40', '6', '0378-1844', '381', '389', '', ''),
('Application of the physico-geographic landscapes in a sector of the Iberian Mountain Range: The Martin River Basin (Aragon, Spain)', 'Interciencia', 'Publicado', 'No', 'francisco.bautista^ivan.franch^angel.priego^manuel.bollo^luis.cancer', '', '', 'Interciencia', '2015', '40', 'N/A', '', '381', '389', '', ''),
('Arquitectura y paisajes en la localidad arqueológica de Andalhuala (valle de Yocavil, Catamarca).', 'Revista del Museo de Antropología', 'Publicado', 'No', 'alina.alvarez', '', 'Latindex; SciELO; RedALyC', 'RMA', '2010', '3', 'n/a', '1852-060X^1852-4826', '33', '48', 'http://revistas.unc.edu.ar/index.php/antropologia', ''),
('Assessing Modifiable Areal Unit Problem (MAUP) Effects in the Analysis of Deforestaion Drivers Using Local Models', 'Proceedings of the 8th International Congress on Environmental Modelling and Software (iEMSs)', 'Publicado', 'Si', 'gabriela.cuevas^jean.mas^azucena.perez^a.andablo.reyes^miguel.castillo^a.flamenco.sandoval', '', '', '', '2016', 'N/A', 'N/A', '', '1313', '1318', '', ''),
('Back to the roots: understanding current agroecological movement, science and practice in Mexico', 'Agroecology and sustainable food systems', 'Aceptado', 'No', 'quetzalcoatl.orozco^marta.astier^jorge.quetzal^maria.gonzalez^jaime.morales^peter.gerritsen^miguel.escalona^julio.sanchez^tomas.martinez^cristobal.sanchez^rene.arzuffi^federico.castrejon^helda.morales^lorena.soto^ramon.mariaca^bruce.ferguson^peter.rosset^hugo.ramirez^ramon.jarquin^mirna.ambrosio', '', '', '', '2016', 'NA', 'NA', '', '1', '1', '', ''),
('Beyond \x91Landscape\x92 in REDD+: The imperative for \x91Territory\x92', 'World Development', 'Publicado', 'No', 'keith.mccall', '', '', 'worlddev', '2016', '85', 'N/A', '0305-750X', '58', '72', '10.1016/j.worlddev.2016.05.001', ''),
('Bioclimatic mapping as a new method to assess effects of climatic change', 'Ecosphere Journal', 'Publicado', 'Si', 'alex^luis.gopar^alejandro.velazquez^joaquin.gimenez', 'luis.gopar', '', 'Ecosphere', '2015', '6', '1', '', '1', '12', '10.1890/ES14-00138.1', ''),
('Biophysical landscapes of a coastal area of Michoacán state in Mexico.', 'Journal of Maps', 'Publicado', 'No', 'angel.priego', '', 'WOS: SCI/SSCI/SCI-EX; Otros indices', '', '2011', 'N/A', '6', '1744-5647', '42', '47', '', ''),
('Caracterización magnética del polvo urbano de calles y plantas por uso de suelo en la Zona Metropolitana del Valle de México', 'Latinmag Letters', 'Publicado', 'Si', 'francisco.bautista^raul.cejudo^o.delgado.carranza^israde.alcantara^avto.gogichaishvili^jaime.morales^ana.soler', '', '', 'Latinmag Letters', '2015', '3', 'N/A', '', '0', '0', '', ''),
('Carbon measurement: an overview of carbon estimation methods and the role of GIS and remote sensing techniques for REDD+ implementation.', 'Journal of Forests and Livelihoods', 'Publicado', 'No', 'margaret.skutsch', '', '', '', '2015', '13', 'N/A', '', '1', '15', '', ''),
('Changes in climate, crops, and tradition: Cajete maize and the rainfed farming systems of Oaxaca, Mexico ', 'Human Ecology', 'Publicado', 'No', 'marta.astier^paul.roge', '', '', '', '2015', '46', '5', ' 0300-7839', '639', '653', '10.1007/s10745-015-9780-y', ''),
('Charcoal contribution accumulation at different scales of production among the rural population of Mutomo District in Kenya', 'Energy for Sustainable Development', 'Publicado', 'No', 'adrian.ghilardi', '', 'WOS: SCI/SSCI/SCI-EX', '', '2016', '33', 'N/A', '0973-0826', '167', '175', '10.1016/j.esd.2016.05.002', ''),
('Chronic institutional failure and enhanced vulnerability to flash-floods in the Cuenca Altadel Río Lerma, Mexico', 'Disasters', 'Publicado', 'No', 'frida.guiza^peter.simmons^keith.mccall', '', '', 'disasters', '2015', 'n/a', 'n/a', '1467-7717', '0', '0', '10.1111/disa.12134', '44/55'),
('Chronic institutional failure and enhanced vulnerability to flash?floods in the Cuenca Altadel Río Lerma, Mexico', 'Disasters', 'Publicado', 'No', 'gabriela.cuevas^frida.guiza^peter.simmons^keith.mccall', '', '', '', '2015', 'N/A', 'N/A', '', '0', '0', '10.1111/disa.12134', ''),
('Clasificación de la diversidad del maíz por mixtecos y chatinos en la Sierra Sur, Oaxaca, México', 'La Revue d´ethnoécologie', 'Aceptado', 'No', 'quetzalcoatl.orozco^stephen.brush', '', '', '', '2016', 'N/A', 'N/A', '2267-2419', '0', '0', '', ''),
('Climatic responses of Pinus pseudostrobus and Abies religiosa in the Monarch Butterfly Biosphere Reserve', 'Dendrochronologia', 'Publicado', 'No', 'manuel.mendoza^t.carlon.allende^diego.perez', 't.carlon.allende', '', '', '2016', '38', 'N/A', '1125-7865', '103', '116', 'http://dx.doi.org/10.1016/j.dendro.2016.04.002', ''),
('Comment on Gebhardt et al. MAD-MEX: Automatic Wall-to-Wall Land Cover Monitoring for the Mexican REDD-MRV Program Using All Landsat Data', 'Remote Sensing', 'Publicado', 'Si', 'jean.mas^stephane.couturier^jaime.paneque^margaret.skutsch^azucena.perez^gerardo.bocco^miguel.castillo', '', 'ISI Web of Knowledge', 'Remote Sens.', '2016', '8', '533', '2072-4292', '1', '14', '10.3390/rs8070533 ', ''),
('Comparison of simulation models in terms of quantity and allocation of land change', 'Environmental Modelling & Software', 'Publicado', 'No', 'jean.mas^mt.camacho.olmedo', '', '', 'Env Mod & Soft', '2015', '69', 'N/A', '13648152', '214', '221', '10.1016/j.envsoft.2015.03.003', ''),
('Componentes del paisaje como predictores de cubiertas de vegetación: estudio de caso del estado de Michoacán, México', 'Investigaciones Geográficas', 'Publicado', 'No', 'alejandro.velazquez^alex^luis.gopar', 'Luis Fernando Gopar-Merino', 'WOS: SCI/SSCI/SCI-EX; Latindex', 'Investigaciones Geográficas', '2016', '90', 'N/A', '0188-4611', '75', '88', 'dx.doi.org/10.14350', ''),
('Composición y estructura de la vegetación arbórea de petenes en la reserva de la biosfera de los petenes, Campeche, México', 'Polibotánica', 'Publicado', 'Si', 'jean.mas^p.zamora.crescencio^v.rico.gray^mr.domínguez.carrasco^c.gutierrez.baez^rc.barrientos.medina', '', ' Latindex', 'Polibotánica', '2015', '39', 'N/A', '1405-2768', '1', '19', '', ''),
('Concentration of toxic elements in topsoils of Metropolitan area of Mexico City: A spatial analysis using Ordinary Kriging and Indicator Kriging', 'Revista Internacional de Contaminación Ambiental', 'Publicado', 'Si', 'francisco.bautista^thomas.j.ihl^raul.cejudo^o.delgado.carranza^avto.gogichaishvili', '', '', 'Rev. Int. Cont. Amb.', '2015', '31', 'N/A', '', '42', '62', '', ''),
('Conceptualizing community monitoring of forest carbon stocks and tracking of safeguards in Kenya', 'Open Journal of Forestry', 'Publicado', 'No', 'keith.mccall^julius.muchemi^francis.wegulo^m.kinyanjui^alfred.gichu^elias.ucakuwun^gilbert.nduru', '', '', 'OJFor', '2015', '5', '4', '1999-4907', '0', '0', '10.4236/ojf.2015.54040', ''),
('Conocimiento tradicional del paisaje en una comunidad indígena: caso de estudio en la región purépecha, occidente de México', 'Investigaciones Geográficas', 'Publicado', 'No', 'gerardo.bocco^juan.pulido', 'juan.pulido', 'Revistas CONACYT; Scopus; SciELO; RedALyC; Latindex', '', '2015', 'na', 'na', '0188-4611', '0', '0', 'dx.doi.org/10.14350/rig.45590 ISI', ''),
('Construcción social del paisaje en comunidades de pescadores artesanales. El caso de la Península de Valdés, Provincia de Chubut, Argentina', 'Biblio 3W. Revista bibliográfica de Geografía y Ciencias Sociales', 'Publicado', 'Si', 'pedro.urquijo^gerardo.bocco', '', 'Otros indices', '', '2013', '18', '1012', '1138-9796', '1', '1', '', ''),
('Consumo de energía en el manejo de huertas de aguacate en  Michoacán, México', 'Revista Chapingo Serie Horticultura', 'Publicado', 'No', 'ana.burgos^carlos.anaya', '', '', '', '2015', '21', '1', '1027-152X', '5', '20', '10.5154/r.rchsh.2014.01.002 ', ''),
('Contenido de carbono orgánico y retención de agua en suelos de un bosque de niebla en Michoacán, México', 'Agrociencia', 'Publicado', 'No', 'manuel.mendoza^carlos.anaya^rosaura.paez^mercedes.rivera^luis.olivares', 'carlos.anaya', 'Revistas CONACYT; ISI Web of Knowledge; SciELO; RedALyC', '', '2016', '50', 'N/A', '1405-3195', '251', '269', '', ''),
('Corporación minera, colusión gubernamental y deposeción campesina. El caso de Goldcorp Inc en Mazapil , Zacatecas', 'Desacatos, Revista de Antropología Social', 'Publicado', 'No', 'pedro.urquijo^claudio.garibay^andrew.boni', 'andrew.boni', 'Revistas CONACYT; RedALyC; SciELO; Latindex', 'Desacatos', '2014', 'NA', '44', '1405-9274', '113', '142', '', ''),
('Correlación entre los elementos potencialmente tóxicos y propiedades magnéticas en suelos de la Ciudad de México para la determinación de sitios contaminados: definición de umbrales magnéticos', 'Revista Mexicana de Ciencias Geológicas', 'Publicado', 'Si', 'raul.cejudo^francisco.bautista^o.delgado.carranza^avto.gogichaishvili^j.morales.contreras', '', '', 'Rev. Mex. Cienc. Geol.', '2015', '32', 'N/A', '', '50', '61', '', ''),
('De lo efímero a lo perdurable, el sello de la religión cristina en el paisaje: el sistema constructivo de los edificios religiosos primitivos', 'Relaciones', 'Enviado', 'No', 'karine.lefebvre', '', '', 'Relaciones', '2016', 'n/a', 'n/a', '', '0', '0', '', ''),
('De montaña, milpa y cañaveral. Transformaciones percibidas de los paisajes en la costa de Chiapas', 'Investigaciones Geográficas', 'Aceptado', 'No', 'sara.barrasa', '', 'Otros indices', 'Invest. Geog', '2016', 'N/A', 'N/A', '0188-4611', '0', '30', '', ''),
('Defining environmental management units based upon integrated landscape principles at the Pacific coast in Mexico. ', 'Revista de Ciencia y Tecnología de América', 'Publicado', 'No', 'angel.priego^m.campos.sanchez^gerardo.bocco^alejandro.velazquez^m.boada.junca', '', 'WOS: SCI/SSCI/SCI-EX; Latindex; Revistas CONACYT; RedALyC; Otros indices', 'INTERCIENCIA', '2010', '35', '1', '0378-1844', '33', '40', '', ''),
('Deforestation and land tenure in Mexico: A response to Bonilla-Moheno et al.', 'Land Use Policy', 'Publicado', 'No', 'gabriela.cuevas^margaret.skutsch^jean.mas^gerardo.bocco^yan.gao', '', '', '', '2014', '39', 'N/A', '0264-8377', '390', '396', '10.1016/j.landusepol.2013.11.013', ''),
('Density of karst depressions in Yucatan state, México', 'Journal of Studies of Cave and Karst', 'Publicado', 'Si', 'francisco.bautista^yameli.aguilar^manuel.mendoza^oscar.frausto^thomas.j.ihl', 'yameli.aguilar', '', 'JSCK', '2016', '78', '1', '', '51', '60', '10. 4311/2015ES01.24', '2222'),
('Density of karst depressions in Yucatan state, México', 'Journal of Studies of Cave and Karst', 'Publicado', 'Si', 'yameli.aguilar^francisco.bautista^manuel.mendoza^oscar.frausto', 'yameli.aguilar', 'ISI Web of Knowledge; WOS: SCI/SSCI/SCI-EX', 'JSCK', '2016', '78', '2', '1090-6924', '51', '60', '10. 4311/2015ES01.24A', ''),
('Determinación de zonas prioritarias para la eco-rehabilitación de la cuenca Lerma-Chapala, México.', 'Gaceta Ecológica, Nueva Época', 'Publicado', 'No', 'angel.priego', '', 'Latindex; Otros indices', '', '2004', 'N/A', '71', '1405-2849', '79', '92', '', ''),
('Diagnóstico agroecológico de la microcuenca periurbana Río Platanitos, Guatemala', 'Tecnología en Marcha', 'Publicado', 'Si', 'francisco.bautista^luis.morales', '', '', 'Tec. en Marcha', '2015', '28', 'N/A', '', '169', '178', '', ''),
('Dictamen Con Proyecto De Decreto Por El Que Se Reforma El Artículo 17 Y La Fracción Vi Del Articulo 56; Y Se Adicionan Las Fracciones Xxvi Bis Y Xlv Bis De La Ley De Desarrollo Rural Integral Sustentable Del Estado De Michoacán De Ocampo', 'Congreso del Estado de Michoacán', 'Publicado', 'No', 'mario.figueroa^erik.juarez^jose.anaya^rosa.molina^osvaldo.esquivel^eduardo.orihuela', '', '', '.', '2012', 'N/A', 'N/A', '', '1', '2', '', ''),
('Dinámica Del Nitrógeno En Lixiviados De Tiraderos Abiertos Aplicados En La Microcuenca Morelia-Tarímbaro, Michoacán, México', 'Coordinación General de Estudios de Posgrado', 'Publicado', 'No', 'mario.figueroa^encarnacion.bobadilla^nayda.bravo^alberto.orozco^jesus.luna', 'alberto.orozco^jesus.luna', '', 'CGEP UMSNH', '2015', 'N/A', 'N/A', '', '1', '8', '', ''),
('Dinámica espacio-temporal del bosque nublado y su estado sucesional en el Estado de Michoacán, México', 'Geografía y Sistema de Información Geográfica', 'Publicado', 'Si', 'manuel.mendoza^y.martinez.ruiz^ge.santana.huicochea^erna.lopez', 'y.martinez.ruiz', '', '', '2016', '8', '8', '1852-8031', '233', '247', '', ''),
('Diseño de las políticas públicas de corte forestal en México: implicaciones para la gestión de la vulnerabilidad social y el territorio', 'Investigaciones Geográficas', 'En prensa', 'Si', 'alex^neyra.sosa^alejandro.velazquez^dante.ayala^gerardo.bocco^luis.gopar', 'neyra.sosa^luis.gopar', 'SciELO; Revistas CONACYT; Scopus; Latindex; RedALyC', 'IG', '2016', 'N/A', 'N/A', ' 0188-4611', '1', '13', '10.14350/rig.53915', ''),
('Diseño de una política de ciencia, tecnología e innovación a partir de métodos cualitativos', 'Intersticios Sociales', 'Aceptado', 'No', 'saray.bucio^jose.solis ', '', '', 'Intersticios', '2016', 'N/A', 'N/A', '2007-4964', '0', '0', '', ''),
('Distribución de bacterias patógenas en el agua para consumo humano en una cuenca rural y sus afectaciones potenciales en la saludo pública', 'Ciencia Nicolaita', 'Publicado', 'Si', 'maria.carmona^yesenia.rodriguez^ruben.hernandez', 'yesenia.rodriguez', '', 'Ciencia Nicolaita', '2015', 'NA', '66', '2007-7068', '25', '40', 'http://www.cic.cn.umich.mx/index.php/cn/issue/view/14', ''),
('Distribución geográfica y ecológica de Ipomoea (Convolvulaceae) en el estado de Michoacán, México', 'Revista Mexicana de Biodiversidad', 'Publicado', 'No', 'gabriela.cuevas^j.alcantar.mejía', '', '', '', '2012', '83', 'N/A', '1870-3453', '731', '741', '', ''),
('Diversidad de maíces en Pátzcuaro, Michoacán, México y su relación con factores ambientales y sociales', 'Agrociencia', 'Enviado', 'No', 'quetzalcoatl.orozco^marta.astier', '', '', '', '2016', 'NA', 'NA', '', '0', '0', '', ''),
('Don Mateo-El Cerro, a Newly Rediscovered Late Period Settlement in Yocavil (Catamarca, Argentina).', 'Andean Past', 'Publicado', 'No', 'alina.alvarez', '', '', '', '2016', '12', 'n/a', '1055-8756', '0', '0', '', ''),
('Ecosystem service trade-offs, perceived drivers and sustainability in contrasting agroecosystems in Central Mexico', 'Ecology and Society', 'Publicado', 'No', 'marta.astier^carlos.gonzalez^mayra.gavito^martin.cardena^ek.del.val^laura.villamil^yair.Merlin^patricia.balvanera', '', '', 'E&S', '2015', '20', '1', '1708-3087', '38', '52', 'http://dx.doi.org/10.5751/ES-06875-200138 ', ''),
('Ecotechnologies for the sustainable management of tropical forest diversity.', 'Nature & Resources', 'Publicado', 'No', 'angel.priego', '', 'Otros indices', '', '1997', '33', '1', '0028-0844.', '2', '17', '', ''),
('Editorial for Special Issue: The Potential Role for Community Monitoring in MRV and in Benefit Sharing in REDD+', 'Forests', 'Publicado', 'No', 'margaret.skutsch^arturo.balderas', '', '', 'For', '2015', '6', '1', '1999-4907', '244', '251', 'doi:10.3390/f6010244', ''),
('Effect of the landscape matrix condition for prioritizing Multi-Species Connectivity Conservation in a Highly Biodiverse Landscape of Central Mexico', 'Environmental Management', 'Enviado', 'No', 'manuel.mendoza^camilo.correa^andres.etter^diego.perez', 'camilo.correa', '', '', '2016', 'NA', 'NA', '', '0', '0', '', ''),
('Effects of biophysical properties on soil erosion within a catchment approach: modeling through WEPP over the last 2000 years', 'Land Degradation and Development', 'Enviado', 'No', 'lourdes.gonzalez^manuel.mendoza^jose.navarrete', '', '', '', '2017', 'N/A', 'N/A', '', '1', '1', '', ''),
('El arte rupestre como geosigno del paisaje (valle de Yocavil, Catamarca, Argentina).', 'Comechingonia, Revista de Arqueología', 'Publicado', 'No', 'alina.alvarez', '', 'Latindex; SciELO', 'Comechingonia', '2012', '16', '2', '0326-7911^2250-7728', '55', '74', 'http://www.comechingonia.com/', ''),
('El color del polvo urbano como indicador de contaminación por elementos potencialmente tóxicos: El caso de Ensenada, Baja California', 'Revista Chapingo Serie Ciencias Forestales y del Ambiente', 'Publicado', 'No', 'francisco.bautista^avto.gogichaishvili', '', '', 'rcsfa', '2015', '21', '3', '', '255', '266', '', ''),
('El paisaje en su connotación ritual. Un caso en la Huasteca Potosina, México', 'Geotrópico', 'Publicado', 'Si', 'pedro.urquijo', '', 'Latindex', '', '2010', 'NA', '2', '1692-0791', '1', '1', '', ''),
('El potencial del magnetismo en la clasificación de suelos: una revisión', 'Boletín de la Sociedad geológica Mexicana', 'Publicado', 'No', 'francisco.bautista^raul.cejudo^yameli.aguilar^avto.gogichaishvili', '', '', 'Bol. Socied. Geol. Mex.', '2015', '66', 'N/A', '', '123', '134', '', ''),
('Elementos del paisaje como predictores de tipos de cubiertas de vegetación.', 'Investigaciones Geográficas', 'En prensa', 'No', 'alex^luis.gopar^alejandro.velazquez', 'luis.gopar', '', '', '2015', 'N/A', 'N/A', '', '1', '10', 'http://dx.doi.org/10.14350/rig.46688', ''),
('Energy consumption in the management of avocado orchards in Michoacán, Mexico', 'Revista Chapingo Serie Horticultura', 'Publicado', 'No', 'gabriela.cuevas^carlos.anaya^ana.burgos', '', '', '', '2015', '21', '1', '', '5', '20', '10.5154/r.rchsh. 2014.01.002', ''),
('Entre la utopía y la distopía. La construcción social de la experiencia de la ciudad en un espacio excluido de la ciudad de Morelia, Michoacán', 'Revista Mexicana De Sociología', 'Enviado', 'No', 'frida.guiza', '', '', '', '2016', 'N/A', 'N/A', '', '0', '0', '', ''),
('Environmental Burden of Traditional Bioenergy Use', 'Annual Review of Environment and Resources', 'Publicado', 'No', 'adrian.ghilardi^omar.masera^bailis.espinoza', '', 'WOS: SCI/SSCI/SCI-EX', 'ANNU REV ENV RESOUR', '2015', '40', 'N/A', '1543-5938', '121', '150', '10.1146/annurev-environ-102014-021318', ''),
('Estudio de propiedades magnéticas en riñon e hígado de Mus musculus para la detección de elementos tóxicos', 'Latimag Letters Special Issues Proceedings Sao Paulo, Brasil', 'Publicado', 'Si', 'francisco.bautista^raul.cejudo^o.delgado.carranza^avto.gogichaishvili^jaime.morales^hilda.rivas', '', '', 'Latinmag', '2016', '6', 'N/A', '2007-9656', '1', '6', '', ''),
('Estudio magnético y geoquímico de lodos lixiviados de sitios de disposición final de residuos urbanos', 'Latimag Letters Special Issues Proceedings Sao Paulo, Brasil', 'Publicado', 'Si', 'francisco.bautista^raul.cejudo^o.delgado.carranza^israde.alcantara^avto.gogichaishvili^jaime.morales^ana.soler', '', '', 'Ltinmag', '2016', '6', 'N/A', '2007-9656', '1', '5', '', ''),
('Estudio Sobre El Desempeño Nutrimental De Cuatro Insumos Orgánicos Utilizados Como Fertilizantes En La Microcuenca Morelia-Tarímbaro, Michoacán, México.', 'CECTI Michoacán', 'Publicado', 'No', 'mario.figueroa^marta.astier^luz.garcia^maria.figueroa^guillermo.figueroa^zoila.cardenas^diego.torres^jose.plancarte', 'Luz Elena García Martínez, María del Socorro Figueroa Béjar, Guillermo Iván Figueroa Béjar, Zoila Cárdenas Mendoza, Diego Torres Huerta, José Aldo Plancarte Trujillo', '', 'CECTI', '2016', 'N/A', 'N/A', '', '1', '8', '', ''),
('Ethnoagroforestry: Integration Of Biocultural Diversity For Food Sovereignty In México', 'Journal of Ethnobiology and Ethnomedicine', 'Publicado', 'No', 'mariana.vallejo^ana.moreno^alejandro.casas^alexis.rivero^yessica.romero^selene.rangel^roberto.fisher^fernando.alvarado^didac.santos', '', '', 'J Ethnobiol Ethnmed', '2016', '12', '54', '', '1', '21', '10.1186/s13002-016-0127-6', ''),
('Evaluación de la contaminación ambiental a partir del aumento magnético en polvos urbanos - Caso de estudio para la ciudad de Mexicali, México', 'Revista Mexicana de Ciencias Geológicas', 'Publicado', 'Si', 'francisco.bautista^a.sanchez.duque^avto.gogichaishvili^raul.cejudo^j.reyez.lopez^f.solis.dominguez^j.morales.contreras', 'a.sanchez.duque', '', 'Rev Mex C Geol', '2016', '32', '3', '1026-8774', '501', '513', 'http://satori.geociencias.unam.mx/32-3/(09)SanchezDuque.pdf', ''),
('Evaluation of annual modis PTC data for deforestation and forest degradation analysis', 'International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences - ISPRS Archives', 'Publicado', 'Si', 'adrian.ghilardi^yan.gao^jean.mas^jaime.paneque^margaret.skutsch', '', 'Scopus', '', '2016', 'N/A', 'N/A', '', '9', '13', '10.5194/isprsarchives-XLI-B2-9-2016', ''),
('Evaluation Of Anthropogenic Impact On Habitat Connectivity Through A Multidimensional Spatial Human Footprint Index In A Highly Biodiverse Landscape Of Central Mexico', 'Ecological Indicators', 'En prensa', 'No', 'manuel.mendoza^camilo.correa^andres.etter^diego.perez', 'camilo.correa', '', '', '2016', '72', '1', '1470-160X', '895', '909', '10.1016/j.ecolind.2016.09.007', ''),
('Exploring indigenous landscape classification across different dimensions: a case study from the Bolivian Amazon', 'Landscape Research', 'Publicado', 'No', 'jaime.paneque^ Riu-Bosoms, Carles; Vidal-Amat, Teresa;  Duane, Andrea; Fernández-Llamazares, A; Guèze, Maximilien; Luz, Ana Catarina; Macía, Manuel J.; Reyes-García, Victoria', '', '', 'Landsc. Res.', '2015', '40', '3', '0142-6397^1469-9710', '318', '337', '10.1080/01426397.2013.829810', ''),
('Fundamentos Agronómicos Para Reformar La Ley De Desarrollo Rural Integral Sustentable En El Estado De Michoacán De Ocampo, México', 'CECTI Michoacán', 'Publicado', 'No', 'mario.figueroa', '', '', 'CECTI', '2016', 'N/A', 'N/A', '', '1706', '1713', '', ''),
('Further evidence for magnetic susceptability as a proxy for the evaluation of heavy metals in mining waste: case study of Thalpujahua and El Oro mining districts', 'Environmental Earth Science', 'Publicado', 'No', 'francisco.bautista^jaime.morales^avto.gogichaishvili', '', '', 'Environ Earth Sci,', '2016', '75', 'NA', '', '309', '318', '10.1007/s12665-015-5187-8', ''),
('General principles behind traditional environmental knowledge: the local dimension in land management', 'The Geographical Journal', 'Publicado', 'No', 'gerardo.bocco^antoinette.winklerprins', '', '', 'TGJ', '2015', 'en linea', 'na', '', '0', '0', 'DOI: 10.1111/geoj.12147', ''),
('Geografía ambiental : Reflexiones teóricas y práctica institucional', 'Región y Sociedad', 'Publicado', 'No', 'pedro.urquijo^gerardo.bocco', '', 'Revistas CONACYT; Clase; RedALyC; Latindex; Otros indices', '', '2013', '25', '44', '1405-9274', '75', '101', '', ''),
('Geographical distribution and diversity of maize (Zea mays L. subsp. mays) races in Mexico', 'Genetic Resources and Crop Evolution', 'Publicado', 'No', 'quetzalcoatl.orozco^hugo.perales^robert.hijmans', '', '', 'Genet Resour Crop Evol ', '2016', 'NA', 'NA', '', '0', '0', 'doi:10.1007/s10722-016-0405-0', ''),
('Geomorpology, internal structure and evolution of alluvial fans at Motozintla, Chiapas, Mexico', 'Geomorphology', 'Publicado', 'No', 'manuel.mendoza^jm.sanchez.nunez^luis.macias^ricardo.saucedo^jr.torres.hernandez', 'jm.sanchez.nunez', '', '', '2015', '230', 'N/A', '', '1', '12', 'http://dx.doi.org/10.1016/j.geomorph.2014.10.003', ''),
('Gran Gruta Grabada de Chiquimí. Noticia acerca de su hallazgo y redescubrimiento, 100 años después. ', 'Boletín del Museo Chileno de Arte Precolombino ', 'Publicado', 'No', 'alina.alvarez^jp.carbonelli', '', 'SciELO; Latindex', '', '2011', '16', '1', '0716-1530', '23', '46', 'http://www.precolombino.cl/biblioteca/boletin-del-museo/', ''),
('Habitar una región. Espacialidad arquitectónica y construcción de paisajes en Andalhuala, valle de Yocavil (Catamarca, Argentina). ', 'Arqueología', 'En prensa', 'No', 'alina.alvarez', '', 'Scopus; SciELO; Latindex', '', '2016', '22', 'N/A', '0327-5159^1853-8126', '0', '0', '', ''),
('Habitat connectivity in biodiversity conservation: a review of recent studies and applications', 'Progress in Physical Geography', 'Publicado', 'No', 'manuel.mendoza^camilo.correa^andres.etter^diego.perez', 'camilo.correa', '', '', '2016', '40', '1', '1477-0296', '7', '37', 'DOI: 10.1177/0309133315598713', ''),
('Health impacts from power plant emissions in Mexico', 'Atmospheric Environment', 'Publicado', 'No', 'gabriela.cuevas', '', '', '', '2005', '39', '7', '', '1199', '1209', '10.1016/j.atmosenv.2004.10.035', ''),
('Heterogeneidad del paisaje y riqueza de flora: Su relación en el archipiélago de Camagüey, Cuba. ', 'Revista de Ciencia y Tecnología de América', 'Publicado', 'No', 'angel.priego^jl.palacio.prieto^p.moreno.casasola^j.lopez.portillo^d.geissert.kientz', '', 'WOS: SCI/SSCI/SCI-EX; Latindex; Otros indices', 'INTERCIENCIA', '2004', '29', '3', '0378-1844', '138', '144', '', ''),
('Historia de la agroecología en México', 'Revista de Agroecología', 'Publicado', 'No', 'marta.astier^pablo.argueta^quetzalcoatl.orozco^peter.gerritsen^miguel.escalona^julio.sanchez^cristobal.sanchez^rene.arzuffi^federico.castrejon^lorena.soto^jaime.morales^peter.rosset^teresa.ramirez^ramon.jarquin^carlos.gonzalez', 'quetzalcoatl.orozco', '', '', '2015', '10', '2', '1989-4686', '9', '18', '', ''),
('Historia de la Agroecología en Mexico', 'Agroecología', 'En prensa', 'No', 'quetzalcoatl.orozco^marta.astier^jorge.quetzal^maria.gonzalez^jaime.morales^peter.gerritsen^miguel.escalona^julio.sanchez^cristobal.sanchez^rene.arzuffi^federico.castrejon^lorena.soto^peter.rosset^hugo.ramirez^joaquin.gimenez^carlos.gonzalez^mirna.ambrosio', '', '', '', '2016', 'NA', 'NA', '', '9', '18', '', ''),
('Historia y paisaje : Explorando un concepto geográfico monista.', 'Andamios, Revista de Investigación Social', 'Publicado', 'No', 'pedro.urquijo', '', 'Otros indices; WOS: SCI/SSCI/SCI-EX; Revistas CONACYT', 'Andamios', '2009', '5', '10', '1870-0063', '227', '252', '', ''),
('History of pedogenesis and geomorphic processes in the Valley of Teotihuacán, Mexico: micromorphological evidence from soil catena', 'Spanish Journal of Soil Science', 'Publicado', 'No', 'lourdes.gonzalez^emily.mcclung^jorge.gama^sergey.sedov^lorenzo.vazquez', '', '', 'sjss', '2013', '3', '3', '', '201', '216', '10.3232/SJSS.2013.V3.N3.05', ''),
('Horizontal and vertical landscape-complexity influence avian species-richness patterns across the conterminous USA', 'Cogent Environmental Science', 'Enviado', 'No', 'brian.napoletano^bryan.pijanowski', '', '', 'COG ENV SCI', '2015', 'N/A', 'N/A', '0143-6228', '0', '0', '', ''),
('How does cultural change affect indigenous peoples\x92 hunting activity? An empirical study among the Tsimane\x92 in the Bolivian Amazon', 'Conservation and Society', 'Publicado', 'No', 'jaime.paneque^marti.orta^victoria.reyes\n', '', '', 'Conservat. Soc.', '2015', '13', '4', '', '382', '394', '10.4103/0972-4923.179879', ''),
('How social capital enables/restricts the livelihoods of poor peri-urban farmers in Mexico', 'Development in Practice', 'Aceptado', 'No', 'lourdes.gonzalez^antonio.vieyra^yadira.mendez', '', 'Otros indices', 'DiP', '2016', 'N/A', 'N/A', '1364-9213', '0', '0', '', ''),
('Human impact on natural systems modeled through soil erosion in GeoWEPP: a comparison between pre-Hispanic periods and modern times in the Teotihuacan Valley (central Mexico)', 'CATENA', 'Publicado', 'No', 'manuel.mendoza^lourdes.gonzalez^lorenzo.vazquez', 'lourdes.gonzalez', '', '', '2016', '149', 'NA', '0341-8162', '505', '513', 'http://dx.doi.org/10.1016/j.catena.2016.07.028', ''),
('Identificación de zonas presumiblemente contaminadas por elementos tóxicos por técnicas no convencionales en la ciudad de Morelia, Michoacán', 'Latimag Letters Special Issues Proceedings Sao Paulo, Brasil', 'Publicado', 'Si', 'francisco.bautista^raul.cejudo^o.delgado.carranza^israde.alcantara^avto.gogichaishvili^jaime.morales', '', '', 'Latinmag', '2016', '6', 'N/A', '2007-9656', '1', '5', '', 'M/A'),
('Identification and quantification of drivers of forest degradation in tropical dry forests: a case study in Western Mexico', 'Land Use Policy', 'Publicado', 'No', 'margaret.skutsch^l.morales.barquero^armonia.borrego^john.healey', '', '', 'LUP', '2015', '69', 'N/A', '0264-8377', '296', '309', 'doi:10.1016/j.landusepol.2015.07.006', ''),
('Identifying future climatic change patterns at basin level in Baja California', 'Atmosfera', 'Enviado', 'No', 'manuel.mendoza^t.carlon.allende^yan.gao', 't.carlon.allende', '', '', '2016', 'N/A', 'N/A', '', '0', '0', '', ''),
('Illegal Logging of 10 Hectares of Forest in the Sierra Chincua Monarch Butterfly Overwintering Area in Mexico', 'American Entomologist', 'Publicado', 'No', 'maria.ramirez^lincoln.brwoer^daniel.slayback^pablo.jaramillo^karen.oberhauser^ernest.williams^linda.fink', '', 'ISI Web of Knowledge', 'Am. Entomol.', '2016', '62', '2', '1046-2821', '92', '97', 'http://dx.doi.org/10.1093/ae/tmw040 ', ''),
('Impacts of Bokashi on survival and growth rates of Pinus pseudostrobus in community reforestation projects', 'Journal of Environmental Management ', 'Publicado', 'No', 'maria.ramirez^pablo.jaramillo^isabel.ramirez^diego.perez^hilda.rivas', '', 'WOS: SCI/SSCI/SCI-EX', 'J ENVIRON MANAGE', '2015', '150', 'n/a', '0301-4797', '48', '56', 'doi:10.1016/j.jenvman.2014.11.003', 'WOS:000349504300006'),
('Impacts of Finnish cooperation in the Mexican policy making process: from community forest management to the liberalisation of forest services.', 'Forest Policy and Economics', 'Publicado', 'No', 'margaret.skutsch', '', '', '', '2016', '73', 'N/A', '', '229', '2380', 'http://dx.doi.org/10.1016/j.forpol.2016.09.011 1389-9341/', ''),
('Implementación del Índice de Condición Forestal (ICF), Como un insumo para el diseño de políticas públicas de corte forestal en México', 'Investigaciones Geográficas', 'Aceptado', 'No', 'alex^neyra.sosa^alejandro.velazquez^dante.ayala^gerardo.bocco^luis.gopar', 'neyra.sosa^dante.ayala^gerardo.bocco^luis.gopar', 'Revistas CONACYT; WOS: SCI/SSCI/SCI-EX', 'Investigaciones Geográficas', '2016', 'N/A', 'N/A', '0188-4611', '0', '0', 'dx.doi.org/10.14350', ''),
('Información geográfica voluntaria (IGV), estado del arte en Latinoamérica', 'Revista Cartográfica', 'Aceptado', 'No', 'frida.guiza^aldo.hernandez', 'aldo.hernandez', '', '', '2016', 'N/A', 'N/A', '', '0', '0', '', ''),
('Iniciativa Ciudadana Con Proyecto De Decreto Para Modificar El Artículo 9º Y Adicionar El Párrafo Tercero De La Ley Ambiental Para El Desarrollo Sustentable Del Estado De Michoacán', 'CECTI Michoacán', 'Publicado', 'No', 'mario.figueroa^guillermo.figueroa^monica.figueroa^maria.figueroa^alberto.orozco', 'alberto.orozco', '', '.', '2014', '.', '1366-1374', '', '1366', '1374', '.', '.'),
('Introducción: el MESMIS en Brasil y en el mundo. ', 'Revista Agricultura Familiar', 'Enviado', 'No', 'marta.astier^carlos.gonzalez^omar.masera', '', '', '', '2016', 'N/A', 'N/A', '1729-7419', '0', '0', '', ''),
('Propuesta De Desarrollo Municipal En Lixiviados Obtenidos De Tiraderos Abiertos Para Ser Aplicados Como Abonos Agrícolas En Michoacán, México.', 'Revista De Investigación En Ciencias De La Administración', 'Publicado', 'No', 'mario.figueroa^mario.figueroa^alberto.orozco^nayda.bravo^jesus.luna^laura.santillan', 'alberto.orozco^jesus.luna', '', 'INCEPTUM', '2014', 'N/A', 'N/A', '', '1', '7', '', ''),
('Is canopy-cover recovery associated to vegetation attributes and diversity recovery in tropical shrubland? ', 'Plant Ecology', 'Enviado', 'No', 'manuel.mendoza^a.lomelí.jimenez^diego.perez^b.figueroa.rangel', 'a.lomelí.jimenez', '', '', '2015', 'N/A', 'N/A', '', '0', '0', '', ''),
('IVAKY: Índice de la vulnerabilidad del acuífero kárstico yucateco a la contaminación', 'Revisa Mexicana de Ingeniería Química', 'Publicado', 'No', 'yameli.aguilar^francisco.bautista^manuel.mendoza^oscar.frausto^thomas.j.ihl^o.delgado.carranza', 'yameli.aguilar', 'WOS: SCI/SSCI/SCI-EX; ISI Web of Knowledge', 'RMIQ', '2016', '15', '3', '2395-8472', '913', '930', 'http://rmiq.org/iqfvp/Pdfs/Vol.%2015,%20No.%203/IA1/RMIQTemplate.pdf', 'http://rmiq.org/iqfvp/Pdfs/Vol.%2015,%20No.%203/IA1/RMIQTemplate.pdf'),
('Ixcatec ethnoecology: plant management and biocultural heritage in Oaxaca, Mexico', 'Journal of Ethnobiology and Ethnomedicine ', 'Publicado', 'No', 'mariana.vallejo^selene.rangel^alejandro.casas', '', '', 'J Ethnobiol  Ethnomed', '2016', '12', '30', '', '0', '83', '10.1186/s13002-016-0101-3', ''),
('La alfarería de inicios del segundo milenio en Yocavil. El problema \x93San José\x94 y las tipologías cerámicas.', 'Arqueologia', 'Publicado', 'Si', 'alina.alvarez^v.palamarczuk^solange.grimoldi', '', 'RedALyC; Latindex; Scopus', '', '2014', '20', 'Dossier', '0327-5159^1853-8126', '107', '134', 'https://sites.google.com/site/revistaarqueologia/', ''),
('La dinámica ambiental de la cuenca Lerma-Chapala, México.', 'Gaceta Ecológica, Nueva Época', 'Publicado', 'No', 'angel.priego', '', 'Latindex; Otros indices', '', '2004', 'N/A', '71', '1405-2849', '23', '77', '', ''),
('La distribución de la diversidad de maíces en la región de Pátzcuaro y sus asociación con factores ambientales y sociales', 'Agrociencia', 'Enviado', 'No', 'marta.astier^quetzalcoatl.orozco', '', '', '', '2016', 'N/A', 'N/A', '1405-3195', '0', '0', '', ''),
('La estación ecológica de Majana: Su vegetación y flora.', 'Fontqueria', 'Publicado', 'No', 'n.aguila.carrasco^l.menéndez.carrera^ricardo.napoles^angel.priego', '', 'Latindex; Otros indices', '', '1994', 'N/A', '39', '0212-0623', '251', '261', '', ''),
('La evolución del campo de los estudios sociales de la ciencia y la tecnología en Venezuela: notas de memoria.', 'Espacio Abierto', 'En prensa', 'No', 'saray.bucio^hebe.vessuri', '', 'WOS: SCI/SSCI/SCI-EX; SciELO', '', '2016', '25', '4', '1315-0006', '0', '0', '', ''),
('La Geografía Física y el Ordenamiento Ecológico del Territorio. Experiencias en México. ', 'Gaceta Ecológica, Nueva Época', 'Publicado', 'No', 'angel.priego^gerardo.bocco', '', 'Latindex; Otros indices', '', '2005', 'N/A', '76', '1405-2849', '23', '34', '', ''),
('Land use and cover change scenarios in the Mesoamerican Biological Corridor-Chiapas, México', 'Botanical Sciences', 'Aceptado', 'No', 'gabriela.cuevas^diana.ramirez^paula.melic^manuel.mendoza', '', '', '', '2016', 'N/A', 'N/A', '', '0', '0', '', ''),
('Landslides in the tropical mountain range of Veracruz (Mexico) - A case-study of the large El Capulin landslide', 'World Landslide Forum', 'En prensa', 'Si', 'berenice.solis^martina.wilde^wendy.morales^daniel.schwindt^matthias.bucker^birgit.terhorst', '', '', '', '2016', 'NA', 'NA', '', '0', '0', '', ''),
('Late Holocene erosion events in the Valley of Teotihuacan, central Mexico: insights from a soil-geomorphic analysis of catenas ', 'CATENA', 'Aceptado', 'No', 'lourdes.gonzalez^emily.mcclung^jorge.gama^sergey.sedov^lorenzo.vazquez', '', '', '', '2016', 'N/A', 'N/A', '', '1', '2', '', ''),
('Los espacios del pueblo de indios tras el proceso de congregación, 1550-1625', 'Investigaciones Geográficas', 'Publicado', 'No', 'pedro.urquijo', '', 'Otros indices; Scopus; Revistas CONACYT', '', '2006', 'NA', '60', '', '145', '158', '', ''),
('Los estudios de paisaje y su importancia en México, 1970-2010', 'Journal of Latin America Geography', 'Publicado', 'No', 'pedro.urquijo^gerardo.bocco', '', '', 'JLAG', '2011', '10', '2', '1545-2476', '37', '63', '', ''),
('Maize diversity associated with social origin and environmental variation in Southern Mexico', 'Heredity', 'Publicado', 'No', 'quetzalcoatl.orozco^jeffrey.ross^amalio.santacruz^stephen.brush', '', '', 'Heredity', '2016', '116', 'NA', '0018-067X', '477', '484', '10.1038/hdy.2016.10', ''),
('Management practices and plant and flower visitor biodiversity in conventional and organic avocado orchards of Michoacán, México', 'Agroecology and Sustainable Food Systems', 'Enviado', 'No', 'marta.astier^laura.villamil^yair.merlin^mayra.gavito', 'yair.merlin', '', '', '2016', 'N/A', 'N/A', '2168-3565', '0', '0', '', ''),
('Management-sensitive hierarchical typology for riparian zones based on biophysical features: a procedure', 'Physical Geography', 'Enviado', 'No', 'adriana.flores^roger.guevara^manuel.mendoza^rosario.langrave^manuel.maass', '', 'ISI Web of Knowledge; Otros indices', '', '2017', 'N/A', 'N/A', '', '0', '0', '', ''),
('Mapa de paisajes físico-geográficos del Parque Cultural del río Martín (Teruel, Aragón) escala 1:50.000', 'Revista Catalana de Geografía', 'Publicado', 'Si', 'manuel.bollo^ivan.franch^a.espinoza.maya^luis.cancer', 'ivan.franch^a.espinoza.maya', '', '', '2016', '. IV época / volumen XXI /', ' núm. 53', ' 1988-2459', '1', '15', '', ''),
('Metales pesados en suelos urbanos de Morelia, Michoacán: influencia de los usos de suelo y tipos de viabilidad', 'Ciencia Nicolaita', 'Publicado', 'No', 'hilda.rivas^o.delgado.carranza^israde.alcantara^francisco.bautista^avto.gogichaishvili^raul.cejudo^jaime.morales', '', '', '', '2015', '65', 'NA', '2007-7068', '120', '138', '', ''),
('Métodos para la evaluación visual del paisaje: entre la estética y la ecología', 'Agrociencia', 'Enviado', 'No', 'sara.barrasa^cruz.lopez^alejandro.collantes^eduardo.alanis', 'cruz.lopez', '', '', '2015', 'N/A', 'N/A', '1405-3195', '0', '15', '', ''),
('Mineral magnetic properties of an alluvial paleosol sequence in the Maya Lowlands: Late Pleistocene-Holocene paleoclimatic implications', 'Quaternary International', 'Aceptado', 'Si', 'berenice.solis^gabriel.vazquez^elizabeth.solleiro^avto.gogichaishvili^juan.morales', '', 'Otros indices', '', '2015', 'N/A', 'N/A', '1040-6182', '0', '1', '', ''),
('Modelación espacial del tiempo de intervención antrópica sobre el paisaje: un caso de estudio en el sistema volcánico transversal de Michoacán, México', 'Geografía y Sistema de Información Geográfica', 'Publicado', 'Si', 'manuel.mendoza^camilo.correa^andres.etter^diego.perez', 'camilo.correa', '', '', '2016', '8', '8', '1852-8031', '183', '205', '', ''),
('Modeling Historical Land Cover and Land Use: A Review from Contemporary Modeling', 'ISPRS International Journal of Geo-Information', 'Publicado', 'Si', 'pedro.urquijo^laura.chang^jean.mas^jf.torrescano.valle', 'laura.chang', 'WOS: SCI/SSCI/SCI-EX', '', '2015', '4', 'NA', '2220-9964', '1791', '1812', '10.3390/ijgi4041791', ''),
('Modeling sea-level change, inundation scenarios and their effect on the Colola Beach Reserve - a nesting - habitat of the black sea turtle, Michoacán, México', 'Geofísica Internacional', 'Publicado', 'No', 'jose.navarrete^y.calvillo.garcía^teresa.ramirez^c.delgado.trejo^g.legorreta.paulin', ' ', '', ' ', '2015', '54', '2', ' ', '179', '190', ' ', ' '),
('Modelling with Stakeholders - Next Generation', 'Environmental Modelling & Software', 'Publicado', 'No', 'keith.mccall^alexey.voinov^nagesh.kolagani^pierre.glynn^marit.kraagt^frank.ostermann^palaniappan.ramu^suzanne.pierce', '', '', 'envsoft', '2016', '77', '00', '1364-8152', '196', '220', 'doi.org/10.1016/j.envsoft.2015.11.016', ''),
('Monitoring Deforestation With MODIS, Proceedings of the ForestSat 07 Conference, Montpellier France', 'Conference Montpellier France', 'Publicado', 'No', 'hugo.zavala^jean.mas^yao.gao^gabriela.cuevas', '', '', '', '2007', 'N/A', 'N/A', '', '0', '0', '', ''),
('Moving from Measuring, Reporting, Verification (MRV) of Forest Carbon to Community Mapping, Measuring, Monitoring (MMM): a case in Mexico', 'Plos One', 'Publicado', 'Si', 'keith.mccall^noah.chutz^margaret.skutsch', '', '', 'plos1', '2016', '11', '6', '1932-6203', '0', '0', 'doi:10.1371/journal.pone.0146038', ''),
('Moving from MRV to community MMM: a case in Mexico.', 'Plos One', 'En prensa', 'No', 'margaret.skutsch^keith.mccall^noah.chutz', '', '', 'Plos1', '2015', '0000000', 'N/A', '', '0', '0', '', ''),
('Narrativas sobre el lugar. Habitar una vivienda de interés social en la periferia urbana', 'Revista INVI', 'Publicado', 'No', 'antonio.vieyra^claudio.garibay', 'fabricio.espinoza', '', '', '2015', '30', '84', '0718-1299', '59', '72', '', ''),
('Ollas como urnas, casas como tumbas: reflexiones en torno a las prácticas de entierro de niños en tiempos tempranos (Andalhuala Banda, sur de Yocavil). ', 'Comechingonia, Revista de Arqueología', 'Enviado', 'No', 'alina.alvarez^solange.grimoldi^romina.spano', '', 'SciELO; Latindex', 'Comechingonia', '2016', 'N/A', 'N/A', '0326-7911', '1', '1', '', ''),
('Opportunities, constraints and perceptions of rural communities regarding their potential to contribute to forest landscape transitions under REDD+: Case studies from Mexico', 'International Forestry Review', 'Publicado', 'No', 'maria.ramirez^margaret.skutsch^armonia.borrego^luis.morales^jaime.paneque^isabel.ramirez^diego.perez^yan.gao', 'armonia.borrego^luis.morales', 'WOS: SCI/SSCI/SCI-EX', 'INT FOREST REV', '2015', '17', 'S1', '1465-5489', '65', '84', 'http://dx.doi.org/10.1505/146554815814669025', 'WOS:000351672700005'),
('Ordenamiento Ecológico Marino en el Pacífico Norte mexicano: propuesta metodológica', 'Hidrobiológica', 'En prensa', 'No', 'gerardo.bocco^benigno.hernandez^raul.aguirre^gilberto.gaxiola^raul.aguirre^gilberto.gaxiola^saul.alvarez^artemio.gallegos^fernando.rosete', 'benigno.hernandez', '', '', '2015', 'na', 'na', '0188-8897', '0', '0', '', ''),
('Paisaje urbano a orillas de la Laguna de Bacalar (Quintana Roo, México): ocupación del suelo y producción del imaginario por el turismo', 'Cuadernos de Geografía', 'Publicado', 'No', 'sara.barrasa^enrique.gomez^ana.garcia', 'enrique.gomez', 'RedALyC; Latindex; SciELO', '', '2016', 'N/A', 'N/A', '0121-215X', '1', '25', '', ''),
('Paisajes agroalfareros del primer y segundo milenio DC en la Mesada de Andalhuala Banda (Yocavil, Noroeste argentino)', 'Ñawpa Pacha. Journal of Andean Archaeology', 'Publicado', 'No', 'alina.alvarez', '', 'Otros indices', 'Ñawpa Pacha', '2016', '36', '2', '0077-6297^2051-6207', '161', '184', 'http://www.instituteofandeanstudies.org/publications.html', ''),
('Paisajes físico-geográficos de Cayo Guillermo, Ciego de Ávila, Cuba. ', 'Revista Del Jardín Botánico Nacional De Cuba', 'Publicado', 'No', 'angel.priego^j.gonzález.areu^l.menéndez.carrera', '', 'Latindex; Otros indices', '', '1999', 'N/A', '20', '0253-5696', '159', '166', '', ''),
('Paisajes físico-geográficos de la cuenca Lerma-Chapala, México.', 'Gaceta Ecológica, Nueva Época', 'Publicado', 'No', 'angel.priego^helda.morales', 'helda.morales', 'Latindex; Otros indices', '', '2004', 'N/A', '71', '1405-2849', '11', '22', '', ''),
('Paisajes físico-geográficos de los manglares de la laguna de La Mancha, Veracruz, México.', 'Revista de Ciencia y Tecnología de América', 'Publicado', 'No', 'angel.priego^h.hernandez.trejo^ja.lopez.portillo^ja.lopez.portillo^e.vera.isunza', '', 'WOS: SCI/SSCI/SCI-EX; Latindex; Otros indices', 'INTERCIENCIA', '2006', '31', '3', '0378-1844', '211', '219', '', ''),
('Paisajes geomorfológicos: base para el levantamiento de suelos en Tabasco, México', 'Ecosistemas y Recursos Agropecuarios', 'Publicado', 'Si', 'francisco.bautista^j.zavala.cruz^r.jimenez.ramirez^d.palma.lopez^f.gavi.reyes', 'r.jimenez.ramirez', '', 'Ecos Rec Agro', '2016', '3', '8', '2007-901X', '161', '171', '358645282002', ''),
('Panorama contemporáneo del ordenamiento ecológico territorial en México.', 'Polígonos, Revista de Geografía', 'Publicado', 'No', 'manuel.bollo^lm.espinosa.rodriguez', '', 'Latindex', '', '2014', '1', '26', '1132-1202. ', '111', '146', '', ''),
('Participatory evaluation of food and nutritional security through sustainability indicators in a highland peasant system in Guatemala', 'Journal of Rural Studies', 'Enviado', 'No', 'marta.astier', '', '', 'J Rural Stud', '2016', 'N/A', 'N/A', '0743-0167', '0', '0', '', ''),
('Participatory Mapping of the Geography of Risk: Risk Perceptions of Children and Adolescents in Two Portuguese Towns', 'Children, Youth and Environments', 'Publicado', 'No', 'keith.mccall^mario.freitas^luis.dourado', '', '', 'CYE', '2016', '26', '1', '', '85', '110', '', ''),
('Participatory methods in the Georgian Caucasus: Understanding vulnerability and response to debrisflow hazards.', 'International Journal of Geosciences', 'Publicado', 'No', 'keith.mccall^  Spanu, Valentina, \nGaprindashvili, George; \n', '', '', 'IJGeosci', '2015', '6', 'N/A', '2156-8359', '666', '674', '0.4236/ijg.2015.67054', ''),
('Patrones Espacio-Temporales En La Condicion Microbiológica Del Agua En Fuentes Comunitarias Y Amenazas A La Salud Familiar En Cuencas Estacionales Del Bajo Balsas (México)', 'Revista Internacional de Contaminación Ambiental', 'Aceptado', 'No', 'rosaura.paez^ana.burgos^margarita.alvarado^ruben.hernandez', 'margarita.alvarado', '', 'Rev. Int. Contam. Ambie.', '2016', 'N/A', 'N/A', '0188-4999 ', '0', '0', '', ''),
('Patterns of distribution along environmental gradients of nine Quercus species in central Mexico', 'Botanical Sciences', 'Publicado', 'No', 'r.aguilar.romero^f.garcía.oliva^f.pineda.garcia^i.torres.garcia^f.pena.vega^adrian.ghilardi^ken.oyama', 'r.aguilar.romero^i.torres.garcia', 'WOS: SCI/SSCI/SCI-EX', '', '2016', '94', '3', '2007-4476', '471', '482', '10.17129/botsci.620', ''),
('Pensamiento geográfico en América Latina: retrospectiva y balances generales', 'Investigaciones Geográficas', 'En prensa', 'No', 'gerardo.bocco^pedro.urquijo', 'paola.segundo', 'Scopus; Revistas CONACYT; RedALyC', '', '2016', 'NA', '90', '0188-4611', '0', '0', '', ''),
('Percepción del cambio climático en comunidades campesinas de la Reserva de la Biosfera La Encrucijada, Chiapas, México', 'Cuadernos Geográficos', 'Enviado', 'No', 'sara.barrasa', '', 'ISI Web of Knowledge; Scopus; RedALyC', '', '2016', 'N/A', 'N/A', '0210-5462 ', '1', '24', '', ''),
('Peri-urban local governance? Intra-government relationships and social capital in a peripheral municipality of Michoacán, Mexico', 'Progress in Development Studies Journal', 'Aceptado', 'No', 'lourdes.gonzalez^lorena.poncela^antonio.vieyra^yadira.mendez', '', 'WOS: SCI/SSCI/SCI-EX', 'PiDS', '2016', 'N/A', 'N/A', '1464-9934', '0', '0', '', ''),
('Periurbanization, agricultural livelihoods and ejidatarios´ social capital: Lessons from a periphery municipality in Michoacán, Mexico', 'Procedia Engineering', 'Enviado', 'No', 'yadira.mendez^antonio.vieyra^lorena^poncela', '', ' Scopus', '', '2016', 'n/a', 'n/a', '1877-7058 ', '0', '0', '', ''),
('Plant management in agroforestry systems of rosetophyllous forests in the Tehuacán Valley, Mexico', 'Economic Botany', 'Aceptado', 'No', 'mariana.vallejo^nadia.campos^alejandro.casas^ana.moreno', 'nadia.campos', '', ' ECON BOT', '2016', 'N/A', 'N/A', '0013-0001^1874-9364', '0', '0', 'DOI:10.1007/s12231-016-9352-0', ''),
('Policy for pro-poor distribution of REDD+ benefits in Mexico: how the legal and technical challenges are being addressed. ', 'Forest Policy and Economics', 'Aceptado', 'No', 'margaret.skutsch^arturo.balderas', '', '', '', '2017', 'na', 'na', ' 1389-9341', '0', '0', '', ''),
('Politics of material agency in vulnerable places ', 'Science Technology and Human Values', 'Enviado', 'No', 'frida.guiza^peter.simmons', '', '', 'SCI TECHNOL HUM VAL', '2016', 'n/a', 'n/a', '', '0', '0', '', ''),
('Potencial para la conservación de la geodiversidad de los paisajes del Estado de Michoacán, México', 'Perspectiva Geográfica', 'Aceptado', 'No', 'angel.priego^luis.ramirez^manuel.bollo', '', 'Clase; Latindex; Otros indices', 'Perspectiva Geográfica', '2017', 'N/A', 'N/A', '0123-3769', '1', '15', '', ''),
('Potential distribution of mountain cloud forest in Michoacan, Mexico: prioritization for conservation in the context of landscape connectivity', 'Environmental Management', 'Enviado', 'No', 'manuel.mendoza^camilo.correa^andres.etter^diego.perez', 'camilo.correa', '', '', '2016', 'N/A', 'N/A', '', '0', '0', '', ''),
('Potential Species Distribution and Richness of Ixodidae Ticks Associated with Wild Vertebrates from Michoacán, Mexico. ', 'Journal Of Geographic Information System', 'Publicado', 'No', 'angel.priego^m.vargas.sandoval^alejandra.larrazabal', '', 'ISI Web of Knowledge; Otros indices', 'JGIS', '2014', 'N/A', '6', '2151 1969', '467', '477', 'http://dx.doi.org/10.4236/jgis.2014.65040', ''),
('Preface to this Virtual Thematic Issue: Modelling with Stakeholders II', 'Environmental Modelling & Software', 'Publicado', 'Si', 'keith.mccall^alexey.voinov^nagesh.kolagani', '', '', 'envsoft', '2016', '77', 'N/A', '1364-8152', '153', '155', 'DOI: 10.1016/j.envsoft.2016.01.006', ''),
('Procesos De Cambio De Cobertura Y Uso De Suelo En Cuencas Tropicales Costeras Del Pacifico Central Mexicano', 'Investigaciones Geográficas', 'Enviado', 'No', 'manuel.mendoza^alejandro.nene^gaspar.gonzalez^francisco.silva', 'alejandro.nene', '', '', '2016', 'NA', 'NA', '', '0', '0', '', ''),
('Procesos participativos intramunicipales como pasos hacia la gobernanza local en territorios periurbanos. La experiencia en el municipio de Tarímbaro, Michoacán, México', 'Journal of Latin America Geography', 'Publicado', 'Si', 'yadira.mendez^lorena.poncela^antonio.vieyra', 'lorena.poncela', ' Latindex; Otros indices', 'JLAG', '2015', '14', '2', '1545-2476', '129', '157', 'DOI: 10.1353/lag.2015.0027', ''),
('Productive identities and community conditions for rural tourism in Mexican tropical drylands', 'Tourism Geographies', 'Publicado', 'No', 'ana.burgos^maxime.kieffer', 'maxime.kieffer', '', '', '2015', '17', '4', '', '561', '585', 'http://dx.doi.org/10.1080/14616688.2015.1043576', ''),
('Promoting local sustainable development and mitigating climate change in indigenous communities of México', 'Climatic Change', 'Publicado', 'No', 'marta.astier^ayesa.martinez^omar.masera', '', '', '', '2015', 'N/A', 'N/A', '1573-1480 ', '1', '15', '10.?1007/?s10584-015-1523-y', ''),
('Propiedades magnéticas y color de polvos urbanos como indicadores proxy de contaminación por metales pesados', 'Latinmag Letters', 'Publicado', 'Si', 'francisco.bautista^avto.gogichaishvili^o.delgado.carranza^raul.cejudo^jaime.morales', '', '', 'Latinmag Letters', '2015', '3', 'N/A', '', '0', '0', '', ''),
('Quantifying the Mexican forest carbon sink', 'Environmental Research Letters', 'Enviado', 'Si', 'jaime.paneque^margaret.skutsch^adrian.ghilardi^arturo.balderas', '', '', 'Env. Res. Let.', '2016', 'N/A', 'N/A', '1748-9326', '0', '0', '', ''),
('Recognized but not supported: Assessing the incorporation of non-timber forest products into Mexican forest policy.  ', 'Forest Policy and Economics', 'Publicado', 'No', 'keith.mccall^tzitzi.sharhi^citlalli.lopez', 'tzitzi.sharhi', '', 'ForPE', '2016', '71', 'N/A', '1389-9341', '36', '42', '', ''),
('Recuento Nacional  De Los Conflictos Mineros Territoriales En México.', 'Les Cahiers des Amériques Latines', 'Aceptado', 'No', 'claudio.garibay', 'sol.perez', '', 'Les Cahiers des Amériques Latines', '2016', 'NA', 'NA', '', '1', '2', '', ''),
('Regional climate on the breeding grounds predicts variation in the natal origin of monarch butterflies overwintering in Mexico over 38 years', 'Global Change Biology', 'Aceptado', 'No', 'maria.ramirez^tyler.flockhart^lincoln.brwoer^keith.hobson^leonard.wassenaar^sonia.altizer^ryan.morris', '', 'WOS: SCI/SSCI/SCI-EX', 'GCB', 'N/A', 'n/a', 'n/a', '1365-2486', '0', '0', '', ''),
('Regional Landscape Change in Fishing Communities of the Mexican North Pacific', 'Landscape Research', 'Publicado', 'No', 'gerardo.bocco^pablo.alvarez^georges.seingier^ileana.espejel^julie.noriega', 'pablo.alvarez', '', 'LR', '2015', '40', '7', '', '855', '874', '10.1080/01426397.2015.1031095', 'http://dx.doi.org/10.1080/01426397.2015.1031095'),
('Relación entre la heterogeneidad del paisaje y la riqueza de especies de flora en cuencas costeras del estado de Veracruz, México. ', 'Investigaciones Geográficas', 'Publicado', 'No', 'angel.priego^p.moreno.casasola^jl.palacio.prieto^ja.lopez.portillo^d.geissert.kientz', '', 'Latindex; Scopus; SciELO; Revistas CONACYT; RedALyC; Otros indices', 'INVESTIGACIONES GEOGRÁFICAS ', '2003', 'N/A', '52', '0188-4611', '31', '51', '', ''),
('Relationship between landscape heterogeneity and plant species richness in the Mexican Pacific coast.', 'Applied Geography', 'Publicado', 'No', 'angel.priego^gerardo.bocco^lg.ramirez.sanchez', 'lg.ramirez.sanchez', 'WOS: SCI/SSCI/SCI-EX; Scopus; Otros indices', '', '2013', 'N/A', '40', '0143-6228', '171', '178', '', ''),
('Religión y naturaleza en la construcción de la identidad de los teenek potosinos', 'Espacio y tiempo, Revista latinoamericana de Ciencias Sociales y humanidades', 'Publicado', 'No', 'pedro.urquijo', '', '', '', '2008', 'NA', '1', '', '19', '30', '', ''),
('Remoteness and remote places. A geographic perspective', 'Geoforum', 'Aceptado', 'No', 'gerardo.bocco', '', 'Scopus; Otros indices', 'Geoforum', '2016', 'N/A', 'N/A', '', '0', '0', '', ''),
('Repensando una época. Aproximación semiótica a los estilos alfareros de inicios del período Tardío en Yocavil por medio del caso \x93Lorohuasi\x94. ', 'Boletín del Museo Chileno de Arte Precolombino', 'Publicado', 'No', 'alina.alvarez^solange.grimoldi', '', 'Latindex; SciELO; RedALyC', '', '2015', '20', '2', '0716-1530', '23', '55', 'http://boletinmuseoprecolombino.cl/wp/wp-content/uploads/2016/01/02-PALAMARCZUK-PRECOLOMBINO-202.pdf', ''),
('Resiliencia, vulnerabilidad y sustentabilidad de sistemas socioecológicos en México', 'Revista mexicana de biodiversidad', 'Aceptado', 'No', 'marta.astier^patricia.balvanera^francisco.gurri^isela.zarmeno', '', '', '', '2016', 'N/A', 'N/A', '1870-3453', '1', '3', '', ''),
('Riesgo volcánico: Estado del arte y desafíos de trabajo', 'Boletín de la Sociedad Geológica Mexicana', 'Enviado', 'No', 'manuel.mendoza^gemma.gomez^luis.macias^erna.lopez', 'gemma.gomez', '', '', '2016', 'N/A', 'N/A', '', '0', '0', '', ''),
('Rural people\x92s knowledge and perception of landscape: A case study from the Mexican Pacific coast. ', 'Society & Natural Resources', 'Publicado', 'No', 'angel.priego^m.campos.sanchez^gerardo.bocco^alejandro.velazquez^m.boada.junca', '', 'Otros indices', '', '2012', 'N/A', '25', '0894-1920 ', '759', '774', '', ''),
('Sex Ratio and Sex-Specific Latitudinal Variation in Floral Characteristics of Gynodioecious Kallstroemia grandiflora (Zygophyllaceae) in Mexico', 'Biotropica', 'Publicado', 'No', 'gabriela.cuevas', '', '', '', '2010', '43', '3', '1744-7429', '317', '323', '10.1111/j.1744-7429.2010.00692.x.', ''),
('Shifting Boundaries of Volunteered Geographic Information Systems and Modalities: Learning from PGIS. ', 'ACME An International E-Journal for Critical Geographies  ', 'Publicado', 'Si', 'keith.mccall^javier.martinez^jeroen.verplanke', '', '', 'ACME', '2015', '14', '3', '1492-9732 ', '791', '826', '', ''),
('Si no comemos tortilla, no vivimos: women, climate change, and food security in central Mexico', 'Agriculture and Human Values', 'Publicado', 'No', 'gabriela.cuevas', '', '', '', '2014', '31', '4', '0889-048X', '607', '620', '10.1007/s10460-014-9503-9', ''),
('Small Drones for Community-Based Forest Monitoring: An Assessment of Their Feasibility and Potential in Tropical Areas', 'Forests', 'Publicado', 'Si', 'brian.napoletano^jaime.paneque^keith.mccall', '', '', 'For', '2014', '5', '6', '1999-4907', '1481', '1507', '10.3390/f5061481', ''),
('Socio-economic and environmental changes related to maize richness in Mexico\x92s central highlands', 'Agriculture and Human Values', 'Publicado', 'Si', 'marta.astier^quetzalcoatl.orozco', '', '', 'Agric Hum Values', '2016', 'N/A', 'N/A', '1572-8366', '0', '0', '10.1007/s10460-016-9720-5', ''),
('Soil & Environment as a tool for soil environmental functions evaluation', 'Programmnye produkty i sistemy', 'Publicado', 'Si', 'francisco.bautista^angeles.gallegos^inna.dubrovina', 'angeles.gallegos', 'Otros indices', '', '2016', '2', '3', '2311-2735', '195', '200', '10.15827/0236-235X.114.195-200', ''),
('Somos en el mundo: seres, materialidad y paisajes', 'La Zaranda de Ideas', 'Publicado', 'No', 'alina.alvarez', '', 'SciELO; Latindex; Scopus; Otros indices', '', '2012', '8', 'n/a', '1853-1296^1853-1296 ', '10', '31', 'http://lazaranda.wix.com/lazarandadeideas', ''),
('Soria 3. Nuevas evidencias de la ocupación aldeana temprana en Yocavil, Noroeste argentino', 'Revista Española de Antropología Americana', 'Enviado', 'Si', 'alina.alvarez^romina.spano^solange.grimoldi', '', 'Latindex; Scopus; RedALyC', 'REAA', '2016', 'n/a', 'n/a', '0556-6533', '0', '0', 'http://revistas.ucm.es/index.php/REAA', ''),
('Spatial fix and metabolic rift as conceptual tools in land-change science', 'Capitalism Nature Socialism', 'Publicado', 'No', 'brian.napoletano^jaime.paneque^antonio.vieyra', '', '', 'CNS', '2015', '26', '4', '0972-4923^0975-3133', '198', '214', '10.1080/10455752.2015.1104706', ''),
('Spatiotemporal modeling of fuelwood environmental impacts: Towards improved accounting for non-renewable biomass', 'Environmental Modelling & Software', 'Publicado', 'No', 'jean.mas^adrian.ghilardi^bailis.espinoza^margaret.skutsch^omar.masera', '', 'WOS: SCI/SSCI/SCI-EX; ISI Web of Knowledge; Scopus', ' Env. Model. & Soft.', '2016', '82', 'N/A', '1364- 8152', '241', '254', '10.1016/j.envsoft.2016.04.023', ''),
('State formation and territorialization in forest lands: historical and geographical evolution of forest conflicts in the state of Michoacán, Mexico', 'Annals of the American Association of Geographers', 'Enviado', 'No', 'jaime.paneque^irene.perez^irene.perez^maria.ramirez^claudio.garibay^pedro.urquijo', '', '', 'An. Amn. Ass. Geog.', '2016', 'N/A', 'N/A', '1467-8306', '0', '0', '', ''),
('Statistical spatial model for multifactorial analyisis of landslides: the case of the municipality of Francisco León, Chiapas', 'Geomorphology', 'Enviado', 'No', 'manuel.mendoza^luis.morales^vm.hernandez.madrigal^jc.mora.chaparro', 'arturo.muniz', '', '', '2015', 'N/A', 'N/A', '', '0', '0', '', ''),
('Supporting environmental and Natural Resources Management. The National Institute of Ecology of Mexico', 'GIM International', 'Publicado', 'No', 'gabriela.cuevas^gerardo.bocco', '', '', '', '2004', '18', '4', '', '69', '71', '', ''),
('Sustainable bioenergy options for Mexico: GHG mitigation and costs', 'Renewable and Sustainable Energy Reviews', 'Publicado', 'No', 'adrian.ghilardi^margaret.skutsch^omar.masera', '', 'WOS: SCI/SSCI/SCI-EX', 'RENEW SUST ENERG REV', '2015', '43', 'N/A', '1364-0321', '545', '552', '10.1016/j.rser.2014.11.062', ''),
('TEK and biodiversity management in agroforestry systems of different socio-ecological contexts of the Tehuacán Valley', 'Journal of Ethnobiology and Ethnomedicine', 'Aceptado', 'No', 'mariana.vallejo^ana.moreno^alejandro.casas', '', '', 'J ETHNOBIOL ETHNOMED', '2016', 'N/A', 'N/A', '1746-4269', '0', '0', '10.1186/s13002-016-0102-2', ''),
('Tendencias recientes de las superficies ocupadas por el lago de Cuitzeo. Un enfoque basado  en percepción remota, sistemas de información geográfica y análisis estadístico', 'Boletín del Instituto de Geografía', 'Publicado', 'No', 'hugo.zavala^manuel.mendoza^gerardo.bocco^erna.lopez^miguel.bravo', '', '', 'Boletín del Instituto de Geografía', '2007', 'Núm. 64', 'Núm. 64', '0188-4611', '43', '62', '', ''),
('The App SOC + a tool to estimate or/and calculate organic carbon in the soil profile', 'Journal of Applied Research and technology', 'Publicado', 'Si', 'francisco.bautista^eduardo.garcia^angeles.gallegos', 'angeles.gallegos', '', 'J App R T', '2016', '14', '2', '1665-6423', '135', '139', 'doi.org/10.1016/j.jart.2016.03.002', ''),
('The carbon footprint of traditional woodfuels', 'Nature Climate Change', 'Publicado', 'No', 'adrian.ghilardi^omar.masera^bailis.espinoza', '', 'WOS: SCI/SSCI/SCI-EX', '', '2015', '5', 'N/A', '1758-678X', '266', '272', '10.1038/nclimate2491', ''),
('The contribution of physical geography to environmental public policy in México. ', 'Singapore Journal Of Tropical Geography', 'Publicado', 'No', 'angel.priego^gerardo.bocco', '', 'WOS: SCI/SSCI/SCI-EX; Otros indices', 'TROPICAL GEOGRAPHY ', '2010', 'N/A', '31', '0129-7619', '215', '223', '', ''),
('The importance of the traditional fire knowledge system in a subtropical montane socio-ecosystem in a protected natural area', 'International Journal of Wildland Fire', 'Publicado', 'No', 'maria.ramirez^leonardo.martinez^alicia.castillo^diego.perez', 'leonardo.martinez', 'WOS: SCI/SSCI/SCI-EX; Scopus', 'IntlJWildlandFire', '2016', '25', '9', '1049-8001', '911', '921', '10.1071/WF15181', ''),
('The networked agency of flash flood\x92s materiality and its socioenvironmental processes, exhibit power performances and inequalities ', 'Geoforum', 'Aceptado', 'No', 'frida.guiza^peter.simmons', '', '', 'Geoforum', '2015', 'n/a', 'n/a', '0016-7185', '0', '0', '', ''),
('The Place of Community Forest Management in the REDD+ Landscape', 'Forests', 'Publicado', 'No', 'margaret.skutsch', '', '', '', '2016', '7', '170', '', '0', '0', 'doi:10.3390/f7080170', ''),
('The science and policy of REDD+ in a sink: Case of Mexico', 'Environmental Science && Policy', 'Enviado', 'No', 'margaret.skutsch^jaime.paneque^adrian.ghilardi^jorge.morfin^josemaria.michel^oswaldo.carrillo', '', '', 'Env. Sci. Pol.', '2016', 'N/A', 'N/A', '1462-9011', '0', '0', '', ''),
('Three approaches to the assessment of spatio-temporal distribution of the water balance: the case of the Cuitzeo basin, Michoacán, Mexico. ', 'Boletín del Instituto de Geografía', 'Publicado', 'No', 'hugo.zavala^alfredo.amador^erna.lopez^manuel.mendoza', '', '', '', '2011', 'Núm. 76', 'N/A', '0188-4611', '34', '55', '', ''),
('Toward a near-real time forest monitoring system (Technical note)', 'Investigaciones Geográficas', 'Publicado', 'Si', 'jean.mas^Lemoine,rodríguez^hind.taud', '', 'Latindex; Revistas CONACYT', '', '2016', 'N/A', '91', '0188- 4611', '168', '175', '10.14350/rig.48600', ''),
("Traditional ecological knowledge and tropical forest conservation. A spatial analysis among Tsimane' Amerindians (Bolivian Amazon)", 'Global Environmental Change', 'Enviado', 'No', 'jaime.paneque^irene.perez^maximilien.gueze^jean.mas^manuel.macia^marti.orta^victoria.reyes', 'irene.perez', '', 'Glob. Environ. Chang.', '2016', 'N/A', 'N/A', '', '0', '0', '', ''),
('Ubicación de los sitios de muestreo, generos de bacterias identificadas y fuentes de origen de las muestras en la CASPJ', 'Ciencia Nicolaita', 'Enviado', 'No', 'jose.navarrete^maria.carmona', ' ', '', ' ', '2015', ' ', ' ', ' ', '1', '1', ' ', ' '),
('Un hallazgo funerario en Shiquimil, Provincia de Catamarca. Bioarqueología y estilos alfareros de inicios del período Tardío en Yocavil', 'Arqueología', 'Publicado', 'No', 'alina.alvarez^solange.grimoldi^v.palamarczuk', '', 'Latindex; Scopus; SciELO', '', '2012', '18', 'n/a', '0327-5159^1853-8126', '11', '37', 'http://revistascientificas.filo.uba.ar/index.php/Arqueologia/about/submissions#onlineSubmissions', ''),
('Unequal Partners, Unequal Exchange: Goldcorp, the Mexican State and Campesino Dispossession at the Peñasquito goldmine', 'Journal of Latin America Geography', 'Publicado', 'No', 'pedro.urquijo^claudio.garibay^andrew.boni', 'andrew.boni', '', '', '2011', '10', '2', '1545-2476', '153', '176', '', ''),
('Urbanscapes of disaster. The sociopolitical and environmental factors underpinning a disaster processes within a vulnerable slum in Mexico.', 'City and Community', 'Aceptado', 'No', 'frida.guiza^yadira.mendez^keith.mccall', '', '', 'CITY COMMUNITY', '2015', 'n/a', 'n/a', '1540-6040', '0', '0', '', '53/142 '),
('Uso comunitario de pequeños vehículos aéreos no tripulados (drones) en conflictos ambientales: ¿un factor innovador desequilibrante? ', 'Teknokultura. Revista de Cultura Digital y Movimientos Sociales', 'En prensa', 'Si', 'jaime.paneque^nicolas.vargas^marcela.morales', '', '', 'Teknokultura', '2016', '13', '2', '', '0', '0', '', ''),
('Validation of MODIS Vegetation Continuous Fields for monitoring deforestation and forest degradation: two cases in Mexico', 'Geocarto International', 'Publicado', 'Si', 'adrian.ghilardi^yan.gao^jean.mas^jaime.paneque^margaret.skutsch ', '', 'WOS: SCI/SSCI/SCI-EX', '', '2016', '31', '9', '1752-0762', '1019', '1031', '10.1080/10106049.2015.1110205', ''),
('Vegetación original y actual de un sector de las playas del Este de Ciudad de La Habana, Cuba. ', 'Fontqueria', 'Publicado', 'No', 'angel.priego', '', 'Latindex; Otros indices', '', '1993', 'N/A', '36', '0212-0623', '429', '437', '', ''),
('Visibility analysis and landscape evaluation in Martin River Cultural Park (Aragon, Spain) integrating biophysical and visual units', 'Journal of Maps', 'Publicado', 'Si', 'brian.napoletano^ivan.franch^luis.cancer', '', '', 'JORN MAPS', 'N/A', 'Aceptado', 'N/A', '', '0', '0', '', ''),
('Volcaniclastic reworked sediments in the Usumacinta River, Mexico: the serendipitous source of volcanic glass for Maya ceramics', 'Geoarchaeology', 'En prensa', 'Si', 'berenice.solis^hector.cabadas^elizabeth.solleiro^sergey.sedov^keiko.tatanisho^rodrigo.liendo', '', '', '', '2016', 'NA', 'NA', '1520-6548', '0', '0', '', ''),
('Vulnerable and invisible: impact of hurricane activity on a peasant population in a mountainous region on the Mexican Pacific coast', 'Journal of Latin America Geography', 'Publicado', 'No', 'gerardo.bocco^itzi.segundo', 'itzi.segundo', '', 'JLAG', '2015', '14', '2', '', '159', '179', '', ''),
('Zonificación funcional ecoturística de la zona costera de Michoacán, México a escala 1:250 000.', 'Revista Geográfica De América Central', 'Publicado', 'No', 'angel.priego^angel.flores', 'angel.flores', 'Latindex; Otros indices', '', '2011', 'N/A', 'Número Especial EGAL 2011 ', '2115-2563', '1', '15', '', ''),
('Zonificación geoecológica del paisaje urbano', 'Mercator', 'Publicado', 'No', 'manuel.bollo^ayesa.martinez', 'ayesa.martinez', 'Latindex; SciELO; RedALyC', '', '2016', ' v.15,', '2', '1676-8329', '117', '136', '10.4215/RM2016.1502. 0008', ''),
('Yes-in-my-backyard: spatial differences in the valuation of forest services and local co-benefits for carbon markets in México.', 'Ecological Economics', 'Publicado', 'No', 'margaret.skutsch^arturo.balderas', '', '', 'Ecolecon', '2015', '109', 'N/A', '', '130', '141', 'doi:10.1016/j.ecolecon.2014.11.008', ''),
('Acceso al suelo ejidal en la periferia urbana mexicana: Análisis desde el Capital Social', 'Economía, Sociedad y territorio', 'Aceptado', 'Si', 'yadira.mendez^sandra.pola^antonio.vieyra', 'sandra.pola', '', 'EST', '2016', 'N/A', 'N/A', '1405-8421', '0', '0', '', ''),
('Estudio del metabolismo social del aguacate en Michoacán, México. Una aproximación agroecológica encaminada al entendimiento y recuperación de sistemas de cultivo tradicionales', 'Sociedad Española de Agricultura Ecológica (SEAE)', 'Publicado', 'No', 'mario.figueroa^zirion.martinez^marta.astier', 'zirion.martinez', '', 'SEAE', '2016', 'N/A', 'N/A', '', '1', '6', '', ''),
('How social capital enables/restricts the livelihoods of poor peri-urban farmers in Mexico', 'Development in Practice', 'Aceptado', 'No', 'yadira.mendez^antonio.vieyra', '', '', 'DiP', '2016', 'N/A', 'N/A', '0961-4524^1364-9213', '0', '0', '', ''),
('La comunicación científica en contextos de complejidad: el acceso abierto\x94  Poster en  Año 17 vols. 57 y 58.  Red de Convergencia del Conocimiento para Beneficio de la Sociedad, Laboratorio Nacional de Informática Avanzada, A.C. México', 'LANIA Newsletter', 'Publicado', 'Si', 'saray.bucio^hebe.vessuri', '', '', '', '2016', '17', '57/58', '', '0', '0', '', '')
)

# select titulo, revista, becarios, electronica, autores_iimas, alumnos, indices, abreviado, anio, volumen, numeros, issn, pagina_i, pagina_f, doi, isiut from ir_articuloscientificos

for i in articulos:
    if i[3] == Si:
        solo_electronico = True
    else:
        solo_electronico = False

    autores = i[4].split('^')
    alumnos = i[5].split('^')
    indices = i[6].split(';')

    a = ArticuloCientifico(titulo=i[0], tipo='ARTICULO', revista=i[1], status=i[2], solo_electronico=solo_electronico, nombre_abreviado_wos=i[7], fecha=date()  )

