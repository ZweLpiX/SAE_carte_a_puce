-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 28, 2023 at 07:25 AM
-- Server version: 5.7.24
-- PHP Version: 8.0.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `purpledragon`
--

-- --------------------------------------------------------

--
-- Table structure for table `compte`
--

CREATE TABLE `compte` (
  `etu_id` int(11) NOT NULL,
  `opr_date` datetime NOT NULL,
  `opr_montant` decimal(15,2) DEFAULT '0.00',
  `opr_libelle` varchar(50) DEFAULT NULL,
  `type_operation` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `compte`
--

INSERT INTO `compte` (`etu_id`, `opr_date`, `opr_montant`, `opr_libelle`, `type_operation`) VALUES
(1, '2023-11-09 09:15:34', '1.00', 'Initial', 'Bonus'),
(2, '2023-11-10 08:23:32', '1.00', 'Inital', 'Bonus'),
(2, '2023-11-10 15:24:45', '-0.20', 'chocolat', 'Dépense'),
(4, '2023-11-10 13:10:41', '-0.20', 'chocolat', 'Dépense'),
(4, '2023-11-10 13:10:42', '-0.20', 'chocolat', 'Dépense'),
(4, '2023-11-10 13:10:43', '-0.20', 'chocolat', 'Dépense'),
(4, '2023-11-10 13:10:45', '-0.20', 'chocolat', 'Dépense'),
(4, '2023-11-10 15:27:04', '1.00', 'intiial', 'Bonus');

-- --------------------------------------------------------

--
-- Table structure for table `etudiant`
--

CREATE TABLE `etudiant` (
  `etu_id` int(11) NOT NULL,
  `etu_nom` varchar(255) DEFAULT NULL,
  `etu_prenom` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `etudiant`
--

INSERT INTO `etudiant` (`etu_id`, `etu_nom`, `etu_prenom`) VALUES
(1, 'Halloumi', 'Nabil'),
(2, 'Solomiac', 'Clément'),
(3, 'Senechal', 'Maxime'),
(4, 'Pauws', 'Nicolas');

-- --------------------------------------------------------

--
-- Table structure for table `type`
--

CREATE TABLE `type` (
  `type_operation` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `type`
--

INSERT INTO `type` (`type_operation`) VALUES
('Bonus'),
('Bonus transféré'),
('Dépense'),
('Recharge');

-- --------------------------------------------------------

--
-- Table structure for table `utilisateurs`
--

CREATE TABLE `utilisateurs` (
  `id` int(11) NOT NULL,
  `utilisateur` varchar(255) NOT NULL,
  `motdepasse` varchar(255) NOT NULL,
  `nom` varchar(255) DEFAULT NULL,
  `prenom` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `utilisateurs`
--

INSERT INTO `utilisateurs` (`id`, `utilisateur`, `motdepasse`, `nom`, `prenom`) VALUES
(1, 'admin', 'admin', 'administrateur', 'test');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `compte`
--
ALTER TABLE `compte`
  ADD PRIMARY KEY (`etu_id`,`opr_date`),
  ADD KEY `type_operation` (`type_operation`);

--
-- Indexes for table `etudiant`
--
ALTER TABLE `etudiant`
  ADD PRIMARY KEY (`etu_id`);

--
-- Indexes for table `type`
--
ALTER TABLE `type`
  ADD PRIMARY KEY (`type_operation`);

--
-- Indexes for table `utilisateurs`
--
ALTER TABLE `utilisateurs`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `etudiant`
--
ALTER TABLE `etudiant`
  MODIFY `etu_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT for table `utilisateurs`
--
ALTER TABLE `utilisateurs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `compte`
--
ALTER TABLE `compte`
  ADD CONSTRAINT `compte_ibfk_1` FOREIGN KEY (`etu_id`) REFERENCES `etudiant` (`etu_id`),
  ADD CONSTRAINT `compte_ibfk_2` FOREIGN KEY (`type_operation`) REFERENCES `type` (`type_operation`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
