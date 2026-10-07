-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 09, 2025 at 01:58 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `leaf_disease`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `leaf_data`
--

CREATE TABLE `leaf_data` (
  `id` int(11) NOT NULL,
  `leaf` varchar(30) NOT NULL,
  `disease` varchar(50) NOT NULL,
  `symptoms` text NOT NULL,
  `solution` text NOT NULL,
  `leaf_img` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `leaf_data`
--

INSERT INTO `leaf_data` (`id`, `leaf`, `disease`, `symptoms`, `solution`, `leaf_img`) VALUES
(1, 'Tomato', 'Bacterial Spot', 'Dark spots with concentric rings develop on older leaves first that touch infected soil. The surrounding leaf area may turn yellow. Affected leaves may die prematurely, exposing the fruits to sunscald. It also infects stems and fruit, presenting as black leathery spots on fruit. ', 'Pinch off leaves with leaf spots and bury them in the compost pile.\r\nIt is okay to remove up to a third of the plant''s leaves if you catch the disease early.\r\nDo not remove more than a third of the plant''s leaves.\r\nKeep leaves dry to reduce spreading the disease.', 'a (2).JPG'),
(2, 'Tomato', 'Early Blight', 'The infection appears as small, dark spots that enlarge to 1/4-inch diameter. The spot develops a tan or gray center, and the leaves eventually wilt and fall off. Older leaves are affected first. ', 'Pinch off leaves with leaf spots and bury them in the compost pile.\r\nIt is okay to remove up to a third of the plant''s leaves if you catch the disease early.\r\nDo not remove more than a third of the plant''s leaves.\r\nKeep leaves dry to reduce spreading the disease.', 'a (26).JPG'),
(3, 'Tomato', 'Late Blight', 'Dieback of twigs; premature leaf drop; dark staining on fruit; leaves and twigs covered in dark spores.', 'Pinch off leaves with leaf spots and bury them in the compost pile.\r\nIt is okay to remove up to a third of the plant''s leaves if you catch the disease early.', 'a (62).JPG'),
(4, 'Tomato', 'Septoria Leaf Spot', 'A highly contagious bacterial infection, citrus canker causes yellow halo-like lesions on fruit, leaves and twigs of citrus trees. If allowed to progress unchecked, this lemon tree problem will eventually result in dieback, fruit drop, and leaf loss.', 'Do not remove more than a third of the plant''s leaves.\r\nKeep leaves dry to reduce spreading the disease.', 'a (83).JPG');

-- --------------------------------------------------------

--
-- Table structure for table `leaf_register`
--

CREATE TABLE `leaf_register` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `rdate` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `leaf_register`
--

INSERT INTO `leaf_register` (`id`, `name`, `email`, `mobile`, `address`, `uname`, `pass`, `rdate`) VALUES
(1, 'Raj', 'raj@gmail.com', 9360967387, 'Trichy', 'raj', '1234', '07-03-2021');

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

CREATE TABLE `register` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `register`
--

INSERT INTO `register` (`id`, `name`, `mobile`, `email`, `uname`, `pass`) VALUES
(1, 'Ram', 9054621096, 'ram@gmail.com', 'ram', '1234');
