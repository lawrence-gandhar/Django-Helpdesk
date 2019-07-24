-- phpMyAdmin SQL Dump
-- version 4.1.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 21, 2019 at 08:42 AM
-- Server version: 5.6.16-log
-- PHP Version: 5.5.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `femsdev`
--

-- --------------------------------------------------------

--
-- Table structure for table `sr_status_changes`
--

CREATE TABLE IF NOT EXISTS `sr_status_changes` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `ticket_id` bigint(20) DEFAULT NULL,
  `status_id` bigint(20) DEFAULT NULL,
  `changed_by` bigint(20) DEFAULT NULL,
  `changed_on` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ticket_id` (`ticket_id`,`status_id`,`changed_by`,`changed_on`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=11 ;

--
-- Dumping data for table `sr_status_changes`
--

INSERT INTO `sr_status_changes` (`id`, `ticket_id`, `status_id`, `changed_by`, `changed_on`) VALUES
(9, 15, 2, 6466, '2019-05-21 08:29:36'),
(8, 15, 3, 6466, '2019-05-21 08:29:30'),
(10, 15, 4, 6466, '2019-05-21 08:29:45'),
(1, 16, 2, 6466, '2019-05-21 08:03:44'),
(2, 16, 3, 6466, '2019-05-21 08:05:02'),
(5, 16, 3, 6466, '2019-05-21 08:20:58'),
(3, 16, 4, 6466, '2019-05-21 08:11:01'),
(6, 16, 4, 6466, '2019-05-21 08:21:04'),
(4, 16, 6, 6466, '2019-05-21 08:18:10'),
(7, 16, 6, 6466, '2019-05-21 08:21:10');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
