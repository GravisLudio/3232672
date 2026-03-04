-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 04-03-2026 a las 21:18:49
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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `asistencias`
--

INSERT INTO `asistencias` (`id_asistencia`, `documento_estudiante`, `id_competencia`, `fecha_registro`, `observaciones`, `fecha_salida`) VALUES
(16, '1010101', 33, '2026-03-02 06:05:00', 'Llegó a tiempo', '2026-03-02 12:00:00'),
(17, '1010102', 33, '2026-03-02 06:25:00', 'Retardo - Trancón en la autopista', '2026-03-02 12:00:00'),
(18, '1010103', 33, '2026-03-02 06:02:00', 'Sin novedades', '2026-03-02 11:55:00'),
(19, '2020201', 41, '2026-03-02 12:10:00', 'Ingreso puntual jornada tarde', '2026-03-02 18:00:00'),
(20, '1010105', 36, '2026-02-24 06:05:00', 'Asistencia normal', '2026-02-24 12:49:42');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auditoria`
--

DROP TABLE IF EXISTS `auditoria`;
CREATE TABLE IF NOT EXISTS `auditoria` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish2_ci DEFAULT NULL,
  `accion` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish2_ci DEFAULT NULL,
  `objeto` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish2_ci DEFAULT NULL,
  `detalles` text CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish2_ci,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=86 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish2_ci;

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
(19, 'admin', 'login admin', '', '', '2026-02-27 15:16:28'),
(20, '1046426401', 'login aprendiz', '', '', '2026-03-01 10:53:01'),
(21, '1046426401', 'logout aprendiz', '', '', '2026-03-01 10:53:29'),
(22, '1046426401', 'login aprendiz', '', '', '2026-03-01 10:53:55'),
(23, '1046426401', 'logout aprendiz', '', '', '2026-03-01 11:05:05'),
(24, 'admin', 'login admin', '', '', '2026-03-01 11:05:20'),
(25, 'admin', 'logout admin', '', '', '2026-03-01 11:05:44'),
(26, '1046426401', 'login aprendiz', '', '', '2026-03-01 11:06:20'),
(27, '1046426401', 'logout aprendiz', '', '', '2026-03-01 11:07:38'),
(28, 'admin', 'login admin', '', '', '2026-03-01 12:27:36'),
(29, 'admin', 'login admin', '', '', '2026-03-01 12:42:59'),
(30, 'admin', 'login admin', '', '', '2026-03-01 12:59:30'),
(31, 'admin', 'login admin', '', '', '2026-03-01 13:02:14'),
(32, 'admin', 'login admin', '', '', '2026-03-01 16:22:05'),
(33, 'admin', 'login admin', '', '', '2026-03-01 16:22:58'),
(34, 'admin', 'login admin', '', '', '2026-03-01 16:23:37'),
(35, 'admin', 'login admin', '', '', '2026-03-01 16:24:19'),
(36, 'ADMIN', 'login admin', '', '', '2026-03-01 16:24:59'),
(37, 'admin', 'login admin', '', '', '2026-03-01 17:32:02'),
(38, 'admin', 'login admin', '', '', '2026-03-01 17:32:43'),
(39, 'admin', 'login admin', '', '', '2026-03-01 17:33:16'),
(40, 'admin', 'login admin', '', '', '2026-03-01 17:34:29'),
(41, 'admin', 'login admin', '', '', '2026-03-01 17:35:48'),
(42, 'admin', 'login admin', '', '', '2026-03-01 17:45:30'),
(43, 'admin', 'login admin', '', '', '2026-03-01 17:47:20'),
(44, 'admin', 'login admin', '', '', '2026-03-01 17:49:53'),
(45, 'admin', 'login admin', '', '', '2026-03-01 17:52:27'),
(46, 'ADMIN', 'login admin', '', '', '2026-03-01 17:53:37'),
(47, 'admin', 'login admin', '', '', '2026-03-01 18:00:50'),
(48, 'admin', 'login admin', '', '', '2026-03-01 18:11:25'),
(49, 'admin', 'login admin', '', '', '2026-03-01 18:12:09'),
(50, 'admin', 'login admin', '', '', '2026-03-01 18:14:07'),
(51, 'admin', 'login admin', '', '', '2026-03-01 18:20:51'),
(52, 'admin', 'login admin', '', '', '2026-03-01 18:22:36'),
(53, 'admin', 'login admin', '', '', '2026-03-01 18:24:25'),
(54, 'admin', 'login admin', '', '', '2026-03-01 18:25:01'),
(55, 'admin', 'login admin', '', '', '2026-03-01 18:26:54'),
(56, 'admin', 'logout admin', '', '', '2026-03-01 18:27:39'),
(57, 'admin', 'login admin', '', '', '2026-03-01 19:07:37'),
(58, 'admin', 'login admin', '', '', '2026-03-01 19:12:12'),
(59, 'admin', 'login admin', '', '', '2026-03-01 19:12:37'),
(60, 'admin', 'login admin', '', '', '2026-03-01 19:40:53'),
(61, 'admin', 'login admin', '', '', '2026-03-01 19:41:54'),
(62, 'admin', 'login admin', '', '', '2026-03-01 19:47:05'),
(63, 'admin', 'login admin', '', '', '2026-03-01 21:09:25'),
(64, 'admin', 'login admin', '', '', '2026-03-01 21:16:23'),
(65, 'admin', 'login admin', '', '', '2026-03-01 21:42:46'),
(66, 'admin', 'login admin', '', '', '2026-03-01 21:43:15'),
(67, 'admin', 'login admin', '', '', '2026-03-01 21:48:54'),
(68, 'admin', 'login admin', '', '', '2026-03-01 21:51:05'),
(69, 'admin', 'login admin', '', '', '2026-03-01 22:12:14'),
(70, 'admin', 'login admin', '', '', '2026-03-01 22:25:19'),
(71, 'admin', 'login admin', '', '', '2026-03-01 22:35:23'),
(72, 'admin', 'login admin', '', '', '2026-03-01 22:36:16'),
(73, 'admin', 'login admin', '', '', '2026-03-01 22:37:19'),
(74, 'admin', 'login admin', '', '', '2026-03-01 22:39:18'),
(75, 'admin', 'login admin', '', '', '2026-03-01 23:17:03'),
(76, 'admin', 'login admin', '', '', '2026-03-01 23:28:14'),
(77, 'admin', 'login admin', '', '', '2026-03-01 23:34:36'),
(78, 'admin', 'login admin', '', '', '2026-03-01 23:58:52'),
(79, 'admin', 'login admin', '', '', '2026-03-02 00:48:21'),
(80, 'admin', 'login admin', '', '', '2026-03-02 00:52:19'),
(81, 'admin', 'login admin', '', '', '2026-03-02 02:07:48'),
(82, 'admin', 'login admin', '', '', '2026-03-04 14:05:34'),
(83, 'admin', 'logout admin', '', '', '2026-03-04 14:08:14'),
(84, 'admin', 'login admin', '', '', '2026-03-04 14:09:04'),
(85, 'admin', 'logout admin', '', '', '2026-03-04 14:10:16');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `competencias`
--

DROP TABLE IF EXISTS `competencias`;
CREATE TABLE IF NOT EXISTS `competencias` (
  `id_competencia` int NOT NULL AUTO_INCREMENT,
  `nombre_competencia` varchar(255) NOT NULL,
  `horas_totales` int NOT NULL,
  `Tipo` enum('Técnica','Complementaria') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id_competencia`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `competencias`
--

INSERT INTO `competencias` (`id_competencia`, `nombre_competencia`, `horas_totales`, `Tipo`) VALUES
(33, 'Analizar conceptos contables y financieros', 48, 'Complementaria'),
(34, 'Desarrollar la estructura de datos del software', 160, 'Técnica'),
(35, 'Diseñar la arquitectura de software', 120, 'Técnica'),
(36, 'Codificar la solución de software', 200, 'Técnica'),
(37, 'Validar la aplicación mediante pruebas', 80, 'Técnica'),
(38, 'Interactuar en lengua inglesa (Técnica)', 60, 'Técnica'),
(39, 'Aplicar prácticas de protección ambiental', 36, 'Complementaria'),
(40, 'Gestionar procesos de comunicación eficaz', 48, 'Complementaria'),
(41, 'Razonar cuantitativamente (Matemáticas)', 48, 'Complementaria'),
(42, 'Utilizar herramientas informáticas', 48, 'Complementaria');

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
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `estudiantes`
--

INSERT INTO `estudiantes` (`id_estudiante`, `documento`, `nombre_completo`, `correo`, `password`, `id_ficha`, `cambio_pass`) VALUES
(11, '1010101', 'Gravis Ludio', 'gravis@sena.edu.co', 'pass123', 5, 0),
(12, '1010102', 'Hidden Sage', 'hidden@sena.edu.co', 'pass123', 5, 0),
(13, '1010103', 'Carlos Mario', 'carlos@sena.edu.co', 'pass123', 5, 0),
(14, '1010104', 'Ana Maria', 'ana@sena.edu.co', 'pass123', 5, 0),
(15, '1010105', 'Beatriz Pinzon', 'betty@sena.edu.co', 'pass123', 5, 0),
(16, '2020201', 'Juan Valdez', 'juan@sena.edu.co', 'pass123', 6, 0),
(17, '2020202', 'Sofia Vergara', 'sofia@sena.edu.co', 'pass123', 6, 0);

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
  `fecha_inicio` date DEFAULT NULL,
  PRIMARY KEY (`id_ficha`),
  UNIQUE KEY `codigo_ficha` (`codigo_ficha`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `fichas`
--

INSERT INTO `fichas` (`id_ficha`, `codigo_ficha`, `nombre_programa`, `jornada`, `fecha_inicio`) VALUES
(5, '2670101', 'Análisis y Desarrollo de Software', 'Mañana', NULL),
(6, '2670102', 'Análisis y Desarrollo de Software', 'Tarde', NULL),
(7, '2670103', 'Programación de Software', 'Mañana', NULL),
(8, '2680201', 'Desarrollo de Aplicaciones Móviles', 'Noche', NULL),
(9, '2680202', 'Análisis y Desarrollo de Software', 'Mañana', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ficha_competencias`
--

DROP TABLE IF EXISTS `ficha_competencias`;
CREATE TABLE IF NOT EXISTS `ficha_competencias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_ficha` int NOT NULL,
  `id_competencia` int NOT NULL,
  `orden` int DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_ficha_comp` (`id_ficha`,`id_competencia`),
  KEY `fk_ficha_comp_ficha` (`id_ficha`),
  KEY `fk_ficha_comp_comp` (`id_competencia`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `ficha_competencias`
--

INSERT INTO `ficha_competencias` (`id`, `id_ficha`, `id_competencia`, `orden`) VALUES
(1, 5, 33, 1),
(2, 5, 34, 2),
(3, 5, 35, 3),
(4, 5, 36, 4),
(5, 5, 37, 5),
(6, 5, 38, 6),
(7, 5, 39, 7),
(8, 5, 40, 8),
(9, 5, 41, 9),
(10, 5, 42, 10),
(11, 6, 33, 1),
(12, 6, 34, 2),
(13, 6, 35, 3),
(14, 6, 36, 4),
(15, 6, 37, 5),
(16, 6, 38, 6),
(17, 6, 39, 7),
(18, 6, 40, 8),
(19, 6, 41, 9),
(20, 6, 42, 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horarios`
--

DROP TABLE IF EXISTS `horarios`;
CREATE TABLE IF NOT EXISTS `horarios` (
  `id_horario` int NOT NULL AUTO_INCREMENT,
  `id_competencia` int NOT NULL,
  `dia_semana` enum('Lunes','Martes','Miércoles','Jueves','Viernes','Sábado') NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `id_ficha` int DEFAULT NULL,
  PRIMARY KEY (`id_horario`),
  KEY `id_competencia` (`id_competencia`),
  KEY `id_ficha` (`id_ficha`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `horarios`
--

INSERT INTO `horarios` (`id_horario`, `id_competencia`, `dia_semana`, `hora_inicio`, `hora_fin`, `id_ficha`) VALUES
(1, 33, 'Lunes', '06:00:00', '12:00:00', 5),
(2, 40, 'Martes', '06:00:00', '12:00:00', 5),
(3, 36, 'Miércoles', '06:00:00', '12:00:00', 5),
(4, 34, 'Jueves', '06:00:00', '12:00:00', 5),
(5, 35, 'Viernes', '06:00:00', '12:00:00', 5),
(6, 41, 'Lunes', '12:00:00', '18:00:00', 6),
(7, 42, 'Martes', '12:00:00', '18:00:00', 6),
(8, 36, 'Miércoles', '12:00:00', '18:00:00', 6),
(9, 34, 'Jueves', '12:00:00', '18:00:00', 6),
(10, 35, 'Viernes', '12:00:00', '18:00:00', 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `instructores`
--

DROP TABLE IF EXISTS `instructores`;
CREATE TABLE IF NOT EXISTS `instructores` (
  `id_instructor` int NOT NULL AUTO_INCREMENT,
  `cedula` varchar(20) NOT NULL,
  `nombre_completo` varchar(150) NOT NULL,
  `id_competencia` int DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_instructor`),
  UNIQUE KEY `cedula` (`cedula`),
  KEY `id_competencia` (`id_competencia`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
-- Filtros para la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  ADD CONSTRAINT `fk_estudiante_ficha` FOREIGN KEY (`id_ficha`) REFERENCES `fichas` (`id_ficha`) ON DELETE SET NULL;

--
-- Filtros para la tabla `ficha_competencias`
--
ALTER TABLE `ficha_competencias`
  ADD CONSTRAINT `fk_ficha_comp_comp` FOREIGN KEY (`id_competencia`) REFERENCES `competencias` (`id_competencia`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_ficha_comp_ficha` FOREIGN KEY (`id_ficha`) REFERENCES `fichas` (`id_ficha`) ON DELETE CASCADE;

--
-- Filtros para la tabla `horarios`
--
ALTER TABLE `horarios`
  ADD CONSTRAINT `horarios_ibfk_2` FOREIGN KEY (`id_competencia`) REFERENCES `competencias` (`id_competencia`) ON DELETE CASCADE,
  ADD CONSTRAINT `horarios_ibfk_3` FOREIGN KEY (`id_ficha`) REFERENCES `fichas` (`id_ficha`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
