-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 27-02-2026 a las 20:31:14
-- Versión del servidor: 9.1.0
-- Versión de PHP: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `techsenahsgs`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistencias`
--

DROP TABLE IF EXISTS `asistencias`;
CREATE TABLE IF NOT EXISTS `asistencias` (
  `id_asistencia` int NOT NULL AUTO_INCREMENT,
  `documento_estudiante` varchar(20) NOT NULL,
  `id_competencia` int NOT NULL,
  `fecha_registro` datetime DEFAULT CURRENT_TIMESTAMP,
  `observaciones` text,
  `fecha_salida` datetime DEFAULT NULL,
  PRIMARY KEY (`id_asistencia`),
  KEY `fk_asistencia_estudiante` (`documento_estudiante`),
  KEY `fk_asistencia_competencia` (`id_competencia`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `asistencias`
--

INSERT INTO `asistencias` (`id_asistencia`, `documento_estudiante`, `id_competencia`, `fecha_registro`, `observaciones`, `fecha_salida`) VALUES
(10, '1046426401', 1, '2026-02-19 21:29:29', '', '2026-02-19 21:29:38'),
(11, '1046426401', 1, '2026-02-19 21:29:45', '', '2026-02-19 21:29:51'),
(12, '1046426401', 1, '2026-02-20 13:17:07', '', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auditoria`
--

DROP TABLE IF EXISTS `auditoria`;
CREATE TABLE IF NOT EXISTS `auditoria` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(50) COLLATE utf8mb3_spanish2_ci DEFAULT NULL,
  `accion` varchar(100) COLLATE utf8mb3_spanish2_ci DEFAULT NULL,
  `objeto` varchar(100) COLLATE utf8mb3_spanish2_ci DEFAULT NULL,
  `detalles` text COLLATE utf8mb3_spanish2_ci,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish2_ci;

--
-- Volcado de datos para la tabla `auditoria`
--

INSERT INTO `auditoria` (`id`, `usuario`, `accion`, `objeto`, `detalles`, `fecha`) VALUES
(1, 'admin', 'login admin', '', '', '2026-02-27 13:31:15'),
(2, 'admin', 'login admin', '', '', '2026-02-27 13:44:54'),
(3, '1102353842', 'login aprendiz', '', '', '2026-02-27 15:04:52'),
(4, '1102353842', 'logout aprendiz', '', '', '2026-02-27 15:05:11'),
(5, 'admin', 'login admin', '', '', '2026-02-27 15:05:39'),
(6, 'admin', 'logout admin', '', '', '2026-02-27 15:07:09'),
(7, 'admin', 'login admin', '', '', '2026-02-27 15:07:54'),
(8, 'admin', 'mover a papelera', '1102353842', '', '2026-02-27 15:08:16'),
(9, 'admin', 'logout admin', '', '', '2026-02-27 15:08:21'),
(10, 'admin', 'login admin', '', '', '2026-02-27 15:08:58'),
(11, 'admin', 'restaurar aprendiz', '1102353842', '', '2026-02-27 15:09:01'),
(12, 'admin', 'logout admin', '', '', '2026-02-27 15:09:15'),
(13, 'admin', 'login admin', '', '', '2026-02-27 15:09:42'),
(14, 'admin', 'mover a papelera', '1102353842', '', '2026-02-27 15:09:48'),
(15, 'admin', 'logout admin', '', '', '2026-02-27 15:09:58'),
(16, 'admin', 'login admin', '', '', '2026-02-27 15:10:04'),
(17, 'admin', 'restaurar aprendiz', '1102353842', '', '2026-02-27 15:10:13'),
(18, 'admin', 'logout admin', '', '', '2026-02-27 15:10:21'),
(19, 'admin', 'login admin', '', '', '2026-02-27 15:16:28');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `competencias`
--

DROP TABLE IF EXISTS `competencias`;
CREATE TABLE IF NOT EXISTS `competencias` (
  `id_competencia` int NOT NULL AUTO_INCREMENT,
  `nombre_competencia` varchar(255) NOT NULL,
  `horas_totales` int NOT NULL,
  PRIMARY KEY (`id_competencia`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `competencias`
--

INSERT INTO `competencias` (`id_competencia`, `nombre_competencia`, `horas_totales`) VALUES
(1, 'Desarrollo de interfaces gráficas', 40),
(2, 'Bases de datos relacionales', 60);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiantes`
--

DROP TABLE IF EXISTS `estudiantes`;
CREATE TABLE IF NOT EXISTS `estudiantes` (
  `id_estudiante` int NOT NULL AUTO_INCREMENT,
  `documento` varchar(20) NOT NULL,
  `nombre_completo` varchar(150) NOT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `password` varchar(255) NOT NULL DEFAULT 'sena123',
  `id_ficha` int DEFAULT NULL,
  `cambio_pass` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id_estudiante`),
  UNIQUE KEY `documento` (`documento`),
  KEY `fk_estudiante_ficha` (`id_ficha`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `estudiantes`
--

INSERT INTO `estudiantes` (`id_estudiante`, `documento`, `nombre_completo`, `correo`, `password`, `id_ficha`, `cambio_pass`) VALUES
(5, '1046426401', 'Elver', 'gravisludio@gmail.com', 'sena123', 1, 0),
(10, '1102353842', 'Omar Alexis Ardila', 'xd@gmai.com', 'sena123', 1, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiantes_eliminados`
--

DROP TABLE IF EXISTS `estudiantes_eliminados`;
CREATE TABLE IF NOT EXISTS `estudiantes_eliminados` (
  `documento` varchar(20) NOT NULL,
  `nombre_completo` varchar(150) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `id_ficha` int DEFAULT NULL,
  `fecha_eliminacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`documento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fichas`
--

DROP TABLE IF EXISTS `fichas`;
CREATE TABLE IF NOT EXISTS `fichas` (
  `id_ficha` int NOT NULL AUTO_INCREMENT,
  `codigo_ficha` varchar(20) NOT NULL,
  `nombre_programa` varchar(150) NOT NULL,
  `jornada` enum('Mañana','Tarde','Noche','Mixta') DEFAULT 'Mañana',
  PRIMARY KEY (`id_ficha`),
  UNIQUE KEY `codigo_ficha` (`codigo_ficha`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `fichas`
--

INSERT INTO `fichas` (`id_ficha`, `codigo_ficha`, `nombre_programa`, `jornada`) VALUES
(1, '2555555', 'Análisis y Desarrollo de Software', 'Mañana'),
(2, '2666666', 'Programación de Software', 'Tarde');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios_admin`
--

DROP TABLE IF EXISTS `usuarios_admin`;
CREATE TABLE IF NOT EXISTS `usuarios_admin` (
  `id_admin` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_admin`),
  UNIQUE KEY `usuario` (`usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `usuarios_admin`
--

INSERT INTO `usuarios_admin` (`id_admin`, `usuario`, `password`, `nombre`) VALUES
(1, 'admin', 'admin123', 'Administrador HSGS');

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `asistencias`
--
ALTER TABLE `asistencias`
  ADD CONSTRAINT `fk_asistencia_competencia` FOREIGN KEY (`id_competencia`) REFERENCES `competencias` (`id_competencia`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_asistencia_estudiante` FOREIGN KEY (`documento_estudiante`) REFERENCES `estudiantes` (`documento`) ON DELETE CASCADE;

--
-- Filtros para la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  ADD CONSTRAINT `fk_estudiante_ficha` FOREIGN KEY (`id_ficha`) REFERENCES `fichas` (`id_ficha`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
