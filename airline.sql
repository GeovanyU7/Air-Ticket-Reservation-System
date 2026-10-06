-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 03, 2025 at 05:39 AM
-- Server version: 9.1.0
-- PHP Version: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `airline`
--

-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

DROP TABLE IF EXISTS `airline`;
CREATE TABLE IF NOT EXISTS `airline` (
  `airline_name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`airline_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`airline_name`) VALUES
('Jet Blue');

-- --------------------------------------------------------

--
-- Table structure for table `airline_staff`
--

DROP TABLE IF EXISTS `airline_staff`;
CREATE TABLE IF NOT EXISTS `airline_staff` (
  `username` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `airline_name` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `a_password` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `first_name` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `last_name` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  PRIMARY KEY (`username`),
  KEY `airline_name` (`airline_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `airline_staff`
--

INSERT INTO `airline_staff` (`username`, `airline_name`, `a_password`, `email`, `first_name`, `last_name`, `date_of_birth`) VALUES
('jsantiago', 'Jet Blue', '5f4dcc3b5aa765d61d8327deb882cf99', 'javier.santiago@jetblue.com', 'Javier', 'Santiago', '1987-04-23');

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

DROP TABLE IF EXISTS `airplane`;
CREATE TABLE IF NOT EXISTS `airplane` (
  `airline_name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `plane_id` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `manufacturer` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `seat_capacity` int DEFAULT NULL,
  `plane_age` int DEFAULT NULL,
  PRIMARY KEY (`airline_name`,`plane_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`airline_name`, `plane_id`, `manufacturer`, `seat_capacity`, `plane_age`) VALUES
('Jet Blue', 'JB001', 'Airbus A321neo', 200, 3),
('Jet Blue', 'JB002', 'Boeing 737 MAX 8', 178, 2),
('Jet Blue', 'JB003', 'Embraer 190', 100, 6);

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

DROP TABLE IF EXISTS `airport`;
CREATE TABLE IF NOT EXISTS `airport` (
  `airport_code` char(5) COLLATE utf8mb4_general_ci NOT NULL,
  `city` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `country` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `airport_type` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`airport_code`)
) ;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`airport_code`, `city`, `country`, `airport_type`) VALUES
('JFK', 'New York', 'USA', 'International'),
('PVG', 'Shanghai', 'China', 'International');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `email` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `c_password` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `name` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `phone_number` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `passport_number` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `passport_expiration` date DEFAULT NULL,
  `passport_country` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `building_number` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `street` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `city` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `state` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`email`, `c_password`, `name`, `phone_number`, `passport_number`, `passport_expiration`, `passport_country`, `date_of_birth`, `building_number`, `street`, `city`, `state`) VALUES
('emily.wu@outlook.com', '5f4dcc3b5aa765d61d8327deb882cf99', 'Emily Wu', '+1-347-918-4452', 'CN5582971', '2032-03-21', 'China', '1996-12-02', '508', 'Flatbush Ave.', 'Brooklyn', 'NY'),
('Marco.DaSilva@yahoo.com', '5f4dcc3b5aa765d61d8327deb882cf99', 'Marco DaSilva', '+1 646-777-0314', 'BR7048829', '2028-11-03', 'Brazil', '1988-11-19', '14B', 'Hudson St.', 'New York', 'NY'),
('mcb748@nyu.edu', '5f4dcc3b5aa765d61d8327deb882cf99', 'max', '3478983984', '3432432432432432', '2028-11-11', 'United States', '2005-10-28', '34', '324st', 'Woodside', 'somewhere'),
('natalie.chen@gmail.com', '5f4dcc3b5aa765d61d8327deb882cf99', 'Natalie Chen', '+1-917-482-2231', 'PZ3985241', '2031-02-14', 'USA', '1992-07-08', '220', 'E 75th St', 'New York', 'NY');

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

DROP TABLE IF EXISTS `flight`;
CREATE TABLE IF NOT EXISTS `flight` (
  `airline_name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `flight_number` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `departure_datetime` datetime NOT NULL,
  `plane_id` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `departure_airport_code` char(5) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `arrival_airport_code` char(5) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `arrival_datetime` datetime DEFAULT NULL,
  `base_price` decimal(10,2) DEFAULT NULL,
  `flight_status` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`airline_name`,`flight_number`,`departure_datetime`),
  KEY `airline_name` (`airline_name`,`plane_id`),
  KEY `departure_airport_code` (`departure_airport_code`),
  KEY `arrival_airport_code` (`arrival_airport_code`)
) ;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`airline_name`, `flight_number`, `departure_datetime`, `plane_id`, `departure_airport_code`, `arrival_airport_code`, `arrival_datetime`, `base_price`, `flight_status`) VALUES
('Jet Blue', '67', '2026-01-01 13:01:00', 'JB001', 'PVG', 'JFK', '2026-01-02 13:01:00', 700.00, 'On-Time'),
('Jet Blue', 'B6101', '2025-11-04 09:18:00', 'JB001', 'JFK', 'PVG', '2025-11-05 11:46:00', 896.13, 'On-Time'),
('Jet Blue', 'B6102', '2025-11-07 15:12:00', 'JB002', 'PVG', 'JFK', '2025-11-07 18:41:00', 901.32, 'Delayed'),
('Jet Blue', 'B6103', '2025-11-09 21:37:00', 'JB003', 'JFK', 'PVG', '2025-11-10 10:06:00', 829.78, 'Delayed'),
('Jet Blue', 'TEST001', '2025-12-25 08:00:00', 'JB001', 'JFK', 'PVG', '2025-12-26 10:00:00', 500.00, 'On-Time');

-- --------------------------------------------------------

--
-- Table structure for table `rating`
--

DROP TABLE IF EXISTS `rating`;
CREATE TABLE IF NOT EXISTS `rating` (
  `email` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `flight_number` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `departure_datetime` datetime NOT NULL,
  `airline_name` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `rate` int DEFAULT NULL,
  `r_comment` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`email`,`flight_number`,`departure_datetime`),
  KEY `airline_name` (`airline_name`,`flight_number`,`departure_datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rating`
--

INSERT INTO `rating` (`email`, `flight_number`, `departure_datetime`, `airline_name`, `rate`, `r_comment`) VALUES
('emily.wu@outlook.com', 'B6103', '2025-11-09 21:37:00', 'Jet Blue', 4, 'Clean plane, quick boarding, good experience overall.'),
('Marco.DaSilva@yahoo.com', 'B6102', '2025-11-07 15:12:00', 'Jet Blue', 3, 'Flight delayed by 2 hours. Crew tried their best though.'),
('natalie.chen@gmail.com', 'B6101', '2025-11-04 09:18:00', 'Jet Blue', 5, 'Very smooth flight, friendly crew. Seats were comfy.'),
('natalie.chen@gmail.com', 'B6102', '2025-11-07 15:12:00', 'Jet Blue', 3, 'wow does this work');

-- --------------------------------------------------------

--
-- Table structure for table `staff_phone`
--

DROP TABLE IF EXISTS `staff_phone`;
CREATE TABLE IF NOT EXISTS `staff_phone` (
  `phone_number` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `username` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`phone_number`,`username`),
  KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `staff_phone`
--

INSERT INTO `staff_phone` (`phone_number`, `username`) VALUES
('+1-718-910-6655', 'jsantiago');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
CREATE TABLE IF NOT EXISTS `ticket` (
  `ticket_id` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `airline_name` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `flight_number` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `departure_datetime` datetime DEFAULT NULL,
  `card_type` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `card_number` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `name_on_card` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `card_expiration_date` date DEFAULT NULL,
  `purchase_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`ticket_id`),
  KEY `email` (`email`),
  KEY `airline_name` (`airline_name`,`flight_number`,`departure_datetime`)
) ;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`ticket_id`, `email`, `airline_name`, `flight_number`, `departure_datetime`, `card_type`, `card_number`, `name_on_card`, `card_expiration_date`, `purchase_datetime`) VALUES
('TCKT21001', 'natalie.chen@gmail.com', 'Jet Blue', 'B6101', '2025-11-04 09:18:00', 'Visa', '4485-2987-5502-1443', 'Natalie Chen', '2028-07-01', '2025-10-20 09:42:36'),
('TCKT21002', 'Marco.DaSilva@yahoo.com', 'Jet Blue', 'B6102', '2025-11-07 15:12:00', 'MasterCard', '5412-1877-9044-3361', 'Marco DaSilva', '2027-10-01', '2025-10-22 14:07:52'),
('TCKT21003', 'emily.wu@outlook.com', 'Jet Blue', 'B6103', '2025-11-09 21:37:00', 'Amex', '3712-002874-44919', 'Emily Wu', '2026-09-01', '2025-10-25 18:27:14'),
('TCKT21004', 'natalie.chen@gmail.com', 'Jet Blue', 'B6102', '2025-11-07 15:12:00', 'Visa', '4485-2987-5502-1443', 'Natalie Chen', '2028-07-01', '2025-10-23 11:05:48'),
('TCKT21005', 'natalie.chen@gmail.com', 'Jet Blue', 'TEST001', '2025-12-25 08:00:00', 'Visa', '1111111111111111', 'awdawd', '2027-10-10', '2025-12-02 23:57:01'),
('TCKT21006', 'mcb748@nyu.edu', 'Jet Blue', 'TEST001', '2025-12-25 08:00:00', 'Visa', '1111111111111111', 'Pat', '2028-10-28', '2025-12-03 00:19:11'),
('TCKT21007', 'mcb748@nyu.edu', 'Jet Blue', 'TEST001', '2025-12-25 08:00:00', 'Visa', '123412341234', 'adawd', '2094-10-12', '2025-12-03 00:20:00');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD CONSTRAINT `airline_staff_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`);

--
-- Constraints for table `airplane`
--
ALTER TABLE `airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`);

--
-- Constraints for table `flight`
--
ALTER TABLE `flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`),
  ADD CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`airline_name`,`plane_id`) REFERENCES `airplane` (`airline_name`, `plane_id`),
  ADD CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`departure_airport_code`) REFERENCES `airport` (`airport_code`),
  ADD CONSTRAINT `flight_ibfk_4` FOREIGN KEY (`arrival_airport_code`) REFERENCES `airport` (`airport_code`);

--
-- Constraints for table `rating`
--
ALTER TABLE `rating`
  ADD CONSTRAINT `rating_ibfk_1` FOREIGN KEY (`email`) REFERENCES `customer` (`email`),
  ADD CONSTRAINT `rating_ibfk_2` FOREIGN KEY (`airline_name`,`flight_number`,`departure_datetime`) REFERENCES `flight` (`airline_name`, `flight_number`, `departure_datetime`);

--
-- Constraints for table `staff_phone`
--
ALTER TABLE `staff_phone`
  ADD CONSTRAINT `staff_phone_ibfk_1` FOREIGN KEY (`username`) REFERENCES `airline_staff` (`username`);

--
-- Constraints for table `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`email`) REFERENCES `customer` (`email`),
  ADD CONSTRAINT `ticket_ibfk_2` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`),
  ADD CONSTRAINT `ticket_ibfk_3` FOREIGN KEY (`airline_name`,`flight_number`,`departure_datetime`) REFERENCES `flight` (`airline_name`, `flight_number`, `departure_datetime`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
