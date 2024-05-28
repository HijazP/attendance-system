-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 28, 2024 at 11:11 AM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pegawai`
--

-- --------------------------------------------------------

--
-- Table structure for table `biodata`
--

CREATE TABLE `biodata` (
  `id_pegawai` varchar(255) NOT NULL,
  `nama_pegawai` varchar(255) NOT NULL,
  `divisi_pegawai` varchar(255) NOT NULL,
  `jabatan_pegawai` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `biodata`
--

INSERT INTO `biodata` (`id_pegawai`, `nama_pegawai`, `divisi_pegawai`, `jabatan_pegawai`) VALUES
('1', 'face1', 'Backend Engineer', 'Senior'),
('10', 'face10', 'Frontend Engineer', 'Junior'),
('11', 'face11', 'Frontend Engineer', 'Intern'),
('12', 'face12', 'IT Support', 'Senior'),
('13', 'face13', 'System Administator', 'Senior'),
('14', 'face14', 'UI Designer', 'Senior'),
('15', 'face15', 'UI Designer', 'Junior'),
('16', 'face16', 'UX Researcher', 'Senior'),
('17', 'face17', 'UX Researcher', 'Junior'),
('18', 'face18', 'DevOps Engineer', 'Senior'),
('19', 'face19', 'DevOps Engineer', 'Senior'),
('2', 'face2', 'Backend Engineer', 'Junior'),
('3', 'face3', 'Backend Engineer', 'Intern'),
('4', 'face4', 'Pimpinan Perusahaan', 'Chief Executive Officer'),
('5', 'face5', 'Cyber Security Engineer', 'Senior'),
('6', 'face6', 'Pimpinan Perusahaan', 'Chief Technology Officer'),
('7', 'face7', 'DevOps Engineer', 'Senior'),
('8', 'face8', 'DevOps Engineer', 'Senior'),
('9', 'face9', 'Frontend Engineer', 'Senior');

-- --------------------------------------------------------

--
-- Table structure for table `presensi`
--

CREATE TABLE `presensi` (
  `id_pegawai` varchar(255) NOT NULL,
  `tanggal_presensi` date NOT NULL,
  `waktu_presensi` time NOT NULL,
  `berhasil_presensi` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `presensi`
--

INSERT INTO `presensi` (`id_pegawai`, `tanggal_presensi`, `waktu_presensi`, `berhasil_presensi`) VALUES
('3', '2024-05-28', '10:46:04', 1),
('3', '2024-05-28', '16:06:33', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `biodata`
--
ALTER TABLE `biodata`
  ADD PRIMARY KEY (`id_pegawai`);

--
-- Indexes for table `presensi`
--
ALTER TABLE `presensi`
  ADD KEY `fk_id_pegawai` (`id_pegawai`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `presensi`
--
ALTER TABLE `presensi`
  ADD CONSTRAINT `fk_id_pegawai` FOREIGN KEY (`id_pegawai`) REFERENCES `biodata` (`id_pegawai`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
