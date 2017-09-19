-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 19-09-2017 a las 07:18:51
-- Versión del servidor: 10.1.19-MariaDB
-- Versión de PHP: 7.0.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `cigacurricula`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ir_librosentidad`
--

CREATE TABLE `ir_librosentidad` (
  `id` varchar(50) NOT NULL,
  `idu` varchar(5) NOT NULL,
  `titulo` text NOT NULL,
  `editor` text NOT NULL,
  `autores_ad` text NOT NULL,
  `autores_ex` text NOT NULL,
  `pais_publi` text NOT NULL,
  `ciudad_publi` text NOT NULL,
  `casas_ed` text NOT NULL,
  `num_ed` text NOT NULL,
  `anio_pub` text NOT NULL,
  `pag_tot` text NOT NULL,
  `colsernumvol` text NOT NULL,
  `isbn` text NOT NULL,
  `proy_rel` text NOT NULL,
  `agradecimiento` text NOT NULL,
  `mencion` text NOT NULL,
  `estado` text NOT NULL,
  `vinculo` text NOT NULL,
  `f_crea` text NOT NULL,
  `f_edi` text NOT NULL,
  `autores` text NOT NULL,
  `editores` text NOT NULL,
  `coordinadores` text NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `ir_librosentidad`
--

INSERT INTO `ir_librosentidad` (`id`, `idu`, `titulo`, `editor`, `autores_ad`, `autores_ex`, `pais_publi`, `ciudad_publi`, `casas_ed`, `num_ed`, `anio_pub`, `pag_tot`, `colsernumvol`, `isbn`, `proy_rel`, `agradecimiento`, `mencion`, `estado`, `vinculo`, `f_crea`, `f_edi`, `autores`, `editores`, `coordinadores`) VALUES
('vjggpljB8rTc38xSOc20jvap0zHwrOxmffqHxaHrVAjuIdz3LG', 'jEvFg', 'Dimensiones Sociales en el Manejo de Cuencas', 'Coordinador', 'null', 'Burgos, Ana, Bocco, Gerardo, Sosa-Ramirez Joaquin ', 'México', 'Morelia', 'Centro de Investigaciones en Geografía Ambiental. Universidad Nacional Autónoma de México', '1', '2015', '320', 'N/A', '978-607-02-6883-0', 'Tercer Congreso Nacional de Manejo de Cuencas Hidrográficas y IV Coloquio de Geografía Ambiental', 'null', 'null', 'Publicado', 'N/A', '2015/12/03 22:26:38', '2015/12/03 22:26:38', 'ana.burgos^gerardo.bocco^joaquin.sosa', 'gerardo.bocco', 'ana.burgos'),
('WjAuADmDHubnXLS1fybEw2fJ5h2K4wTTx6uWyC5d9sY0ZTab1n', 'Yl5I4', 'Morelia y sus ríos. Relaciones entre los procesos históricos, biofísicos y sociales en el contexto urbano.', 'Coordinador', 'Güiza Valverde, Frida; Mendoza Cantú, Manuel Eduardo; Urquijo Torres, Pedro', 'Güiza Valverde, Frida; Mendoza Cantú, Manuel Eduardo; Urquijo Torres, Pedro', 'México', 'morelia', 'Centro de Investigaciones en Geografía Ambiental. Universidad Nacional Autónoma de México', '0', '2017', '0', 'n/a', 'n/a', 'catedras conacyt', 'null', 'null', 'Aceptado', 'n/a', '2016/06/13 21:00:03', '2016/06/13 21:00:03', 'frida.guiza^manuel.mendoza^pedro.urquijo', '', ''),
('T643QuS4wSyfij7XSH8PgDHqfo3iyLlESS2xffHDk85YrFhY8a', 'f4r8Q', 'Tres niveles de análisis en la Sierra-Costa michoacana (insumos para el ordenamiento ecológico)', 'Editor', 'Priego Santander, Angel', 'Priego Santander, Angel & Gerardo Bocco', 'México', 'Morelia', 'Centro de Investigaciones en Geografía Ambiental. Universidad Nacional Autónoma de México', '1', '2015', '223', 'NA', '978-607-02-6530-3', 'CONACYT-SEMARNAT 23490', 'null', 'null', 'Publicado', 'www.ciga.unam.mx/publicaciones', '2015/11/12 05:47:18', '2015/11/12 05:47:18', 'gerardo.bocco^angel.priego', '', ''),
('H58gnSepfHd3G9SXgF9ru6Fr5mQRk8Yjg09XqHa1HSwhOFUSla', 'f4r8Q', 'Conocimiento, paisaje, territorio. Procesos de cambio individual y colectivo', 'Editor', 'null', 'Vessuri, Hebe y Gerardo Bocco', 'Argentina', 'Comodoro Rivadavia', 'Universidad Nacional de Río Negro/ Universidad Nacional de la Patagonia Austral/ Centro Nacional Patagónico-CONICET', '1', '2015', '400', 'na', '978-987-3714-06-1', 'PAPIIT IN 301914', 'null', 'null', 'Publicado', 'na', '2015/11/12 05:56:03', '2015/11/12 05:56:03', 'hebe.vessuri^gerardo.bocco', '', 'gerardo.bocco'),
('oErLuHIKu4oH4didDyhdSHHYKf8mTxUJlR8S31RXWjDROHOSnG', 'J8YEd', 'XIX Reunión Nacional SELPER México. Memorias', 'Coordinador', 'Mas , Jean-Francois; Cuevas García, Gabriela', 'Mas, J.F. y Cuevas, G.', 'México', 'Morelia', 'UNAM: CIGA', '1', '2012', '420', 'N/A', '978-607-02-3172-8', 'N/A', 'No', 'null', 'Publicado', 'http://www.ciga.unam.mx/publicaciones/', '2015/11/13 11:53:46', '2015/11/13 11:53:46', 'gabriela.cuevas^jean.mas', '', ''),
('pox36jl26gxHfH34rvkCediI3Sk80Zu2gwsOpku9ikgXOarlfr', '9hUCZ', 'La regionalización físico-geográfica del estado de Guerrero, México', 'Autor', 'Bollo Manent, Manuel; Priego Santander, Ángel Guadalupe', 'Ortíz Rivera, A., Bollo Manent, M., Hernández Santana, J.R. & A.G. Priego-Santander ', 'México', 'Morelia', 'Centro de Investigaciones en Geografía Ambiental. Universidad Nacional Autónoma de México', '1', '2015', '157', 'N/A', '978-607-02-6706-2', 'N/A', '', '', 'Publicado', 'http://www.ciga.unam.mx/publicaciones/images/abook_file/9786070267062.pdf', '2015/11/17 06:26:15', '2015/11/17 07:40:08', 'angel.priego^manuel.bollo^angel.priego^alberto.ortiz', '', ''),
('ez371UwdRwZu2ITST5SHhBOduaVqKIl17W3g7no7uZdVjJhswD', '9hUCZ', 'Tres niveles de análisis en la Sierra-Costa Michoacana (Insumos para el ordenamiento ecológico).', 'Editor', 'Priego Santander, Ángel Guadalupe; Bocco Verdinelli, Gerardo', 'Priego-Santander, A.G. & G. Bocco .', 'México', 'Morelia', 'Centro de Investigaciones en Geografía Ambiental. Universidad Nacional Autónoma de México', '1', '2015', '223', 'N/A', '978-607-02-6530-3', 'Proyecto CONACyT: “Ecoregionalización como la base para la evaluación de la aptitud del territorio”. ', 'null', 'null', 'Publicado', 'http://www.ciga.unam.mx/publicaciones/index.php?option=com_abook&view=book&catid=12%3Acoleccionesciga&id=74%3Atres-niveles-de-analisis-en-la-sierra-costa-michoacana&Itemid=16', '2015/11/17 06:33:23', '2015/11/17 06:33:23', 'angel.priego^gerardo.bocco', '', ''),
('US8SqLfsgFjeD37f8drfy3SovjBEsfrm7AbklfP3hVwfd2eqaq', '9hUCZ', 'Una propuesta de regionalización físico-geográfica de México', 'Autor', 'Bollo Manent, Manuel; Priego Santander, Ángel Guadalupe', 'Bollo-Manent, M., Hernández-Santana, J.R., Priego-Santander, A.G., Zaragoza-Álvarez, R.A., Ortíz-Rivera, A., Espinosa-Maya, A. & R. Ruíz-López.', 'México', 'Morelia', 'Centro de Investigaciones en Geografía Ambiental. Universidad Nacional Autónoma de México', '1', '2015', '59', 'N/A', '978-607-02-6527-3', 'Proyecto UNAM: Regionalización geoecológica de México a escala 1:1000 000. ', 'null', 'null', 'Publicado', 'http://www.ciga.unam.mx/publicaciones/images/abook_file/PropuestadelaRFGdeMexico.pdf', '2015/11/17 07:08:29', '2015/11/17 07:08:29', 'angel.priego^manuel.bollo', '', ''),
('3WjS3Fa0k3nUxfYBb2fFEHb8Hkvb3ixFFpuMd2y8bkGsOTjlfE', '9hUCZ', 'Propuesta para la generación de unidades de paisajes de manera semi-automatizada. Fundamentos y método', 'Autor', 'Priego Santander, Ángel Guadalupe; Bocco Verdinelli, Gerardo; Mendoza Cantu, Manuel', 'Priego-Santander, AG., G. Bocco, M. Mendoza y A. Garrido ', 'México', 'México, D.F.', 'SEMARNAT-INE, CIGA-UNAM.', '1', '2010', '104', 'N/A', '978-968-817-923-9', 'Proyecto CONACyT: “Ecoregionalización como la base para la evaluación de la aptitud del territorio”. ', '', '', 'Publicado', 'http://www2.inecc.gob.mx/publicaciones/descarga.html?cv_pub=633&tipo_file=pdf&filename=633', '2015/11/17 07:31:30', '2015/11/17 07:40:45', 'angel.priego^gerardo.bocco^manuel.mendoza', '', ''),
('2AhFSeMIqWJwCTJdwZgsKsBkDrf91yvxEf8UKvuftufEgauEV4', '9hUCZ', 'La cartografía de sistemas naturales como base geográfica para la planeación territorial. Una revisión de la bibliografía', 'Autor', 'Bocco Verdinelli, Gerardo; Mendoza Cantu, Manuel; Priego Santander, Ángel Guadalupe; Burgos Tornadú , Ana Laura', '5-	Bocco, G., Mendoza, M., Priego-Santander, A.G. y A. Burgos ', 'México', 'México, D.F.', 'SEMARNAT-INE, CIGA-UNAM.', '1', '2010', '72', 'N/A', '978-968-817-920-8', 'Proyecto CONACyT: “Ecoregionalización como la base para la evaluación de la aptitud del territorio”. ', 'null', 'null', 'Publicado', 'http://www.ciga.unam.mx/publicaciones/index.php?option=com_abook&view=book&catid=12%3Acoleccionesciga&id=15%3Ala-cartografia-de-los-sistemas-naturales-como-base-geografica-para-la-planeacion-territorial&Itemid=16', '2015/11/17 07:45:07', '2015/11/17 07:45:07', 'angel.priego^gerardo.bocco^manuel.mendoza^ana.burgos', '', ''),
('uYGdhWjDZdmBFHWIRzkrLpHARffJrfDkqfFs7N3uih5Sfghkdc', '9hUCZ', '30 Años en el Paisaje Costero Veracruzano: Central Nucleoeléctrica Laguna Verde.', 'Autor', 'Priego Santander, Ángel Guadalupe', 'Guevara, S., P. Moreno–Casasola, G. Castillo-Campos, C. Dorantes, F. González-García, G. Halffter, E. Isunza, A. Lot H., R. Mendoza, K. Paradowska, A.G. Priego-Santander, G. Sánchez Vigil y G. Vázquez. ', 'México', 'Xalapa, Veracruz.', 'INECOL', '1', '2008', '239', 'N/A', '970-709-106-1', 'Proyecto CONACyT: “Plan de Manejo Integral de la Zona de La Mancha, Veracruz, México.” ', 'null', 'null', 'Publicado', 'N/A', '2015/11/17 07:48:37', '2015/11/17 07:48:37', 'angel.priego^p.moreno.casasola^e.vera.isunza', '', ''),
('dmw9u4usfFfHtjFjH1nfQdrxfjjY3dldRoellhOUc6V3ssdHty', 'fs3S7', 'Procesos Urbanos, Pobreza y Ambiente. Experiencias en Megaciudades y Ciudades Medias', 'Coordinador', 'Vieyra Medrano, Antonio; Méndez-Lemus , Yadira', 'Vieyra, A., Méndez-Lemus, Y. y Hernández, J. ', 'México', 'Morelia', 'UNAM - CIGA, CONACYT', '1', '2016', '179', 'N/A', '978-607-02-8098-6', 'Precariedad social en la periferia urbana de Morelia, Michoacán. CONACYT', '', '', 'Publicado', 'N/A', '2015/11/19 13:42:10', '2016/09/20 12:03:43', 'yadira.mendez^antonio.vieyra^alejandra.larrazabal', '', ''),
('1xWt4W434nEuoYa02S5PS6GaYrXfdddarvbL1Ht33WEWYYSIt2', '98big', 'Consejos a los jóvenes con vocación científica o de cómo perderle el miedo al estudio de las ciencias', 'Autor', 'null', 'Bautista F. y V. Luna', 'México', 'México D.F.', 'Skiu (Eds)', '2', '2015', '227', '2', '978-607-96883-0-1', 'N/A', 'null', 'null', 'Publicado', 'N/A', '2015/11/26 11:10:17', '2015/11/26 11:10:17', 'francisco.bautista', '', ''),
('zdxWbVhSdpOkdfPMuFdosgSp2FSGs3wsFFwS37i5HrSD3Isdab', '98big', 'La evaluación automatizada de las funciones ambientales del suelo con base en datos de perfiles', 'Autor', 'null', 'Bautista F., A. Gallegos-Tavera y O. Álvarez Arriaga', 'México', 'Morelia, Michoacán', 'Centro de Investigaciones en Geografía Ambiental. Universidad Nacional Autónoma de México', '1', '2015', '109', 'N/A', '978-607-02-6600-3', 'N/A', 'null', 'null', 'Publicado', 'N/A', '2015/11/26 11:12:46', '2015/11/26 11:12:46', 'francisco.bautista', '', ''),
('FTf3lh3rOEMLlhFljDj8r3w8sL2zdi1l2rDEf7oEcjQIUdgZh3', '98big', 'Atlas de Solos da América Latina e Caribe', 'Autor', 'null', 'Gardi, C., M. Angelini, S. Barceló, F. Olmedo, J. Comerma, C. Cruz, A. Encina, A. Jones, P. Krasilnikov, M. L. Mendonça, L. Montanarella, O. Muñiz, P. Schad, M. I.  Vara, R. Vargas, F. Bautista,', 'México', 'N/A', 'Food and Agriculture Organization', '0', '2015', '0', 'N/A', 'N/A', 'N/A', 'null', 'null', 'Publicado', 'N/A', '2015/11/26 11:14:50', '2015/11/26 11:14:50', 'francisco.bautista^', '', ''),
('O8tOghWCTgS66zFYjaFdgk6k7lIKefiACddjuNbiHssO89Eo8r', '98big', 'Soil Atlas of Latin America and Caribbean', 'Autor', 'null', 'Gardi, C., M. Angelini, S. Barceló, F. Olmedo, J. Comerma, C. Cruz, A. Encina, A. Jones, P. Krasilnikov, M. L. Mendonça, L. Montanarella, O. Muñiz, P. Schad, M. I.  Vara, R. Vargas, F. Bautista, et al.', 'México', 'N/A', 'Lovell-Johns', '0', '2015', '0', 'N/A', '978-92-79-25599-1', 'N/A', 'null', 'null', 'Publicado', 'N/A', '2015/11/26 11:16:15', '2015/11/26 11:16:15', 'francisco.bautista', '', ''),
('BkDo2Cvf0s8hYPejlsk9yeOrSyL9ft5ztd8pOh6duXOgXwgt0h', 'zF8gk', 'Una propuesta de Regionalización Físico-Geográfica de México.', 'Autor', 'Priego Santander, Angel', '2.	Bollo Manent Manuel, José Ramón Hernández Santana, Ángel Priego Santander, Rigel Alfonso Zaragoza Álvarez, Alberto Ortiz Rivera, Alejandra Espinosa Maya, Rodolfo Ruiz López', 'México', 'Morelia ', 'Centro de Investigaciones en Geografía Ambiental. Universidad Nacional Autónoma de México', '1', '2015', '60', 'N/A', '978-607-02-6527-3', 'N/A', 'No', 'null', 'Publicado', 'www.ciga.unam.mx/publicaciones/', '2015/11/30 16:53:48', '2015/11/30 16:53:48', 'manuel.bollo^ramon.hernandez^angel.priego^rigel.zaragoza', '', ''),
('q6vh9ND9sf6p30Vy9ffwiA3EeSre3alkD8Sl2v0HRiH2MHVO8a', 'zF8gk', 'La Regionalización físico-geográfica del Estado de Guerrero, México', 'Autor', 'Priego Santander, Angel', 'Ortiz Alberto, Bollo Manent Manuel, Hernández Santana José Ramón, Priego Santander Ángel', 'México', 'Morelia', 'Centro de Investigaciones en Geografía Ambiental. Universidad Nacional Autónoma de México', '1', '2015', '152', 'N/A', '978-607-02-6706-2', 'N/A', 'No', 'null', 'Publicado', 'www.ciga.unam.mx/publicaciones/', '2015/11/30 16:56:08', '2015/11/30 16:56:08', 'manuel.bollo^angel.priego^alberto.ortiz', '', ''),
('D9lkfV1Ysa822SHwUbSRp6Nq2xp3yYGhSr0krbxnANfOhg0FBh', 'zF8gk', 'La Región como categoría geográfica.', 'Autor', 'null', 'Mateo Rodríguez J. M,\r\n Bollo Manent. M. ', 'México', 'Morelia', 'Morevalladolid', '200', '2016', '108', 'Primera edición', '978-607-02-7872-3. ', 'PAPIME: PE302015', 'No', 'null', 'Publicado', 'www.ciga.unam.mx/publicaciones/ ', '2016/06/29 20:25:35', '2016/06/29 20:25:35', 'manuel.bollo', '', ''),
('sNjZmQdYryfcW4D1EmSKnN9lKwYs9h2gnHsS3s8XAkEhGk8mSs', 'fEVor', 'Humboldt y el Jorullo. Historia de una exploración', 'Autor', 'Urquijo Torres, Pedro', 'Urquiko, P.S.', 'México', 'Morelia Michoacán', 'INECOL', '1', '2008', '103', 'NA', '978-703-475-0', 'NA', 'No', '', 'Publicado', 'NA', '2016/06/30 11:27:56', '2016/06/30 12:26:16', 'pedro.urquijo', '', ''),
('3a6cFRwXafF2JZUMs3FLQ8VuadyDdMF3hegekrSEG3hhFSNEiW', 'fEVor', 'Proyectos de educación en México. Perspectivas históricas', 'Coordinador', 'Urquijo Torres, Pedro', 'Santana, J. y P. S. Urquijo', 'México', 'Morelia Michoacán', 'UNAM-Escuela Nacional de Estudios Superiores Unidad Morelia', '1', '2014', '494', 'NA', '978-607-02-6251-7', 'NA', 'No', '', 'Publicado', 'NA', '2016/06/30 11:39:34', '2016/06/30 12:27:07', 'pedro.urquijo', '', ''),
('0guSfh3ks2k0qb6AtFjgHgSydedorMjSdjkbdurjEfA0sxYrYR', 'fEVor', 'Estudio costero del suroccidente de México', 'Editor', 'null', 'Brand, Donald. D', 'México', 'Morelia Michoacán ', 'CIDEM Michoacán', '1', '2013', '264', 'NA', '978-607-02-4149-9', 'NA', 'No', 'null', 'Publicado', 'NA', '2016/06/30 11:51:23', '2016/06/30 11:51:23', 'donald.brand', 'pedro.urquijo', ''),
('zvsz8Fd38pwOsY48igsvDdAf8owjOjO4d2AsSsjv4S2dsHtd2b', 'fEVor', 'Corografía y escala local. Enfoques desde la geografía humana. ', 'Coordinador', 'Urquijo Torres, Pedro', 'Fernández-Christlieb, F. & P. S. Urquijo ', 'México', 'Morelia Michoacán', 'Centro de Investigaciones en Geografía Ambiental. Universidad Nacional Autónoma de México', '1', '2012', '116', 'NA', '978-607-02-3152-0', 'Proyecto Saberes locales y manejo de la diversidad eco-geográfica en áreas rurales de tradición indígena DGAPA , PAPIIT IN 306806', 'No', '', 'Publicado', 'www.ciga.unam.mx/publicaciones', '2016/06/30 11:59:05', '2016/06/30 12:47:09', 'pedro.urquijo', '', 'pedro.urquijo'),
('w2tGyWFSFof8vhUr7Lg7rMc5ffYm4osJrlF4a58ddiJv7fGkFd', 'fEVor', 'Cocula contra Coatepec de los Costales: un conflicto territorial, 1802-1804. Archivo Dr. Fructuoso Martínez Román', 'Coordinador', 'Garibay Orozco, Claudio; Urquijo Torres, Pedro', 'Garibay, C. & P. S. Urquijo', 'México', 'Morelia Michoacán', 'Centro de Investigaciones en Geografía Ambiental. Universidad Nacional Autónoma de México', '1', '2011', '30', 'NA', '978-607-02-2497-3', 'NA', 'No', '', 'Publicado', 'www.ciga.unam.mx/publicaciones', '2016/06/30 12:38:26', '2016/06/30 12:46:40', 'claudio.garibay^pedro.urquijo', '', 'pedro.urquijo'),
('4fO83sjgecNsaafgj3OvQe4g5fER4acFkAUxs8fAd2obfS5f8n', 'fEVor', 'Geografía y ambiente en América Latina', 'Coordinador', 'Bocco Verdinelli, Gerardo; Urquijo Torres, Pedro; Vieyra Medrano, Antonio', 'Bocco, G., P. S. Urquijo & A. Vieyra ', 'México', 'Morelia Michoacán', 'INE-SEMARNAT', '1', '2011', '355', 'NA', '978-607-02-2496-6', 'NA', 'No', 'null', 'Publicado', 'www.ciga.unam.mx , www2.ine.gob.mx/publicaciones/index.html', '2016/06/30 12:45:07', '2016/06/30 12:45:07', 'gerardo.bocco^pedro.urquijo^antonio.vieyra', '', 'pedro.urquijo'),
('b9ge4vJFe3rBYu8Jar7CyY0N809S47SoCajOdfFmDJn2vDLgrr', 'fEVor', 'Temas de geografía latinoamericana', 'Coordinador', 'Urquijo Torres, Pedro', 'Urquijo, P. S. & N. Barrera ', 'México', 'Morelia Michoacán', 'CIDEM Michoacán', '1', '2009', '443', 'NA', '978-968-9529-12-5', 'NA', 'No', 'null', 'Publicado', 'NA', '2016/06/30 12:54:36', '2016/06/30 12:54:36', 'pedro.urquijo', '', ''),
('Y8faMf8Pj4wfF1rz3YoCW2sfDET1pEi8qoh4rfW3aR8wkQ7s53', 'vmh1r', 'Science for Sustainable Development (Agenda 2030', 'Autor', '', 'Vessuri, Hebe', 'Francia', 'Paris', 'UNESCO', '1', '2016', '16', 'Policy Briefs CILAC', 'http:creative commons/licenses/by-sa/3.0/igo/', 'N/A', '', '', 'Publicado', 'N/A', '2016/12/02 12:26:47', '2016/12/02 12:26:47', 'hebe.vessuri', '', ''),
('22ehRoo332lF00aWgDiszdSdKX4oe4VH30o33xHBjBp7O3AWhI', '4th7o', 'Etonoagroforestería en México', 'Editor', 'Vallejo Ramos, Mariana', 'Ana Isabel Moreno-Calles, Alejandro Casas, Víctor M. Toledo y Mariana Vallejo Ramos', 'México', 'Morelia, Michoacán', 'ENES Morelia. Universidad Nacional Autónoma de México', '1', '2015', '432', 'N/A', '978-607-02-8164-8', 'PAPIIT IA203213. Caracterización de sistemas agroforestales tradicionales desde un enfoque biocultural.', '', '', 'Publicado', 'N/A', '2015/11/30 12:15:02', '2016/12/03 20:43:53', 'mariana.vallejo^ana.moreno^alejandro.casas^victor.toledo', '', ''),
('EYjCtW3wVceBn3bRrjjsyySHwss7SfeqoFlhZ8BSGEhSbHw51j', 'rWKXd', 'Standardized Hierarchical, Vegetation, Classification, Mexican and Global Patterns', 'Autor', 'Velázques Montes, Alejandro', 'Alejandro Velázquez\nConsuelo Medina García\nElvira Durán Medina · Alfredo Amador\nLuis Fernando Gopar Merino', 'Suiza', 'NA', 'Springer', '1', '2016', '143', 'Library of Congress Control Number: 2016943442', 'ISBN 978-3-319-41221-4', 'N/A', '', '', 'Publicado', 'https://scholar.google.es/scholar?q=Standardized+Hierarchical+Vegetation+Classification+Mexican+and+Global+Patterns&&&&btnG=&&&&hl=es&&&&as_sdt=0%2C5&&&&as_vis=1', '2016/11/30 18:34:18', '2016/12/02 12:18:53', 'alejandro.velazquez^consuelo.medina^elvira.duran^alfredo.amador', '', ''),
('sneJO53R0W3wsD8rmTFjIsY8F6fYF4EyY3uj4l1Hg31okdeIkf', '7Gs53', 'La memoria de los nombres : la toponimia en la conformación histórica del territorio. De Mesoamerica a México ', 'Coordinador', 'lefebvre , karine', 'Karine Lefebve, Carlos Paredes Martínez', 'México', 'Morelia', 'Centro de Investigaciones en Geografía Ambiental. Universidad Nacional Autónoma de México', '0', 'N/A', '475', 'N/A', 'N/A', 'N/A', '', '', 'En prensa', 'N/A', '2016/12/01 13:24:12', '2016/12/01 13:24:12', 'karine.lefebvre^carlos.paredes^', '', 'karine.lefebvre'),
('ehf3H3O0D8hSjpiWvg1fw8J1Gj8rrk2hYd81faugllf2h7BDy3', 'vmh1r', 'The global social science world – under and beyond ‘Western’ universalism.', 'Editor', '', 'Michael Kuhn, Hebe Vessuri, Carmen Bueno Castellanos, Kwang Yeong Shin,Huri ISlamoglu, Doris Weidermann, MAuricio Nieto Olarte, Reiner Grundmann, Sujata Patel, Igor Yegorov, Pal Tamas, Kumaran Rajagopal, Kazumi Okamoto', 'Alemania', 'Stuttgart', 'Ibidem', '1', '2016', '278', 'Beyond the Social Sciences, vol. 3', '978-3-8382-0893-0', 'Proyecto CONACYT 221883', '', '', 'Publicado', 'N/A', '2016/12/02 10:06:25', '2016/12/02 10:06:25', 'hebe.vessuri^michael.kuhn^hebe.vessuri^kwang.yeong^huri.islamoglu^doris.weidermann^mauricio.nieto^reinerg.grundmann^sujata.patel^igor.yegorov^pal.tamas^kumaran.rajagopal^kazumi.okamoto', '', ''),
('5kNRgTt5jh6y2Ou0gFxhSOjgRkjcAP5Tu0w7ddHg3QymUCuDgn', 'vmh1r', 'Some Contributions to Alternative Concepts of Knowledge', 'Editor', '', 'Kuhn, Michael, Hebe Vessuri, Juan Pablo Vazquez Gutierrez, Pablo Reyna Estévez, Léon Marie Nkolo Njodo, Christiane Hartnack, Roger Magazine, Claudia Magallanes-Blanco, Leandro Rodriguez Medina, Ivan da Costa Marquez, Michel Christie, Kumaran Rajagopal, Quodratullah Qorbani.', 'Alemania', 'Stuttgart', 'Ibidem', '1', '2016', '272', 'Beyond thE SOCIAL SCIENCES, VOL. 4', '978-3-8382-0894-7', 'PROYECTO CONACY 221883', '', '', 'Publicado', 'N/A', '2016/12/02 10:12:20', '2016/12/02 10:12:20', 'hebe.vessuri^michael.kuhn^juan.vazquez^pablo.reyna^leon.nkolo^christiane.hartnack^roger.magazine^claudia.magallanes^leandro.rodriguez^ivan.costa^michel.christie^kumaran.rajagopal^quodratullah.qorbani', '', ''),
('iuDomH3sajcgY3DNsYLfNLJ3I8Sbr1vrEjHJkjgYKWpO66dlfh', 'vmh1r', 'Conocimiento, Paisaje y Territorio. Procesos de cambio individual y colectivo.', 'Coordinador', '', 'Albarracín, Dalma; Alvarez Gamboa, Gabriela; Bekerman, Fabiana; Bocco, Gerardo; Cinti, Ana; Curti, Leticia; FLores, Cristina; Guber, Rosana; Kaminker, Sergio Andrees; Laztra, CArolina; Sánchez-Rose, Isabelle; Serrano, Javier, SOurrouille, Marcos; Taire, Damián Leonardo ; Urquijo, Pedro; Vessuri, Hebe; Vezub, Julio', 'Argentina', 'Buenos Aires', 'CONICET', '1', '2016', '400', 'N/A', '978-987-3714-0', 'N/A', '', '', 'Publicado', 'N/A', '2016/12/02 11:23:41', '2016/12/02 11:23:41', 'dalma.albarracin^gabriela.alvarez^fabiana.bekerman^gerardo.bocco^ana.cinti^leticia.curti^cristina.flores^rosana.guber^sergio.kaminker^carolina.laztra^javier.serrano^marcos.sourrouille^damian.taire^pedro.urquijo^hebe.vessuri', '', 'hebe.vessuri'),
('4uddrC3h8SgwfhibzDTqkjsFibO9znnEZFDFHrtcPCoSf6fdkR', 'vmh1r', 'La Otra, El Mismo. Mujeres en la ciencia y la tecnología en Venezuela', 'Coordinador', '', 'Vessuri, Hebe; Ma. Victoria Canino; Rosa Bolivar; Ana Castellanos; Maria Alejandra Aray; ', 'Venezuela', 'Caracas', 'Fundación Escuela Editorial El perro y la rana', '1', '2016', '0', 'N/A', 'N/A', 'N/A', '', '', 'En prensa', 'N/A', '2016/12/02 11:48:51', '2016/12/02 11:48:51', 'hebe.vessuri^victoria.canino^rosa.bolivar^ana.castellanos^alejandra.aray', '', 'hebe.vessuri'),
('82fmFn2nC3OTo5ybSjRwq4siDC984ctJhx8gRF3fb8l4OhumZH', '58Tln', 'Procesos Urbanos, Pobreza y Ambiente. Implicaciones en Ciudades Medias y Megaciudades', 'Coordinador', 'Vieyra Medrano, José Antonio; Méndoza  Lemus , Yadira Mireya', 'Vieyra, A., Méndez-Lemus, Y., Hernández, J. ', 'México', 'Morelia', 'Centro de Investigaciones en Geografía Ambiental. Universidad Nacional Autónoma de México', '1', '2016', '0', 'N/A', '978-607-02-8100-6 ', 'N/A', '', '', 'Publicado', 'N/A', '2016/12/06 15:16:14', '2016/12/06 15:16:14', 'yadira.mendez^antonio.vieyra^alejandra.larrazabal', '', ''),
('GaSjKS778Sn5tpdPfsNOrOgs3lN7XC2uqfjbTNWrdrFds6g0JW', '58Tln', 'Procesos periurbanos: Desequilibrios territoriales, desigualdades sociales, ambientales y pobreza', 'Coordinador', 'Vieyra Medrano, José Antonio; Mendez  Lemus, Yadira Mireya; Larrazábal De la Vía, Alejandra', 'Vieyra, A., Méndez-Lemus, Y., Larrazabal, A.\r\n', 'México', 'Morelia', 'Centro de Investigaciones en Geografía Ambiental. Universidad Nacional Autónoma de México', '1', '2016', '0', 'N/A', 'N/A', 'N/A', '', '', 'En prensa', 'N/A', '2016/12/06 18:29:17', '2016/12/06 18:29:17', 'yadira.mendez^antonio.vieyra^alejandra.larrazabal', '', ''),
('R4bS8XwbV8MqOfHrDfszEy80fHBeCU5i91z2fVK3pCyNDnsyLG', 'f4r8Q', 'Geopedology. An integration of Geomorphology and Pedology for Soil and Landscape Studies', 'Editor', 'Bocco Verdinelli, Gerardo', 'Joseph Alfred Zinck\nGraciela Metternicht\nGerardo Bocco\nHéctor Francisco del Valle', 'Estados Unidos de América', 'New York', 'Springer', '1', '2015', '556', 'N/A', '978-3-319-19158-4', 'N/A', '', '', 'Publicado', 'DOI 10.1007/978-3-319-19159-1', '2016/12/06 18:45:23', '2016/12/06 18:45:23', 'gerardo.bocco^alfred.zinck^graciela.metternicht^hector.delvalle', 'gerardo.bocco', '');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `ir_librosentidad`
--
ALTER TABLE `ir_librosentidad`
  ADD PRIMARY KEY (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
