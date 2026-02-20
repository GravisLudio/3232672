-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 19-02-2026 a las 22:30:26
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
-- Estructura de tabla para la tabla `historial_eliminados`
--

DROP TABLE IF EXISTS `historial_eliminados`;
CREATE TABLE IF NOT EXISTS `historial_eliminados` (
  `id_item` int NOT NULL,
  `referencia` varchar(50) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `marca` varchar(100) NOT NULL,
  `stock` int NOT NULL,
  `costo_unitario` decimal(12,2) NOT NULL,
  `fecha_eliminado` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`referencia`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `historial_eliminados`
--

INSERT INTO `historial_eliminados` (`id_item`, `referencia`, `descripcion`, `marca`, `stock`, `costo_unitario`, `fecha_eliminado`) VALUES
(2, 'HSGS-002', 'Licencia de Software HSGS', 'High Softwares', 50, 150.00, '2026-02-19 21:28:07'),
(15, 'HSGS-CORE-113', 'Disco Duro SSD Logitech Modelo-X13', 'Logitech', 54, 845.69, '2026-02-19 21:55:29'),
(8, 'HSGS-GPU-106', 'Fuente de Poder Intel Modelo-X6', 'Intel', 35, 1008.67, '2026-02-19 21:59:50');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario`
--

DROP TABLE IF EXISTS `inventario`;
CREATE TABLE IF NOT EXISTS `inventario` (
  `id_item` int NOT NULL AUTO_INCREMENT,
  `referencia` varchar(50) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `marca` varchar(100) NOT NULL,
  `stock` int NOT NULL DEFAULT '0',
  `costo_unitario` decimal(12,2) NOT NULL,
  PRIMARY KEY (`id_item`),
  UNIQUE KEY `referencia` (`referencia`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `inventario`
--

INSERT INTO `inventario` (`id_item`, `referencia`, `descripcion`, `marca`, `stock`, `costo_unitario`) VALUES
(1, 'HSGS-001', 'Servidor de Datos Pro', 'Gravis Tech', 5, 1200.00),
(3, 'HSGS-MEM-101', 'Placa Base Asus Modelo-X1', 'Asus', 83, 923.17),
(4, 'HSGS-MEM-102', 'Fuente de Poder Samsung Modelo-X2', 'Samsung', 66, 1456.06),
(5, 'HSGS-PERI-103', 'Disco Duro SSD Corsair Modelo-X3', 'Corsair', 56, 1128.88),
(6, 'HSGS-PERI-104', 'Teclado Mecánico TechSena Modelo-X4', 'TechSena', 92, 127.65),
(7, 'HSGS-MEM-105', 'Monitor LED Kingston Modelo-X5', 'Kingston', 78, 1004.72),
(9, 'HSGS-MEM-107', 'Teclado Mecánico Intel Modelo-X7', 'Intel', 76, 1320.44),
(10, 'HSGS-GPU-108', 'Disco Duro SSD Samsung Modelo-X8', 'Samsung', 67, 588.45),
(12, 'HSGS-DISP-110', 'Mouse Gamer Nvidia Modelo-X10', 'Nvidia', 5, 909.04),
(13, 'HSGS-MEM-111', 'Procesador Kingston Modelo-X11', 'Kingston', 69, 701.97),
(14, 'HSGS-GPU-112', 'Memoria RAM Logitech Modelo-X12', 'Logitech', 59, 1179.24),
(16, 'HSGS-CORE-114', 'Gabinete Nvidia Modelo-X14', 'Nvidia', 58, 1307.91),
(18, 'HSGS-STOR-116', 'Tarjeta de Video Logitech Modelo-X16', 'Logitech', 58, 1092.54),
(19, 'HSGS-DISP-117', 'Gabinete Logitech Modelo-X17', 'Logitech', 77, 577.13),
(20, 'HSGS-GPU-118', 'Monitor LED Logitech Modelo-X18', 'Logitech', 53, 111.59),
(21, 'HSGS-DISP-119', 'Monitor LED Asus Modelo-X19', 'Asus', 100, 1420.61),
(22, 'HSGS-DISP-120', 'Mouse Gamer Nvidia Modelo-X20', 'Nvidia', 45, 1226.71),
(23, 'HSGS-PERI-121', 'Mouse Gamer Nvidia Modelo-X21', 'Nvidia', 88, 550.45),
(24, 'HSGS-MEM-122', 'Memoria RAM Kingston Modelo-X22', 'Kingston', 42, 62.17),
(25, 'HSGS-STOR-123', 'Teclado Mecánico TechSena Modelo-X23', 'TechSena', 47, 552.21),
(26, 'HSGS-PERI-124', 'Memoria RAM AMD Modelo-X24', 'AMD', 74, 26.36),
(27, 'HSGS-PERI-125', 'Gabinete Nvidia Modelo-X25', 'Nvidia', 83, 1376.73),
(28, 'HSGS-DISP-126', 'Placa Base Corsair Modelo-X26', 'Corsair', 95, 1194.10),
(29, 'HSGS-CORE-127', 'Disco Duro SSD Samsung Modelo-X27', 'Samsung', 48, 493.32),
(30, 'HSGS-GPU-128', 'Memoria RAM Logitech Modelo-X28', 'Logitech', 21, 571.24),
(31, 'HSGS-STOR-129', 'Disco Duro SSD Corsair Modelo-X29', 'Corsair', 6, 186.96),
(32, 'HSGS-MEM-130', 'Monitor LED Asus Modelo-X30', 'Asus', 14, 585.31),
(33, 'HSGS-GPU-131', 'Fuente de Poder Intel Modelo-X31', 'Intel', 60, 187.49),
(34, 'HSGS-GPU-132', 'Placa Base Intel Modelo-X32', 'Intel', 64, 35.76),
(35, 'HSGS-DISP-133', 'Mouse Gamer Samsung Modelo-X33', 'Samsung', 65, 1209.41),
(36, 'HSGS-STOR-134', 'Mouse Gamer Kingston Modelo-X34', 'Kingston', 80, 1151.66),
(37, 'HSGS-STOR-135', 'Monitor LED Samsung Modelo-X35', 'Samsung', 50, 1242.16),
(38, 'HSGS-MEM-136', 'Fuente de Poder Intel Modelo-X36', 'Intel', 82, 33.74),
(41, 'HSGS-STOR-139', 'Fuente de Poder Asus Modelo-X39', 'Asus', 67, 1253.39),
(42, 'HSGS-PERI-140', 'Placa Base Kingston Modelo-X40', 'Kingston', 19, 600.50),
(43, 'HSGS-DISP-141', 'Disco Duro SSD Samsung Modelo-X41', 'Samsung', 39, 914.45),
(44, 'HSGS-GPU-142', 'Teclado Mecánico Nvidia Modelo-X42', 'Nvidia', 19, 547.92),
(46, 'HSGS-CORE-144', 'Teclado Mecánico Intel Modelo-X44', 'Intel', 74, 1189.95),
(47, 'HSGS-PERI-145', 'Monitor LED Samsung Modelo-X45', 'Samsung', 28, 965.67),
(49, 'HSGS-MEM-143', 'Gabinete TechSena Modelo-X43', 'TechSena', 34, 1479.47);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
