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

articulos = (
    ['Charcoal contribution accumulation at different scales of production among the rural population of Mutomo District in Kenya', 'Energy for Sustainable Development', '33', '', 2016, '0973-0826', 'PUBLICADO', 'No', 'adrian.ghilardi', 'Web of Science: SCI/SSCI/SCI-EX', 167, 175, '10.1016/j.esd.2016.05.002'],
    ['Spatiotemporal modeling of fuelwood environmental impacts: towards improved accounting for non-renewable biomass', 'Environmental Modelling & Software', '82', '', 2016, '1364-8152', 'PUBLICADO', 'No', 'adrian.ghilardi^bailis.espinoza^jean.mas^margaret.skutsch^omar.masera', 'Web of Science: SCI/SSCI/SCI-EX', 241, 254, '10.1016/j.envsoft.2016.04.023'],
    ['Análisis de la producción de carbón vegetal en la Cuenca del Lago de Cuitzeo, Michoacán, México: implicaciones para una producción sustentable', 'Investigación Ambiental', '6', '2', 2014, '2007-4492', 'PUBLICADO', 'No', 'adrian.ghilardi^ken.oyama^omar.masera', 'Otros indices', 127, 138, ''],
    ['Sustainable bioenergy options for Mexico: GHG mitigation and costs', 'Renewable and Sustainable Energy Reviews', '43', '', 2015, '1364-0321', 'PUBLICADO', 'No', 'adrian.ghilardi^margaret.skutsch^omar.masera', 'Web of Science: SCI/SSCI/SCI-EX', 545, 552, '10.1016/j.rser.2014.11.062'],
    ['The carbon footprint of traditional woodfuels', 'Nature Climate Change', '5', '', 2015, '1758-678X', 'PUBLICADO', 'No', 'adrian.ghilardi^omar.masera^bailis.espinoza', 'Web of Science: SCI/SSCI/SCI-EX', 266, 272, '10.1038/nclimate2491'],
    ['Environmental Burden of Traditional Bioenergy Use', 'Annual Review of Environment and Resources', '40', '', 2015, '1543-5938', 'PUBLICADO', 'No', 'adrian.ghilardi^omar.masera^bailis.espinoza', 'Web of Science: SCI/SSCI/SCI-EX', 121, 150, '10.1146/annurev-environ-102014-021318'],
    ['Evaluation of annual modis PTC data for deforestation and forest degradation analysis', 'International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences - ISPRS Archives', '', '', 2016, '', 'PUBLICADO', 'Si', 'adrian.ghilardi^yan.gao^jean.mas^jaime.paneque^margaret.skutsch', 'Scopus', 9, 13, '10.5194/isprsarchives-XLI-B2-9-2016'],
    ['Management-sensitive hierarchical typology for riparian zones based on biophysical features: a procedure', 'Physical Geography', '', '', 2017, '', 'ENVIADO', 'No', 'adriana.flores^roger.guevara^manuel.mendoza^rosario.langrave^miguel.maass', 'Web of Science: SCI/SSCI/SCI-EX; Otros indices', 0, 0, ''],
    ['Componentes del paisaje como predictores de cubiertas de vegetación: estudio de caso del estado de Michoacán, México', 'Investigaciones Geográficas, Boletín del Instituto de Geografía', '90', '', 2016, '0188-4611', 'PUBLICADO', 'No', 'luis.gopar', 'Web of Science: SCI/SSCI/SCI-EX; Latindex', 75, 88, 'dx.doi.org/10.14350'],
    ['Elementos del paisaje como predictores de tipos de cubiertas de vegetación', 'Investigaciones Geográficas, Boletín del Instituto de Geografía', '', '', 2015, '', 'EN_PRENSA', 'No', 'luis.gopar^alejandro.velazquez', 'Otros indices', 1, 10, 'http://dx.doi.org/10.14350/rig.46688'],
    ['Bioclimatic mapping as a new method to assess effects of climatic change', 'Ecosphere Journal', '6', '1', 2015, '', 'PUBLICADO', 'Si', 'luis.gopar^alejandro.velazquez^joaquin.gimenez', 'Otros indices', 1, 12, '10.1890/ES14-00138.1'],
    ['Implementación del Índice de Condición Forestal (ICF), Como un insumo para el diseño de políticas públicas de corte forestal en México', 'Investigaciones Geográficas, Boletín del Instituto de Geografía', '', '', 2016, '0188-4611', 'ACEPTADO', 'No', 'neyra.sosa^alejandro.velazquez^dante.ayala^gerardo.bocco^luis.gopar', 'Revistas CONACYT; Web of Science: SCI/SSCI/SCI-EX', 0, 0, 'dx.doi.org/10.14350'],
    ['Diseño de las políticas públicas de corte forestal en México: implicaciones para la gestión de la vulnerabilidad social y el territorio', 'Investigaciones Geográficas, Boletín del Instituto de Geografía', '', '', 2016, ' 0188-4611', 'EN_PRENSA', 'Si', 'neyra.sosa^alejandro.velazquez^dante.ayala^gerardo.bocco^luis.gopar', 'SciELO; Revistas CONACYT; Scopus; Latindex; RedALyC', 1, 13, '10.14350/rig.53915'],
    ['Habitar una región. Espacialidad arquitectónica y construcción de paisajes en Andalhuala, valle de Yocavil (Catamarca, Argentina)', 'Arqueología', '22', '', 2016, '0327-5159', 'EN_PRENSA', 'No', 'alina.alvarez', 'Scopus; SciELO; Latindex', 0, 0, ''],
    ['Paisajes agroalfareros del primer y segundo milenio DC en la Mesada de Andalhuala Banda (Yocavil, Noroeste argentino)', 'Ñawpa Pacha. Journal of Andean Archaeology', '36', '2', 2016, '0077-6297', 'PUBLICADO', 'No', 'alina.alvarez', 'Otros indices', 161, 184, 'http://www.instituteofandeanstudies.org/publications.html'],
    ['Don Mateo-El Cerro, a Newly Rediscovered Late Period Settlement in Yocavil (Catamarca, Argentina)', 'Andean Past', '12', '', 2016, '1055-8756', 'PUBLICADO', 'No', 'alina.alvarez', 'Otros indices', 0, 0, ''],
    ['El arte rupestre como geosigno del paisaje (valle de Yocavil, Catamarca, Argentina)', 'Comechingonia, Revista de Arqueología', '16', '2', 2012, '0326-7911', 'PUBLICADO', 'No', 'alina.alvarez', 'Latindex; SciELO', 55, 74, 'http://www.comechingonia.com/'],
    ['Somos en el mundo: seres, materialidad y paisajes', 'La Zaranda de Ideas', '8', '', 2012, '1853-1296', 'PUBLICADO', 'No', 'alina.alvarez', 'SciELO; Latindex; Scopus; Otros indices', 10, 31, 'http://lazaranda.wix.com/lazarandadeideas'],
    ['Arquitectura y paisajes en la localidad arqueológica de Andalhuala (valle de Yocavil, Catamarca)', 'Revista del Museo de Antropología', '3', '', 2010, '1852-O6OX', 'PUBLICADO', 'No', 'alina.alvarez', 'Latindex; SciELO; RedALyC', 33, 48, 'http://revistas.unc.edu.ar/index.php/antropologia'],
    ['Gran Gruta Grabada de Chiquimí. Noticia acerca de su hallazgo y redescubrimiento, 100 años después', 'Boletín del Museo Chileno de Arte Precolombino', '16', '1', 2011, '0716-1530', 'PUBLICADO', 'No', 'alina.alvarez^jp.carbonelli', 'SciELO; Latindex', 23, 46, 'http://www.precolombino.cl/biblioteca/boletin-del-museo/'],
    ['Soria 3. Nuevas evidencias de la ocupación aldeana temprana en Yocavil, Noroeste argentino', 'Revista Española de Antropología Americana', '', '', 2016, '0556-6533', 'ENVIADO', 'Si', 'alina.alvarez^romina.spano^solange.grimoldi', 'Latindex; Scopus; RedALyC', 0, 0, 'http://revistas.ucm.es/index.php/REAA'],
    ['Repensando una época. Aproximación semiótica a los estilos alfareros de inicios del período Tardío en Yocavil por medio del caso Lorohuasi', 'Boletín del Museo Chileno de Arte Precolombino', '20', '2', 2015, '0716-1530', 'PUBLICADO', 'No', 'alina.alvarez^solange.grimoldi', 'Latindex; SciELO; RedALyC', 23, 55, 'http://boletinmuseoprecolombino.cl/wp/wp-content/uploads/2016/01/02-PALAMARCZUK-PRECOLOMBINO-202.pdf'],
    ['Ollas como urnas, casas como tumbas: reflexiones en torno a las prácticas de entierro de niños en tiempos tempranos (Andalhuala Banda, sur de Yocavil)', 'Comechingonia, Revista de Arqueología', '', '', 2016, '0326-7911', 'ENVIADO', 'No', 'alina.alvarez^solange.grimoldi^romina.spano', 'SciELO; Latindex', 1, 1, ''],
    ['Un hallazgo funerario en Shiquimil, Provincia de Catamarca. Bioarqueología y estilos alfareros de inicios del período Tardío en Yocavil', 'Arqueología', '18', '', 2012, '0327-5159', 'PUBLICADO', 'No', 'alina.alvarez^solange.grimoldi^v.palamarczuk', 'Latindex; Scopus; SciELO', 11, 37, 'http://revistascientificas.filo.uba.ar/index.php/Arqueologia/about/submissions#onlineSubmissions'],
    ['La alfarería de inicios del segundo milenio en Yocavil. El problema San José y las tipologías cerámicas', 'Arqueología', '20', 'Dossier', 2014, '0327-5159', 'PUBLICADO', 'Si', 'alina.alvarez^v.palamarczuk^solange.grimoldi', 'RedALyC; Latindex; Scopus', 107, 134, 'https://sites.google.com/site/revistaarqueologia/'],
    ['Consumo de energía en el manejo de huertas de aguacate en  Michoacán, México', 'Revista Chapingo Serie Horticultura', '21', '1', 2015, '1027-152X', 'PUBLICADO', 'No', 'ana.burgos^carlos.anaya', 'Otros indices', 5, 20, '10.5154/r.rchsh.2014.01.002 '],
    ['Patrones espacio-temporales en la condición microbiológica del agua de fuentes comunitarias y amenazas a la salud familiar en cuencas estacionales del Bajo Balsas (México)', 'Revista Internacional de Contaminación Ambiental', '2', '33', 2017, '', 'EN_PRENSA', 'No', 'ana.burgos^margarita.alvarado^rosaura.paez^ruben.hernandez', 'Otros indices', 0, 0, ''],
    ['Productive identities and community conditions for rural tourism in Mexican tropical drylands', 'Tourism Geographies', '17', '4', 2015, '', 'PUBLICADO', 'No', 'ana.burgos^maxime.kieffer', '', 561, 585, 'http://dx.doi.org/10.1080/14616688.2015.1043576'],
    ['Ecotechnologies for the sustainable management of tropical forest diversity', 'Nature & Resources', '33', '1', 1997, '0028-0844', 'PUBLICADO', 'No', 'angel.priego', 'Otros indices', 2, 17, ''],
    ['Determinación de zonas prioritarias para la eco-rehabilitación de la cuenca Lerma-Chapala, México', 'Gaceta Ecológica, Nueva Época', '', '71', 2004, '1405-2849', 'PUBLICADO', 'No', 'angel.priego', 'Latindex; Otros indices', 79, 92, ''],
    ['Biophysical landscapes of a coastal area of Michoacán state in Mexico', 'Journal of Maps', '', '6', 2011, '1744-5647', 'PUBLICADO', 'No', 'angel.priego', 'Web of Science: SCI/SSCI/SCI-EX; Otros indices', 42, 47, ''],
    ['La dinámica ambiental de la cuenca Lerma-Chapala, México', 'Gaceta Ecológica, Nueva Época', '', '71', 2004, '1405-2849', 'PUBLICADO', 'No', 'angel.priego', 'Latindex; Otros indices', 23, 77, ''],
    ['Vegetación original y actual de un sector de las playas del Este de Ciudad de La Habana, Cuba', 'Fontqueria', '', '36', 1993, '0212-0623', 'PUBLICADO', 'No', 'angel.priego', 'Latindex; Otros indices', 429, 437, ''],
    ['Zonificación funcional ecoturística de la zona costera de Michoacán, México a escala 1:250 000', 'Revista Geográfica De América Central', '', 'Número Especial EGAL 2011', 2011, '2115-2563', 'PUBLICADO', 'No', 'angel.priego^angel.flores', 'Latindex; Otros indices', 1, 15, ''],
    ['The contribution of physical geography to environmental public policy in México', 'Singapore Journal Of Tropical Geography', '', '31', 2010, '0129-7619', 'PUBLICADO', 'No', 'angel.priego^gerardo.bocco', 'Web of Science: SCI/SSCI/SCI-EX; Otros indices', 215, 223, ''],
    ['La Geografía Física y el Ordenamiento Ecológico del Territorio. Experiencias en México', 'Gaceta Ecológica, Nueva Época', '', '76', 2005, '1405-2849', 'PUBLICADO', 'No', 'angel.priego^gerardo.bocco', 'Latindex; Otros indices', 23, 34, ''],
    ['Relationship between landscape heterogeneity and plant species richness in the Mexican Pacific coast', 'Applied Geography', '', '40', 2013, '0143-6228', 'PUBLICADO', 'No', 'angel.priego^gerardo.bocco^lg.ramirez.sanchez', 'Web of Science: SCI/SSCI/SCI-EX; Scopus; Otros indices', 171, 178, ''],
    ['Paisajes físico-geográficos de los manglares de la laguna de La Mancha, Veracruz, México', 'Interciencia, Revista de Ciencia y Tecnología de América Latina', '31', '3', 2006, '0378-1844', 'PUBLICADO', 'No', 'angel.priego^h.hernandez.trejo^ja.lopez.portillo^ja.lopez.portillo^e.vera.isunza', 'Web of Science: SCI/SSCI/SCI-EX; Latindex; Otros indices', 211, 219, ''],
    ['Paisajes físico-geográficos de la cuenca Lerma-Chapala, México', 'Gaceta Ecológica, Nueva Época', '', '71', 2004, '1405-2849', 'PUBLICADO', 'No', 'angel.priego^helda.morales', 'Latindex; Otros indices', 11, 22, ''],
    ['Aplicación de los paisajes físico-geográficos en un sector de la cordillera Ibérica: La cuenca del río Martín (Aragón, España)', 'Interciencia, Revista de Ciencia y Tecnología de América Latina', '40', '6', 2015, '0378-1844', 'PUBLICADO', 'No', 'angel.priego^ivan.franch^manuel.bollo^luis.cancer', 'Web of Science: SCI/SSCI/SCI-EX; Latindex; SciELO; Otros indices', 381, 389, ''],
    ['Paisajes físico-geográficos de Cayo Guillermo, Ciego de Ávila, Cuba', 'Revista Del Jardín Botánico Nacional De Cuba', '', '20', 1999, '0253-5696', 'PUBLICADO', 'No', 'angel.priego^j.gonzález.areu^l.menéndez.carrera', 'Latindex; Otros indices', 159, 166, ''],
    ['Heterogeneidad del paisaje y riqueza de flora: Su relación en el archipiélago de Camagüey, Cuba', 'Interciencia, Revista de Ciencia y Tecnología de América Latina', '29', '3', 2004, '0378-1844', 'PUBLICADO', 'No', 'angel.priego^jl.palacio.prieto^p.moreno.casasola^ja.lopez.portillo^d.geissert.kientz', 'Web of Science: SCI/SSCI/SCI-EX; Latindex; Otros indices', 138, 144, ''],
    ['Potencial para la conservación de la geodiversidad de los paisajes del Estado de Michoacán, México', 'Perspectiva Geográfica', '', '', 2017, '0123-3769', 'ACEPTADO', 'No', 'angel.priego^luis.ramirez^manuel.bollo', 'Clase; Latindex; Otros indices', 1, 15, ''],
    ['An interdisciplinary approach to depict landscape change drivers: A case study of the Ticuiz agrarian community in Michoacan, Mexico', 'Applied Geography', '', '32', 2012, '0143-6228', 'PUBLICADO', 'No', 'angel.priego^m.campos.sanchez^alejandro.velazquez^gerardo.bocco^margaret.skutsch^m.boada.junca', 'Web of Science: SCI/SSCI/SCI-EX; Scopus; Otros indices', 409, 419, ''],
    ['Rural peoples knowledge and perception of landscape: A case study from the Mexican Pacific coast', 'Society & Natural Resources', '', '25', 2012, '0894-1920', 'PUBLICADO', 'No', 'angel.priego^m.campos.sanchez^gerardo.bocco^alejandro.velazquez^m.boada.junca', 'Otros indices', 759, 774, ''],
    ['Defining environmental management units based upon integrated landscape principles at the Pacific coast in Mexico', 'Interciencia, Revista de Ciencia y Tecnología de América Latina', '35', '1', 2010, '0378-1844', 'PUBLICADO', 'No', 'angel.priego^m.campos.sanchez^gerardo.bocco^alejandro.velazquez^m.boada.junca', 'Web of Science: SCI/SSCI/SCI-EX; Latindex; Revistas CONACYT; RedALyC; Otros indices', 33, 40, ''],
    ['Potential Species Distribution and Richness of Ixodidae Ticks Associated with Wild Vertebrates from Michoacán, Mexico', 'Journal Of Geographic Information System', '', '6', 2014, '2151 1969', 'PUBLICADO', 'No', 'angel.priego^m.vargas.sandoval^alejandra.larrazabal', 'Web of Science: SCI/SSCI/SCI-EX; Otros indices', 467, 477, 'http://dx.doi.org/10.4236/jgis.2014.65040'],
    ['Relación entre la heterogeneidad del paisaje y la riqueza de especies de flora en cuencas costeras del estado de Veracruz, México', 'Investigaciones Geográficas, Boletín del Instituto de Geografía', '', '52', 2003, '0188-4611', 'PUBLICADO', 'No', 'angel.priego^p.moreno.casasola^jl.palacio.prieto^ja.lopez.portillo^d.geissert.kientz', 'Latindex; Scopus; SciELO; Revistas CONACYT; RedALyC; Otros indices', 31, 51, ''],
    ['Spatial fix and metabolic rift as conceptual tools in land-change science', 'Capitalism Nature Socialism', '26', '4', 2015, '1045-5752', 'PUBLICADO', 'No', 'antonio.vieyra^brian.napoletano^jaime.paneque', '', 198, 214, 'DOI: 10.1080/10455752.2015.1104706'],
    ['Narrativas sobre el lugar. Habitar una vivienda de interés social en la periferia urbana', 'Revista INVI', '30', '84', 2015, '07181299', 'PUBLICADO', 'No', 'antonio.vieyra^claudio.garibay', '', 59, 72, ''],
    ['Procesos participativos intramunicipales como pasos hacia la  gobernanza local en territorios periurbanos. La experiencia en el municipio de Tarímbaro, Michoacán, México', 'Journal of Latin American Geography', '14', '2', 2015, '15452476', 'PUBLICADO', 'No', 'antonio.vieyra^lorena.poncela^yadira.mendez', '', 129, 157, 'DOI: 10.1353/lag.2015.0027'],
    ['Acceso al suelo ejidal en la periferia urbana mexicana: Análisis desde el Capital Social', 'Economía, Sociedad y Territorio', '', '', 2016, '1405-8421', 'ACEPTADO', 'Si', 'yadira.mendez^sandra.pola^antonio.vieyra', '', 0, 0, ''],
    ['How social capital enables/restricts the  livelihoods of poor peri-urban farmers in Mexico', 'Development in Practice', '', '', 2016, '0961-4524', 'ACEPTADO', 'No', 'antonio.vieyra^yadira.mendez', '', 0, 0, ''],
    ['Peri-urban local governance? Intra-government relationships and social capital in a peripheral municipality of Michoacán, Mexico', 'Progress in Development Studies Journal', '0', '0', 2016, '1464-9934', 'ACEPTADO', 'No', 'antonio.vieyra^yadira.mendez^lorena.poncela', '', 0, 0, '0'],
    ['A detailed paleomagnetic and rock-magnetic investigation of the Matuyama-Brunhes geomagnetic reversal recorded in the tephra-paleosol sequence of Tlaxcala (Central Mexico)', 'Frontiers in Earth Science', '3', '', 2015, '2296-6463', 'PUBLICADO', 'No', 'berenice.solis^ana.soler^avto.gogichaishvili^angel.carrancho^sergey.sedov^cecilia.caballero^beatriz.ortega^juan.morales^jaime.urrutia^francisco.bautista', 'Otros indices', 1, 24, 'http://dx.doi.org/10.3389/feart.2015.00011'],
    ['Mineral magnetic properties of an alluvial paleosol sequence in the Maya Lowlands: Late Pleistocene-Holocene paleoclimatic implications', 'Quaternary International', '', '', 2015, '1040-6182', 'ACEPTADO', 'Si', 'berenice.solis^gabriel.vazquez^elizabeth.solleiro^avto.gogichaishvili^juan.morales', 'Otros indices', 0, 1, ''],
    ['Volcaniclastic reworked sediments in the Usumacinta River, Mexico: the serendipitous source of volcanic glass for Maya ceramics', 'Geoarchaeology', '', '', 2016, '1520-6548', 'EN_PRENSA', 'Si', 'berenice.solis^hector.cabadas^elizabeth.solleiro^sergey.sedov^keiko.tatanisho^rodrigo.liendo', '', 0, 0, ''],
    ['Landslides in the tropical mountain range of Veracruz (Mexico) - A case-study of the large El Capulin landslide', 'World Landslide Forum', '', '', 2016, '', 'EN_PRENSA', 'Si', 'berenice.solis^martina.wilde^wendy.morales^daniel.schwindt^matthias.bucker^birgit.terhorst', '', 0, 0, ''],
    ['Horizontal and vertical landscape-complexity influence avian species-richness patterns across the conterminous USA', 'Cogent Environmental Science', '', '', 2015, '0143-6228', 'ENVIADO', 'No', 'brian.napoletano^bryan.pijanowski', '', 0, 0, ''],
    ['Visibility analysis and landscape evaluation in Martin River Cultural Park (Aragon, Spain) integrating biophysical and visual units', 'Journal of Maps', '', '', 1900, '', 'PUBLICADO', 'Si', 'brian.napoletano^ivan.franch^luis.cancer', '', 0, 0, ''],
    ['Small Drones for Community-Based Forest Monitoring: An Assessment of Their Feasibility and Potential in Tropical Areas', 'Forests', '5', '6', 2014, '1999-4907', 'PUBLICADO', 'Si', 'brian.napoletano^jaime.paneque^keith.mccall', '', 1481, 1507, '10.3390/f5061481'],
    ['Recuento nacional de los conflictos mineros territoriales en México', 'Les Cahiers des Amériques Latines', '', '', 2016, '', 'ACEPTADO', 'No', 'claudio.garibay', '', 1, 2, ''],
    ['A. Brigitte Nellie Luisa Boehm Shchoendube (1938-2005)', 'International Encyclopedia of Anthropology', '', '', 2016, '', 'EN_PRENSA', 'No', 'claudio.garibay^andrew.roth', '', 0, 1, ''],
    ['Evaluación de la contaminación ambiental a partir del aumento magnético en polvos urbanos - Caso de estudio para la ciudad de Mexicali, México', 'Revista Mexicana de Ciencias Geológicas', '32', '3', 2016, '1026-8774', 'PUBLICADO', 'Si', 'francisco.bautista^a.sanchez.duque^avto.gogichaishvili^raul.cejudo^j.reyez.lopez^f.solis.dominguez^j.morales.contreras', '', 501, 513, 'http://satori.geociencias.unam.mx/32-3/(09)SanchezDuque.pdf'],
    ['Soil & Environment as a tool for soil environmental functions evaluation', 'Programmnye produkty i sistemy', '2', '3', 2016, '2311-2735', 'PUBLICADO', 'Si', 'francisco.bautista^angeles.gallegos^inna.dubrovina', 'Otros indices', 195, 200, '10.15827/0236-235X.114.195-200'],
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
    ['The networked agency of flash floods materiality and its socioenvironmental processes, exhibit power performances and inequalities', 'Geoforum', '', '', 2015, '0016-7185', 'ACEPTADO', 'No', 'frida.guiza^peter.simmons', '', 0, 0, ''],
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
    ['Absence of detectable transgenes in local landraces of maize in Oaxaca, Mexico (20032004)', 'Proceedings of National Academy of Sciences of USA', '102', '35', 2015, '1091-6490', 'PUBLICADO', 'No', 'gabriela.cuevas^s.ortiz.garcia', '', 12338, 12343, '10.1073/pnas.0503356102'],
    ['An Accuracy Index with Positional and Thematic Fuzzy Bounds for Land-use/Land-cover Maps', 'Photogrammetric Engineering and Remote Sensing', '75', '7', 2009, '0099-1112', 'PUBLICADO', 'No', 'gabriela.cuevas^stephane.couturier^jean.mas', '', 789, 805, '10.14358/PERS.75.7.789'],
    ['Remoteness and remote places. A geographic perspective', 'Geoforum', '', '', 2016, '', 'ACEPTADO', 'No', 'gerardo.bocco', 'Scopus; Otros indices', 0, 0, ''],
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
    ['How does cultural change affect indigenous peoples hunting activity? An empirical study among the Tsimane in the Bolivian Amazon', 'Conservation and Society', '13', '4', 2015, '', 'PUBLICADO', 'No', 'jaime.paneque^marti.orta^victoria.reyes', '', 382, 394, '10.4103/0972-4923.179879'],
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
    ['Beyond Landscape in REDD+: The imperative for Territory', 'World Development', '85', '', 2016, '0305-750X', 'PUBLICADO', 'No', 'keith.mccall', '', 58, 72, '10.1016/j.worlddev.2016.05.001'],
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
    ['Socio-economic and environmental changes related to maize richness in Mexicos central highlands', 'Agriculture and Human Values', '', '', 2016, '1572-8366', 'PUBLICADO', 'Si', 'marta.astier^quetzalcoatl.orozco', '', 0, 0, '10.1007/s10460-016-9720-5'],
    ['La distribución de la diversidad de maíces en la región de Pátzcuaro y sus asociación con factores ambientales y sociales', 'Agrociencia', '', '', 2016, '1405-3195', 'ENVIADO', 'No', 'marta.astier^quetzalcoatl.orozco', '', 0, 0, ''],
    ['Changes in climate, crops, and tradition: Cajete maize and the rainfed farming systems of Oaxaca, Mexico', 'Human Ecology', '46', '5', 2015, '0300-7839', 'PUBLICADO', 'No', 'marta.astier^paul.roge', '', 639, 653, '10.1007/s10745-015-9780-y'],
    ['Promoting local sustainable development and mitigating climate change in indigenous communities of México', 'Climatic Change', '', '', 2015, '1573-1480', 'PUBLICADO', 'No', 'marta.astier^ayesa.martinez^omar.masera', '', 1, 15, '10.?1007/?s10584-015-1523-y'],
    ['Ecosystem service trade-offs, perceived drivers and sustainability in contrasting agroecosystems in Central Mexico', 'Ecology and Society', '20', '1', 2015, '1708-3087', 'PUBLICADO', 'No', 'marta.astier^carlos.gonzalez^mayra.gavito^martin.cardena^ek.del.val^laura.villamil^yair.Merlin^patricia.balvanera', '', 38, 52, 'http://dx.doi.org/10.5751/ES-06875-200138 '],
    ['Resiliencia, vulnerabilidad y sustentabilidad de sistemas socioecológicos en México', 'Revista Mexicana de Biodiversidad', '', '', 2016, '1870-3453', 'ACEPTADO', 'No', 'marta.astier^patricia.balvanera^francisco.gurri^isela.zarmeno', '', 1, 3, ''],
    ['Management practices and plant and flower visitor biodiversity in conventional and organic avocado orchards of Michoacán, México', 'Agroecology and Sustainable Food Systems', '', '', 2016, '2168-3565', 'ENVIADO', 'No', 'marta.astier^laura.villamil^yair.merlin^mayra.gavito', '', 0, 0, ''],
    ['Back to the roots: understanding current agroecological movement, science and practice in Mexico', 'Agroecology and Sustainable Food Systems', '', '', 2016, '2168-3573', 'ENVIADO', 'No', 'marta.astier^quetzalcoatl.orozco^peter.gerritsen^miguel.escalona^julio.sanchez^rene.arzuffi^federico.castrejon^ruben.hernandez^lorena.soto^peter.rosset^carlos.gonzalez^mirna.ambrosio', '', 0, 0, ''],
    ['Quantifying the Mexican forest carbon sink', 'Environmental Research Letters', '', '', 2016, '1748-9326', 'ENVIADO', 'Si', 'jaime.paneque^margaret.skutsch^adrian.ghilardi^arturo.balderas', '', 0, 0, ''],
    ['La estación ecológica de Majana: Su vegetación y flora', 'Fontqueria', '', '39', 1994, '0212-0623', 'PUBLICADO', 'No', 'n.aguila.carrasco^l.menéndez.carrera^ricardo.napoles^angel.priego', 'Latindex; Otros indices', 251, 261, ''],
    ['El paisaje en su connotación ritual. Un caso en la Huasteca Potosina, México', 'Geotrópico', '', '2', 2010, '1692-0791', 'PUBLICADO', 'Si', 'pedro.urquijo', 'Latindex', 1, 1, ''],
    ['Religión y naturaleza en la construcción de la identidad de los teenek potosinos', 'Espacio y tiempo, Revista latinoamericana de Ciencias Sociales y humanidades', '', '1', 2008, '', 'PUBLICADO', 'No', 'pedro.urquijo', '', 19, 30, ''],
    ['Los estudios de paisaje y su importancia en México, 1970-2010', 'Journal of Latin American Geography', '10', '2', 2011, '1545-2476', 'PUBLICADO', 'No', 'pedro.urquijo^gerardo.bocco', '', 37, 63, ''],
    ['Los espacios del pueblo de indios tras el proceso de congregación, 1550-1625', 'Investigaciones Geográficas, Boletín del Instituto de Geografía', '', '60', 2006, '', 'PUBLICADO', 'No', 'pedro.urquijo', 'Otros indices; Scopus; Revistas CONACYT', 145, 158, ''],
    ['Historia y paisaje : Explorando un concepto geográfico monista', 'Andamios, Revista de Investigación Social', '5', '10', 2009, '1870-0063', 'PUBLICADO', 'No', 'pedro.urquijo', 'Otros indices; Web of Science: SCI/SSCI/SCI-EX; Revistas CONACYT', 227, 252, ''],
    ['Geografía ambiental : Reflexiones teóricas y práctica institucional', 'Región y Sociedad', '25', '44', 2013, '1405-9274', 'PUBLICADO', 'No', 'pedro.urquijo^gerardo.bocco', 'Revistas CONACYT; Clase; RedALyC; Latindex; Otros indices', 75, 101, ''],
    ['Construcción social del paisaje en comunidades de pescadores artesanales. El caso de la Península de Valdés, Provincia de Chubut, Argentina', 'Biblio 3W. Revista bibliográfica de Geografía y Ciencias Sociales', '18', '1012', 2013, '1138-9796', 'PUBLICADO', 'Si', 'pedro.urquijo^gerardo.bocco', 'Otros indices', 1, 1, ''],
    ['Corporación minera, colusión gubernamental y deposeción campesina. El caso de Goldcorp Inc en Mazapil , Zacatecas', 'Desacatos, Revista de Antropología Social', '', '44', 2014, '1405-9274', 'PUBLICADO', 'No', 'pedro.urquijo^claudio.garibay^andrew.boni', 'Revistas CONACYT; RedALyC; SciELO; Latindex', 113, 142, ''],
    ['Unequal Partners, Unequal Exchange: Goldcorp, the Mexican State and Campesino Dispossession at the Peñasquito goldmine', 'Journal of Latin American Geography', '10', '2', 2011, '1545-2476', 'PUBLICADO', 'No', 'pedro.urquijo^claudio.garibay^andrew.boni', '', 153, 176, ''],
    ['Geographical distribution and diversity of maize (Zea mays L. subsp. mays) races in Mexico', 'Genetic Resources and Crop Evolution', '', '', 2016, '', 'PUBLICADO', 'No', 'quetzalcoatl.orozco^hugo.perales^robert.hijmans', '', 0, 0, 'doi:10.1007/s10722-016-0405-0'],
    ['Maize diversity associated with social origin and environmental variation in Southern Mexico', 'Heredity', '116', '', 2016, '0018-067X', 'PUBLICADO', 'No', 'quetzalcoatl.orozco^jeffrey.ross^amalio.santacruz^stephen.brush', '', 477, 484, '10.1038/hdy.2016.10'],
    ['Diversidad de maíces en Pátzcuaro, Michoacán, México y su relación con factores ambientales y sociales', 'Agrociencia', '', '', 2016, '', 'ENVIADO', 'No', 'quetzalcoatl.orozco^marta.astier', '', 0, 0, ''],
    ['Patterns of distribution along environmental gradients of nine Quercus species in central Mexico', 'Botanical Sciences', '94', '3', 2016, '2007-4476', 'PUBLICADO', 'No', 'r.aguilar.romero^f.garcía.oliva^f.pineda.garcia^i.torres.garcia^f.pena.vega^adrian.ghilardi^ken.oyama', 'Web of Science: SCI/SSCI/SCI-EX', 471, 482, '10.17129/botsci.620'],
    ['Correlación entre los elementos potencialmente tóxicos y propiedades magnéticas en suelos de la Ciudad de México para la determinación de sitios contaminados: definición de umbrales magnéticos', 'Revista Mexicana de Ciencias Geológicas', '32', '', 2015, '', 'PUBLICADO', 'Si', 'raul.cejudo^francisco.bautista^o.delgado.carranza^avto.gogichaishvili^j.morales.contreras', '', 50, 61, ''],
    ['De montaña, milpa y cañaveral. Transformaciones percibidas de los paisajes en la costa de Chiapas', 'Investigaciones Geográficas, Boletín del Instituto de Geografía', '', '', 2016, '0188-4611', 'ACEPTADO', 'No', 'sara.barrasa', 'Otros indices', 0, 30, ''],
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
    ['Abundance and hábitat use of the lizard Sceloporus utiformis (Squamata: Phrynosomatidae) during seasonal transitional in a tropical environment', 'Revista Mexicana de Biodiversidad', '87', '4', 2016, '', 'PUBLICADO', 'No', 'yan.gao', 'RedALyC; Latindex; Otros indices', 1301, 1307, 'http://dx.doi.org/10.1016/j.rmb.2016.10.011']
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
    ['Science for Sustainable Development (Agenda 2030', 'Paris', 'UNESCO', 'PUBLICADO', 2016, 1, 16, '', 'http://creative commons/licenses/by-sa/3.0/igo/', 'hebe.vessuri'],
    ['Etonoagroforestería en México', 'Morelia', 'ENES Unidad Morelia', 'PUBLICADO', 2015, 1, 432, '978-607-02-8164-8', '', 'mariana.vallejo^ana.moreno^alejandro.casas^victor.toledo'],
    ['Standardized Hierarchical, Vegetation, Classification, Mexican and Global Patterns', 'Ciudad de México, CDMX', 'Springer', 'PUBLICADO', 2016, 1, 143, '978-3-319-41221-4', 'https://scholar.google.es/scholar?q=Standardized+Hierarchical+Vegetation+Classification+Mexican+and+Global+Patterns&&&&btnG=&&&&hl=es&&&&as_sdt=0%2C5&&&&as_vis=1', 'alejandro.velazquez^consuelo.medina^elvira.duran^alfredo.amador'],
    ['La memoria de los nombres: la toponimia en la conformación histórica del territorio. De Mesoamerica a México ', 'Morelia', 'CIGA-UNAM', 'EN_PRENSA', 2015, 1, 475, '', '', 'karine.lefebvre^carlos.paredes'],
    ['The global social science world  under and beyond Western universalism', 'Morelia', 'Ibidem Sociedad Editorial De Formacion Juridica Y Economica S. L.', 'PUBLICADO', 2016, 1, 278, '978-3-8382-0893-0', '', 'hebe.vessuri^michael.kuhn^hebe.vessuri^kwang.yeong^huri.islamoglu^doris.weidermann^mauricio.nieto^reinerg.grundmann^sujata.patel^igor.yegorov^pal.tamas^kumaran.rajagopal^kazumi.okamoto'],
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
              es_libro_completo=True
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

