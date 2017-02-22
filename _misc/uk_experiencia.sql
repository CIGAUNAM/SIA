-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Jan 18, 2017 at 10:55 PM
-- Server version: 10.1.16-MariaDB
-- PHP Version: 5.6.24

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cigacurricula`
--

-- --------------------------------------------------------

--
-- Table structure for table `uk_experiencia`
--

CREATE TABLE `uk_experiencia` (
  `id` varchar(50) NOT NULL,
  `idu` varchar(5) NOT NULL,
  `mes_ini` text NOT NULL,
  `anio_ini` text NOT NULL,
  `mes_fin` text NOT NULL,
  `anio_fin` text NOT NULL,
  `nombre` text NOT NULL,
  `cargo_aca` text NOT NULL,
  `cargo_adm` text NOT NULL,
  `departamento` text NOT NULL,
  `institucion` text NOT NULL,
  `definitividad` text NOT NULL,
  `f_crea` text NOT NULL,
  `f_edi` text NOT NULL,
  `otro` varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `uk_experiencia`
--

INSERT INTO `uk_experiencia` (`id`, `idu`, `mes_ini`, `anio_ini`, `mes_fin`, `anio_fin`, `nombre`, `cargo_aca`, `cargo_adm`, `departamento`, `institucion`, `definitividad`, `f_crea`, `f_edi`, `otro`) VALUES
('pzSiYslPheHfcG1Qs8yqYK7DFqdv17Yn3ftQuScwhNsSOlVG3e', '16ymf', 'Enero', '2014', 'A la fecha', 'A la fecha', 'no', 'no', 'Diseñador Instruccional Y Tutor Universidad Virtual Michoacán', 'Control Escolar', 'Universidad Virtual del Estado de Michoacán (UNIVIM)', 'No', '2016/12/08 21:35:26', '2016/12/08 21:35:26', 'no'),
('V1jIj7FDGCoGEXY01Dl2Gz0Erqw2NuDjFiDeD6vgIUgHq8dhH9', 'Y9jOf', 'Marzo', '2014', 'A la fecha', 'A la fecha', 'Profesor Investigador Titular B, Tiempo completo', 'no', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'Si', '2015/11/02 15:30:44', '2015/12/02 15:52:36', ''),
('sKYH3fyYHfhk3wglJuRyEOyHL8DkkbeuyehmgHYisyloLFXdvx', '16ymf', 'Junio', '1968', 'A la fecha', 'A la fecha', 'Pensionado Jubilado Pemex', 'no', 'no', 'Superintendencia de Control de Calidad', 'Petróleos Mexicanos (PEMEX)', 'Si', '2016/12/08 21:32:41', '2016/12/08 21:32:41', ''),
('ksdekeMcxOSu1cfTEHFuxKPkp42NQf9ndkTZegWWW2RibSyxsE', 'J8YEd', 'Abril', '2011', 'Marzo', '2016', 'Técnico Académico Asociado C de Tiempo Completo', 'no', 'no', 'Laboratorio de Análisis Espacial', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/10 17:13:24', '2016/05/31 13:00:50', ''),
('Sr1shHkpeXrf10hLtF3Gra8xFS9SGVQlbbLeX1k8v39Wk3dqBt', 'J8YEd', 'Julio', '2010', 'Diciembre', '2010', 'Profesor de asignatura ordinario Nivel “A” [Interino]', 'no', 'no', 'Coordinación de Ciencias, Centro de Investigaciones en Ecosistemas', 'Instituto de Investigaciones en Ecosistemas y Sustentabilidad (IIES)', 'No', '2015/11/10 17:18:36', '2015/11/10 17:18:36', ''),
('PHidfhO8SpLQAyR4Ffwa2UK7bRJwJrs2eYGeSd30vBn5OIlibY', 'J8YEd', 'Febrero', '2000', 'Septiembre', '2005', 'Subdirectora de Sistemas de Información Geográfica', 'no', 'no', 'Dirección de Ordenamiento Ecológico', 'Instituto Nacional de Ecología y Cambio Climático (INECC)', 'No', '2015/11/10 17:21:09', '2015/11/10 17:21:09', ''),
('FZfHfdegdjyyrEb8Srs7hvknfUhlgTuf3lsinZwHCufbno2UuY', 'J8YEd', 'Junio', '1999', 'Enero', '2000', 'Jefe de Departamento de Migración Interna', 'no', 'no', 'Dirección de  Estudios Socioeconómicos y Regionales', 'Consejo Nacional de Población (CONAPO)', 'No', '2015/11/10 17:23:26', '2015/11/10 17:23:26', ''),
('2bEbwthfoal1RYYfE8dG0e4quxslpsfOj8k5GffAdF4fdAsFOs', 'J8YEd', 'Mayo', '1998', 'Julio', '1999', 'no', 'no', 'Colaborador', 'Centro de Estudios Demográficos y de Desarrollo Urbano', 'El Colegio de México, A.C.', 'No', '2015/11/10 17:25:52', '2015/11/10 17:25:52', ''),
('3swjd8HfrriB0g9mnefLswuyab3kjnjSLmX33fgtSNpn5Kyrej', 'J8YEd', 'Agosto', '1997', 'Abril', '1998', 'no', 'no', 'no', 'no', 'Instituto de Biología', 'No', '2015/11/10 17:27:59', '2015/11/10 17:31:57', 'Colaborador'),
('0KiSSdyeB1SLv85sxwS3Yh8MTolc7u8imlgYAUoPpr3Rf0IFrP', 'J8YEd', 'Mayo', '1997', 'Julio', '1997', 'no', 'no', 'no', 'no', 'Instituto para el Desarrollo Sustentable en Mesoamérica, A.C.', 'No', '2015/11/10 17:29:47', '2015/11/10 17:29:47', 'Colaborador'),
('R2SfcHdvsRpLFrhFgrHjsxGXbSurZFygscEf3RSZwRHPSdRErs', 'J8YEd', 'Octubre', '1994', 'Enero', '1995', 'Jefe de Departamento', 'no', 'no', 'Diseño de Proyectos de la Subsecretaria Técnica', 'Instituto Federal Electoral', 'No', '2015/11/10 17:36:50', '2015/11/10 17:36:50', ''),
('anipljr3k8FUpFbyjkNhxsrBGLySPMdgCh3K48rPeALJXjrjDV', 'J8YEd', 'Enero', '1993', 'Diciembre', '1994', 'no', 'no', 'no', 'Laboratorio de SIG, Instituto de Geografía', 'Instituto de Geografía', 'No', '2015/11/10 17:39:50', '2015/11/10 17:39:50', 'Colaborador'),
('cCkc3wamqWifzqtZgC3LebhaWGgFSf32dFdTh32hArPfesFZFw', 'J8YEd', 'Enero', '1991', 'Diciembre', '1992', 'no', 'no', 'no', 'Laboratorio de Ecología Global', 'Instituto de Ecología', 'No', '2015/11/10 17:43:37', '2015/11/10 17:43:37', 'Colaborador'),
('S3k8YZXLdWRHrLOFsiT9yjL4JUkBHGSFId13herOd3QM7fWpYX', 'J8YEd', 'Octubre', '1989', 'Diciembre', '1990', 'no', 'no', 'no', 'no', 'Sistemas de Información Geográfica, S.A. de C.V.', 'No', '2015/11/10 17:47:08', '2015/11/10 17:50:32', 'Digitalizador'),
('bs3sWWdr2fUafSyatW8Br6YGfbbhseuQGrgfskG2rS3sQju8yZ', 'J8YEd', 'Enero', '1989', 'Agosto', '1989', 'no', 'no', 'Analista', 'Subdirección de Geografía, de la Dirección Regional en el D.F. ', 'Instituto Nacional de Estadística y Geografía (INEGI)', 'No', '2015/11/10 17:49:24', '2015/11/10 17:49:24', ''),
('jeegx5bhvpE3CWgyuS2uu9LgMricRJcx3rr2Se86Id9DFFBuIs', 'f4r8Q', 'Febrero', '1995', 'A la fecha', 'A la fecha', 'Investigador Titular', 'no', 'no', 'no', 'Coordinación de la Investigación Científica (CIC)', 'Si', '2015/11/11 06:53:38', '2015/11/11 06:53:38', ''),
('vcsup7chFtAsygg82lSPFhQBsQ433dOKXNCQqFRhFFjy3Gl4sM', 'hnSDn', 'Octubre', '2012', 'Febrero', '2014', 'Técnico de investigación', 'no', 'no', 'Manejo de recursos costeros y terrestres', 'Universidad Autónoma de Baja California', 'No', '2015/11/11 14:29:28', '2015/11/11 14:29:28', ''),
('AHzFsfaMHoEPIbpu4DeooQhFoYygjPuggtnHTDDEWjQFhpc4Hs', '9hUCZ', 'Febrero', '1988', 'Noviembre', '2001', 'Investigador Agregado de T.C.', 'Investigador Agregado', 'no', 'Ecología del Paisaje', 'Instituto de Ecología y Sistemática', 'No', '2015/11/12 08:12:25', '2015/11/12 08:13:38', ''),
('6IjBjYSid2LOyO4g2p5f4j5HbY8OdFGDrhLNjeExukgjglsjLf', '9hUCZ', 'Noviembre', '2001', 'Abril', '2004', 'Subdirector de Estudios del Medio Biofísico', 'no', 'Subdirector de Área', 'Dirección de Manejo Integrado de Cuencas Hídricas', 'Instituto Nacional de Ecología y Cambio Climático (INECC)', 'No', '2015/11/12 08:16:00', '2015/11/12 08:16:00', ''),
('og3ThnYQFyCap1MkidHkADH3euyRkEgRjbFHVDDfxd8I5hHb7H', '9hUCZ', 'Abril', '2004', 'Abril', '2006', 'Investigador Asociado C de T.C.', 'Investigador Asociado', 'no', 'Unidad Académica en Morelia', 'Instituto de Geografía', 'No', '2015/11/12 08:18:08', '2015/11/12 08:18:08', ''),
('p6vHl4ueRatj5diytjEjj3Fesr8yiFj5E7dXIgUERk8jweHrxS', '9hUCZ', 'Marzo', '2007', 'A la fecha', 'A la fecha', 'Investigador Titular A de T.C.', 'Investigador Titular', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'Si', '2015/11/12 08:20:07', '2015/11/12 08:20:07', ''),
('fFj7FfE8h6SOT8YyH4JYYWIdty2eogTjFmkwy38L44WCHxekjF', 'n80rn', 'Octubre', '2014', 'A la fecha', 'A la fecha', 'Técnico Académico Titular "B" T.C.', 'Técnico Académico Titular "B" T.C.', 'no', 'Unidad de Computo', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'Si', '2015/11/12 10:29:23', '2016/06/28 10:12:44', ''),
('FWEHx3kwJsSsFAElRjuFyjkOGeueSireG3JlEJJ48prYffDDw0', 'n80rn', 'Junio', '2011', 'Octubre', '2014', 'Técnico Académico Titular "A" T.C.', 'Técnico Académico Titular "A" T.C.', 'no', 'Unidad de Computo', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'Si', '2015/11/12 10:32:49', '2016/06/28 10:12:58', ''),
('2ifDra5LfBBR1kc6hD2fgdr3IAdyFY8vZ2uSseSdugyrodujRf', 'n80rn', 'Marzo', '2007', 'Junio', '2011', 'Técnico Académico Asociado "C" T.C.', 'Técnico Académico Asociado "C" T.C.', 'no', 'Unidad de Computo', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/12 10:35:36', '2015/11/12 10:35:36', ''),
('hbmqv7jfuuQHcG2aqskKeEUhRuNG33s8J4W4GyujOdQWyNRyYa', 'n80rn', 'Marzo', '2006', 'Febrero', '2007', 'Responsable de Computo', 'no', 'no', 'Unidad de Computo', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/12 10:37:51', '2015/11/12 10:38:44', ''),
('WkkSt9XoOOf7sHddHMi5f8YREbelGEFGN6gfN81RHRAakjFTKk', 'n80rn', 'Enero', '2001', 'Diciembre', '2005', 'Encargado del Área de Computación ', 'no', 'no', 'Desarrollo de Sistemas y Soporte Técnico', 'Signos Diseño & Publicidad', 'No', '2015/11/12 10:41:13', '2015/11/12 10:41:13', ''),
('FRV7FHtHHHeHGmd8KrHdswXWyqfOSo7HvgHEoyFoMwg0x7lkj0', 'n80rn', 'Junio', '2004', 'Diciembre', '2004', 'Servicio Social', 'no', 'no', 'Departamento de Actividades extraescolares', 'Instituto Tecnológico de Morelia (ITM)', 'No', '2015/11/12 10:42:26', '2015/11/12 10:42:26', ''),
('jzvlY8jkFuF3SSJE4iemseQuFwy3LdkEk0xQh03fHwLf0dAwj7', 'n80rn', 'Febrero', '1999', 'Agosto', '1999', 'no', 'no', 'no', 'Dirección del CBTa #89', 'Centro de Bachillerato Tecnológico Agropecuario #89 José Vasconcelos (CBTA 89)', 'No', '2015/11/12 10:43:50', '2015/11/12 10:43:50', 'Servicio Social'),
('B3sFgSDHW487d3GUYSusdhjnHgswUE1fYX7EfQqzS4j5QH7LcM', 'GUKjy', 'Enero', '1994', 'Febrero', '1996', 'Técnico Académico Titular "A"', 'no', 'no', 'Laboratorio SIG', 'Instituto de Geografía', 'No', '2015/11/13 18:37:44', '2015/11/13 18:37:44', ''),
('gfkFf3ksBufhODe3TFS8OCuthn4s732ELelWezraf3ppUeuFki', 'GUKjy', 'Febrero', '1996', 'Marzo', '2000', 'Profesor / investigador Asociado "C"', 'no', 'no', 'Centro de Ecología, Pesquerías y Oceanografía del Golfo de México (EPOMEX)', 'Universidad Autónoma de Campeche (UACAM)', 'No', '2015/11/13 18:39:20', '2015/11/13 18:39:20', ''),
('E7v2krI0yrsDHiGY9bF9qlAjyrfZRebrHyASWo4OurOxG8yELV', 'GUKjy', 'Julio', '2000', 'Julio', '2004', 'Investigador Asociado "C"', 'no', 'no', 'no', 'Instituto de Geografía, Unidad Morelia (UNAM Morelia)', 'No', '2015/11/13 18:41:03', '2015/11/13 18:41:03', ''),
('Cd7I2HtLuI8Fj6dDss8r8rFLYHoeIkSaOWFahSefPQSFqZcHY2', 'GUKjy', 'Agosto', '2007', 'Febrero', '2010', 'Investigador Titular "A"', 'no', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/13 18:42:39', '2015/11/13 18:42:39', ''),
('QqFroslec8s8hsdkDSIrE5gwj72bYSw5wx2MLI8wMugaJG4E3d', 'GUKjy', 'Febrero', '2010', 'Mayo', '2015', 'Investigador Titular "B"', 'no', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'Si', '2015/11/13 18:44:53', '2015/11/13 18:45:00', ''),
('vwugsFHffig2n3dDfjFfwrIulgw048rjwrjNaoBrdoEFfgfRkn', 'GUKjy', 'Junio', '2015', 'A la fecha', 'A la fecha', 'Investigador Titular "C"', 'no', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'Si', '2015/11/13 18:45:44', '2015/11/13 18:45:44', ''),
('eoHSjsiewdFvsV2pfLlOeyD2rp5qji4Usdr8YeT5ekehfE9uds', 'Yl5I4', 'Octubre', '2014', 'A la fecha', 'A la fecha', 'no', 'Catedrático CONACYT', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/19 12:08:51', '2015/11/19 12:08:51', ''),
('uFGwF3kt1OagHx1mlfPvoHHSw18qfn3uqvJrJ9ZfbDZh3HHxA1', 'EeGJW', 'Septiembre', '2014', 'A la fecha', 'A la fecha', 'Investigadora Posdoctoral', 'Docencia', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/20 17:11:17', '2016/12/05 11:36:03', ''),
('UEJeiYutSqYvQ0LjIS2ceeei78LFP8ut0pUwNfu8VtHbrUgSsf', 'EeGJW', 'Octubre', '2008', 'Julio', '2009', 'no', 'no', 'no', 'Ingeniera Agrónoma', 'Instituto Cartográfico y Geológico de Cataluña', 'No', '2015/11/20 17:12:51', '2015/11/20 17:12:51', 'Levantamiento y elaboración de mapas de suelos'),
('FUhq3ojuDOSa4u0qBaAfqfqcF5S1FsfBdhg98F333RHowa1w3O', 'EeGJW', 'Abril', '2006', 'Septiembre', '2006', 'Ingeniera Técnico Agrícola', 'no', 'Plan de mejora de los caminos rurales de Catalunya', 'no', 'Tecnologías y Servicios Agrarios, S.A (Tragsatec)', 'No', '2015/11/20 17:14:15', '2015/11/20 17:14:15', ''),
('KRdj4m4j8hWhSbbK8s9d3e5csn8agSaykA0nsk8DF1ftHYVdWa', 'EeGJW', 'Septiembre', '2005', 'Febrero', '2006', 'Ingeniera Técnico Agrícola', 'no', 'Responsable de Calidad', 'no', 'Chiquita, C.B. (Meneu Distribuciones, S.A.)', 'No', '2015/11/20 17:15:11', '2015/11/20 17:15:11', ''),
('ndkGjL21d2JnwFsdpYrk7SKsm8tauH7sDHyf8RlvRYS0dJJ3ws', 'Yrcbo', 'Diciembre', '1994', 'Diciembre', '1997', 'Técnico Académico Asociado C de Tiempo Completo', 'no', 'no', 'LAFQA', 'Instituto de Geografía', 'No', '2015/11/23 10:13:22', '2015/11/23 10:13:22', ''),
('e4RhE7Yjfd3FEjF4ndrgecVB2cHsm33S1c3Yg9VmfjiHQlFvEK', 'Yrcbo', 'Diciembre', '1997', 'Diciembre', '2001', 'Técnico Académico Titular A de Tiempo Completo', 'no', 'no', 'LAFQA', 'Instituto de Geografía', 'No', '2015/11/23 10:16:07', '2015/11/23 10:16:07', ''),
('8XuzhK3sl3kflFsIFD9utlaLBxmJ47gwENj6ZIJOlkehTrj8dF', 'Yrcbo', 'Diciembre', '2001', 'Agosto', '2006', 'Técnico Académico Titular B de Tiempo Completo', 'no', 'no', 'LAFQA', 'Instituto de Geografía', 'Si', '2015/11/23 10:19:08', '2015/11/23 10:19:08', ''),
('dgev2jL2hddophFodj83yHb1iIbaJAduLRZOb428u9gaXefstr', 'Yrcbo', 'Septiembre', '2006', 'Julio', '2007', 'Técnico Académico Titular B de Tiempo Completo', 'no', 'no', 'Unidad Académica', 'Instituto de Geografía', 'Si', '2015/11/23 10:21:42', '2015/11/23 10:21:42', ''),
('ZftfWtrFa8qYqvH42FrfrJZRH5asdtyQg8Hb7jss0j5I5Lnhjs', 'Yrcbo', 'Agosto', '2006', 'Diciembre', '2008', 'Técnico Académico Titular B de Tiempo Completo', 'no', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'Si', '2015/11/23 10:27:16', '2015/11/23 10:31:13', ''),
('yyYpFTW4dFpz68k3mFfsrSUfxNe03uxMIF8H83afO1IFv7W84j', 'Yrcbo', 'Octubre', '2015', 'A la fecha', 'A la fecha', 'Técnico Académico Titular C de Tiempo Completo', 'no', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'Si', '2015/11/23 10:28:39', '2015/11/23 10:28:39', ''),
('Thxt53cF87m7ef1FfNFHojanWSPrIEyZ0ShhVFd7kHrbnsXe64', 'Yrcbo', 'Enero', '2009', 'Septiembre', '2015', 'Técnico Académico Titular B de Tiempo Completo', 'no', 'Secretaría Técnica', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'Si', '2015/11/23 10:33:11', '2015/11/23 10:33:11', ''),
('SaYqSpSO2HFl8FPraDfE78TncScUjGjxjEOhusLY0wad8AAsM4', 'fEVor', 'Noviembre', '2007', 'Octubre', '2011', 'Miembro de la Mesa Directiva del Colegio del Personal Académico ', 'no', 'no', 'Personal Académico', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/26 15:30:15', '2016/08/18 08:48:02', ''),
('DtfhOnrkdFPDdI36Mp2DvLtwVargww8ZfSq1wsSrokMV12W3j3', 'fEVor', 'Octubre', '2007', 'Octubre', '2011', 'Representante de los técnicos académicos ante el Consejo Interno', 'no', 'no', 'Consejo Interno', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/26 15:31:13', '2016/08/18 08:47:34', ''),
('fEOWrQWhhAchrefNWyu2nwhTyrHSvA3Wy892Vf9kFdjytdrorm', 'fEVor', 'Noviembre', '2011', 'Abril', '2012', 'no', 'no', 'no', 'Geohistoria', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/26 15:32:02', '2016/08/18 08:47:19', 'Corresponsable del Proyecto de Creación de la Licenciatura en Geohistoria'),
('bsFlejj2ZghtldfrpJ23OrbudoSXuttWF171YSFjwLaesrrgeV', 'fEVor', 'Diciembre', '2010', 'Abril', '2012', 'no', 'no', 'no', 'Ciencias Ambientales', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/26 15:32:36', '2016/08/18 08:47:01', 'Comisión para la elaboración del Nuevo Plan de la Licenciatura en Ciencias Ambientales'),
('kdjh23PfSE1Sk8ldtYtS8HFELLDgFQskvaF8m0hKfl3ckk0HHa', 'fEVor', 'Agosto', '2008', 'Junio', '2012', 'Representante del Director ante el Consejo Académico de Área en Ciencias Sociales ', 'no', 'no', 'Ciencias Ambientales', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/26 15:33:04', '2016/08/18 08:45:12', ''),
('rdMjU8rIIhGSvE08FkaC0mSfiY2GaDkaogu23irOvHheYgXdFf', 'fEVor', 'Noviembre', '2011', 'Junio', '2012', 'Representante del personal académico del CIGA ante el Consejo Académico de la Licenciatura en Ciencias Ambientales', 'no', 'no', 'Ciencias Ambientales', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/26 15:33:34', '2016/08/18 08:44:47', ''),
('8mYHQgj8oqlre0d2ftbJSTdHS81Sj83sscNSraSErjO3sdprlf', 'fEVor', 'Octubre', '2013', 'Octubre', '2014', 'Miembro del Comité Académico Asesor de la Licenciatura en Ciencias Ambientales', 'no', 'no', 'Ciencias Ambientales', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/26 15:34:05', '2016/08/18 08:49:24', ''),
('v8WgnuM2IIqakDdOWSG6hCHlWng9ifSylS3qkDedThEZ6YDuzF', 'fEVor', 'Febrero', '2013', 'Marzo', '2014', 'no', 'no', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/26 15:34:37', '2016/08/18 08:21:43', 'Comisión para la Creación de la Licenciatura en Estudios Sociales y Gestión Local'),
('ubYk4I9Ub1WK3rKrj3kAO6d1DeH72eWwEwlrhSegg2XvJMfJkv', 'fEVor', 'Febrero', '2014', 'Diciembre', '2014', 'Miembro de la Comisión para la Creación del Bachillerato Regional UNAM Michoacán', 'no', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/26 15:35:12', '2016/08/18 08:21:58', ''),
('7dfr67dFWuAFEO5aFgcuqmS4WxI4uwhcLF2bIoSFNslFyFCDss', 'fEVor', 'Octubre', '2013', 'A la fecha', 'A la fecha', 'Miembro del Comité Académico Asesor de la Licenciatura en Geohistoria', 'no', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/26 15:35:41', '2016/08/18 08:22:23', ''),
('f3X1H633iSEuGsus9yElkS0rJjkNLzkEqdSHgPcpuGE2ehhDqH', 'fEVor', 'Octubre', '2014', 'A la fecha', 'A la fecha', 'Miembro del Comité Académico Asesor de la Licenciatura en Estudios Sociales y Gestión Local', 'no', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/26 15:36:06', '2016/08/18 08:23:00', ''),
('ng2gz8wDs8aDsArBrhg15hrAe3RFs8HfhhzGJShIEwfxTt9aKI', 'fEVor', 'Enero', 'N/A', 'A la fecha', 'A la fecha', 'Miembro del Comité de Publicaciones, representante del Área de Ciencias Sociales', 'no', 'no', 'Ciencias Sociales', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/26 15:36:32', '2016/08/18 08:44:34', ''),
('0t4tdSlOnrkckfJa2yGDbvFfNhEyk0HnhlFbv8rggNLSeF8xeM', 'fEVor', 'Enero', 'N/A', 'A la fecha', 'A la fecha', 'Editor Académico del Comité Editorial ', 'no', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/26 15:36:59', '2016/08/18 08:43:21', ''),
('GhiKn7RahAjSraE42Bjr4AOfMaRPYFH6Fbo9XjVetBEp1fdUde', 'fEVor', 'Octubre', '2015', 'A la fecha', 'A la fecha', 'Representante académico ante el Comité Académico del Posgrado en Geografía', 'no', 'Jefe de departamento de docencia', 'Docencia', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/26 15:37:53', '2016/08/18 08:43:44', ''),
('fFWSrjMy8kfq6abeLu2HI83llFcErlgh3s3rH3YLXO9aOsdafS', 'fEVor', 'Abril', '2012', 'Febrero', '2015', 'no', 'no', 'Coordinador de la Licenciatura en Geohistoria', 'Geohistoria', 'Escuela Nacional de Estudios Superiores, Unidad Morelia (ENES Morelia)', 'No', '2015/11/26 15:39:11', '2016/08/18 08:44:16', 'no'),
('0LfukxCfPYflGO48pFo8lr84U8hgfvSk8dHewhYpH4dk2f03ho', 'fEVor', 'Octubre', '2015', 'A la fecha', 'A la fecha', 'Jefe del Departamento de Docencia', 'no', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/26 15:39:43', '2016/08/19 19:09:37', ''),
('yILSQBbfswwtHYKYRsgs4inz4Xfl9riSwCsH5OxzvubSPf8NLT', 'fEVor', 'Noviembre', '2004', 'Agosto', '2007', 'Técnico Académico Asociado “C” de Tiempo Completo ', 'no', 'no', 'no', 'Instituto de Geografía, Unidad Morelia (UNAM Morelia)', 'No', '2015/11/26 16:30:32', '2015/11/26 16:30:32', ''),
('hjtH9odEgeFdOW9ISbYY45C8S0YIdoIBmS3juWwFFsr9SDjXWR', 'fEVor', 'Agosto', '2007', 'Febrero', '2011', 'Técnico Académico Asociado “C” de Tiempo Completo', 'no', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/26 16:36:02', '2015/11/26 16:36:02', ''),
('mSTFFgwWJ3dFsnNyHPftu6O6FyIh0dkL9L7phGjI2kcUf0F29s', 'fEVor', 'Febrero', '2011', 'Marzo', '2015', 'Técnico Académico Titular “A” de Tiempo Completo ', 'no', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'Si', '2015/11/26 16:36:47', '2015/11/26 16:36:47', ''),
('DiN5arJ9AafMFkFbdJokG2jFFOS6osa3gxxWfoSSb4f7wkYO7K', 'fEVor', 'Marzo', '2015', 'A la fecha', 'A la fecha', 'Técnico Académico Titular “B” de Tiempo Completo', 'no', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'Si', '2015/11/26 16:37:12', '2015/11/26 16:37:12', ''),
('8PWS1UdDgi2spD3cRrGSbI3145XjYy8dxFxSqfELhrFfFOFv5w', 'YxU7H', 'Enero', '1974', 'Septiembre', '1982', 'Lecturer', 'no', 'no', 'Urban and Rural Planning', 'Universidad de Dar es-Salam', 'No', '2015/11/26 19:44:43', '2015/11/26 19:44:43', ''),
('djrGC0feGHXwwjsOGSfjF2rOAQUFpfufYRoqjhcA97vbdsYfxh', 'YxU7H', 'Septiembre', '1982', 'Junio', '2008', 'Unversitaire Hoog Docent', 'no', 'no', 'Technology and Development', 'University of Twente', 'Si', '2015/11/26 19:46:00', '2015/11/26 19:46:00', ''),
('bvuYSr3h7xuK387EEWIMdechRcndpuHygn3hy8sbdHorf97fz8', '4th7o', 'Agosto', '2012', 'A la fecha', 'A la fecha', 'Profesor titular de asignatura', 'no', 'no', 'Licenciatura en Ciencias Biológicas', 'Escuela Nacional de Estudios Superiores, Unidad Morelia (ENES Morelia)', 'No', '2015/11/30 10:51:54', '2015/11/30 10:51:54', ''),
('s4Eg8ZuhO9uRlwFl5rziLfSdeAN4FyR1CngYjlWwe1df8YsRhH', '4th7o', 'Julio', '2012', 'Agosto', '2012', 'Profesor invitado', 'no', 'no', 'Licenciatura en Ciencias Ambientales', 'Universidad Autónoma de Tlaxcala', 'No', '2015/11/30 10:59:33', '2015/11/30 10:59:33', ''),
('Jb1SDDdIQsDio2wBk8ob0dYhzZHrTeo2X6Rcclr3N4EhmSGM4r', 'zF8gk', 'Junio', '2013', 'A la fecha', 'A la fecha', 'Técnico Académico Titular C de tiempo completo', 'no', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'Si', '2015/11/30 16:37:55', '2016/12/07 09:37:50', ''),
('0fjcg2wCLoHAtaEnIFdqxf6Rsh3qnh7g4h8esShGHPHlSqu5X1', 'prgh0', 'Enero', '2009', 'Octubre', '2014', 'Profesor Investigador Asociado C, Tiempo completo', 'Profesor Investigador ', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'Si', '2015/11/30 18:58:14', '2015/11/30 18:58:14', ''),
('irSdnQjt38Y8C1uibNN7SPPbDhgewZKPb62dzdk1jQToOrsFow', 'prgh0', 'Noviembre', '2014', 'A la fecha', 'A la fecha', 'Profesor Investigador Asociado C, Tiempo completo', 'Profesor Investigador', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/11/30 18:58:46', '2015/11/30 18:58:46', ''),
('uowrS5f9SlcTsrcFd8vL1vgru3lcY8H289fFWgRjYcihEQyWEb', 'DgFdm', 'Abril', '2011', 'Marzo', '2016', 'Investigador Ordinario de Carrera Asociado “C” de Tiempo Completo ', 'No aplica', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2015/12/01 15:00:05', '2016/06/27 12:37:09', ''),
('YOc4uwrpSq3Ydrc3FzwSSFEwjW9R2SDoeUyhPgSFF8S1jySth3', 'J8YEd', 'Abril', '2016', 'A la fecha', 'A la fecha', 'Técnico Académico Titular "A" de Tiempo Completo', 'no', 'no', 'Laboratorio de Análisis Espacial', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'Si', '2016/05/31 13:03:18', '2016/05/31 13:03:56', ''),
('JKNHgL2rWEJU9D6r6sFPwfHugTWFDMzn0eWjUHdSQLP0V3XyFm', 'h8fvn', 'Abril', '2009', 'Marzo', '2014', 'no', 'no', 'no', 'Museo Etnográfico, Facultad de Filosofía y Letras', 'Consejo Nacional de Investigaciones Científicas y Técnicas (CONICET)', 'No', '2016/06/01 10:25:53', '2016/12/01 11:06:22', ''),
('YUsjGSderJssr3Gszehtj9Td46rmSF2pl7jgcGYyJxHFC8Fd9f', 'biabG', 'Marzo', '2010', 'Diciembre', '2015', 'Técnico de Proyecto  en Área de Sistemas de Información', 'no', 'no', 'Cómputo', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2016/06/08 16:33:02', '2016/06/13 11:27:41', ''),
('7e87kdgrxcMafD4RjehShgjdsO2ZF3IOiRDDHSlh3MR8sXOau9', 'biabG', 'Agosto', '2004', 'Diciembre', '2004', 'no', 'no', 'Administrador de Sistemas de información (SIG’s)', 'no', 'Coordinación General de Gabinete y Planeación (CPLADE)', 'No', '2016/06/08 16:40:27', '2016/06/08 16:40:27', ''),
('kka5H1sKA4Cznnh49CgjbBadEtu9FRXNOWwGUL1Us5hQwBvIlC', 'biabG', 'Julio', '2005', 'Diciembre', '2005', 'Técico Superior', 'no', 'no', 'no', 'Instituto Nacional de Estadística y Geografía (INEGI)', 'No', '2016/06/08 16:43:11', '2016/06/08 16:43:11', ''),
('beGsdee3jQqZZltHZruoF6YlujzNHujWuGMinhSValih0rHskv', 'biabG', 'Junio', '2005', 'Marzo', '2007', 'Encargada de Sistemas', 'no', 'no', 'Sistemas del Club de Golf Tres Marías', 'Harlen Administrativo SA de CV', 'No', '2016/06/08 16:47:24', '2016/06/08 16:47:24', ''),
('Ruuw9eP7mcOk08sfekGcpgydgsw3vrxeWS3jyFfKOdGRfTjhkS', 'biabG', 'Marzo', '2007', 'Septiembre', '2007', 'Técnico Informático de Zona', 'no', 'no', 'Censo Agropecuario', 'Instituto Nacional de Estadística y Geografía (INEGI)', 'No', '2016/06/08 16:49:42', '2016/06/08 16:49:42', ''),
('hTFFdRJmnOxugJejIe1f0rsRy93se1483497343Exjd4fLdrdA', 'biabG', 'Septiembre', '2007', 'Febrero', '2010', 'Encargada del Área de Soporte Técnico', 'no', 'no', 'Sistemas', 'CodiNet S.A. DE C.V.', 'No', '2016/06/08 17:01:25', '2016/06/08 17:01:25', ''),
('APnO4iIfMsEpPURJ3Ej0REX78yHKcgaf93uF853sv2fGzhQzSc', 'n80rn', 'Febrero', '2006', 'Mayo', '2006', 'Residencia Profesional', 'no', 'no', 'Departamento de Computación y Telecomunicaciones', 'Instituto de Geografía', 'No', '2016/06/23 18:54:33', '2016/06/23 18:54:33', ''),
('k03nfFXEFz3obbhFR8dYjs1eH2nG1rOx3pdeyEekPHuLhkEBd3', 'DgFdm', 'Abril', '2016', 'A la fecha', 'A la fecha', 'Investigador Ordinario de Carrera Titular “A” de Tiempo Completo', 'no', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'Si', '2016/06/27 12:36:48', '2016/06/27 12:36:48', ''),
('WetIlPjZ2DdroW8WakrbwYRe5iynS3NlgYbLjeusfaxydddjYr', 'puYq7', 'Abril', '2016', 'A la fecha', 'A la fecha', 'Técnico Académico Titular "A"', 'no', 'no', 'Laboratorio de Análisis de Suelo y Agua', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'Si', '2016/06/27 13:04:50', '2016/06/27 13:04:50', ''),
('abfdhzl5eh18Pabd8x85gfeORY5S3GmZy4k6SfFkpphf0WN8Re', 'fEVor', 'Abril', '2006', 'Diciembre', '2008', 'Miembro por invitación de la International Society for the Study of Religion, Nature and Culture (ISSRNC)', 'no', 'Conference Director', 'Sede en la Universidad de Florida, Gainesville, EUA', 'International Society for the Study of Religion, Nature and Culture (ISSRNC)', 'No', '2016/10/08 16:02:38', '2016/10/08 16:05:31', ''),
('cwgdFjeavu3vRFkgfseexlF4rWRfSjLDTYq9blsJgL4nud2uQh', 'fEVor', 'Abril', '2007', 'A la fecha', 'A la fecha', 'no', 'Asamblea General Constitutiva, celebrada en el Instituto de Geografía, UNAM, el 19 de abril de 2007. ', 'Miembro fundador, por invitación, de la Asociación de Historiadores de las Ciencias y las Humanidades A.C. (HCyH)', 'no', 'Instituto de Geografía', 'Si', '2016/10/08 16:04:26', '2016/10/08 16:04:26', ''),
('gb28KHdUZft3kFNFGwy02jzswrji8x8TuulsxccwW8qdfjbr8o', 'fEVor', 'Febrero', '2011', 'A la fecha', 'A la fecha', 'Miembro regular de la Conference of Latin Americanist Geographers (CLAG). ', 'no', 'no', 'no', 'Conference of Latin Americanist Geographers (CLAG)', 'No', '2016/10/08 16:06:37', '2016/10/08 16:06:37', ''),
('d3P9kfn3ECJjl7SfYbjH1eoluOb1G3fskYFu4FHOybHf6L0SS4', 'rWKXd', 'Septiembre', '2015', 'A la fecha', 'A la fecha', 'no', 'no', 'Director', 'Dirección de Cooperación Académica', 'Dirección General de Cooperación e Internacionalización (DGECI)', 'No', '2016/11/30 11:21:27', '2016/11/30 17:27:48', 'Director de Cooperación Académica'),
('XijJBotdjE23TBDIEFRs25fmVNFoLOg2ndLStQyl2rSYrtEwPL', 'gb4go', 'Enero', '2014', 'Diciembre', '2016', 'Profesor de Asignatura', 'no', 'no', 'no', 'Facultad de Economía', 'No', '2016/11/30 15:20:10', '2016/11/30 15:20:10', ''),
('ybsdg20RfIw15gRPBhjuuyOODFr070htYRvUhalr7Xk0n2532g', 'ubFaE', 'Agosto', '2008', 'Agosto', '2009', 'Subdirector de recursos genéticos', 'no', 'Subdirector de recursos genéticos', 'Dirección general del sector primario y recursos naturales renovables', 'Secretaría de Medio Ambiente y Recursos Naturales (SEMARNAT)', 'No', '2016/12/05 10:16:36', '2016/12/05 10:17:00', ''),
('RHdpzeDHHjmLbp3eyFijerAHxk5q505OsH3sgewFk8r2lbC6bj', '88SSU', 'Marzo', '2007', 'A la fecha', 'A la fecha', 'Investigador Titular A', 'no', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'Si', '2016/12/05 11:42:17', '2016/12/05 11:42:17', ''),
('kdOIrALYjwRESfHE82yfv4dirul7HFUSladSldwK3W7fYTXN38', 'c3fhV', 'Junio', '2016', 'A la fecha', 'A la fecha', 'Técnico Académico Asociado C T.C.', 'Técnico Académico Asociado C T.C.', 'no', 'Unidad de Cómputo', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2016/12/06 12:29:15', '2016/12/06 12:30:52', ''),
('qkfs36pdkbdN8EFxjkfcUeuXFajr2SSs354Swke8uySYz9ecU3', 'c3fhV', 'Enero', 'N/A', 'A la fecha', 'A la fecha', 'Servicio Profesional en la Unidad de Cómputo', 'no', 'no', 'Unidad de Cómputo', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2016/12/06 12:32:21', '2016/12/06 12:32:21', ''),
('4B10FbQlJOb8U4Ca9uzdf13GgjbkdkerwaNqu30Hxut36I28S5', 'c3fhV', 'Agosto', '2008', 'Diciembre', '2008', 'Pasante en desarrollo Web', 'no', 'no', 'Unidad de Cómputo', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2016/12/06 12:33:37', '2016/12/06 12:33:37', ''),
('Ox48Fmmw8HE2jws0F3GS1ydHF6VKtwpdd3b2S3Cy26qAkOkO0r', 'c3fhV', 'Agosto', '2007', 'Diciembre', '2007', 'Residente Profesional en desarrollo Web', 'no', 'no', 'Unidad de Cómputo', 'Instituto de Investigaciones en Ecosistemas y Sustentabilidad (IIES)', 'No', '2016/12/06 12:34:50', '2016/12/06 12:34:50', ''),
('CRVahdF1Fx8zqTkXP7yESmjfsHDu4OItsHKZQrtDkf33lhgtdF', 'c3fhV', 'Octubre', '2015', 'Diciembre', '2015', 'no', 'no', 'no', 'no', 'H. Ayuntamiento de Morelos', 'No', '2016/12/06 12:36:28', '2016/12/06 12:36:28', 'Consultor Externo en Soporte Técnico'),
('evYE4f3DE13SxewHtdukHCkvb0gPLk2svHYfnYu3FMhDsfrgdr', 'c3fhV', 'Enero', '2013', 'Enero', '2015', 'Servicio Profesional de apoyo a Control Escolar', 'no', 'no', 'Control Escolar', 'Telebachillerato Michoacán', 'No', '2016/12/06 12:37:38', '2016/12/06 12:37:38', ''),
('EsOherFl43wFSnJdufif8gcAlHuwhuY4GStmsHhrMP1lF3tk85', 'c3fhV', 'Enero', '2009', 'Diciembre', '2010', 'Servicio Profesional de apoyo a Control Escolar', 'no', 'no', 'Dirección de Control Escolar', 'Universidad Michoacana de San Nicolás de Hidalgo (UMSNH)', 'No', '2016/12/06 12:39:00', '2016/12/06 12:39:00', ''),
('DGJV8h0Y0z3FfNUGs9r8jaMkq7YgH8z3Lrj4vhF8kbsay4wwQL', 'c3fhV', 'Enero', '2009', 'Octubre', '2009', 'no', 'no', 'no', 'no', 'TECIF', 'No', '2016/12/06 12:40:12', '2016/12/06 12:40:12', 'Desarrollador Web'),
('fHY4ZtUGlDQHK0FKGy5mFlfWHHRsWFsOuI9E7GJl37Hivy3gZ1', 'c3fhV', 'Enero', 'N/A', 'A la fecha', 'A la fecha', 'Servicio Social', 'no', 'no', 'Cómputo', 'Fideicomisos Instituidos en Relación con la Agrícultura (FIRA)', 'No', '2016/12/06 12:41:47', '2016/12/06 12:41:47', ''),
('C3jrEO9i69q8YOKQa3ixyHpOh23cB4ihLr6kwgs2bmAssqSnkB', 'ftTrS', 'Agosto', '1984', 'Octubre', '1986', 'Técnico Académico Auxiliar B de Tiempo Completo', 'no', 'no', 'División de Estudios de Posgrado', 'Facultad de Ingeniería', 'No', '2016/12/07 11:27:10', '2016/12/07 11:27:10', ''),
('8gdOfrYf0kmhpheFSoFX22xOnyMkeJEf51Ywr5mtrsOH3sbSRV', 'ftTrS', 'Noviembre', '1986', 'Septiembre', '1990', 'Técnico Académico Asociado C de Tiempo Completo. ', 'no', 'Jefe del Laboratorio de Cómputo', 'no', 'Instituto de Geografía', 'No', '2016/12/07 11:29:56', '2016/12/07 11:44:12', ''),
('sUizyasIiaVRF8gxwwH9EuAhQdp8YS9MWs4rw4YtVZeXeEsfme', 'ftTrS', 'Octubre', '1992', 'Abril', '1994', 'Técnico Académico Titular B de Tiempo Completo', 'no', 'no', 'no', 'Instituto de Geografía', 'No', '2016/12/07 11:31:58', '2016/12/07 11:31:58', ''),
('ObfSlFOd4xHNF7jFwWeluDwRcjnFdeTLs3FsKMHpHAS1Xqb92R', 'ftTrS', 'Octubre', '1998', 'Octubre', '2001', 'Técnico Académico Titular B de Tiempo Completo. ', 'no', 'Jefe del Laboratorio de Sistemas de Información Geográfica y Percepción Remota', 'no', 'Instituto de Geografía', 'No', '2016/12/07 11:33:51', '2016/12/07 11:33:51', ''),
('EnIwu249OJxS8sSwKuf8fyLe8VRXOWVhbfxIj4XtdI2R0FOVS2', 'ftTrS', 'Noviembre', '2001', 'Noviembre', '2004', 'Técnico Académico Titular C de Tiempo Completo', 'Jefe del Laboratorio de Sistemas de Información Geográfica y Percepción Remota', 'no', 'no', 'Instituto de Geografía', 'No', '2016/12/07 11:35:40', '2016/12/07 11:35:40', ''),
('j85OXWgwRFvdx7pBFHl9bl3kDYfhxdkd7EmV6seJgssQff2Qf9', 'ftTrS', 'Diciembre', '2004', 'Diciembre', '2009', 'Técnico Académico Titular C de Tiempo Completo', 'no', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2016/12/07 11:38:00', '2016/12/07 11:38:00', ''),
('eRFyo1axt8G9j8eaY8Txf3ZSP9n2ERpjYYSfJ3gKc3QkKLYF9g', 'ftTrS', 'Enero', '2009', 'Noviembre', '2015', 'Técnico Académico Titular C, Tiempo completo', 'Coordinador del Laboratorio de Análisis Espacial', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'Si', '2016/12/07 11:40:45', '2016/12/07 11:41:16', ''),
('g3eH3rgVdb14huf4UOBdflhfhrb8yuuFS3hwIyLlQDdnjqupkc', 'ftTrS', 'Noviembre', '2015', 'A la fecha', 'A la fecha', 'Técnico Académico Titular C de Tiempo Completo', 'no', 'Secretario Técnico', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'Si', '2016/12/07 11:43:15', '2016/12/07 11:43:15', ''),
('kqle5sgE7S2DiYy88rkcb32FrgInRyVqwb3ffu1Y86odYi9YHa', 'ftTrS', 'Febrero', '1995', 'Febrero', '1996', 'no', 'no', 'no', 'no', 'Instituto Nacional de Ecología y Cambio Climático (INECC)', 'No', '2016/12/07 12:55:03', '2016/12/07 13:42:42', 'Coordinador de Proyecto'),
('sYFjHSIH9FntU6eaeLRguHf42rh58rEh5hQddkOE3uD0szN4HE', 'ftTrS', 'Febrero', '1996', 'Octubre', '1998', 'Technical Officer', 'no', 'no', 'no', 'Commission for Environmental Cooperation', 'No', '2016/12/07 13:45:29', '2016/12/07 13:45:29', ''),
('gjW86l5oA8BSCRjVog7wHYLpjI6FYwkHVcyNNLTcfIoXKo1fSw', 'Y6pdF', 'Octubre', '2014', 'Diciembre', '2015', 'no', 'Cátedras CONACYT', 'no', 'no', 'Consejo Nacional de Ciencia y Tecnología (CONACYT)', 'No', '2016/12/08 04:13:13', '2016/12/08 04:13:13', ''),
('qjgexDw4TgESfFFDmJifHDS9Jd8FOsCrKqOnYGfvsxWwRSac2b', 'Y6pdF', 'Enero', '2016', 'N/A', 'N/A', 'Investigador Asociado C Tiempo Completo', 'Investigador', 'no', 'no', 'Centro de Investigaciones en Geografía Ambiental (CIGA)', 'No', '2016/12/08 04:14:33', '2016/12/08 04:14:33', ''),
('bRf4wd9Z453ieAlKjfgXfES8DOM92iasR3Lr8credL8zbOHz8q', '16ymf', 'Enero', '2012', 'A la fecha', 'A la fecha', 'Profesor De Maestría En Derecho', 'Profesor', 'no', 'Control Escolar', 'Universidad Vasco de Quiroga (UVAQ)', 'No', '2016/12/08 21:37:07', '2016/12/08 21:37:07', ''),
('runb1hEEPEVh8Ffj8uMOObYFmjfvn3cAerd3B0LhZXj9jXRDKe', '16ymf', 'Junio', '2014', 'Abril', '2015', 'Evaluador Del Proyecto', 'no', 'no', 'Departamento De Vinculación', 'Universidad Michoacana de San Nicolás de Hidalgo (UMSNH)', 'No', '2016/12/08 21:38:54', '2016/12/08 21:38:54', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `uk_experiencia`
--
ALTER TABLE `uk_experiencia`
  ADD PRIMARY KEY (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
