-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 19-02-2026 a las 18:29:24
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
-- Base de datos: `base_datos`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

DROP TABLE IF EXISTS `productos`;
CREATE TABLE IF NOT EXISTS `productos` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `CODIGO` char(10) NOT NULL DEFAULT '0',
  `NOMBRE` char(20) NOT NULL DEFAULT '0',
  `MODELO` char(20) NOT NULL DEFAULT '0',
  `PRECIO` char(50) NOT NULL DEFAULT '0',
  `CANTIDAD` char(50) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=188 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`ID`, `CODIGO`, `NOMBRE`, `MODELO`, `PRECIO`, `CANTIDAD`) VALUES
(39, 'RES001', 'RESISTENCIA', 'RV', '2.00', '222'),
(40, 'TRAS-11', 'TRANSISTOR', 'PNP', '1.00', '554'),
(44, '10101', 'CONDENSADOR', 'CERAMICO', '2.00', '100'),
(168, 'DB121', 'DIODO', 'ZENER', '1.50', '231'),
(169, 'IC002', 'IC', 'AND', '1.00', '200'),
(170, 'IC003', 'IC', 'XOR', '1.00', '300'),
(171, 'D0092', 'DIOD0', 'ZENER', '2.00', '232'),
(172, 'RE21', 'RELE', '221R', '2.50', '423'),
(173, '2560', 'ARDUINO', 'MEGA', '30.0', '37'),
(174, '2021DS', 'ARDUINO', 'UNO R3', '15.50', '73'),
(175, 'RES2021', 'RESISTENCIA', '4B', '0.10', '1000'),
(176, 'LED122', 'LED', 'GREENR3', '0.50', '144'),
(177, 'LDR43', 'LDR', 'LDRG', '2.00', '43'),
(178, 'FUSI232', 'FUSIBLE', '23FDEW', '2.00', '331'),
(179, 'MATRIZ32', 'MATRIZ', '32X8', '50.0', '56'),
(180, 'SENSORRE', 'ULTRASONIC', 'RGR0544', '5.00', '231'),
(181, '555N', 'TIMER', '555', '1.50', '621'),
(182, 'ER43', 'PILAS', 'AAA', '2.00', '544'),
(185, '1212', '12121', '12121', '22121', '12121');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
