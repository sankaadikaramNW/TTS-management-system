-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 05, 2026 at 05:35 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `slaf_tts_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `academic_attendance`
--

CREATE TABLE `academic_attendance` (
  `id` varchar(36) NOT NULL,
  `timetable_id` varchar(36) NOT NULL,
  `student_id` varchar(36) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `remarks` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `academic_attendance`
--

INSERT INTO `academic_attendance` (`id`, `timetable_id`, `student_id`, `status`, `remarks`, `created_at`, `updated_at`) VALUES
('46f1a5c4-15b0-453c-a668-879dcbac24af', '99dc4d29-6bda-4f99-9996-3c796e92fcdd', '3b0e40ad-cfbf-4df7-804d-2c686c40ad2f', 'LEAVE', NULL, '2026-08-17 11:39:01', '2026-08-17 11:39:01'),
('54e893f8-987f-429a-95fe-bcc8a5d9ac69', '99dc4d29-6bda-4f99-9996-3c796e92fcdd', 'd0fca849-4bf5-4c56-be89-38a21d42a187', 'PRESENT', NULL, '2026-08-17 11:39:01', '2026-08-17 11:39:01'),
('61ebaa74-2d61-4117-8c63-ed8593c5ece9', '99dc4d29-6bda-4f99-9996-3c796e92fcdd', 'e59d3871-3fa2-44db-bcb0-068ba53fe6e1', 'PRESENT', NULL, '2026-08-17 11:39:01', '2026-08-17 11:39:01'),
('b35fe861-7084-4a18-b8f7-389b138957ef', '99dc4d29-6bda-4f99-9996-3c796e92fcdd', 'e1650c87-f565-471c-85e8-a157df7dc81b', 'PRESENT', NULL, '2026-08-17 11:39:01', '2026-08-17 11:39:01'),
('bd36e71c-7dcb-4d60-b161-88c8afcf0dc7', '99dc4d29-6bda-4f99-9996-3c796e92fcdd', '49599a29-88c3-4e4f-bad3-ef2d05785b27', 'PRESENT', NULL, '2026-08-17 11:39:01', '2026-08-17 12:10:25');

-- --------------------------------------------------------

--
-- Table structure for table `accommodation_allocations`
--

CREATE TABLE `accommodation_allocations` (
  `id` varchar(36) NOT NULL,
  `student_id` varchar(36) NOT NULL,
  `bed_id` varchar(36) DEFAULT NULL,
  `allocated_at` datetime DEFAULT NULL,
  `allocated_by` varchar(36) DEFAULT NULL,
  `vacated_at` datetime DEFAULT NULL,
  `vacated_by` varchar(36) DEFAULT NULL,
  `vacate_reason` varchar(100) DEFAULT NULL,
  `remarks` text DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `bed_position_id` varchar(36) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accommodation_allocations`
--

INSERT INTO `accommodation_allocations` (`id`, `student_id`, `bed_id`, `allocated_at`, `allocated_by`, `vacated_at`, `vacated_by`, `vacate_reason`, `remarks`, `status`, `created_at`, `updated_at`, `bed_position_id`) VALUES
('1321d7ed-f392-43a0-8d13-519d8721c142', '4847c54d-9b0c-496f-9682-cf79cefe57e3', NULL, '2026-10-26 04:35:08', 'user-slaf-admin', NULL, NULL, NULL, '', 'Active', '2026-10-26 04:35:08', '2026-10-26 04:35:08', '4a47ab50-65b3-4af3-b9e6-3207c978f983'),
('1f0d6dd6-d0dc-43c2-afb5-0acdd668216a', 'a1000f6d-0983-4dea-b2fd-ffd32faaf80a', NULL, '2026-08-12 10:06:01', 'user-slaf-admin', '2026-09-24 09:39:05', 'user-slaf-admin', 'Course Completed', '', 'History', '2026-08-12 10:06:01', '2026-09-24 09:39:05', '68ebb960-eb3a-42fb-802b-2d27bca00ff1'),
('5a785dcd-4edd-4060-a614-e905ce2439f7', '4ae38410-0c6f-4091-b88a-f2c271e038bb', NULL, '2026-09-14 10:57:54', NULL, '2026-09-14 10:57:54', NULL, 'Course/Batch Passed Out', 'Automatically vacated upon course/batch completion on 2026-09-14.', 'History', '2026-09-14 10:57:54', '2026-09-14 10:57:54', 'a0133050-050f-4c6d-9d7f-38ba6874571b'),
('65722b40-8b14-49a5-a7c4-e65c3a794314', 'bbd307bd-5dff-4d7e-9da6-701db2ee5c72', NULL, '2026-09-14 10:38:48', NULL, '2026-09-14 10:38:49', NULL, 'Course/Batch Passed Out', 'Automatically vacated upon course/batch completion on 2026-09-14.', 'History', '2026-09-14 10:38:48', '2026-09-14 10:38:49', 'a0133050-050f-4c6d-9d7f-38ba6874571b'),
('6c560145-a2cc-4f9b-b35a-08f63cdfa8aa', 'b92a011e-8967-4e81-9456-93b923d19866', NULL, '2026-09-14 10:39:17', NULL, '2026-09-14 10:39:17', NULL, 'Course/Batch Passed Out', 'Automatically vacated upon course/batch completion on 2026-09-14.', 'History', '2026-09-14 10:39:17', '2026-09-14 10:39:17', 'a0133050-050f-4c6d-9d7f-38ba6874571b'),
('ddb9a4c8-c737-4d5e-b712-385033c378bd', '012f5d6a-01f0-4b01-8a83-51a3d0a7dd37', '052b11b6-068c-4523-be11-25ac4967efed', '2026-08-11 15:22:46', 'user-slaf-admin', '2026-09-24 09:38:55', 'user-slaf-admin', 'Course Completed', '', 'History', '2026-08-11 15:22:46', '2026-09-24 09:38:55', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `accommodation_beds`
--

CREATE TABLE `accommodation_beds` (
  `id` varchar(36) NOT NULL,
  `billet_id` varchar(36) NOT NULL,
  `bed_number` varchar(30) NOT NULL,
  `status` varchar(30) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accommodation_beds`
--

INSERT INTO `accommodation_beds` (`id`, `billet_id`, `bed_number`, `status`, `created_at`, `updated_at`, `deleted_at`) VALUES
('052b11b6-068c-4523-be11-25ac4967efed', '9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'Bed 5', 'Vacant', '2026-08-11 15:21:27', '2026-09-24 09:38:55', NULL),
('36188ef3-a072-42b6-84fc-3f3e394ca894', '9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'Bed 10', 'Vacant', '2026-08-11 15:21:27', '2026-08-11 15:21:27', NULL),
('37a73ac2-4318-4010-b11f-b6c055124be2', '9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'Bed 2', 'Vacant', '2026-08-11 15:21:27', '2026-08-11 15:21:27', NULL),
('409ab34b-c9a4-4f09-a2c8-b3528c8fbac7', '9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'Bed 1', 'Vacant', '2026-08-11 15:21:27', '2026-08-11 15:21:27', NULL),
('4a58b33a-4380-4bcc-9e11-98031f986b77', '9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'Bed 6', 'Vacant', '2026-08-11 15:21:27', '2026-08-11 15:21:27', NULL),
('6b28f193-b106-4af1-987c-8b253a0f9a61', '9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'Bed 7', 'Vacant', '2026-08-11 15:21:27', '2026-08-11 15:21:27', NULL),
('85557fa6-c18b-40c5-afc7-ede21bcad6c6', '9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'Bed 3', 'Vacant', '2026-08-11 15:21:27', '2026-08-11 15:21:27', NULL),
('ba3f7836-25d3-4042-993a-3c49fd044b11', '9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'Bed 9', 'Vacant', '2026-08-11 15:21:27', '2026-08-11 15:21:27', NULL),
('bed-t1-a-1', 'bill-t1-a', 'Bed 01', 'Vacant', '2026-08-10 09:31:21', '2026-08-10 09:31:21', NULL),
('bed-t1-a-2', 'bill-t1-a', 'Bed 02', 'Vacant', '2026-08-10 09:31:21', '2026-08-10 09:31:21', NULL),
('bed-t1-a-3', 'bill-t1-a', 'Bed 03', 'Vacant', '2026-08-10 09:31:21', '2026-08-10 09:31:21', NULL),
('bed-t1-a-4', 'bill-t1-a', 'Bed 04', 'Vacant', '2026-08-10 09:31:21', '2026-08-10 09:31:21', NULL),
('cdaba76e-26d5-4929-bdf6-6f35ca698452', '9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'Bed 8', 'Vacant', '2026-08-11 15:21:27', '2026-08-11 15:21:27', NULL),
('ef7910f1-813f-4a4b-8fe1-134b8c08a62c', '9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'Bed 4', 'Vacant', '2026-08-11 15:21:27', '2026-08-11 15:21:27', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `accommodation_bed_positions`
--

CREATE TABLE `accommodation_bed_positions` (
  `id` varchar(36) NOT NULL,
  `bunk_bed_id` varchar(36) NOT NULL,
  `position_type` varchar(20) NOT NULL,
  `position_code` varchar(60) NOT NULL,
  `status` varchar(30) DEFAULT 'Available',
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accommodation_bed_positions`
--

INSERT INTO `accommodation_bed_positions` (`id`, `bunk_bed_id`, `position_type`, `position_code`, `status`, `created_at`, `updated_at`, `deleted_at`) VALUES
('1c0aa5ba-9c08-4cd7-9671-b4e2e809c0f0', 'a66fa878-d818-4d3c-a32f-76ed34549c25', 'BOTTOM', 'Bunk-02-BOTTOM', 'Available', '2026-08-12 05:41:09', '2026-08-12 05:41:09', NULL),
('1efa3cd3-86d9-4252-8acd-ac98ea1793c2', '2162e4ce-1532-44ec-8a54-6d32988af642', 'TOP', 'Bunk-07-TOP', 'Available', '2026-08-12 05:41:10', '2026-08-12 05:41:10', NULL),
('22c1ccaf-0da7-450c-a545-4c5867a333dc', 'a78b805e-6176-47aa-aa8f-f23ddbc0a4c7', 'TOP', 'Bunk-09-TOP', 'Available', '2026-08-12 05:41:10', '2026-08-12 05:41:10', NULL),
('340007a6-d404-4385-a44d-7e5875db775d', '4e8e867e-53ed-42b0-86bb-c46f1c160f8a', 'TOP', 'Bunk-06-TOP', 'Available', '2026-08-12 05:41:10', '2026-08-12 05:41:10', NULL),
('4a47ab50-65b3-4af3-b9e6-3207c978f983', 'd3116180-6128-44f1-a481-9d3eb7c69068', 'TOP', 'Bunk-10-TOP', 'Occupied', '2026-08-12 05:41:10', '2026-10-26 04:35:08', NULL),
('5045d31f-5631-4834-b097-f03d7a1a6db4', 'cf313b56-676e-4857-9cc4-996fa6143440', 'BOTTOM', 'Bunk-03-BOTTOM', 'Available', '2026-08-12 05:41:09', '2026-08-12 05:41:09', NULL),
('5379cec6-91e2-4eff-8249-51ac628fe09d', '4e8e867e-53ed-42b0-86bb-c46f1c160f8a', 'BOTTOM', 'Bunk-06-BOTTOM', 'Available', '2026-08-12 05:41:10', '2026-08-12 05:41:10', NULL),
('5da7f81b-cb7e-4cb4-a8f2-f437d68d2cc4', 'a78b805e-6176-47aa-aa8f-f23ddbc0a4c7', 'BOTTOM', 'Bunk-09-BOTTOM', 'Available', '2026-08-12 05:41:10', '2026-08-12 05:41:10', NULL),
('682f8e56-cbaf-46f7-858c-7b4c4031766f', '3878aa51-48c1-4600-a76c-1f851d3f514b', 'BOTTOM', 'Bunk-08-BOTTOM', 'Available', '2026-08-12 05:41:10', '2026-08-12 05:41:10', NULL),
('68ebb960-eb3a-42fb-802b-2d27bca00ff1', 'a66fa878-d818-4d3c-a32f-76ed34549c25', 'TOP', 'Bunk-02-TOP', 'Available', '2026-08-12 05:41:09', '2026-09-24 09:39:05', NULL),
('6ab958b0-45f1-4d22-bc1b-fd70637972a3', 'de799891-a8ac-4c68-8a00-7fc6d16591ea', 'TOP', 'Bunk-05-TOP', 'Available', '2026-08-12 05:41:10', '2026-08-12 05:41:10', NULL),
('6cb92f97-2380-445e-a726-f61d41ebafc2', 'd3116180-6128-44f1-a481-9d3eb7c69068', 'BOTTOM', 'Bunk-10-BOTTOM', 'Available', '2026-08-12 05:41:10', '2026-08-12 05:41:10', NULL),
('76d83170-90aa-41a0-8255-a6c99d64a00c', 'cf313b56-676e-4857-9cc4-996fa6143440', 'TOP', 'Bunk-03-TOP', 'Available', '2026-08-12 05:41:09', '2026-08-12 05:41:09', NULL),
('87762c7a-5fa4-461b-a9f9-a9e83cfe84e7', '3878aa51-48c1-4600-a76c-1f851d3f514b', 'TOP', 'Bunk-08-TOP', 'Available', '2026-08-12 05:41:10', '2026-08-12 05:41:10', NULL),
('9e27dc8e-4359-4d5d-a3aa-f2de735dc1a5', '07a73eac-a8f1-42c4-8ca9-38eab91a9145', 'BOTTOM', 'Bunk-01-BOTTOM', 'Available', '2026-08-12 05:41:09', '2026-08-12 05:41:09', NULL),
('9e94b0dc-5292-4619-9002-b784307f6bce', 'de799891-a8ac-4c68-8a00-7fc6d16591ea', 'BOTTOM', 'Bunk-05-BOTTOM', 'Available', '2026-08-12 05:41:10', '2026-08-12 05:41:10', NULL),
('a0133050-050f-4c6d-9d7f-38ba6874571b', '14e56d5e-604c-4288-afa1-eb50781e49c1', 'TOP', 'TB-01-TOP', 'Available', '2026-09-14 10:38:48', '2026-09-14 10:57:54', NULL),
('aeb6c6a4-a580-42c4-87f5-8f399120096b', '847870ea-8ed0-4593-ab5b-a40ad3c11e41', 'TOP', 'Bunk-04-TOP', 'Available', '2026-08-12 05:41:09', '2026-08-12 05:41:09', NULL),
('e0c8909b-468b-49f3-8ba2-47336ed66598', '2162e4ce-1532-44ec-8a54-6d32988af642', 'BOTTOM', 'Bunk-07-BOTTOM', 'Available', '2026-08-12 05:41:10', '2026-08-12 05:41:10', NULL),
('f7283794-9271-4b7b-9622-9b84cc81b056', '847870ea-8ed0-4593-ab5b-a40ad3c11e41', 'BOTTOM', 'Bunk-04-BOTTOM', 'Available', '2026-08-12 05:41:10', '2026-08-12 05:41:10', NULL),
('ffe156f5-b16b-4cc6-bd94-6dad5162947a', '07a73eac-a8f1-42c4-8ca9-38eab91a9145', 'TOP', 'Bunk-01-TOP', 'Available', '2026-08-12 05:41:09', '2026-08-12 05:41:09', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `accommodation_billets`
--

CREATE TABLE `accommodation_billets` (
  `id` varchar(36) NOT NULL,
  `building_id` varchar(36) NOT NULL,
  `name` varchar(100) NOT NULL,
  `capacity` int(11) NOT NULL,
  `current_occupancy` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `block` varchar(50) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `bunk_bed_count` int(11) DEFAULT 0,
  `status` varchar(30) DEFAULT 'Active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accommodation_billets`
--

INSERT INTO `accommodation_billets` (`id`, `building_id`, `name`, `capacity`, `current_occupancy`, `created_at`, `updated_at`, `deleted_at`, `block`, `location`, `description`, `bunk_bed_count`, `status`) VALUES
('9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'd11a1221-df23-47a3-b6ea-62939c51a3a3', 'Adavnce Admin', 20, 1, '2026-08-11 15:20:36', '2026-10-26 04:35:08', NULL, NULL, NULL, NULL, 10, 'Active'),
('bill-t1-a', 'bldg-t1', 'Billet Alpha-1', 24, 0, '2026-08-10 09:31:20', '2026-08-10 09:31:20', NULL, NULL, NULL, NULL, 0, 'Active'),
('c1629655-ad49-4a5d-8a37-464000ad5056', '48193aff-1952-4568-ba25-c7556c39da8c', 'Test Billet 01', 10, 0, '2026-09-14 10:38:48', '2026-09-14 10:38:48', NULL, NULL, NULL, NULL, 0, 'Active'),
('d255ff24-4b17-4c32-915a-0f2256cfa445', 'd11a1221-df23-47a3-b6ea-62939c51a3a3', 'Advance Billet -comtech', 10, 0, '2026-08-11 15:20:02', '2026-08-11 15:20:02', NULL, NULL, NULL, NULL, 0, 'Active');

-- --------------------------------------------------------

--
-- Table structure for table `accommodation_buildings`
--

CREATE TABLE `accommodation_buildings` (
  `id` varchar(36) NOT NULL,
  `name` varchar(100) NOT NULL,
  `type` varchar(30) NOT NULL,
  `capacity` int(11) NOT NULL,
  `current_occupancy` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accommodation_buildings`
--

INSERT INTO `accommodation_buildings` (`id`, `name`, `type`, `capacity`, `current_occupancy`, `created_at`, `updated_at`, `deleted_at`) VALUES
('48193aff-1952-4568-ba25-c7556c39da8c', 'Test Hangar Bld', 'Airmen', 20, 0, '2026-09-14 10:38:48', '2026-09-14 10:38:48', NULL),
('bldg-t1', 'Training Block Alpha (T1)', 'Airmen', 48, 0, '2026-08-10 09:31:20', '2026-08-10 09:31:20', NULL),
('d11a1221-df23-47a3-b6ea-62939c51a3a3', 'E 09', 'Airmen', 61, 1, '2026-08-11 15:18:57', '2026-10-26 04:35:08', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `accommodation_bunk_beds`
--

CREATE TABLE `accommodation_bunk_beds` (
  `id` varchar(36) NOT NULL,
  `billet_id` varchar(36) NOT NULL,
  `bunk_no` varchar(50) NOT NULL,
  `status` varchar(30) DEFAULT 'Active',
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accommodation_bunk_beds`
--

INSERT INTO `accommodation_bunk_beds` (`id`, `billet_id`, `bunk_no`, `status`, `created_at`, `updated_at`, `deleted_at`) VALUES
('07a73eac-a8f1-42c4-8ca9-38eab91a9145', '9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'Bunk-01', 'Active', '2026-08-12 05:41:09', '2026-08-12 05:41:09', NULL),
('14e56d5e-604c-4288-afa1-eb50781e49c1', 'c1629655-ad49-4a5d-8a37-464000ad5056', 'TB-01', 'Active', '2026-09-14 10:38:48', '2026-09-14 10:38:48', NULL),
('2162e4ce-1532-44ec-8a54-6d32988af642', '9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'Bunk-07', 'Active', '2026-08-12 05:41:10', '2026-08-12 05:41:10', NULL),
('3878aa51-48c1-4600-a76c-1f851d3f514b', '9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'Bunk-08', 'Active', '2026-08-12 05:41:10', '2026-08-12 05:41:10', NULL),
('4e8e867e-53ed-42b0-86bb-c46f1c160f8a', '9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'Bunk-06', 'Active', '2026-08-12 05:41:10', '2026-08-12 05:41:10', NULL),
('847870ea-8ed0-4593-ab5b-a40ad3c11e41', '9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'Bunk-04', 'Active', '2026-08-12 05:41:09', '2026-08-12 05:41:09', NULL),
('a66fa878-d818-4d3c-a32f-76ed34549c25', '9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'Bunk-02', 'Active', '2026-08-12 05:41:09', '2026-08-12 05:41:09', NULL),
('a78b805e-6176-47aa-aa8f-f23ddbc0a4c7', '9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'Bunk-09', 'Active', '2026-08-12 05:41:10', '2026-08-12 05:41:10', NULL),
('cf313b56-676e-4857-9cc4-996fa6143440', '9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'Bunk-03', 'Active', '2026-08-12 05:41:09', '2026-08-12 05:41:09', NULL),
('d3116180-6128-44f1-a481-9d3eb7c69068', '9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'Bunk-10', 'Active', '2026-08-12 05:41:10', '2026-08-12 05:41:10', NULL),
('de799891-a8ac-4c68-8a00-7fc6d16591ea', '9c9ed6c5-e32c-4780-900d-e188b4194fcb', 'Bunk-05', 'Active', '2026-08-12 05:41:09', '2026-08-12 05:41:09', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `audit_logs`
--

CREATE TABLE `audit_logs` (
  `id` varchar(36) NOT NULL,
  `user_id` varchar(36) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `module` varchar(50) DEFAULT NULL,
  `action` varchar(100) NOT NULL,
  `previous_value` varchar(1000) DEFAULT NULL,
  `new_value` varchar(1000) DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` varchar(255) DEFAULT NULL,
  `details` varchar(1000) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `audit_logs`
--

INSERT INTO `audit_logs` (`id`, `user_id`, `username`, `module`, `action`, `previous_value`, `new_value`, `ip_address`, `user_agent`, `details`, `created_at`) VALUES
('01466a84-f0b3-4c87-9fa1-cd70edb64a65', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-11 11:05:09'),
('017b3eef-5907-40bb-838b-fad84feb17ce', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 05:54:17'),
('020b9cc9-3edb-411d-8768-66acb5b441ca', 'user-slaf-admin', NULL, 'Student Management', 'CREATE_PERSONAL_OCCURRENCE', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Recorded ACHIEVEMENT \'Outstanding perfromance\' on 14.08.2026 for trainee 50833 (LAKSHAN)', '2026-08-14 11:47:51'),
('021e9318-adb6-474c-a7e6-3f5fc43d9370', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-14 11:44:55'),
('02600fd9-7e26-423b-8cc6-fcb276e733b8', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-11 10:24:58'),
('02aff789-3b49-43b1-bf95-a5ba0ad2e02a', '1b514baf-ebde-4fcc-b838-902659c5c3e3', NULL, 'Student Management', 'DELETE_PERSONAL_OCCURRENCE', NULL, NULL, NULL, NULL, 'Soft-deleted ACHIEVEMENT record \'Test Achievement Automated Verification\' (ID 047610ca-fa41-4da6-8d20-ff286394d418) for trainee 50833', '2026-09-15 11:14:57'),
('039cedc6-446e-4929-ba6b-b9ecb5e0663a', NULL, 'System Scheduler', 'Academic Management', 'AUTOMATIC_BATCH_CLOSURE', 'Status: Active', 'Status: PASSED OUT', '127.0.0.1', 'System Automated Batch Task', 'Batch \'Batch-TEST-EXP-1789362528\' automatically closed and moved to PASSED OUT state. Course End Date / Passing Out Date (2026-03-01) has passed as of 2026-09-14.', '2026-09-14 10:38:49'),
('03acbcd2-dc82-41b3-bb9c-c3e9dbb0ba2e', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-10-26 04:12:00'),
('03e3806d-a8cc-478f-87f7-e5312bd931e1', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-24 11:41:27'),
('040550fb-aa6f-495a-a326-ef61a69aba7c', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: []', '2026-10-05 12:04:09'),
('045aeae3-0c7e-4401-8a41-2995bec96edc', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 05:16:52'),
('04a20fa9-c6b9-4502-8eb4-4e33563c2574', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated PARADE_STATE report with parameters: [parade_date=2026-09-21]', '2026-09-21 05:02:03'),
('0588d1b6-514b-43d3-82f6-6f6f0c0f2b85', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: []', '2026-08-31 10:17:59'),
('058ab052-63e6-4a68-b790-e8f5a8aadf1b', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-11 15:18:25'),
('065b231e-3d98-4e85-afef-597903652eab', 'user-slaf-admin', NULL, 'User Management', 'NIGHT_PARADE_COMPLETED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Completed Night Parade Roll Call for trade \'All\' on 2026-09-21 by SLAF Administrator. Expected: 31, Accounted: 31, Changed: 3. Status Changes: 7c03548a-fe20-40b5-9ac0-6f1ee3d1a886: Present -> Sick Report; 49599a29-88c3-4e4f-bad3-ef2d05785b27: Present -> Leave; e59d3871-3fa2-44db-bcb0-068ba53fe6e1: Present -> Hospital', '2026-09-21 11:49:29'),
('06ee5c0e-f9a2-41de-b13d-75fb11623412', 'user-slaf-admin', '51098', 'User Management', 'USER_CREATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'Created user username=\'51098\', full_name=\'Kithmal MPS\', role_id=\'role-instructor\'', '2026-10-26 04:45:55'),
('06ee8443-5571-49fb-9a7a-00aed72529dd', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-09 11:22:50'),
('07487f36-55bc-4bf4-b5d9-cbbb567918e5', 'user-slaf-admin', NULL, 'User Management', 'PARADE_STATE_SUBMITTED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Submitted parade state for trade \'Computer Technician\' on 2026-08-12 to officer Saman Kumara. Records: 5', '2026-08-12 04:43:24'),
('075d1e44-13a7-4c76-96fa-b0d7c54a3745', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-18 10:09:41'),
('0760222d-3218-437f-a9a2-a7fabd59c2aa', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-08-24 10:27:54'),
('084d2ef0-a4ab-4e5d-a9d0-bbac59026c7a', 'c96d5ee9-93ee-41cc-b9e6-f31ecba02f4e', '51837', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'User \'51837\' logged in successfully', '2026-09-21 09:50:11'),
('08ec6c85-9cfa-44a0-81df-d31c8c5c106f', 'c96d5ee9-93ee-41cc-b9e6-f31ecba02f4e', '51837', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'User \'51837\' logged out successfully', '2026-09-21 09:51:12'),
('0b0b0298-ff1a-4bf9-809a-7ed9fc063a1a', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-17 11:38:42'),
('0bf81b76-6475-4a7d-a5c7-3317f2307959', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 11:58:30'),
('0cb2a11f-d931-46e1-b39e-67aff7226bd6', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-18 10:51:45'),
('0e7da2d3-585a-4819-b040-615450950f10', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Generated OCCURRENCES report with parameters: [occurrence_type=ALL]', '2026-08-31 09:50:40'),
('0eeebf3d-9fbe-464b-bf7c-0fbf7e20a0d2', 'user-slaf-admin', NULL, 'User Management', 'NIGHT_PARADE_REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Generated Night Parade State Report for date: 2026-09-21, trade: All', '2026-09-21 09:52:01'),
('100ae801-15ce-4fc2-b018-06d476ecbf5a', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-07 06:28:13'),
('10888802-90af-4e71-93ad-c6b44c2fa85b', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'Generated OCCURRENCES report with parameters: [trainee_id=56ab9898-66d0-4a4e-bbec-294e14953e4e, occurrence_type=MISCONDUCT_OFFENSE]', '2026-10-26 04:26:20'),
('10cf60be-bdaf-4d0c-83a1-d00ccdd2026f', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-10-05 12:05:56'),
('112a3148-7464-4d1a-9365-c91b12e50f73', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-17 11:19:57'),
('1137482f-08b5-4732-a559-0ad98a354fc8', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-10-26 04:53:04'),
('11aad7b5-f206-4668-85d2-fbbfbf40e6ce', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-10-26 04:43:32'),
('11ce63c3-c6a2-4028-8e80-6c437cb08250', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-14 10:29:30'),
('124c145d-8e46-4573-8120-3c15672ec5ef', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-17 03:52:14'),
('12581d66-f2b1-4f3e-9aef-a9c5eaac1228', 'user-slaf-admin', NULL, 'User Management', 'PARADE_DRAFT_TRADE_SAVE', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Draft-saved parade state for trade \'Computer Technician\' — 5 students on 2026-08-12', '2026-08-12 04:36:49'),
('1264fe4e-97d6-40ba-b223-e2e47e2b9f6d', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Generated ACADEMIC_RESULTS report with parameters: [course=Comp Tech Adv, subject=Desktop Application Development, exam_type=Phase Test, exam_date=2026-09-16, result_status=ALL]', '2026-09-21 11:55:40'),
('1270bc6c-5862-4dbd-89f8-d85083c0b43e', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 05:22:03'),
('12ed1cad-aff1-4320-8d36-65e1c588223e', 'user-slaf-admin', NULL, 'User Management', 'OIC_ASSIGNMENT_REMOVED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Removed Officer I/C assignment 317890d8-306f-4f1e-a7d9-220cf7cf69b9', '2026-08-31 10:30:24'),
('136d5990-ccf8-4eb3-ab6d-29bbc5418593', 'f6f853a0-a3db-481e-bb6b-95e469c45dc8', NULL, 'Academic', 'LESSON_PLAN_ARCHIVED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Archived lesson plan \'Test Lesson Plan Document\' (ID: 46a93fac-6987-44be-8189-bd39fddb701a)', '2026-08-12 04:27:05'),
('151d71a9-ac78-45c1-b528-215a6c4489bf', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-12 11:37:28'),
('152ede83-b1a7-4eba-a773-9d4efa97b1cb', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 09:48:17'),
('158a48d8-40d9-424e-96a5-42710c3d2961', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-10-05 11:24:44'),
('172e322b-7e57-4c4e-b2e0-f1e466f78f00', 'user-slaf-admin', NULL, 'Student Management', 'CREATE_PERSONAL_OCCURRENCE', NULL, NULL, 'testclient', 'testclient', 'Recorded ACHIEVEMENT \'Test REST Endpoint Occurrence\' on 15.09.2026 for trainee 50833 (LAKSHAN)', '2026-09-15 11:20:47'),
('1734148b-2723-49b2-a3bd-dbe070166829', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-31 10:27:42'),
('177f431f-5520-4d9e-9456-27ca4807521e', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-07 06:29:41'),
('18047232-bec3-43a1-8960-48bc4d047255', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 05:35:36'),
('18380aea-c998-465a-8ded-bee13a4a5d67', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated ATTENDANCE_REGISTER report with parameters: [course_id=544f0ae2-2ee5-403b-84cf-58ac0aa193af, date_range=2026-09-17 to 2026-09-17]', '2026-09-17 11:44:39'),
('18a110e6-8164-44f3-8be3-0207b7e04b45', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: []', '2026-09-24 09:40:33'),
('18e83670-c9f3-4f1e-b68a-9a00abcf86a3', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-10 09:59:51'),
('18ec90a9-fe5c-4c2d-9ff0-6c1d5652ed53', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated ATTENDANCE_REGISTER report with parameters: []', '2026-09-17 03:53:30'),
('195bbd53-c03c-42bc-b29e-1db3a8b85016', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 05:37:57'),
('1a7c8cf4-5489-4cfe-92ac-0f6eeb17809f', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged out successfully', '2026-09-17 10:23:39'),
('1b0e0507-f26e-4dc8-a819-3cdd2bbd9925', 'user-slaf-admin', NULL, 'Academic Management', 'CREATE_COURSE_CALENDAR_ENTRY', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Added calendar phase \'Test entry\' (S/No: 2, Instructor Status: NOT_ASSIGNED) for course \'Test Radar Basic Course\'', '2026-08-13 11:53:29'),
('1bbf0245-cf4f-4cdf-a2d6-febca1fa6bd9', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-15 11:26:31'),
('1c5f07c0-ff3b-4815-96bb-ba7236f6da88', 'c96d5ee9-93ee-41cc-b9e6-f31ecba02f4e', NULL, 'User Management', 'NIGHT_PARADE_REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated Night Parade State Report for date: 2026-09-21, trade: All', '2026-09-21 05:47:03'),
('1ca6579d-667e-4cc9-950e-fd8e94b44ba6', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-10-26 04:12:19'),
('1ca7c4d3-fbeb-444e-9675-b413cd82d5ea', 'user-slaf-admin', NULL, 'User Management', 'STUDENT_CREATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Created student record TA/40218 (Tharanga)', '2026-09-10 11:32:31'),
('1cd0d7cc-cb44-40be-a409-0dcdf1e3103b', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-31 09:27:06'),
('1e6923c0-bd49-4efa-9e34-17bee54d26fb', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 09:51:41'),
('1e726d4e-b713-4d98-a8da-30b1a501e65f', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-11 15:32:46'),
('1e830e34-c603-4fb5-a0f6-2768bd30b293', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: []', '2026-09-17 03:52:15'),
('1ea65e6f-3686-4a42-9b29-2433b5137a7c', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 05:43:37'),
('1fe63a0d-a5c4-4c68-8174-d20a5ae99f0e', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-08-17 11:32:53'),
('20010d55-34a2-4c07-97cc-ff44faa27128', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-17 11:45:19'),
('200f175d-3e0e-4943-b2c0-85c8e4b6bd9c', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-24 10:27:05'),
('20473bc5-1b83-417d-8376-8d3aceadb3e8', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-08-20 10:43:42'),
('21f8aa1d-dd00-4b9f-a3a4-1e5a5ff1c966', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 05:19:23'),
('221d4ad0-11bf-4f4d-a9b0-45df2deff069', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 11:50:48'),
('23206f16-9617-4cb6-8b83-58652c0c9bff', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-10-26 03:53:54'),
('246cd563-2f8c-4913-89f8-ce3c273e067c', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-10 11:00:49'),
('26204a8a-ecf6-4544-94d8-0b3855d28e46', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 11:01:06'),
('262cfc1f-2951-4a62-916f-8750cc0b4f19', 'user-slaf-admin', NULL, 'User Management', 'TIMETABLE_ATTENDANCE_UPDATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Updated classroom attendance registry for timetable session ID 99dc4d29-6bda-4f99-9996-3c796e92fcdd (5 trainees)', '2026-08-17 11:39:01'),
('263c3229-c18d-4058-a03f-dd0bb9b1db3f', 'user-slaf-admin', NULL, 'User Management', 'BED_POSITION_VACATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Vacated bed position (Reason: Course Completed) previously held by trainee 50845', '2026-09-24 09:39:05'),
('2760d5c0-e77b-4a5c-bde3-bf967a1aefd0', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 05:35:54'),
('2776b14f-b916-4566-8e59-99f94724b5d9', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated ACADEMIC_RESULTS report with parameters: [exam_id=144be146-1c60-4caf-95ad-389c941978d0, course=Comp Tech Adv, subject=Desktop Application Development, exam_type=Phase Test, exam_date=2026-09-16]', '2026-09-17 09:50:00'),
('27d3da0d-d3ea-435a-8d16-ca6beee6038c', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-07 06:30:42'),
('28c73cc1-2fab-4102-bc61-dff3ecc75c2e', 'user-slaf-admin', NULL, 'Academic Management', 'UPDATE_COURSE', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Updated course \'Test Expired Course Aircraft Assist\' (TEST-EXP-1789363673). Duration: 48 Weeks (47 Weeks 6 Days). Period: 2026-01-01 to 2026-12-01. Status: Inactive', '2026-09-14 10:59:57'),
('2967fb0f-b04b-4362-947f-bfee4aad2757', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-09 11:52:17'),
('29704878-6b58-41ea-927a-1821f2a822fc', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-18 09:19:51'),
('29cf669b-f343-47f0-9e2e-e2afb6c540ca', 'user-slaf-admin', NULL, 'User Management', 'STUDENT_CREATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Created student record 50327 (Rashmika)', '2026-08-11 15:15:23'),
('29d229a6-aad4-4008-8627-756375f1e965', 'user-slaf-admin', NULL, 'User Management', 'EXAM_MARKS_UPDATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Entered/updated grades for exam ID 144be146-1c60-4caf-95ad-389c941978d0 for 5 trainees', '2026-09-17 03:56:16'),
('2a052230-b0c6-40b2-95cb-383cbd657ad9', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-18 10:52:01'),
('2a63f4fd-1ed8-4e1b-8699-a4fd3654a8ac', 'user-slaf-admin', NULL, 'User Management', 'PARADE_STATE_SUBMITTED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Submitted parade state for trade \'Computer Technician\' on 2026-08-17 to officer Saman Kumara. Records: 5', '2026-08-17 10:50:49'),
('2b14b76e-afda-4da3-ae73-13222800c90e', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-10-05 12:04:09'),
('2ba11e00-5af7-4853-996e-a1be326bc868', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-12 11:25:05'),
('2c08154f-d8d9-4aa0-98b1-872043f37466', NULL, 'System Scheduler', 'Academic Management', 'AUTOMATIC_BATCH_CLOSURE', 'Status: ONGOING', 'Status: PASSED OUT', '127.0.0.1', 'System Automated Batch Task', 'Course \'TEST-EXP-1789362528 - Test Expired Course Aircraft Assist\' automatically closed and moved to PASSED OUT state. Course End Date (2026-03-01) has passed as of 2026-09-14.', '2026-09-14 10:38:49'),
('2c3aae73-e05f-4321-9d35-5d7c3b680301', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated OCCURRENCES report with parameters: [occurrence_type=ALL]', '2026-09-17 03:53:31'),
('2c3b136a-837c-42df-b7ca-92ed43cf2a9d', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-31 12:03:44'),
('2d6e4950-8b89-427e-8e80-963f2fca57ad', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-08-17 12:22:11'),
('2db9572f-211b-4c90-b1ae-0600499c811d', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-14 11:49:28'),
('2e7eeaab-8652-4bcb-8f35-ffd5522a3eaa', 'user-slaf-admin', NULL, 'Academic', 'LESSON_PLAN_UPLOADED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Uploaded lesson plan \'Acct 13 SLAF Non Public Funds\' for course Basic Course Of Account Assistant (ID: 2/2026)', '2026-09-18 10:40:37'),
('2fab56db-0f5c-4e86-8156-c66117506206', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-15 11:26:26'),
('2fdfafe2-97c3-47ac-9000-e163bc2fef42', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-24 09:38:09'),
('3016246d-98c1-4573-80eb-fa228e488258', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-16 09:40:50'),
('303adb65-ec59-45cb-9a2f-6d64bf3ceb53', 'user-slaf-admin', NULL, 'User Management', 'PARADE_STATE_APPROVED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Approved parade state submission ac931c09-9bcf-47be-969a-84dfcccb7c31 for trade \'Account Assistant\' on 2026-09-21', '2026-09-21 07:17:30'),
('30c732dd-484c-4058-adfd-fea29d95f166', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-07 06:32:08'),
('331c097f-2c23-4e3e-9a38-0cdddfc532ce', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-16 09:41:06'),
('337be135-bb2b-4da9-a178-8633b02f2857', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-12 11:35:59'),
('338fa241-0b94-4799-8232-27bd83c63c27', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-16 09:30:59'),
('3393930d-baec-403e-a301-99b2734cc572', 'user-slaf-admin', NULL, 'User Management', 'PARADE_STATE_SUBMITTED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Submitted parade state for trade \'Administrative\' on 2026-09-21 to INSTRUCTOR NOT ASSIGNED. Records: 18', '2026-09-21 07:17:47'),
('35112c87-f562-498e-b448-250128a1e92a', '1b514baf-ebde-4fcc-b838-902659c5c3e3', NULL, 'User Management', 'PARADE_STATE_APPROVED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Approved parade state submission 90b9f2ea-ea8b-48ac-b994-9aaccb1c91d6 for trade \'Computer Technician\' on 2026-08-10', '2026-08-10 11:08:56'),
('353de1a1-e7e8-4c49-b027-9d979d5e8d39', 'dc5d99d0-d369-4487-a9df-27b663200f83', NULL, 'Academic Management', 'CREATE_COURSE_CALENDAR_ENTRY', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Added calendar phase \'[17] SLAF non Public Accounts Procedures\' (S/No: 1, Instructor Status: ASSIGNED) for course \'Basic Course Of Account Assistant\'', '2026-09-17 10:39:31'),
('35762290-9586-47b2-8c64-1be5e4f36570', '1b514baf-ebde-4fcc-b838-902659c5c3e3', NULL, 'User Management', 'PARADE_STATE_APPROVED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Approved parade state submission 8e60adda-1391-4592-b0c5-ef4bbad98862 for trade \'Computer Technician\' on 2026-08-11', '2026-08-11 15:17:55'),
('35d47267-03cf-469f-b220-09e926b58038', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-24 09:40:37'),
('360d9505-bb29-4704-b850-8312dbca1814', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-17 04:00:43'),
('37338050-8971-458c-967a-344884d1597e', 'user-slaf-admin', NULL, 'User Management', 'PARADE_STATE_SUBMITTED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Submitted parade state for trade \'Computer Technician\' on 2026-09-16 to WO HFAI Fonseka. Records: 5', '2026-09-16 11:23:48'),
('37af1734-a558-480a-9a75-dfc3aa425a0c', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged in successfully', '2026-09-17 09:45:14'),
('37d62afc-64ba-4192-9b92-311ad6aeb2ba', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-17 11:42:05'),
('37dd6fab-eb9c-450f-88a8-79029fbe0346', 'user-slaf-admin', NULL, 'User Management', 'EXAM_MARKS_UPDATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Entered/updated grades for exam ID a8665362-dfe8-48e7-8168-f7834b44cee1 for 5 trainees', '2026-08-17 12:06:27'),
('38199038-ca2b-4915-b59b-5fa53800ef9e', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 05:40:53'),
('387bd3dc-e6b6-4614-a140-57308116f84e', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-11 11:25:57'),
('38a6ff69-a323-4298-94f3-a54ab7a2f0b5', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged in successfully', '2026-09-17 10:25:23'),
('38ebc145-714d-4173-b21b-8efe1da545b2', 'user-slaf-admin', NULL, 'User Management', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Generated Outstanding Parade State Report for date: 2026-08-31', '2026-08-31 09:48:13'),
('38fe131b-12bf-480e-a12e-a023ea092c5b', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-09 09:50:47'),
('392fa69d-afe6-40df-9e49-bb839775f706', 'user-slaf-admin', NULL, 'User Management', 'NIGHT_PARADE_REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Generated Night Parade State Report for date: 2026-09-21, trade: All', '2026-09-21 11:49:36'),
('39a5c228-1596-4d62-ae50-1ebf01a92b37', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-07 06:28:03'),
('3a30ea81-48d1-4265-8e52-7d190f557668', 'user-slaf-admin', NULL, 'Academic', 'LESSON_PLAN_UPLOADED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Uploaded lesson plan \'Introduction to accounting concepts\' for course Basic Course Of Account Assistant (ID: 2/2026)', '2026-09-18 10:38:18'),
('3cccf9b9-a06b-44ce-9e8d-a19847b1cf45', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Generated PARADE_STATE report with parameters: [parade_date=2026-08-31, trade=Computer Technician]', '2026-08-31 10:29:54'),
('3ddf72b6-de13-4d7b-8249-e40934378485', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-10-26 04:24:56'),
('3e749920-9efa-433c-a21b-91743a6ac855', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: []', '2026-09-21 05:17:23'),
('3e93f4dc-adc0-4946-b62e-21c9802b3bb0', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated ACCOMMODATION_BILLET report with parameters: []', '2026-09-21 05:02:05'),
('3f0e6c5a-371e-4cba-b7fa-69c0d579c600', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated PARADE_STATE report with parameters: [parade_date=2026-09-18]', '2026-09-18 11:04:19'),
('3f2656cc-760b-42ea-aa71-06951c68d866', 'user-slaf-admin', NULL, 'User Management', 'BED_POSITION_ALLOCATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'Allocated position \'Bunk-10-TOP\' to trainee 51098 (Kithmal)', '2026-10-26 04:35:08'),
('4052049f-4a16-4427-a84f-6faec40ffbc9', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-14 11:46:54'),
('40818332-7e02-4dd5-97ea-031d677dc4e0', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 11:58:40'),
('40973309-6aad-453d-abcf-9424fe842cd9', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated PARADE_STATE report with parameters: [parade_date=2026-09-21]', '2026-09-21 05:35:03'),
('40a88480-20b9-497d-b03d-667d95c75153', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated ACADEMIC_RESULTS report with parameters: [exam_id=144be146-1c60-4caf-95ad-389c941978d0, course=Comp Tech Adv, subject=Desktop Application Development, exam_type=Phase Test, exam_date=2026-09-16]', '2026-09-16 11:45:10'),
('40e5810e-7480-4f0d-8cda-3f88e9d1f20a', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-11 15:12:17'),
('4245df12-7719-48f7-ae98-0332be71f897', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-18 10:37:16'),
('4274d7c6-79dc-4eb3-b6a2-c7b51e8ba8ec', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-14 11:50:29'),
('4296a6fd-4516-49b5-86e9-6349928c0340', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated PARADE_STATE report with parameters: [parade_date=2026-09-21]', '2026-09-21 05:12:40'),
('42b5d7d0-1aa3-4bde-a7b7-85a8cd8644b4', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-18 10:09:57'),
('42fbd478-1b23-41ba-b818-19730ff5215f', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated PARADE_STATE report with parameters: [parade_date=2026-09-21]', '2026-09-21 05:02:25'),
('4358b118-122b-43a0-a44c-e29d0a7c020b', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-11 09:19:23'),
('4375d783-c427-4684-956d-e44fcefcc91f', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Generated ACADEMIC_RESULTS report with parameters: [exam_id=0c12c704-245d-4fdd-b14c-1d6ce8404874, course=Comp Tech Adv, subject=Desktop Application Development, exam_type=Final Exam, exam_date=2026-08-24]', '2026-08-24 11:42:01'),
('449bdf73-0155-4410-a003-cb2821dbb030', '1b514baf-ebde-4fcc-b838-902659c5c3e3', '04253', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'04253\' logged in successfully', '2026-08-10 11:10:41'),
('452ff2e1-b3c6-4bcf-859d-21fd5d230033', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-17 03:56:42'),
('45ace731-bd90-4343-9a9c-9adf5bbcdc8b', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged in successfully', '2026-09-17 09:45:53'),
('45e3f53c-0083-4ec1-9da2-d405e8cea901', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated OCCURRENCES report with parameters: [occurrence_type=ALL]', '2026-09-21 05:20:41'),
('463e9cc5-32ce-4d89-bf0f-26e867fcd32a', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated ACADEMIC_RESULTS report with parameters: [exam_id=a8665362-dfe8-48e7-8168-f7834b44cee1, course=Comp Tech Adv, subject=Data Base Management System, exam_type=Phase Test, exam_date=2026-08-17]', '2026-09-17 09:50:55'),
('465b8868-8ff2-44a2-84a9-c7a9f135938a', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-12 09:59:04'),
('46adb706-4017-419a-b3da-ed1fed02272d', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Generated COURSE_CALENDAR report with parameters: [course=Basic Course Of Account Assistant]', '2026-09-21 11:55:21'),
('46bce995-74d7-4622-9661-fe7dcd77bc34', 'user-slaf-admin', NULL, 'User Management', 'PARADE_STATE_SUBMITTED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Submitted parade state for trade \'Computer Technician\' on 2026-08-31 to Warrant Officer HFAI Fonseka. Records: 5', '2026-08-31 12:06:00'),
('47cdf5c5-6bcf-4719-8c3b-82c1dedc7116', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-10-05 11:55:01'),
('480c24b4-6ec0-4b32-b9a6-ae3669ca95f1', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-10-05 11:54:49'),
('4896aa95-4402-4b2c-8d9d-c7c68982a1bd', '1b514baf-ebde-4fcc-b838-902659c5c3e3', '04253', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'04253\' logged in successfully', '2026-08-11 15:17:31'),
('48f4990b-bf8d-4beb-b3c7-2e5f1abc2434', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-10-05 11:59:07'),
('490d864d-a70d-416c-b74a-5e59587454c5', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-16 11:27:53');
INSERT INTO `audit_logs` (`id`, `user_id`, `username`, `module`, `action`, `previous_value`, `new_value`, `ip_address`, `user_agent`, `details`, `created_at`) VALUES
('498b526e-8d7a-4533-9b5a-41598299725d', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-11 09:19:29'),
('49ed46fb-0524-414b-9716-17498ac938ae', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: [course_id=544f0ae2-2ee5-403b-84cf-58ac0aa193af]', '2026-08-31 09:52:09'),
('4a24233b-182b-4e07-9015-8cf4a39a81e2', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-18 10:37:00'),
('4aeba1d3-0d6d-4be6-8fe3-8c2d3165eeaa', 'user-slaf-admin', NULL, 'Academic', 'LESSON_PLAN_UPLOADED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Uploaded lesson plan \'Com tech\' for course Comp Tech Adv (ID: 26/1)', '2026-09-07 06:37:20'),
('4b4e70f1-2fae-4e4b-9de6-dca225b7007c', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 05:38:46'),
('4c001e48-1c46-4128-8351-5a08eb8be819', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated ACADEMIC_RESULTS report with parameters: [exam_id=144be146-1c60-4caf-95ad-389c941978d0, course=Comp Tech Adv, subject=Desktop Application Development, exam_type=Phase Test, exam_date=2026-09-16]', '2026-09-17 10:08:47'),
('4c098a20-71d0-486a-8c37-8a78d70283ad', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 05:19:35'),
('4c16a7b0-16d7-4ecf-a745-1f44d7f396ac', 'user-slaf-admin', NULL, 'User Management', 'PARADE_NIGHT_SAVED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'Saved Night Parade Roll Call for trade \'All\' on 2026-10-26. Records: 33, Changes: 1', '2026-10-26 04:49:46'),
('4d83d8cc-d4d9-4229-9088-97e098d49f76', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Generated PARADE_STATE report with parameters: [parade_date=2026-08-31]', '2026-08-31 09:49:43'),
('4d8a11dd-e939-4e95-ac5c-eb1107b775a6', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated PARADE_STATE report with parameters: [parade_date=2026-09-21]', '2026-09-21 05:12:56'),
('4da26a39-a44b-4943-9c3b-de6fa3477331', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-08-17 11:32:12'),
('4e19da3a-ab0d-4c3d-a1bf-d6ca3cab04b6', 'user-slaf-admin', NULL, 'User Management', 'PARADE_STATE_SUBMITTED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Submitted parade state for trade \'Account Assistant\' on 2026-09-21 to WO HFAI Fonseka. Records: 4', '2026-09-21 05:22:52'),
('4e269648-c9df-402c-b9ed-8dc51f86d97e', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 05:17:08'),
('4f5607cb-5c1d-404b-9036-3e6b73f2333b', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-24 03:19:02'),
('4fd04f07-d622-4306-84ce-c4a1ca05d7d6', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated ATTENDANCE_REGISTER report with parameters: []', '2026-09-21 05:20:19'),
('51015461-0adb-427f-8819-dfc2e5838fda', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Generated ATTENDANCE_REGISTER report with parameters: []', '2026-09-21 11:55:40'),
('51162f74-a315-48d3-b782-dd657b885492', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-10 10:58:39'),
('51a3c9d4-7887-4c6b-86d0-00a1af5b99cb', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Generated PARADE_STATE report with parameters: [parade_date=2026-09-21]', '2026-09-21 11:55:46'),
('51c8ed8e-09db-459a-a293-df8bdcb3f202', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-10-05 12:05:43'),
('522768ce-7e12-4b82-ada1-20d8b08fa5c7', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated OCCURRENCES report with parameters: [trainee_id=3b0e40ad-cfbf-4df7-804d-2c686c40ad2f, occurrence_type=ALL]', '2026-09-17 03:57:51'),
('52427dd1-9a79-4ab4-83b0-b7965b87d2dc', 'c5f0985e-45f7-4086-9bb7-06019de7cea3', '51098', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'51098\' logged out successfully', '2026-10-26 04:46:37'),
('5311d9df-9bba-452c-b05b-794e2f8e56b0', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged out successfully', '2026-09-17 10:30:56'),
('53a2bb59-4b91-480e-8b79-b2a0d5cd188a', 'user-slaf-admin', NULL, 'User Management', 'NIGHT_PARADE_REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Generated Night Parade State Report for date: 2026-09-21, trade: (ADMINISTRATIVE)', '2026-09-21 10:17:24'),
('54db8202-5470-4e5c-aed0-140b8e8e0a35', 'user-slaf-admin', NULL, 'User Management', 'BED_POSITION_ALLOCATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Allocated position \'Bunk-02-TOP\' to trainee 50845 (PRASANNA)', '2026-08-12 10:06:01'),
('5597809f-05fb-4980-96a7-e8328d6062da', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-17 09:47:30'),
('56017c77-07e1-4f1f-b8b2-48f324821a5c', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Generated ATTENDANCE_REGISTER report with parameters: []', '2026-08-31 09:52:34'),
('56099d54-50ac-4858-b238-3eb8af9c34b5', 'c96d5ee9-93ee-41cc-b9e6-f31ecba02f4e', '51837', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'51837\' logged in successfully', '2026-09-21 05:41:18'),
('56274a88-c8f5-44cd-bbc1-80a623af5878', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 12:00:14'),
('56a38319-ee84-423d-b4fb-7c93a6225ab2', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-16 11:22:31'),
('56ae2a1b-5667-4df7-ab27-24aa8fd6053c', 'user-slaf-admin', NULL, 'User Management', 'STUDENT_CREATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Created student record TA/40216 (Senevirathne)', '2026-09-09 10:30:56'),
('56fb65ae-33af-4c1e-83c0-2e7248ad44f2', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-11 15:30:20'),
('584582ee-9b53-4374-9540-235c292dfed3', 'user-slaf-admin', NULL, 'User Management', 'TIMETABLE_ATTENDANCE_UPDATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Updated classroom attendance registry for timetable session ID 99dc4d29-6bda-4f99-9996-3c796e92fcdd (5 trainees)', '2026-08-17 12:10:25'),
('586f17cd-da33-4082-a908-ef3d00ef76aa', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-10-26 04:05:24'),
('589be16a-15e0-4264-a247-79455a7225d8', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 05:39:12'),
('58afbdfd-f431-4831-bf67-7c1b14b68ff8', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-24 10:30:15'),
('58c15e7f-b9a5-437d-8a7e-596c722d8fef', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-24 03:12:33'),
('58f94235-b4ac-43c4-9f63-5cd9eb535133', 'dc5d99d0-d369-4487-a9df-27b663200f83', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated COURSE_CALENDAR report with parameters: [course=Basic Course Of Account Assistant]', '2026-09-17 10:41:17'),
('58fae300-07fb-4c64-b7d0-f82020e1bb08', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-18 10:10:26'),
('58ff521e-2bb4-4923-bf9d-09f0e348b686', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated PARADE_STATE report with parameters: [parade_date=2026-09-21]', '2026-09-21 05:35:30'),
('5ab171cb-52e2-4fe5-9fe0-431da561ca54', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-10 09:49:57'),
('5ced99ef-c2f0-4504-ba98-82bd29ff635e', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged out successfully', '2026-09-16 11:27:28'),
('5d2cd02c-1a1e-4cc6-9792-2c95bb263428', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-10-26 04:24:42'),
('5d61dbc2-6e14-411a-9543-c5aa898dfeff', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-18 11:04:34'),
('5db0835f-dbfc-4a10-8379-4b9b23a9f089', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: [course_id=ca0ae649-cffd-4712-b156-8209ffd159d4]', '2026-08-31 09:51:55'),
('5dc3aeb9-acfa-4df7-ab3e-1afa1942d458', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged in successfully', '2026-09-17 10:30:43'),
('5de7889d-1408-4f80-b53d-e4a733cf12d0', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-17 03:43:56'),
('5e6c9c08-c6f1-4bcf-a97f-fa2070f31ce6', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'test', 'User \'admin\' logged in successfully', '2026-08-17 10:56:53'),
('5f5e2446-6f3e-40f9-95b0-6dd341c12c8a', 'user-slaf-admin', NULL, 'Student Management', 'CREATE_PERSONAL_OCCURRENCE', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Recorded ACHIEVEMENT \'Best Student\' on 14.08.2026 for trainee 50327 (Rashmika)', '2026-08-14 11:51:19'),
('5f70dd4d-a509-42c7-9339-fb2ca147180f', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-08-17 12:23:21'),
('5f94e1b3-09f6-448a-902e-c630d353c95e', 'user-slaf-admin', NULL, 'User Management', 'STUDENT_CREATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Created student record TA/40218 (Tharanga)', '2026-09-09 10:09:54'),
('62670e5c-aa8f-454e-952e-8566cb5f6d94', 'user-slaf-admin', NULL, 'User Management', 'NIGHT_PARADE_REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Generated Night Parade State Report for date: 2026-09-21, trade: All', '2026-09-21 10:18:52'),
('63d86eef-2f9d-4709-a8ee-77531be518ca', 'user-slaf-admin', NULL, 'Academic', 'LESSON_PLAN_ARCHIVED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Archived lesson plan \'Comp tech lesson plan\' (ID: 34333541-a464-43be-84f0-c38c26e59d81)', '2026-08-12 10:37:42'),
('642d79fd-3536-4852-9b42-29c44dcb0d13', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-14 11:51:33'),
('644a2572-ff48-4553-be85-ea67885398f9', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Generated ACCOMMODATION_BILLET report with parameters: []', '2026-08-31 09:50:01'),
('6579f70b-dc76-4adc-a6e3-5254982fcec6', 'user-slaf-admin', NULL, 'User Management', 'NIGHT_PARADE_COMPLETED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Completed Night Parade Roll Call for trade \'All\' on 2026-09-21 by SLAF Administrator. Expected: 31, Accounted: 31, Changed: 1. Status Changes: 7c03548a-fe20-40b5-9ac0-6f1ee3d1a886: Present -> Sick Report', '2026-09-21 11:41:12'),
('664dd6d9-40ec-45d4-827c-dab0ccae8aeb', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-10 09:37:58'),
('6691de9a-ef2a-4229-bce1-9a92c6f7d264', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Generated ACCOMMODATION_BILLET report with parameters: []', '2026-09-21 11:55:39'),
('6694900e-b44c-4b03-8121-45c1f3fb40e1', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-07 06:29:28'),
('67451e25-2621-49ab-977b-98e1c65732ea', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-16 10:33:45'),
('67a2f6ae-7c41-4948-81ff-660a2aab650f', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 07:29:59'),
('67d4739b-a5be-4209-a6d8-25fb56d012d4', '1b514baf-ebde-4fcc-b838-902659c5c3e3', NULL, 'User Management', 'PARADE_STATE_APPROVED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Approved parade state submission 873e9481-6a19-4cf9-9f47-021abd7a66ec for trade \'Computer Technician\' on 2026-08-17', '2026-08-17 10:53:46'),
('6846f683-462a-40ee-98cd-89ed2db9236e', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Generated ACADEMIC_RESULTS report with parameters: [exam_id=0c12c704-245d-4fdd-b14c-1d6ce8404874, course=Comp Tech Adv, subject=Desktop Application Development, exam_type=Final Exam, exam_date=2026-08-24]', '2026-08-24 11:53:21'),
('6bf6540f-711b-42dc-b6d0-9e7ce14c90d2', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: []', '2026-09-21 05:20:23'),
('6c2d39d3-afe3-4cb7-8d83-f2412deec3e6', 'user-slaf-admin', NULL, 'User Management', 'PARADE_NIGHT_SAVED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Saved Night Parade Roll Call for trade \'All\' on 2026-09-21. Records: 31, Changes: 1', '2026-09-21 11:40:48'),
('6d79510d-d111-4c6d-b1c1-35104196ebe6', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-10 10:52:32'),
('6dca4dc8-41eb-4976-a950-d7101f2ba13e', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-10-26 04:48:54'),
('6ed7a283-eae8-42d5-9f86-63c6258bc5d6', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-10-26 04:27:16'),
('6fc5fec5-d9c1-4bf1-a193-78fa67f9c052', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-17 04:03:14'),
('700a8a1a-2426-4052-bee4-d46d8ca4cbe9', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-13 11:50:25'),
('70e67be6-cfc7-446d-bdd2-7e44d03d355f', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated COURSE_CALENDAR report with parameters: [course=Basic Course Of Account Assistant]', '2026-09-17 03:52:34'),
('7111e1d9-2775-44dd-900f-739fb743d45b', 'dc5d99d0-d369-4487-a9df-27b663200f83', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated COURSE_CALENDAR report with parameters: [course=Basic Course Of Account Assistant]', '2026-09-17 10:41:17'),
('7122f4a4-3e7a-42d3-b636-96600cfb561b', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged in successfully', '2026-09-16 11:26:44'),
('71f66801-27fa-49c1-8fb2-c5e15d2d987e', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-10-26 04:48:34'),
('722ad76d-5dd7-46ec-95b9-7ca26865abe7', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: []', '2026-08-31 10:17:59'),
('73671056-1612-46d2-8658-6ecd5e9cf01c', '1b514baf-ebde-4fcc-b838-902659c5c3e3', '04253', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'04253\' logged in successfully', '2026-08-17 10:53:17'),
('7377785a-0c82-40ee-a244-43dd5a4ca03c', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-10 11:41:48'),
('739be8ec-2400-4af0-a078-04d5e6193dcf', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated ACCOMMODATION_BILLET report with parameters: []', '2026-09-17 03:53:29'),
('75bffbc2-77c1-474c-b88f-13b692056874', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-10-26 04:32:34'),
('76106e7b-c63c-4364-bd09-a2caf5b1db04', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: []', '2026-10-05 12:04:09'),
('766cc954-ad49-41f4-85ed-2961d9350f68', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 05:48:39'),
('769bc61b-0210-4046-86b0-7a37b281d877', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-10 10:24:12'),
('76ab686f-11ba-49bc-9f17-4e9757097ddf', 'c96d5ee9-93ee-41cc-b9e6-f31ecba02f4e', '51837', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'51837\' logged out successfully', '2026-09-21 05:41:25'),
('7799734c-c211-4baf-8da2-6b1ba6ba772f', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'ACCOUNT_LOCKED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Account auto-locked due to 5 consecutive failed login attempts', '2026-08-10 11:31:56'),
('78224d57-4122-47bf-96ed-78417d3abac8', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 05:42:26'),
('793eb3e8-4f29-421e-b027-cb3cec49fd60', '1b514baf-ebde-4fcc-b838-902659c5c3e3', '04253', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'04253\' logged in successfully', '2026-08-10 11:08:27'),
('7975f7c4-b025-4a50-8dd6-bbfefaa2e919', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-17 11:16:24'),
('79fee462-c6a4-4000-bbe1-719b28924afe', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-10 11:34:49'),
('7a6f6541-d58e-41c9-af20-b4526f73cad4', '1b514baf-ebde-4fcc-b838-902659c5c3e3', '04253', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'04253\' logged in successfully', '2026-08-10 11:19:35'),
('7abde5ff-4e56-46f4-8111-0a0abc42f909', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-07 07:14:17'),
('7bb364c9-1b96-4a83-aaf9-cc3695134741', 'dc5d99d0-d369-4487-a9df-27b663200f83', NULL, 'User Management', 'PARADE_STATE_APPROVED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Approved parade state submission e8d58de6-4072-4245-a900-50bcd5e460a9 for trade \'Computer Technician\' on 2026-08-31', '2026-08-31 12:19:28'),
('7e35aefc-397d-4ee2-96fe-eced6c955ed8', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-10-26 04:30:11'),
('7e3caf74-ca5d-4b26-8b01-809e7059acf4', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-18 09:32:38'),
('7e819318-8e87-4f7f-b80e-49f53f52ba5e', 'user-slaf-admin', NULL, 'User Management', 'STUDENT_CREATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Created student record TA/40217 (Chinthaka)', '2026-09-10 11:30:03'),
('7ee3ef27-7db1-498b-88ab-ab647982ad98', 'user-slaf-admin', NULL, 'User Management', 'STUDENT_CREATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Created student record TA/40219 (HERATH)', '2026-09-09 10:25:29'),
('7f5acaff-460a-44cd-b9fa-747285dfc117', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 07:19:42'),
('81067690-8388-4468-bbcc-fe3ae4d63ee1', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-17 10:50:09'),
('823707b2-3a73-4c1d-89ad-22cec6931b2c', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-12 05:29:46'),
('82a63345-433b-4d47-9276-d026c8c8e508', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated PARADE_STATE report with parameters: [parade_date=2026-09-21]', '2026-09-21 05:35:03'),
('82ff6dfe-e613-421c-aae1-dff5e5da95bd', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged out successfully', '2026-09-17 09:46:05'),
('830a16c2-ab7e-412c-99c8-f038935e7eb6', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-17 10:54:23'),
('83db7303-458b-426b-a9e6-3b9c61ce0519', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-10-26 04:26:57'),
('84072437-c0b5-4683-9f87-f8644593c651', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-17 12:16:31'),
('84bf890d-48c7-4a3a-865f-c847a19d15bf', 'user-slaf-admin', NULL, 'Student Management', 'CREATE_PERSONAL_OCCURRENCE', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Recorded MISCONDUCT_OFFENSE \'test bad\' on 14.08.2026 for trainee 50327 (Rashmika)', '2026-08-14 11:54:21'),
('853d4a7c-d81a-4536-849b-479414909abd', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-08-20 10:41:57'),
('85cd8910-f8a1-4114-943a-ef0c8508c9ab', 'user-slaf-admin', NULL, 'User Management', 'NIGHT_PARADE_REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Generated Night Parade State Report for date: 2026-09-21, trade: All', '2026-09-21 11:29:49'),
('863f1b1f-80e8-481a-9bb8-cfc750087d5e', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-16 10:34:33'),
('86beb9c9-2b10-4bce-9492-a405e0bf2d50', 'f6f853a0-a3db-481e-bb6b-95e469c45dc8', '51088', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'51088\' logged in successfully', '2026-08-12 04:25:31'),
('87a70a0f-dd64-4a4e-9a29-57c7e5b1b3ab', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-10-26 04:45:59'),
('87b7b463-3ee7-419d-ab06-bca76b4c9c7a', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-08-24 03:18:22'),
('87ca8584-c251-4b77-9e32-418c41139e46', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: []', '2026-09-24 09:40:33'),
('88114b0b-fe0c-4dc3-af88-889a1518e561', NULL, 'System Scheduler', 'Academic Management', 'AUTOMATIC_BATCH_CLOSURE', 'Status: ONGOING', 'Status: PASSED OUT', '127.0.0.1', 'System Automated Batch Task', 'Course \'TEST-EXP-1789363673 - Test Expired Course Aircraft Assist\' automatically closed and moved to PASSED OUT state. Course End Date (2026-03-01) has passed as of 2026-09-14.', '2026-09-14 10:57:54'),
('8934a1a1-233f-4f30-9703-fa7b340698a8', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-16 10:34:25'),
('89712caf-c17c-414a-856a-9da3f3a7c8be', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-11 09:25:46'),
('89d5d580-1309-4430-b075-ad26517c4cb6', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged out successfully', '2026-09-17 10:26:28'),
('8a7a9864-aa31-4e05-a277-12d00d105274', 'user-slaf-admin', NULL, 'User Management', 'PARADE_STATE_SUBMITTED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Submitted parade state for trade \'Computer Technician\' on 2026-08-10 to officer Saman Kumara. Records: 4', '2026-08-10 11:08:11'),
('8ab260a8-68d1-4675-96c6-4de983490442', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-12 04:35:43'),
('8b19cf4d-f95b-4518-8149-63db004994bc', 'c96d5ee9-93ee-41cc-b9e6-f31ecba02f4e', '51837', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'51837\' logged in successfully', '2026-09-21 05:43:57'),
('8c6cee46-a0d9-4622-94e8-6f30d9c0d021', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-08-24 11:54:23'),
('8ca1a018-a830-463d-9570-f5e0cd6438b9', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-17 11:38:39'),
('8d115163-e583-4b02-aec9-14b1373fbeec', 'user-slaf-admin', NULL, 'Academic Management', 'DELETE_COURSE_CALENDAR_ENTRY', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Deleted calendar phase \'Practical Lab Phase 02\' from course ID 860749a8-7b0e-4e22-b439-5f22b63e3db1', '2026-08-14 09:56:21'),
('8d40d40e-9712-4454-9d61-068f146be8f8', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged out successfully', '2026-09-17 10:29:45'),
('8d84e573-71ab-4f85-b658-c6e76d4b12db', 'user-slaf-admin', NULL, 'User Management', 'NIGHT_PARADE_REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated Night Parade State Report for date: 2026-09-21, trade: All', '2026-09-21 05:34:11'),
('8d92abaf-4d02-4eb9-9805-c5f7eb9ebacc', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-11 15:34:17'),
('8dfe4240-02a8-44d7-a9e8-8c297efbcfe3', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-08-31 10:39:38'),
('8e357c33-4c2f-4bbc-8fd0-c57b5d1bf592', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged in successfully', '2026-09-17 10:30:02'),
('8e8657fc-1f82-4bab-ac46-b1d634cdde3c', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-14 11:49:51'),
('8f72ff18-db8e-4229-8eda-ec1e396d5462', 'dc5d99d0-d369-4487-a9df-27b663200f83', NULL, 'Academic Management', 'CREATE_COURSE_CALENDAR_ENTRY', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Added calendar phase \'[15] Introdution of Accounting & Basic Concepts\' (S/No: 3, Instructor Status: NOT_ASSIGNED) for course \'Basic Course Of Account Assistant\'', '2026-09-17 10:45:21'),
('8f798162-2990-4240-9f1d-637335783e99', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-10-26 04:37:06'),
('916c597d-ea87-4973-a19f-fa1362e62b81', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated ACADEMIC_RESULTS report with parameters: [course=Comp Tech Adv, subject=Desktop Application Development, exam_type=Phase Test, exam_date=2026-09-16, result_status=ALL]', '2026-09-21 05:20:20'),
('91c6cf3d-4682-4208-9a25-91cf1b568760', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated ACADEMIC_RESULTS report with parameters: [exam_id=144be146-1c60-4caf-95ad-389c941978d0, course=Comp Tech Adv, subject=Desktop Application Development, exam_type=Phase Test, exam_date=2026-09-16]', '2026-09-16 11:50:02'),
('9359430b-6bc7-4f4c-8370-d7cb78ad1553', 'user-slaf-admin', NULL, 'Academic Management', 'CREATE_COURSE_CALENDAR_ENTRY', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Added calendar phase \'Database Managemet System\' (S/No: 1, Instructor Status: ASSIGNED) for course \'Comp Tech Adv\'', '2026-08-14 10:11:50'),
('93bba781-f984-4b42-9dc0-1231838394ca', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-08-31 12:03:26'),
('9546fcff-d26a-4a79-8e99-e179c7dd79ad', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged in successfully', '2026-09-17 10:31:14'),
('9564a44e-99bd-4ab5-9b80-2544b37f1277', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-16 10:33:32'),
('957be88c-139c-4233-aae7-9bae0a09f519', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-17 11:16:24'),
('96af089b-e2b3-4e7a-9354-82bd742a3f31', NULL, 'System Scheduler', 'Academic Management', 'AUTOMATIC_BATCH_CLOSURE', 'Status: ONGOING', 'Status: PASSED OUT', '127.0.0.1', 'System Automated Batch Task', 'Course \'TEST-EXP-1789362557 - Test Expired Course Aircraft Assist\' automatically closed and moved to PASSED OUT state. Course End Date (2026-03-01) has passed as of 2026-09-14.', '2026-09-14 10:39:17'),
('9799f852-1280-4059-aa55-e68d86e05867', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 05:01:42'),
('97f57884-27be-4d16-ba78-4cf02b717fa1', 'user-slaf-admin', NULL, 'User Management', 'PARADE_STATE_SUBMITTED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Submitted parade state for trade \'Computer Technician\' on 2026-08-24 to officer Saman Kumara. Records: 5', '2026-08-24 10:27:49'),
('9825d904-cdf5-4a0e-9492-4a54985901ca', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 05:21:16'),
('987e6f65-d2cb-4681-aa75-704fd3dae69c', '1b514baf-ebde-4fcc-b838-902659c5c3e3', '04253', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'04253\' logged out successfully', '2026-08-24 10:29:59'),
('987f71bb-48aa-48b8-81c5-7247391b4445', 'user-slaf-admin', NULL, 'User Management', 'STUDENT_DELETED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Soft-deleted student record S-1789363674 (Test Trainee Expiration)', '2026-09-17 03:59:39'),
('9954e710-4cf9-4606-ad64-334e74bb18a4', 'user-slaf-admin', NULL, 'Student Management', 'DELETE_PERSONAL_OCCURRENCE', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Soft-deleted ACHIEVEMENT record \'Best Student\' (ID 64446e34-971a-4f10-b485-a272c2ead90b) for trainee 50327', '2026-08-14 11:55:06'),
('997e238b-01f2-4ea2-afb7-9a0463a92939', 'user-slaf-admin', NULL, 'User Management', 'PARADE_NIGHT_SAVED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'Saved Night Parade Roll Call for trade \'All\' on 2026-10-26. Records: 33, Changes: 1', '2026-10-26 04:51:11'),
('99ff6092-9683-4509-81b2-8a6a58662fef', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-08-17 12:15:51'),
('9a6adff4-12d6-469a-a0e5-31d1ed12a363', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-17 03:51:47'),
('9acaf8bb-5b25-482c-91a4-c78befbafb94', 'user-slaf-admin', '51837', 'User Management', 'USER_CREATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Created user username=\'51837\', full_name=\'sanka adikaram\', role_id=\'role-instructor\'', '2026-09-21 05:40:48'),
('9acdc674-2823-4f63-9b18-8df832ba6eff', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-14 10:56:29'),
('9b6e6abe-ddf1-4fa7-8bb0-95d7d15f63f2', 'dc5d99d0-d369-4487-a9df-27b663200f83', NULL, 'User Management', 'PARADE_STATE_APPROVED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Approved parade state submission 30e8d3c9-7ebc-4890-ba9a-8f6d460e498f for trade \'Computer Technician\' on 2026-09-16', '2026-09-16 11:27:17'),
('9b8c7b62-0250-4bbc-89d3-6199e34dcc9d', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: []', '2026-09-21 05:20:17'),
('9be312e8-fa67-4969-be76-9fb7b802bd04', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: []', '2026-08-31 09:51:12');
INSERT INTO `audit_logs` (`id`, `user_id`, `username`, `module`, `action`, `previous_value`, `new_value`, `ip_address`, `user_agent`, `details`, `created_at`) VALUES
('9c2a48aa-f170-4762-bf41-beaa4ce309ea', 'user-slaf-admin', NULL, 'User Management', 'STUDENT_CREATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'Created student record aw/4618 (Ranasinghe)', '2026-10-26 04:22:34'),
('9c36026e-68f5-4c0a-87ea-619100fc9fe6', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged in successfully', '2026-09-17 10:14:25'),
('9c372d68-90da-4f92-9449-464319ff5bb7', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated ACADEMIC_RESULTS report with parameters: [exam_id=144be146-1c60-4caf-95ad-389c941978d0, course=Comp Tech Adv, subject=Desktop Application Development, exam_type=Phase Test, exam_date=2026-09-16]', '2026-09-16 11:29:40'),
('9c9ff2d2-a675-460b-97ec-f4ff65fafc6a', 'user-slaf-admin', NULL, 'User Management', 'STUDENT_CREATED', NULL, NULL, '127.0.0.1', 'test', 'Created student record TEST-001 (TEST KARUNARATNE)', '2026-09-09 11:35:11'),
('9d2b5548-71ee-489d-91e1-20b8a2d4bc78', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged out successfully', '2026-09-17 10:30:11'),
('9d609eb4-6baf-4762-9c16-faade8f5fc8c', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Generated PARADE_STATE report with parameters: [parade_date=2026-08-31]', '2026-08-31 09:49:43'),
('9e20c396-f1dd-4c0f-b4a1-616f6624f8db', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-14 11:57:44'),
('9e3691df-d57e-40b4-a848-d9e8c424db84', 'user-slaf-admin', NULL, 'User Management', 'EXAM_MARKS_UPDATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Entered/updated grades for exam ID a8665362-dfe8-48e7-8168-f7834b44cee1 for 3 trainees', '2026-09-17 09:49:28'),
('9edaf2b2-9792-46d9-8010-41374c53fcdb', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 07:28:05'),
('9f4e54f8-3783-4975-aa43-3b3febdfe758', 'user-slaf-admin', NULL, 'User Management', 'PARADE_STATE_SUBMITTED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Submitted parade state for trade \'Computer Technician\' on 2026-08-11 to officer Saman Kumara. Records: 5', '2026-08-11 15:16:58'),
('9f66d051-3621-460f-a20e-84b2d58b7fb4', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-12 10:15:41'),
('9f8ca739-7f08-4e09-a3ca-213d1610fe04', 'user-slaf-admin', NULL, 'User Management', 'EXAM_MARKS_UPDATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Entered/updated grades for exam ID 33d73d9e-0ee9-430a-a308-5a42747aefbf for 5 trainees', '2026-08-17 12:14:08'),
('a04708fa-5f93-4a13-aec6-160e8af3eced', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-15 11:26:43'),
('a056b248-5a97-448b-b621-f9cdbd562b0d', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-10-26 04:30:27'),
('a09f1d2f-d22c-4531-b4d2-5ca18c6995c3', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-10 11:19:08'),
('a0cce226-8371-445c-b4af-633cbb23478a', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-17 05:43:48'),
('a12cefea-86ac-433b-8596-eac8dfaab43b', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-17 11:33:06'),
('a1568e2a-4e0a-4097-8ef9-b411dcd269fc', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 05:39:33'),
('a18233d2-340c-4730-ab39-c5ed4b6db80a', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: []', '2026-09-17 03:52:46'),
('a18ac57d-0a94-4fa0-a818-65e7999eddb8', 'user-slaf-admin', '51088', 'User Management', 'USER_CREATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Created user username=\'51088\', full_name=\'Dayanada\', role_id=\'role-instructor\'', '2026-08-11 15:32:32'),
('a1926dbd-0d5f-40bc-bae4-061ae4790d7d', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-10-05 12:02:26'),
('a20e06a4-c953-4a99-aa05-7b8d803a7386', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-14 11:38:44'),
('a2430539-bbce-4504-b0f9-cd325634d5d9', '1b514baf-ebde-4fcc-b838-902659c5c3e3', NULL, 'Academic', 'LESSON_PLAN_UPLOADED', NULL, NULL, 'unknown', 'unknown', 'Uploaded lesson plan \'Test Lesson Plan Document\' for course Basic Course Of Account Assistant (ID: 2/2026)', '2026-09-18 09:39:25'),
('a321ab6b-7cfa-498f-8acf-3e07bd40f5df', 'user-slaf-admin', NULL, 'User Management', 'NIGHT_PARADE_REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated Night Parade State Report for date: 2026-09-21, trade: All', '2026-09-21 05:23:31'),
('a358c714-bc65-4f3f-9fc3-91c250d00ed2', 'user-slaf-admin', NULL, 'Academic Management', 'DELETE_COURSE_CALENDAR_ENTRY', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Deleted calendar phase \'English Intensive\' from course ID 32d6af23-5645-4cf8-bc5a-1e6672c9b86b', '2026-08-14 09:54:58'),
('a4a6b718-b1f8-4c9a-83bd-5f5baaa8ace3', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged out successfully', '2026-09-17 09:47:04'),
('a4aef456-2d84-4cdd-ba76-d89245a42de4', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-15 12:31:14'),
('a50ff33b-0ff8-4796-b5f3-d97b22bddf07', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-08-24 03:20:39'),
('a529f728-ac8a-4b8e-9a4d-dfc624482425', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: []', '2026-09-17 03:52:14'),
('a5c1d55d-62d9-41f4-b8fe-a3b996fa4419', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-17 04:01:55'),
('a637ce6c-9565-4adc-902b-1cc65e3e32c9', 'user-slaf-admin', NULL, 'Academic', 'LESSON_PLAN_UPLOADED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Uploaded lesson plan \'Introduction to accounting concepts\' for course Basic Course Of Account Assistant (ID: 2/2026)', '2026-09-18 10:41:51'),
('a65ec466-5195-4a5c-96ec-4ff8512cc7e1', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-10-26 03:52:17'),
('a6e13147-9a7c-4ca8-9370-7b5b2c61f3dc', 'user-slaf-admin', NULL, 'Student Management', 'DELETE_PERSONAL_OCCURRENCE', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Soft-deleted MISCONDUCT_OFFENSE record \'test bad\' (ID 398a0eb2-7f7f-4181-b148-7b54e5a62ef5) for trainee 50327', '2026-08-14 11:55:00'),
('a6f1bdd0-b02d-4f58-b450-5f6412b1f10f', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 07:30:12'),
('a7bd1493-5777-4493-9ebd-fb08038f9c23', 'user-slaf-admin', NULL, 'Academic Management', 'CREATE_COURSE_CALENDAR_ENTRY', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Added calendar phase \'English Intensive\' (S/No: 3, Instructor Status: ASSIGNED) for course \'Test Radar Basic Course\'', '2026-08-13 12:01:53'),
('a8bd4847-622f-42f9-8ce9-002fcf9d5603', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-09 10:31:19'),
('a8df7281-6261-43c9-a0d3-48d266457234', 'user-slaf-admin', NULL, 'User Management', 'NIGHT_PARADE_COMPLETED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'Completed Night Parade Roll Call for trade \'All\' on 2026-10-26 by SLAF Administrator. Expected: 33, Accounted: 33, Changed: 1. Status Changes: e1650c87-f565-471c-85e8-a157df7dc81b: Course Visit -> Present', '2026-10-26 04:51:13'),
('a93fadf0-eedc-477b-b102-44f0fd8f1f3e', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-10-05 12:03:48'),
('a95a098e-163b-415d-a402-5c725dddddf4', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'32853\' logged in successfully', '2026-08-31 12:09:27'),
('a9d0d514-2410-408f-9f99-910fc0cf8d1f', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-20 10:42:10'),
('a9dfc859-4d3e-4721-973d-6b47de55201c', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged in successfully', '2026-09-17 10:24:14'),
('a9e3dcba-f3c5-4469-8602-e2457a1d7c4d', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-18 09:28:43'),
('aa09cb8a-ac05-4d7c-8e2b-939ec21de7a7', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-24 02:59:40'),
('aab84658-fb99-43d8-a6ff-ae46f2f8a801', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 05:54:30'),
('aabc6793-54df-4780-b258-38b0ee057f1d', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 05:22:15'),
('ac35d545-7d97-4ac9-87ab-fd75e8d31501', 'user-slaf-admin', NULL, 'Academic Management', 'CREATE_COURSE_CALENDAR_ENTRY', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Added calendar phase \'[DBMS] Data Base Management System\' (S/No: 2, Instructor Status: ASSIGNED) for course \'Comp Tech Adv\'', '2026-08-17 10:55:23'),
('ac7a11f5-e9ad-4624-8cec-4863e394e750', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-18 10:10:11'),
('acc3edb9-e0a0-4c8c-8b44-b840c399a62c', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated ACADEMIC_RESULTS report with parameters: [course=Comp Tech Adv, subject=Desktop Application Development, exam_type=Phase Test, exam_date=2026-09-16, result_status=ALL]', '2026-09-17 03:53:28'),
('ad15d841-da64-48c3-bcbb-d2f1875614e6', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-17 03:57:03'),
('ad23e5a5-bc7f-4e49-a38d-d552e2d806e6', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-10-26 04:43:13'),
('adc60847-9c3a-4ea0-a57b-dc2ac1ec87d1', 'user-slaf-admin', NULL, 'Academic', 'LESSON_PLAN_UPLOADED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Uploaded lesson plan \'Comp tech lesson plan\' for course Comp Tech Adv (ID: 26/1)', '2026-08-12 10:36:31'),
('adf6be07-c943-4da1-a9c8-c092a36a28e5', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-10-05 11:24:27'),
('af08c191-7d5d-45ea-bc7e-637a77e0b4cd', '1b514baf-ebde-4fcc-b838-902659c5c3e3', NULL, 'Student Management', 'CREATE_PERSONAL_OCCURRENCE', NULL, NULL, NULL, NULL, 'Recorded ACHIEVEMENT \'Test Achievement Automated Verification\' on 15.09.2026 for trainee 50833 (LAKSHAN)', '2026-09-15 11:14:57'),
('af62f3d3-c8c9-48ba-a206-89226282ec0e', 'user-slaf-admin', NULL, 'Academic', 'LESSON_PLAN_UPLOADED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Uploaded lesson plan \'Introduction to accounting concepts\' for course Basic Course Of Account Assistant (ID: 2/2026)', '2026-09-18 10:39:45'),
('afa6cf36-156e-4c44-bedc-ee1c17decffd', '1b514baf-ebde-4fcc-b838-902659c5c3e3', '04253', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'04253\' logged in successfully', '2026-08-24 10:29:26'),
('aff3a417-6bb5-4a97-b0f9-191d30c7bc46', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-11 09:20:11'),
('b094ccfd-e137-453c-925d-e86ec3f3cba7', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 12:00:26'),
('b0d44cfc-e215-45ab-8ebb-e5149f42d76c', 'user-slaf-admin', NULL, 'User Management', 'STUDENT_CREATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Created student record TA/40216 (Senevirathne)', '2026-09-10 11:26:07'),
('b2347b11-e7e1-4680-92f5-697261efd6bc', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-10 10:52:32'),
('b3920edf-5798-4f84-a035-a6e1ca38c176', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: []', '2026-09-21 11:55:01'),
('b4e35f74-b4be-4cdb-8a89-b042064a53fa', 'user-slaf-admin', NULL, 'User Management', 'NIGHT_PARADE_REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'Generated Night Parade State Report for date: 2026-10-26, trade: All', '2026-10-26 04:51:22'),
('b673eee5-e3b0-44b3-8cef-41dc4b641c4a', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged out successfully', '2026-09-17 10:24:30'),
('b6a8eab6-a363-4478-9a0c-d43be2a2cef3', 'dc5d99d0-d369-4487-a9df-27b663200f83', NULL, 'Academic Management', 'CREATE_COURSE_CALENDAR_ENTRY', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Added calendar phase \'[18] Gagana Viru Sawiya Walfare Scheme\' (S/No: 2, Instructor Status: ASSIGNED) for course \'Basic Course Of Account Assistant\'', '2026-09-17 10:40:31'),
('b6f6d71e-d226-4d9b-a32a-240334b38efd', 'c5f0985e-45f7-4086-9bb7-06019de7cea3', '51098', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'51098\' logged in successfully', '2026-10-26 04:46:11'),
('b7a3ce85-7b33-4a72-9023-0354afdcc65e', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: []', '2026-09-21 05:17:23'),
('b7b77e36-94be-46f8-af7e-05b16b12e260', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-11 15:35:29'),
('b82ce3e9-12ce-4b03-a6cb-2f41ffdfa50c', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 11:51:10'),
('b8f22ebf-169d-40c9-9c49-01503dc080bf', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Generated ATTENDANCE_REGISTER report with parameters: [date_range=2026-08-30 to 2026-08-31]', '2026-08-31 09:53:05'),
('b9a1a3fc-759a-4200-b30a-f3e66650d881', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-10 10:53:47'),
('b9bfab99-a41e-49f0-9a33-3fa504ea8cbe', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Generated COURSE_CALENDAR report with parameters: [course=Test Radar Basic Course]', '2026-08-31 09:50:34'),
('b9c6a71a-b44d-4296-965f-e5a0b2037024', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-10-05 11:18:32'),
('bab82fee-6356-45bd-b650-813eba7e4640', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-14 09:28:36'),
('bb88c939-c5fc-4b16-ae52-2c014ceb864d', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-10 09:34:44'),
('bc1eeb06-5ba5-46db-a53a-daab324b1db6', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-10-05 12:02:12'),
('bdf637db-c347-45de-95df-b38cb2cf7427', 'user-slaf-admin', NULL, 'Academic', 'LESSON_PLAN_ARCHIVED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Archived lesson plan \'Comp tech lesson plan\' (ID: e0407688-6cf2-43b4-b754-1a253ea4c787)', '2026-08-20 10:27:27'),
('be2967a6-3fee-41e7-9a8a-c78a5e243e14', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 05:21:27'),
('be8c2605-d78f-455f-82f4-63a7da732643', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-16 09:38:23'),
('bf1fe3cf-3792-4e71-97d2-e3199cab91b2', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-09 09:50:59'),
('bfe93029-9abd-4061-8fd5-04fadbafa634', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-09 11:17:05'),
('c033b00f-b3a8-4934-9a67-03acb814eeb3', 'user-slaf-admin', NULL, 'Academic Management', 'CREATE_COURSE_CALENDAR_ENTRY', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Added calendar phase \'English Intensive Period\' (S/No: 1) for course \'Comp Tech Adv\'', '2026-08-12 11:50:03'),
('c1808a73-2cad-4e8f-99e9-d4a6c547c71e', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-31 11:55:49'),
('c1bc6acd-3a78-440f-87c5-f016295d59ff', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-11 15:24:26'),
('c1f20f6b-4fc1-4ac0-bf8d-474dd7e61b03', 'user-slaf-admin', NULL, 'Academic Management', 'DELETE_COURSE_CALENDAR_ENTRY', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Deleted calendar phase \'English Intensive Period\' from course ID 544f0ae2-2ee5-403b-84cf-58ac0aa193af', '2026-08-14 09:55:22'),
('c215e9cb-0efb-47fe-b445-a7c8e6e945df', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'32853\' logged in successfully', '2026-08-10 11:33:39'),
('c23d98ae-2c20-40d9-9b6a-6b2b10bbc207', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged in successfully', '2026-09-17 09:46:26'),
('c2823651-0b7f-4624-9eb9-affb48e33aed', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged out successfully', '2026-09-17 09:45:40'),
('c29f2b39-e7e9-4995-ba66-8e813dbf2698', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 07:28:39'),
('c2cb0d9d-28a8-42b4-9121-7d127c7f5005', 'user-slaf-admin', NULL, 'Academic Management', 'CREATE_COURSE', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'Created course \'Telephone Operator\' (26/2). Duration: 10 Weeks (9 Weeks 1 Day). Period: 2026-10-28 to 2026-12-30', '2026-10-26 04:29:39'),
('c2d55b49-1579-4fb1-8781-ef35c5cf0d9e', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated PARADE_STATE report with parameters: [parade_date=2026-09-21]', '2026-09-21 05:35:30'),
('c3006b26-5a2a-4c2d-af09-7587c094ab5a', '1b514baf-ebde-4fcc-b838-902659c5c3e3', NULL, 'User Management', 'PARADE_STATE_APPROVED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Approved parade state submission bebc58fe-0fd4-488d-8041-679441786665 for trade \'Computer Technician\' on 2026-08-24', '2026-08-24 10:29:52'),
('c313215c-9210-422a-a434-eb569f4b8dde', NULL, 'System Scheduler', 'Academic Management', 'AUTOMATIC_BATCH_CLOSURE', 'Status: Active', 'Status: PASSED OUT', '127.0.0.1', 'System Automated Batch Task', 'Batch \'Batch-TEST-EXP-1789363673\' automatically closed and moved to PASSED OUT state. Course End Date / Passing Out Date (2026-03-01) has passed as of 2026-09-14.', '2026-09-14 10:57:54'),
('c367c765-c451-4975-8831-02db4302a043', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-08-31 12:06:15'),
('c3b33c45-d21f-4e0b-ba7c-f85d5c3511ed', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-17 03:54:46'),
('c3bbef60-3e9f-46bb-9f90-52090e312eaa', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated ACCOMMODATION_BILLET report with parameters: []', '2026-09-17 03:52:33'),
('c555568f-38dd-4235-815b-fb648c209974', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-15 11:26:07'),
('c5c6e726-c0b4-4c6d-9977-179c294596c6', 'dc5d99d0-d369-4487-a9df-27b663200f83', NULL, 'User Management', 'PARADE_STATE_SUBMITTED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Submitted parade state for trade \'Computer Technician\' on 2026-09-17 to WO HFAI Fonseka. Records: 5', '2026-09-17 09:46:52'),
('c637ef39-22b3-4f88-848b-2b8bb842056a', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-17 04:01:39'),
('c7b945f6-c4ae-4d53-bc67-276cf2ca7b52', 'user-slaf-admin', NULL, 'User Management', 'BED_POSITION_VACATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Vacated bed position (Reason: Course Completed) previously held by trainee 50833', '2026-09-24 09:38:55'),
('c80c73f8-62d8-470c-af42-d8e73bec428c', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'32853\' logged in successfully', '2026-08-10 11:37:55'),
('c92604f3-6ab2-49d5-84ae-7305cbef336e', 'user-slaf-admin', NULL, 'User Management', 'PARADE_DRAFT_TRADE_SAVE', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Draft-saved parade state for trade \'Computer Technician\' — 5 students on 2026-08-12', '2026-08-12 04:36:15'),
('cb000748-9ac3-4d7a-b3b4-bdfb7a6a240b', 'f6f853a0-a3db-481e-bb6b-95e469c45dc8', NULL, 'Academic', 'LESSON_PLAN_ARCHIVED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Archived lesson plan \'Comp tech lesson plan\' (ID: 4c118c0b-c2e4-4aa6-97de-714cfc78f2ca)', '2026-08-12 04:26:56'),
('cb1a473c-41f6-4f69-bf93-da5ba84860b4', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-16 09:38:38'),
('cb2382fa-1d11-460b-9614-de3a3965f49b', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 11:55:01'),
('cbbefc2f-afb4-4fd0-ade1-cdc33f45ee21', 'user-slaf-admin', 'admin', 'User Management', 'USER_UPDATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Updated user account profile for \'51837\'', '2026-09-21 05:43:34'),
('cc078cf9-8e06-46ba-ae7f-d2073ecb5f0f', 'user-slaf-admin', '04253', 'User Management', 'USER_CREATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Created user username=\'04253\', full_name=\'Saman Kumara\', role_id=\'role-co\'', '2026-08-10 11:06:34'),
('cd4c1d70-5108-4cfd-98ab-95c89186727e', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated COURSE_CALENDAR report with parameters: [course=Basic Course Of Account Assistant]', '2026-09-17 03:53:44'),
('cef39e3b-4837-4e63-8187-21b4e54d6762', 'c96d5ee9-93ee-41cc-b9e6-f31ecba02f4e', '51837', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'51837\' logged out successfully', '2026-09-21 05:42:12'),
('cf156db2-85ca-4a5b-bfc5-6cb922ca70d5', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-09 11:23:09'),
('cf92b639-d1c1-47ea-bebd-734f28342b11', 'c96d5ee9-93ee-41cc-b9e6-f31ecba02f4e', '51837', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'51837\' logged in successfully', '2026-09-21 05:41:49'),
('cf9fc039-f04c-4d11-89c9-4ef2dadc46c9', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-17 12:22:33'),
('cfcdabf7-a4ea-4f3c-93b2-28bb3417124a', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated OCCURRENCES report with parameters: [occurrence_type=ALL]', '2026-09-17 03:52:35'),
('cffa827b-520f-4dff-80ed-5ecdc39ce7ad', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Generated ACCOMMODATION_BILLET report with parameters: [bunk_level=TOP]', '2026-08-31 09:50:21'),
('d079e052-bf01-4a31-90a1-5e674be372dd', 'c96d5ee9-93ee-41cc-b9e6-f31ecba02f4e', '51837', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'51837\' logged out successfully', '2026-09-21 05:41:53'),
('d0a501f3-8746-43d7-8f6c-f9512e445535', 'user-slaf-admin', NULL, 'Academic Management', 'DELETE_COURSE_CALENDAR_ENTRY', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Deleted calendar phase \'Theory Phase 01\' from course ID 860749a8-7b0e-4e22-b439-5f22b63e3db1', '2026-08-14 09:56:16'),
('d0a9a1c8-d28a-433a-a58c-e8dfc278ce88', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated ATTENDANCE_REGISTER report with parameters: []', '2026-09-17 03:52:32'),
('d0fa05c0-dcd7-4267-8791-451e6672e564', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-17 11:32:31'),
('d1094b36-b365-4f7c-b1fb-5d840d0b19a5', 'user-slaf-admin', NULL, 'User Management', 'NIGHT_PARADE_REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Generated Night Parade State Report for date: 2026-09-21, trade: All', '2026-09-21 10:20:04'),
('d13d6dcc-4ea5-410e-9aa5-de9e005ecdad', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 11:53:10'),
('d168d566-0e0f-4c86-af3a-ff5e81810ec4', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-16 11:22:41'),
('d18b35e9-fbab-4fb4-b09e-25c6c9d7cb71', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: []', '2026-09-21 05:20:17'),
('d30df787-3f70-45b1-aed4-fdab50eeafa7', 'user-slaf-admin', '32853', 'User Management', 'USER_CREATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Created user username=\'32853\', full_name=\'HFAI Fonseka\', role_id=\'role-instructor\'', '2026-08-10 11:23:21'),
('d3437819-5797-4b8a-a21a-cc7accfb72a4', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated PARADE_STATE report with parameters: [parade_date=2026-09-21]', '2026-09-21 05:02:25'),
('d370282f-64f7-4323-976d-7dc9aca0c9df', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-11 15:16:21'),
('d37d9c27-c082-403d-bf44-30217bbe68cb', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-17 03:54:32'),
('d3ef46c9-7254-4833-8d2d-4eab0be8f2bd', 'user-slaf-admin', NULL, 'User Management', 'EXAM_MARKS_UPDATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Entered/updated grades for exam ID 144be146-1c60-4caf-95ad-389c941978d0 for 5 trainees', '2026-09-17 10:10:50'),
('d3f205a1-0eac-445c-9a83-c78af302e14a', 'user-slaf-admin', NULL, 'User Management', 'BULK_BEDS_CREATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Bulk created 10 beds in billet \'Adavnce Admin\'', '2026-08-11 15:21:27'),
('d4513c1b-52f2-44ce-8313-6c64a7f5d09e', 'user-slaf-admin', NULL, 'Academic', 'LESSON_PLAN_UPLOADED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Uploaded lesson plan \'Comp tech lesson plan\' for course Comp Tech Adv (ID: 26/1)', '2026-08-11 11:34:03'),
('d4aa02dc-8088-4de5-9151-17945324018d', 'user-slaf-admin', NULL, 'User Management', 'NIGHT_PARADE_REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Generated Night Parade State Report for date: 2026-09-21, trade: All', '2026-09-21 11:41:27'),
('d4b2a4f1-852d-4700-86c5-f21036cea093', 'user-slaf-admin', NULL, 'User Management', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated Outstanding Parade State Report for date: 2026-09-21', '2026-09-21 05:33:54'),
('d54e765d-729c-4c73-8bd9-4be67bfde3ad', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 07:19:52'),
('d5a7bf5c-b954-4fb7-88d9-762209e7f7c4', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated PARADE_STATE report with parameters: [parade_date=2026-09-18]', '2026-09-18 11:04:19'),
('d5dc0850-4449-4810-94a6-74c859c236d4', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 07:28:12'),
('d646f486-e0c1-4dd4-87be-9dacf58588db', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-07 06:32:19'),
('d724c483-f2bd-4dc4-a900-9247601888fe', 'c96d5ee9-93ee-41cc-b9e6-f31ecba02f4e', '51837', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'51837\' logged out successfully', '2026-09-21 05:48:15'),
('d7630309-e440-4940-9d5b-065145096475', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-17 10:45:44'),
('d78dc536-b1d3-4a61-bebc-bc83f3edf822', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-17 10:13:43'),
('d7b21121-0173-47f4-a20f-a944531eded7', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated PARADE_STATE report with parameters: [parade_date=2026-09-17]', '2026-09-17 03:53:28'),
('d8051077-4f9d-4137-b38a-638f50de0316', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-09 10:02:31'),
('d83d9936-81f1-4915-b3ec-3b9edf837b55', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-10 11:07:06'),
('d87ffa41-41f3-4fc7-9918-552575fea947', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-10-05 11:59:25'),
('d8bdfee0-3da4-4258-8235-dcb49b3b1886', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated ACADEMIC_RESULTS report with parameters: [course=Comp Tech Adv, subject=Desktop Application Development, exam_type=Phase Test, exam_date=2026-09-16, result_status=ALL]', '2026-09-17 03:52:31'),
('d8c4a12a-44e1-418c-b7a6-3501a693049f', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged in successfully', '2026-09-17 10:26:51'),
('d92dfe15-0049-4b6f-956f-2d4d5a3a5c93', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-07 06:29:17'),
('da4e8fbc-2be4-42fa-b64b-66e782539fc2', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-18 09:32:52'),
('da7891c4-2665-4a1f-9b77-f91315732583', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated COURSE_CALENDAR report with parameters: [course=Basci Course Of Account Assistant]', '2026-09-09 11:19:58'),
('da8f6618-6755-4227-9509-e80755e49d33', 'user-slaf-admin', NULL, 'Academic Management', 'DELETE_COURSE_CALENDAR_ENTRY', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Deleted calendar phase \'Test entry\' from course ID 32d6af23-5645-4cf8-bc5a-1e6672c9b86b', '2026-08-14 09:54:55'),
('dae54601-e9bf-4d65-8fe5-a02e273769ed', 'dc5d99d0-d369-4487-a9df-27b663200f83', NULL, 'User Management', 'PARADE_STATE_APPROVED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Approved parade state submission 37682c5a-5e8b-473b-9f3e-1b70b5df5274 for trade \'Computer Technician\' on 2026-09-17', '2026-09-17 10:28:47'),
('dc72d188-1dfd-415c-aa24-c28e9f20afcd', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-07 06:41:42'),
('ddb6ea72-6aa3-4261-af32-46960f963037', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated PARADE_STATE report with parameters: [parade_date=2026-09-17]', '2026-09-17 03:52:31'),
('ddcf5ecd-3692-409f-a6bd-95c24168e71e', 'user-slaf-admin', NULL, 'Student Management', 'CREATE_PERSONAL_OCCURRENCE', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'Recorded MISCONDUCT_OFFENSE \'Absent\' on 26.10.2020 for trainee aw/4618 (Ranasinghe)', '2026-10-26 04:24:05');
INSERT INTO `audit_logs` (`id`, `user_id`, `username`, `module`, `action`, `previous_value`, `new_value`, `ip_address`, `user_agent`, `details`, `created_at`) VALUES
('dddeca1d-a62a-4b3d-862f-e571891b4381', 'user-slaf-admin', NULL, 'User Management', 'STUDENT_CREATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Created student record TA/40219 (HERATH)', '2026-09-10 11:35:05'),
('de8a2fcb-8153-40f3-a534-b7c9bb7a4d57', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-16 11:26:32'),
('df949b19-6e9b-4fc2-9131-ecfdc3b5e17f', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: [search=51098]', '2026-10-26 04:16:40'),
('dff93f2e-0bdf-4773-aca0-4e984ebffd1e', 'user-slaf-admin', NULL, 'User Management', 'PARADE_STATE_SUBMITTED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'Submitted parade state for trade \'Computer Technician\' on 2026-10-26 to WO HFAI Fonseka. Records: 7', '2026-10-26 04:48:29'),
('e0434449-ba54-4dbe-99e7-acbae062d4e0', 'user-slaf-admin', NULL, 'Academic Management', 'DELETE_COURSE_CALENDAR_ENTRY', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Deleted calendar phase \'Psychological Lecture\' from course ID 860749a8-7b0e-4e22-b439-5f22b63e3db1', '2026-08-14 09:56:26'),
('e0c1e0ab-a7dc-473a-9206-2773c3521733', 'user-slaf-admin', NULL, 'Academic', 'LESSON_PLAN_UPLOADED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Uploaded lesson plan \'Comp tech lesson plan\' for course Comp Tech Adv (ID: 26/1)', '2026-08-12 10:40:55'),
('e207b4f2-40c3-47de-bac6-9b2ed9d15b45', NULL, 'System Scheduler', 'Academic Management', 'AUTOMATIC_BATCH_CLOSURE', 'Status: Active', 'Status: PASSED OUT', '127.0.0.1', 'System Automated Batch Task', 'Batch \'Batch-TEST-EXP-1789362557\' automatically closed and moved to PASSED OUT state. Course End Date / Passing Out Date (2026-03-01) has passed as of 2026-09-14.', '2026-09-14 10:39:17'),
('e2d76c44-3f2f-4bee-bff6-2a940a70a519', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated ACCOMMODATION_BILLET report with parameters: []', '2026-09-17 03:53:42'),
('e36c46f0-31c4-42e5-bb1d-78760b2f02b6', 'user-slaf-admin', NULL, 'User Management', 'STUDENT_CREATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'Created student record 51098 (Kithmal)', '2026-10-26 04:16:20'),
('e5198994-e4e8-4b12-87b2-1172fb305405', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: []', '2026-09-21 11:55:57'),
('e5bb34de-93c8-47bb-8789-25f3d44a94bb', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-09 09:51:11'),
('e5f61191-cfa3-4982-9c21-d2b7cce47711', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-31 10:39:54'),
('e66f5a79-5e22-4d05-ba9d-8302b7b2b53d', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-10-26 04:32:18'),
('e7041fbb-0ada-41ce-aa20-d8b35f4baa0d', 'user-slaf-admin', NULL, 'User Management', 'EXAM_MARKS_UPDATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Entered/updated grades for exam ID 144be146-1c60-4caf-95ad-389c941978d0 for 5 trainees', '2026-09-17 09:48:42'),
('e70e3dab-211a-4c00-8b92-6f4f333036bb', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-10-26 04:36:45'),
('e8399ed9-9efd-48c1-86a6-1ca951ac3a4f', 'user-slaf-admin', NULL, 'Academic Management', 'DELETE_COURSE_CALENDAR_ENTRY', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Deleted calendar phase \'Parallel Course Phase\' from course ID 32d6af23-5645-4cf8-bc5a-1e6672c9b86b', '2026-08-14 09:54:51'),
('e84d2d5d-fc12-4f02-9b36-11e8213f19f2', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated PARADE_STATE report with parameters: [parade_date=2026-09-21, trade=Account Assistant]', '2026-09-21 05:33:40'),
('e8685f1d-0857-4f03-bf75-ee25cba804cf', 'user-slaf-admin', NULL, 'User Management', 'BULK_BUNKS_CREATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Bulk created 10 bunk beds in billet \'Adavnce Admin\'', '2026-08-12 05:41:10'),
('e8ef9a0c-4d25-4b41-9ab8-d6985c80f308', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Generated ATTENDANCE_REGISTER report with parameters: [date_range=2026-08-24 to 2026-08-24]', '2026-08-24 11:43:59'),
('e9de3c45-3895-4de1-9ca9-434e69aef007', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated COURSE_CALENDAR report with parameters: [course=Basic Course Of Account Assistant]', '2026-09-17 03:53:30'),
('ea3321cc-80d3-4ca6-9d68-41adfef0c314', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-17 04:01:44'),
('eb2507f2-4803-460d-b868-97426ea27f5b', 'user-slaf-admin', NULL, 'User Management', 'STUDENT_CREATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Created student record TA/40217 (Chinthaka)', '2026-09-09 10:22:08'),
('eb7d661f-7f71-4944-a689-1fe11d1ff373', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 11:52:48'),
('ec19423b-5db1-4b8b-bcea-fdadd9c1a4fb', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated COURSE_CALENDAR report with parameters: [course=Basci Course Of Account Assistant]', '2026-09-09 11:19:58'),
('ec4bce4a-5921-4eef-8829-bdd02347a4d4', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-21 06:50:24'),
('eca7c8dc-c350-4e5f-89c1-e7b7155b20b5', 'user-slaf-admin', NULL, 'Academic Management', 'CREATE_COURSE_CALENDAR_ENTRY', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Added calendar phase \'Networking\' (S/No: 1, Instructor Status: ASSIGNED) for course \'174 A  Comp Tech Basic Course\'', '2026-08-14 10:13:45'),
('ecf4dcc6-c0fc-4dd8-9b52-20433de53275', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-10 11:21:22'),
('ed9deb29-ddd4-4abb-be67-264d751b64f7', 'c96d5ee9-93ee-41cc-b9e6-f31ecba02f4e', '51837', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'51837\' logged in successfully', '2026-09-21 05:42:09'),
('edc6dfa9-398f-4b7f-a16f-64a1fa1ac1cb', 'user-slaf-admin', NULL, 'Student Management', 'DELETE_PERSONAL_OCCURRENCE', NULL, NULL, 'testclient', 'testclient', 'Soft-deleted ACHIEVEMENT record \'Test REST Endpoint Occurrence\' (ID 0c6d823b-67af-43b7-b9f7-3f8bd208a4f7) for trainee 50833', '2026-09-15 11:20:47'),
('ef16a222-82cb-4145-b1de-560772b3351a', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-08-10 10:03:37'),
('ef3287eb-0458-4d1d-aa7b-e87630fcb10f', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 06:50:11'),
('f0d39288-2c06-42e3-a8e8-c8302d6385ae', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-16 11:23:09'),
('f146dd2f-f0b6-4ff4-b8e4-370a9d3caf13', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-10-26 03:52:58'),
('f197d036-6ea2-404a-a2c7-734c3c387f6f', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated PARADE_STATE report with parameters: [parade_date=2026-09-21]', '2026-09-21 05:02:03'),
('f24297e4-bb21-4be7-adb8-d22875f13a9a', 'user-slaf-admin', NULL, 'User Management', 'NIGHT_PARADE_COMPLETED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Completed Night Parade Roll Call for trade \'All\' on 2026-09-21 by SLAF Administrator. Expected: 31, Accounted: 31, Changed: 2. Status Changes: 7c03548a-fe20-40b5-9ac0-6f1ee3d1a886: Present -> Sick Report; 49599a29-88c3-4e4f-bad3-ef2d05785b27: Present -> Leave', '2026-09-21 11:42:32'),
('f244fab7-fb0e-4bcb-88fe-c6625b6df893', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: []', '2026-09-21 11:55:01'),
('f27abc8a-0bd7-4ca9-9c8d-623abf0eca38', 'user-slaf-admin', NULL, 'User Management', 'BED_ALLOCATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Allocated bed Bed 5 to trainee 50833 in Billet Adavnce Admin', '2026-08-11 15:22:46'),
('f3479a25-316c-4019-b8c0-1e71651fa2b8', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-09 10:31:03'),
('f3efdfb3-eacd-408f-b3e1-cc91faf6eba7', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged out successfully', '2026-09-21 05:38:25'),
('f3f82f50-24d3-4c4b-87cd-28b190e08854', 'user-slaf-admin', NULL, 'Academic', 'LESSON_PLAN_UPLOADED', NULL, NULL, 'testclient', 'testclient', 'Uploaded lesson plan \'Test Lesson Plan Document\' for course Basic Airframe Mechanics Course (ID: BA-AER-01)', '2026-08-11 11:32:30'),
('f54da6ef-9228-4856-877c-7615736eaced', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-10 11:42:09'),
('f55cb0bf-b665-4707-9343-6cae53e4f425', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', 'Generated ACADEMIC_RESULTS report with parameters: [course=Comp Tech Adv, subject=Desktop Application Development, exam_type=Final Exam, exam_date=2026-08-24, result_status=ALL]', '2026-08-31 09:49:46'),
('f6f74543-f666-417d-a90e-2372d34cf6d2', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'Generated STUDENT_DOSSIER report with parameters: [course_id=631f5810-ac42-4f45-954f-5c886f4ce601]', '2026-09-17 03:51:07'),
('f785c92a-2b4e-43fb-aec3-4eb72add8368', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-07 06:41:55'),
('f814df1e-a94b-4452-8032-56e9e41385ab', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'32853\' logged in successfully', '2026-09-21 05:38:10'),
('f8cf384c-94fa-462a-94a5-b127a57469b0', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-18 09:27:52'),
('f9dcc4a7-368b-48b0-a4f1-5d07aea729fa', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-09-07 06:32:38'),
('fb2f187f-915c-4e4b-be06-8b5bdfc991c5', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 11:53:44'),
('fbf0b316-3d19-436f-bece-c75e22aa69df', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGIN', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', 'User \'admin\' logged in successfully', '2026-10-26 04:47:24'),
('fcf72838-3e38-4a08-9239-56860eec1824', 'user-slaf-admin', NULL, 'Enterprise Reports', 'REPORT_GENERATED', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'Generated ACADEMIC_RESULTS report with parameters: [course=Comp Tech Adv, subject=Desktop Application Development, exam_type=Phase Test, exam_date=2026-09-16, result_status=ALL]', '2026-09-21 11:55:06'),
('fd0e023a-dbea-48c2-9074-3f8d3506dd62', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-16 11:22:59'),
('ffe61ce5-5139-45d7-ae6a-3e04ef7c1fa2', 'user-slaf-admin', 'admin', 'Authentication', 'USER_LOGOUT', NULL, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', 'User \'admin\' logged out successfully', '2026-09-21 09:50:01');

-- --------------------------------------------------------

--
-- Table structure for table `batches`
--

CREATE TABLE `batches` (
  `id` varchar(36) NOT NULL,
  `name` varchar(100) NOT NULL,
  `course_id` varchar(36) NOT NULL,
  `trade_id` varchar(36) DEFAULT NULL,
  `intake_date` date DEFAULT NULL,
  `passing_out_date` date DEFAULT NULL,
  `capacity` int(11) DEFAULT NULL,
  `classroom_id` varchar(36) DEFAULT NULL,
  `instructor_id` varchar(36) DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `batches`
--

INSERT INTO `batches` (`id`, `name`, `course_id`, `trade_id`, `intake_date`, `passing_out_date`, `capacity`, `classroom_id`, `instructor_id`, `status`, `created_at`, `updated_at`, `deleted_at`) VALUES
('07ad7d67-76d5-4549-92f3-e51c1d1990e5', 'Batch-TEST-EXP-1789362557', '8116f096-d83b-4000-9308-6b6b7ddf7e05', 'b260e0d3-c8f9-4857-aad2-e05b9b5a6257', '2026-01-01', '2026-03-01', 30, NULL, NULL, 'PASSED OUT', '2026-09-14 10:39:17', '2026-09-14 10:39:17', NULL),
('0c2acb5d-22aa-434d-bfbd-7d4c6c54a0ac', '2026/01', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '5d312046-1f95-4bbd-adbe-cda9e70c44bd', '2026-08-10', '2027-07-01', 30, '4f39d1ac-8bae-4ad5-be4a-49afdd935582', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'Active', '2026-08-10 11:40:21', '2026-08-10 11:40:21', NULL),
('1438d32b-8ef0-4a77-ac87-c8826b4a4ec0', 'Batch-TEST-EXP-1789363673', '631f5810-ac42-4f45-954f-5c886f4ce601', 'b260e0d3-c8f9-4857-aad2-e05b9b5a6257', '2026-01-01', '2026-03-01', 30, NULL, NULL, 'PASSED OUT', '2026-09-14 10:57:54', '2026-09-14 10:57:54', NULL),
('1fe27631-6323-47cd-ba73-55a71e6887c6', 'Basic 174', 'ca0ae649-cffd-4712-b156-8209ffd159d4', '5d312046-1f95-4bbd-adbe-cda9e70c44bd', '2026-08-11', '2027-06-11', 30, '4f39d1ac-8bae-4ad5-be4a-49afdd935582', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'Active', '2026-08-11 15:27:57', '2026-08-11 15:27:57', NULL),
('a3574ff6-0830-4646-b146-e6823f9d0c9e', '2/2026', '0b7a2bcf-5ac0-4590-a777-05febce54289', '26b9799b-914a-4414-8ae4-3be16e56c74e', '2026-05-27', '2026-12-18', 4, '8814d345-d2d1-4666-9133-81b1386ae396', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'Active', '2026-09-09 09:56:55', '2026-09-09 09:56:55', NULL),
('aeb2898e-ffef-4ae1-9cca-037e6d180965', 'Batch-TEST-EXP-1789362528', '9ef4c9a9-ad44-49d0-a514-b3c533af66d1', 'b260e0d3-c8f9-4857-aad2-e05b9b5a6257', '2026-01-01', '2026-03-01', 30, NULL, NULL, 'PASSED OUT', '2026-09-14 10:38:48', '2026-09-14 10:38:49', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `classrooms`
--

CREATE TABLE `classrooms` (
  `id` varchar(36) NOT NULL,
  `code` varchar(50) NOT NULL,
  `name` varchar(150) NOT NULL,
  `block` varchar(100) DEFAULT NULL,
  `building` varchar(100) DEFAULT NULL,
  `capacity` int(11) NOT NULL,
  `description` text DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `classrooms`
--

INSERT INTO `classrooms` (`id`, `code`, `name`, `block`, `building`, `capacity`, `description`, `is_active`, `created_at`, `updated_at`, `deleted_at`) VALUES
('4f39d1ac-8bae-4ad5-be4a-49afdd935582', 'H-05', 'H-05', 'H Block', 'Main Complex', 30, '', 0, '2026-08-10 11:39:04', '2026-08-14 11:41:53', NULL),
('8814d345-d2d1-4666-9133-81b1386ae396', 'E-18', 'E-18', 'Block E', '', 30, '', 1, '2026-09-09 09:55:29', '2026-09-17 10:48:12', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

CREATE TABLE `courses` (
  `id` varchar(36) NOT NULL,
  `code` varchar(30) NOT NULL,
  `name` varchar(150) NOT NULL,
  `trade_id` varchar(36) DEFAULT NULL,
  `course_type` varchar(50) DEFAULT NULL,
  `duration_weeks` int(11) NOT NULL,
  `intake_capacity` int(11) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `description` text DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `status` varchar(30) DEFAULT 'ONGOING'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`id`, `code`, `name`, `trade_id`, `course_type`, `duration_weeks`, `intake_capacity`, `start_date`, `end_date`, `description`, `is_active`, `created_at`, `updated_at`, `deleted_at`, `status`) VALUES
('0b7a2bcf-5ac0-4590-a777-05febce54289', '2/2026', 'Basic Course Of Account Assistant', '26b9799b-914a-4414-8ae4-3be16e56c74e', 'Basic', 20, 4, NULL, NULL, NULL, 1, '2026-09-09 09:54:06', '2026-09-09 09:54:06', NULL, 'ONGOING'),
('544f0ae2-2ee5-403b-84cf-58ac0aa193af', '26/1', 'Comp Tech Adv', '5d312046-1f95-4bbd-adbe-cda9e70c44bd', 'Advance', 40, 19, NULL, NULL, 'Comtech advnce', 1, '2026-08-10 10:35:50', '2026-08-10 10:35:50', NULL, 'ONGOING'),
('6221dc9c-4875-416a-8ef8-fae1119f2d08', '26/2', 'Telephone Operator', '04748ef0-2827-4f70-915b-2c07078074fc', 'Advance', 10, 15, '2026-10-28', '2026-12-30', NULL, 1, '2026-10-26 04:29:39', '2026-10-26 04:29:39', NULL, 'UPCOMING'),
('631f5810-ac42-4f45-954f-5c886f4ce601', 'TEST-EXP-1789363673', 'Test Expired Course Aircraft Assist', 'b260e0d3-c8f9-4857-aad2-e05b9b5a6257', 'Basic', 48, 30, '2026-01-01', '2026-12-01', NULL, 0, '2026-09-14 10:57:54', '2026-09-14 10:59:57', NULL, 'ONGOING'),
('8116f096-d83b-4000-9308-6b6b7ddf7e05', 'TEST-EXP-1789362557', 'Test Expired Course Aircraft Assist', 'b260e0d3-c8f9-4857-aad2-e05b9b5a6257', 'Basic', 8, 30, '2026-01-01', '2026-03-01', NULL, 0, '2026-09-14 10:39:17', '2026-09-14 10:39:17', NULL, 'PASSED OUT'),
('9ef4c9a9-ad44-49d0-a514-b3c533af66d1', 'TEST-EXP-1789362528', 'Test Expired Course Aircraft Assist', 'b260e0d3-c8f9-4857-aad2-e05b9b5a6257', 'Basic', 8, 30, '2026-01-01', '2026-03-01', NULL, 0, '2026-09-14 10:38:48', '2026-09-14 10:38:49', NULL, 'PASSED OUT'),
('ca0ae649-cffd-4712-b156-8209ffd159d4', '174 A ', '174 A  Comp Tech Basic Course', '5d312046-1f95-4bbd-adbe-cda9e70c44bd', 'Basic', 39, 30, NULL, NULL, NULL, 1, '2026-08-11 15:26:49', '2026-08-11 15:26:49', NULL, 'ONGOING'),
('course-basic-admin', 'BA-ADM-01', 'Basic Administrative Assistant Course', 'trade-admin', 'Basic', 16, 30, NULL, NULL, NULL, 1, '2026-08-20 10:24:11', '2026-08-20 10:24:11', NULL, 'ONGOING'),
('course-basic-airframe', 'BA-AER-01', 'Basic Airframe Mechanics Course', 'trade-airframe', 'Basic', 24, 30, NULL, NULL, 'Introductory training program for SLAF airframe technicians on structural integrity and aircraft maintenance.', 1, '2026-08-10 09:31:20', '2026-08-20 10:23:08', NULL, 'ONGOING'),
('course-basic-avionics', 'BA-AV-01', 'Basic Avionics Maintenance Course', 'trade-avionics', 'Basic', 24, 30, NULL, NULL, 'Fundamental course in aircraft electrical systems, radar instruments, and communications navigation.', 1, '2026-08-10 09:31:20', '2026-08-20 10:23:08', NULL, 'ONGOING'),
('course-basic-engine', 'BA-ENG-01', 'Basic Aero Engine Mechanics Course', 'trade-engine', 'Basic', 24, 30, NULL, NULL, NULL, 1, '2026-08-20 10:24:11', '2026-08-20 10:24:11', NULL, 'ONGOING'),
('course-basic-logistics', 'BA-LOG-01', 'Basic Logistics Management Course', 'trade-logistical', 'Basic', 20, 30, NULL, NULL, NULL, 1, '2026-08-20 10:24:11', '2026-08-20 10:24:11', NULL, 'ONGOING'),
('course-basic-opair', 'BA-OP-01', 'Air Operations Basic Course', '5c162d3f-e913-4568-8372-844975e54bff', 'Basic', 20, 30, NULL, NULL, NULL, 1, '2026-08-20 10:24:11', '2026-08-20 10:24:11', NULL, 'ONGOING'),
('course-basic-safety', 'BA-SE-01', 'Basic Safety Equipment Fitters Course', 'trade-safety', 'Basic', 16, 30, NULL, NULL, 'Instruction in parachute systems, life preservation equipment, and survival tactics.', 1, '2026-08-10 09:31:20', '2026-08-20 10:23:08', NULL, 'ONGOING');

-- --------------------------------------------------------

--
-- Table structure for table `course_calendar`
--

CREATE TABLE `course_calendar` (
  `id` varchar(36) NOT NULL,
  `course_id` varchar(36) NOT NULL,
  `serial_number` int(11) NOT NULL,
  `phase_name` varchar(255) NOT NULL,
  `theory_periods` int(11) DEFAULT 0,
  `practical_periods` int(11) DEFAULT 0,
  `total_periods` int(11) DEFAULT 0,
  `working_days` int(11) DEFAULT 0,
  `commencement_date` date NOT NULL,
  `completion_date` date NOT NULL,
  `instructor_id` varchar(36) DEFAULT NULL,
  `remarks` text DEFAULT NULL,
  `status` varchar(30) DEFAULT 'Active',
  `created_by` varchar(36) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `instructor_status` varchar(30) DEFAULT 'NOT_ASSIGNED',
  `subject_id` varchar(36) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `course_calendar`
--

INSERT INTO `course_calendar` (`id`, `course_id`, `serial_number`, `phase_name`, `theory_periods`, `practical_periods`, `total_periods`, `working_days`, `commencement_date`, `completion_date`, `instructor_id`, `remarks`, `status`, `created_by`, `created_at`, `updated_at`, `instructor_status`, `subject_id`) VALUES
('08b1af36-32af-40be-8148-c456832a88a1', '0b7a2bcf-5ac0-4590-a777-05febce54289', 3, '[15] Introdution of Accounting & Basic Concepts', 9, 3, 12, 0, '2026-09-25', '2026-09-30', NULL, 'WO Sampath', 'Active', 'dc5d99d0-d369-4487-a9df-27b663200f83', '2026-09-17 10:45:21', '2026-09-17 10:45:21', 'NOT_ASSIGNED', '90d50500-01db-4003-8299-ad1817ec00b0'),
('19a94041-c2e8-40fc-9474-9171b7a50afe', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', 2, '[DBMS] Data Base Management System', 5, 5, 10, 5, '2026-08-17', '2026-08-22', 'ac814c9f-08ef-476f-8de4-15192d2e7f71', NULL, 'Active', 'user-slaf-admin', '2026-08-17 10:55:23', '2026-08-17 10:55:23', 'ASSIGNED', 'ebc66534-457f-430e-bb3b-4a2747015e8c'),
('1c84b33b-c50e-4058-848e-2f7e765bd8c7', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', 1, 'Database Managemet System', 2, 2, 4, 2, '2026-08-15', '2026-08-16', 'f6f853a0-a3db-481e-bb6b-95e469c45dc8', NULL, 'Active', 'user-slaf-admin', '2026-08-14 10:11:50', '2026-08-14 10:11:50', 'ASSIGNED', NULL),
('59a05b8d-0255-4ec0-b99a-f7595cc6594a', '0b7a2bcf-5ac0-4590-a777-05febce54289', 2, '[18] Gagana Viru Sawiya Walfare Scheme', 6, 0, 6, 0, '2026-09-24', '2026-09-24', 'dc5d99d0-d369-4487-a9df-27b663200f83', NULL, 'Active', 'dc5d99d0-d369-4487-a9df-27b663200f83', '2026-09-17 10:40:31', '2026-09-17 10:40:31', 'ASSIGNED', '805b4507-676a-426c-a1eb-5a94e8ddf14d'),
('6a57ef6a-e501-4609-b92c-a1e90cf2a86a', '0b7a2bcf-5ac0-4590-a777-05febce54289', 1, '[17] SLAF non Public Accounts Procedures', 36, 0, 36, 0, '2026-09-16', '2026-09-23', 'dc5d99d0-d369-4487-a9df-27b663200f83', NULL, 'Active', 'dc5d99d0-d369-4487-a9df-27b663200f83', '2026-09-17 10:39:31', '2026-09-17 10:39:31', 'ASSIGNED', '68a7987d-6be2-4980-8829-8a23f85309b2'),
('dab024b8-9cd6-4f15-b7e9-e2caf377b90a', 'ca0ae649-cffd-4712-b156-8209ffd159d4', 1, 'Networking', 2, 2, 4, 2, '2026-08-15', '2026-08-16', 'ac814c9f-08ef-476f-8de4-15192d2e7f71', NULL, 'Active', 'user-slaf-admin', '2026-08-14 10:13:45', '2026-08-14 10:13:45', 'ASSIGNED', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `exams`
--

CREATE TABLE `exams` (
  `id` varchar(36) NOT NULL,
  `course_id` varchar(36) NOT NULL,
  `subject_id` varchar(36) NOT NULL,
  `type` varchar(30) NOT NULL,
  `date` date NOT NULL,
  `max_marks` double DEFAULT NULL,
  `pass_marks` double DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `exams`
--

INSERT INTO `exams` (`id`, `course_id`, `subject_id`, `type`, `date`, `max_marks`, `pass_marks`, `created_at`, `updated_at`, `deleted_at`) VALUES
('0c12c704-245d-4fdd-b14c-1d6ce8404874', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', 'fafb3737-e8b6-4270-b01d-912335afc118', 'Final Exam', '2026-08-24', 100, 50, '2026-08-24 10:30:47', '2026-08-24 10:30:47', NULL),
('144be146-1c60-4caf-95ad-389c941978d0', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', 'fafb3737-e8b6-4270-b01d-912335afc118', 'Phase Test', '2026-09-16', 100, 50, '2026-09-16 11:28:26', '2026-09-16 11:28:26', NULL),
('33d73d9e-0ee9-430a-a308-5a42747aefbf', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '294a13c2-da21-4208-b925-23af2b0fb371', 'Final Exam', '2026-08-17', 100, 40, '2026-08-17 12:12:49', '2026-08-17 12:12:49', NULL),
('a8665362-dfe8-48e7-8168-f7834b44cee1', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', 'ebc66534-457f-430e-bb3b-4a2747015e8c', 'Phase Test', '2026-08-17', 100, 50, '2026-08-17 11:22:49', '2026-08-17 11:22:49', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `exam_marks`
--

CREATE TABLE `exam_marks` (
  `id` varchar(36) NOT NULL,
  `exam_id` varchar(36) NOT NULL,
  `student_id` varchar(36) NOT NULL,
  `marks_obtained` double NOT NULL,
  `status` varchar(20) NOT NULL,
  `remarks` text DEFAULT NULL,
  `entered_by` varchar(36) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_overridden` tinyint(1) DEFAULT 0,
  `override_reason` text DEFAULT NULL,
  `overridden_by` varchar(36) DEFAULT NULL,
  `overridden_at` datetime DEFAULT NULL,
  `original_parade_status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `exam_marks`
--

INSERT INTO `exam_marks` (`id`, `exam_id`, `student_id`, `marks_obtained`, `status`, `remarks`, `entered_by`, `created_at`, `updated_at`, `is_overridden`, `override_reason`, `overridden_by`, `overridden_at`, `original_parade_status`) VALUES
('0090c2ec-4d61-4f37-88cf-7a9fb2d2a85a', '33d73d9e-0ee9-430a-a308-5a42747aefbf', 'd0fca849-4bf5-4c56-be89-38a21d42a187', 89, 'Pass', '', 'user-slaf-admin', '2026-08-17 12:14:08', '2026-08-17 12:14:08', 0, NULL, NULL, NULL, NULL),
('065bfbe8-953f-415e-b3cf-602fe2957faf', 'a8665362-dfe8-48e7-8168-f7834b44cee1', 'd0fca849-4bf5-4c56-be89-38a21d42a187', 23, 'Fail', '', 'user-slaf-admin', '2026-08-17 12:06:27', '2026-08-17 12:06:27', 0, NULL, NULL, NULL, NULL),
('0fd77740-a150-493e-bc21-8f085eaaddaf', 'a8665362-dfe8-48e7-8168-f7834b44cee1', '49599a29-88c3-4e4f-bad3-ef2d05785b27', 89, 'Pass', '', 'user-slaf-admin', '2026-08-17 12:06:27', '2026-08-17 12:06:27', 0, NULL, NULL, NULL, NULL),
('3a3142cf-a00b-41f2-a468-598a65fd5ec7', '144be146-1c60-4caf-95ad-389c941978d0', '49599a29-88c3-4e4f-bad3-ef2d05785b27', 50, 'Pass', '', 'user-slaf-admin', '2026-09-17 03:56:16', '2026-09-17 03:56:16', 0, NULL, NULL, NULL, NULL),
('4528b3d4-20dd-4244-a61e-adae0a0a947d', '33d73d9e-0ee9-430a-a308-5a42747aefbf', 'e1650c87-f565-471c-85e8-a157df7dc81b', 83, 'Pass', '', 'user-slaf-admin', '2026-08-17 12:14:08', '2026-08-17 12:14:08', 0, NULL, NULL, NULL, NULL),
('47ed90f8-09fc-47d8-b519-6673523c69d6', '144be146-1c60-4caf-95ad-389c941978d0', '3b0e40ad-cfbf-4df7-804d-2c686c40ad2f', 75, 'Pass', '', 'user-slaf-admin', '2026-09-17 03:56:16', '2026-09-17 10:10:50', 0, NULL, NULL, NULL, NULL),
('67db2331-2bfb-42d9-a87c-e2436c01a35b', '144be146-1c60-4caf-95ad-389c941978d0', 'd0fca849-4bf5-4c56-be89-38a21d42a187', 50, 'Pass', '', 'user-slaf-admin', '2026-09-17 03:56:16', '2026-09-17 03:56:16', 0, NULL, NULL, NULL, NULL),
('735febc6-f634-44cf-8a90-3f520af80bc1', 'a8665362-dfe8-48e7-8168-f7834b44cee1', 'e59d3871-3fa2-44db-bcb0-068ba53fe6e1', 10, 'Fail', '', 'user-slaf-admin', '2026-08-17 12:06:27', '2026-08-17 12:06:27', 0, NULL, NULL, NULL, NULL),
('7fb2877b-9854-463f-886a-4a9a3cc3ceab', '33d73d9e-0ee9-430a-a308-5a42747aefbf', 'e59d3871-3fa2-44db-bcb0-068ba53fe6e1', 85, 'Pass', '', 'user-slaf-admin', '2026-08-17 12:14:08', '2026-08-17 12:14:08', 0, NULL, NULL, NULL, NULL),
('94a16749-2894-4ba3-97f2-d9bc0b6ba627', '33d73d9e-0ee9-430a-a308-5a42747aefbf', '49599a29-88c3-4e4f-bad3-ef2d05785b27', 39, 'Fail', '', 'user-slaf-admin', '2026-08-17 12:14:08', '2026-08-17 12:14:08', 0, NULL, NULL, NULL, NULL),
('a2b6f1b8-8627-46d9-a7c7-2a5b853fa4fc', '144be146-1c60-4caf-95ad-389c941978d0', 'e1650c87-f565-471c-85e8-a157df7dc81b', 84, 'Pass', '', 'user-slaf-admin', '2026-09-17 03:56:16', '2026-09-17 03:56:16', 0, NULL, NULL, NULL, NULL),
('a614dc0d-08c6-42aa-acec-6e9f0682f277', 'a8665362-dfe8-48e7-8168-f7834b44cee1', '3b0e40ad-cfbf-4df7-804d-2c686c40ad2f', 65, 'Pass', '', 'user-slaf-admin', '2026-08-17 12:06:27', '2026-08-17 12:06:27', 0, NULL, NULL, NULL, NULL),
('c8f42d8f-2242-4bf0-8807-ade8de1d8a40', '144be146-1c60-4caf-95ad-389c941978d0', 'e59d3871-3fa2-44db-bcb0-068ba53fe6e1', 50, 'Pass', '', 'user-slaf-admin', '2026-09-17 03:56:16', '2026-09-17 03:56:16', 0, NULL, NULL, NULL, NULL),
('f033d680-038a-4f42-9a2b-361eac7d9fe0', '33d73d9e-0ee9-430a-a308-5a42747aefbf', '3b0e40ad-cfbf-4df7-804d-2c686c40ad2f', 52, 'Pass', '', 'user-slaf-admin', '2026-08-17 12:14:08', '2026-08-17 12:14:08', 0, NULL, NULL, NULL, NULL),
('f4f69682-9a48-4f5d-b1f5-501b5475ede4', 'a8665362-dfe8-48e7-8168-f7834b44cee1', 'e1650c87-f565-471c-85e8-a157df7dc81b', 84.5, 'Pass', '', 'user-slaf-admin', '2026-08-17 12:06:27', '2026-09-17 09:49:28', 0, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `lessons`
--

CREATE TABLE `lessons` (
  `id` varchar(36) NOT NULL,
  `subject_id` varchar(36) NOT NULL,
  `name` varchar(150) NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `lessons`
--

INSERT INTO `lessons` (`id`, `subject_id`, `name`, `description`, `created_at`, `updated_at`) VALUES
('04673170-69a7-4a12-8679-7184c9e6294c', 'ebc66534-457f-430e-bb3b-4a2747015e8c', 'Module Lesson 03: Data Base Management System', 'Core theory and trade practical application', '2026-08-17 11:30:13', '2026-08-17 11:30:13'),
('21464371-1c1d-44c3-a81c-7ea70dcb9222', '20b7a2c2-d14f-4d8c-94d5-34b2a89def3a', 'Module Lesson 04: Public Account', 'Core theory and trade practical application', '2026-09-11 09:26:02', '2026-09-11 09:26:02'),
('2b4e2908-405e-47d0-bed0-f6337cab72a3', '005b5e66-2fa6-4568-88c9-13cc8817326c', 'Module Lesson 01: SLAF Non Public Funds', 'Core theory and trade practical application', '2026-09-11 09:26:02', '2026-09-11 09:26:02'),
('5b9ccd5c-9532-4d7b-84be-5ce5cac633ab', '3ffa680a-7a95-4520-9712-979cc000e392', 'Module Lesson 01: Basic Administrative Assistant Course Core Modules', 'Core theory and trade practical application', '2026-09-17 10:49:16', '2026-09-17 10:49:16'),
('5da752f1-0dd1-461a-a310-35bc05031e59', '736ebc24-5a3d-44b2-9012-39e71ac9b333', 'Module Lesson 02: Mobile Application Development', 'Core theory and trade practical application', '2026-08-17 11:30:13', '2026-08-17 11:30:13'),
('5db47a16-e3a7-46c9-a9df-96e0d61f7bff', '12517d10-edbd-4ee9-96de-4b4d0f6f1a46', 'Module Lesson 02: Bank Accounts public Imprests', 'Core theory and trade practical application', '2026-09-11 09:26:02', '2026-09-11 09:26:02'),
('98e1933c-53d1-4a2d-8560-20d0222631fe', 'fafb3737-e8b6-4270-b01d-912335afc118', 'Module Lesson 04: Desktop Application Development', 'Core theory and trade practical application', '2026-08-17 11:30:13', '2026-08-17 11:30:13'),
('bac287ab-d947-4c0d-851f-d77003831682', '294a13c2-da21-4208-b925-23af2b0fb371', 'Agile Method', 'SDLC', '2026-08-12 10:27:23', '2026-08-12 10:27:23'),
('e7d7cd40-510f-4aac-b2ee-0ebf305424b6', '159f77c9-e545-46eb-bca6-49503136353c', 'Module Lesson 03: Public Imprests', 'Core theory and trade practical application', '2026-09-11 09:26:02', '2026-09-11 09:26:02');

-- --------------------------------------------------------

--
-- Table structure for table `lesson_plans`
--

CREATE TABLE `lesson_plans` (
  `id` varchar(36) NOT NULL,
  `lesson_id` varchar(36) NOT NULL,
  `instructor_id` varchar(36) NOT NULL,
  `duration_minutes` int(11) DEFAULT NULL,
  `objectives` text DEFAULT NULL,
  `training_aids` text DEFAULT NULL,
  `references_used` text DEFAULT NULL,
  `plan_doc_path` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `lesson_plan_documents`
--

CREATE TABLE `lesson_plan_documents` (
  `id` varchar(36) NOT NULL,
  `course_id` varchar(36) NOT NULL,
  `lesson_id` varchar(36) DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `subject_name` varchar(150) DEFAULT NULL,
  `version` varchar(20) DEFAULT NULL,
  `academic_year` varchar(20) DEFAULT NULL,
  `remarks` text DEFAULT NULL,
  `original_file_name` varchar(255) NOT NULL,
  `cloudinary_public_id` varchar(255) NOT NULL,
  `cloudinary_url` varchar(500) NOT NULL,
  `resource_type` varchar(30) DEFAULT NULL,
  `file_size` int(11) NOT NULL,
  `mime_type` varchar(50) DEFAULT NULL,
  `uploaded_by` varchar(36) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `uploaded_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `lesson_plan_documents`
--

INSERT INTO `lesson_plan_documents` (`id`, `course_id`, `lesson_id`, `title`, `description`, `subject_name`, `version`, `academic_year`, `remarks`, `original_file_name`, `cloudinary_public_id`, `cloudinary_url`, `resource_type`, `file_size`, `mime_type`, `uploaded_by`, `status`, `uploaded_at`, `updated_at`) VALUES
('127521ef-7dda-4844-a4f8-8cdcec622b21', '0b7a2bcf-5ac0-4590-a777-05febce54289', NULL, 'Introduction to accounting concepts', 'ZXcvbnm.,.', 'lesson plan', '1.0', '2026', 'Zxcvbnghmj,kl;', 'Acct 14- 03 SLAF Non Public Accounting Procedure.pdf', 'tts-lesson-plans/Acct 14- 03 SLAF Non Public Accounting Procedure_20260918104147', 'https://res.cloudinary.com/wtc5iadz/raw/upload/v1789728112/tts-lesson-plans/Acct%2014-%2003%20SLAF%20Non%20Public%20Accounting%20Procedure_20260918104147', 'raw', 187410, 'application/pdf', 'user-slaf-admin', 'Active', '2026-09-18 10:41:51', '2026-09-18 10:41:51'),
('33151dfc-ed8c-4c1c-a711-f14fd14d7f41', '0b7a2bcf-5ac0-4590-a777-05febce54289', NULL, 'Introduction to accounting concepts', '4t4hythj', 'lesson plan', '1.0', '2026', 'Introduction to accounting concepts', 'Acct 12- 01  Introduction of Accounting & Concepts (1).pdf', 'local_lp_Acct 12- 01  Introduction of Accounting & Concepts (1)_20260918103818.pdf', '/static/uploads/lesson_plans/Acct 12- 01  Introduction of Accounting & Concepts (1)_20260918103818.pdf', 'raw', 185195, 'application/pdf', 'user-slaf-admin', 'Active', '2026-09-18 10:38:18', '2026-09-18 10:38:18'),
('34333541-a464-43be-84f0-c38c26e59d81', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', NULL, 'Comp tech lesson plan', 'test', 'lesson plan', '1.0', '2026', 'testing', 'Sanka  Adikaram - 2024-06-05.pdf', 'tts-lesson-plans/Sanka  Adikaram - 2024-06-05_20260812103628', 'https://res.cloudinary.com/wtc5iadz/image/upload/v1786530991/tts-lesson-plans/Sanka%20%20Adikaram%20-%202024-06-05_20260812103628.pdf', 'raw', 89231, 'application/pdf', 'user-slaf-admin', 'Archived', '2026-08-12 10:36:31', '2026-08-12 10:37:42'),
('46a93fac-6987-44be-8189-bd39fddb701a', 'course-basic-airframe', NULL, 'Test Lesson Plan Document', NULL, NULL, NULL, NULL, NULL, 'test_plan.pdf', 'tts-lesson-plans/test_plan_20260811113228', 'https://res.cloudinary.com/wtc5iadz/raw/upload/v1786447950/tts-lesson-plans/test_plan_20260811113228', 'raw', 44, 'application/pdf', 'user-slaf-admin', 'Archived', '2026-08-11 11:32:30', '2026-08-12 04:27:05'),
('4c118c0b-c2e4-4aa6-97de-714cfc78f2ca', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', NULL, 'Comp tech lesson plan', 'test', 'lesson plan', '1.0', '2026', 'testing', 'Sanka  Adikaram - 2024-06-05.pdf', 'tts-lesson-plans/Sanka  Adikaram - 2024-06-05_20260811113400', 'https://res.cloudinary.com/wtc5iadz/raw/upload/v1786448043/tts-lesson-plans/Sanka%20%20Adikaram%20-%202024-06-05_20260811113400', 'raw', 89231, 'application/pdf', 'user-slaf-admin', 'Archived', '2026-08-11 11:34:03', '2026-08-12 04:26:56'),
('abf33660-8df6-46cf-b524-4db348a41261', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', NULL, 'Com tech', 'bnm,', 'lesson plan', '1.0', '2026', NULL, 'Memo in laptop.pdf', 'tts-lesson-plans/Memo in laptop_20260907063716', 'https://res.cloudinary.com/wtc5iadz/raw/upload/v1788763038/tts-lesson-plans/Memo%20in%20laptop_20260907063716', 'raw', 145790, 'application/pdf', 'user-slaf-admin', 'Active', '2026-09-07 06:37:20', '2026-09-07 06:37:20'),
('e0407688-6cf2-43b4-b754-1a253ea4c787', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', NULL, 'Comp tech lesson plan', 'lesson plan', 'lesson plan', '1.0', '2026', 'testing', 'Module 13 Database Design.pdf', 'tts-lesson-plans/Module 13 Database Design_20260812104052', 'https://res.cloudinary.com/wtc5iadz/image/upload/v1786531254/tts-lesson-plans/Module%2013%20Database%20Design_20260812104052.pdf', 'raw', 1152985, 'application/pdf', 'user-slaf-admin', 'Archived', '2026-08-12 10:40:55', '2026-08-20 10:27:27'),
('f5f5a1ac-733e-4432-9f63-8922c7c3fe98', '0b7a2bcf-5ac0-4590-a777-05febce54289', NULL, 'Acct 13 SLAF Non Public Funds', 'dfghj', 'Acct 13 SLAF Non Public Funds', '1.0', '2026', 'Acct 13 SLAF Non Public Funds', 'Acct 13 SLAF Non Public Funds.pdf', 'tts-lesson-plans/Acct 13 SLAF Non Public Funds_20260918104033', 'https://res.cloudinary.com/wtc5iadz/raw/upload/v1789728038/tts-lesson-plans/Acct%2013%20SLAF%20Non%20Public%20Funds_20260918104033', 'raw', 187451, 'application/pdf', 'user-slaf-admin', 'Active', '2026-09-18 10:40:37', '2026-09-18 10:40:37'),
('f97ed1bc-30b7-45d2-b43a-a6d6fc46ec14', '0b7a2bcf-5ac0-4590-a777-05febce54289', NULL, 'Introduction to accounting concepts', '23trehjhkl', 'lesson plan', '1.0', '2026', 'Introduction to accounting concepts', 'Acct 12- 02 Introduction of Accounting & Concepts (1).pdf', 'local_lp_Acct 12- 02 Introduction of Accounting & Concepts (1)_20260918103945.pdf', '/static/uploads/lesson_plans/Acct 12- 02 Introduction of Accounting & Concepts (1)_20260918103945.pdf', 'raw', 184629, 'application/pdf', 'user-slaf-admin', 'Active', '2026-09-18 10:39:45', '2026-09-18 10:39:45');

-- --------------------------------------------------------

--
-- Table structure for table `login_history`
--

CREATE TABLE `login_history` (
  `id` varchar(36) NOT NULL,
  `user_id` varchar(36) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` varchar(255) DEFAULT NULL,
  `logout_time` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `login_history`
--

INSERT INTO `login_history` (`id`, `user_id`, `username`, `status`, `ip_address`, `user_agent`, `logout_time`, `created_at`) VALUES
('003b091a-855e-474f-97bc-60cf5ab6dda7', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', '2026-10-26 04:48:34', '2026-10-26 04:47:24'),
('018b9e37-3a52-4476-91b6-a3ae9cc2266d', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-14 11:49:51'),
('06f738ff-81cf-4c80-b827-af5384d61e29', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-14 11:49:28'),
('06fac973-e67d-4923-bebd-0d3ca1d46dc9', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 09:49:57'),
('0709083f-259d-44ab-bd81-5e2da7c1fc65', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-16 09:38:23', '2026-09-16 09:30:59'),
('0962e108-b834-4f2b-bf80-e30041d3f980', 'user-slaf-admin', 'admin', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', NULL, '2026-09-18 09:28:37'),
('09b23b63-1286-458f-9133-d3b87a183293', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-11 15:18:25'),
('0bcd7e4d-6fee-482d-b168-dc0e4128c211', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-14 09:28:36'),
('0c7f7dff-e379-421c-817b-6b94e3059bc2', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', '2026-10-05 11:54:49', '2026-10-05 11:24:44'),
('0dd8b3f3-df8a-4d42-927f-c07e480e09f8', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 09:59:51'),
('0f99bdef-f9e8-4ff3-8543-12403a806b99', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', '2026-10-26 04:24:42', '2026-10-26 04:12:19'),
('0f9d18ac-4847-4b26-b584-2d51d62baf5a', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-17 11:38:42', '2026-09-17 11:38:39'),
('11f601a2-409d-4cdd-8b3c-f6fe20f4ff80', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 11:34:49'),
('125e8549-f9d0-4694-b40d-a3e193434d9d', 'user-slaf-admin', 'admin', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-24 03:21:16'),
('1267f678-709b-406f-9f78-ab20ff1be557', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-17 11:45:19', '2026-09-17 11:42:05'),
('130f1236-fd5a-48ef-9353-310415f03319', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-21 07:28:39', '2026-09-21 07:28:12'),
('14f37cd1-0b38-40e3-b3a2-c69265ca2d88', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', '2026-09-21 11:52:48', '2026-09-21 11:51:10'),
('164e0cbe-69b7-4351-b216-d95e0e245265', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-21 07:19:42', '2026-09-21 06:50:24'),
('17001e08-2ea6-4fc1-8694-2b29f9cdf956', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-10 11:41:48', '2026-09-10 10:53:47'),
('17fd47d8-4170-4a0d-b72a-f9c3ade06bc4', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-16 11:26:32', '2026-09-16 11:23:09'),
('18ac927c-f9b3-41af-979f-6f4af2fe90dd', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-21 05:39:12', '2026-09-21 05:38:46'),
('1b2add56-b4e7-48cc-a0d0-b73786619610', 'user-slaf-admin', 'admin', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36', NULL, '2026-10-26 04:05:12'),
('1f0217dd-635f-4522-a5fc-dd88557d4481', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', '2026-10-26 04:53:04', '2026-10-26 04:48:54'),
('20e44d52-1737-4527-9fa8-1b76295adf1d', '1b514baf-ebde-4fcc-b838-902659c5c3e3', '04253', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 11:10:41'),
('21b2c66a-4eea-4983-9cfd-839fbc5d1028', 'user-slaf-admin', 'admin', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 09:59:43'),
('22b55989-6e1c-4dca-b3c8-fe27d872ffaf', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-18 10:51:45', '2026-09-18 10:37:16'),
('2609d0b6-8cb6-4400-9e5b-158afa21905a', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-17 10:45:44'),
('267619a2-6690-4d02-8767-97e46ebad471', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-13 11:50:25'),
('27c5f821-2405-45d8-8551-c0bf07e2bf2e', '1b514baf-ebde-4fcc-b838-902659c5c3e3', '04253', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-17 10:52:23'),
('28ce7e6f-50e2-477c-a6bd-026140ea9433', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', '2026-10-05 12:02:12', '2026-10-05 11:59:25'),
('29e1f142-e683-4128-ac4b-b88bdcc111d5', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-15 11:26:07', '2026-09-14 10:56:29'),
('2f2c3c90-9ae2-4af3-8047-611473014daa', 'c5f0985e-45f7-4086-9bb7-06019de7cea3', '51098', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', '2026-10-26 04:46:37', '2026-10-26 04:46:11'),
('2f871ffb-a4b3-4cf6-96fd-bfba7fcbd321', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 11:23:55'),
('309fec70-91e2-4280-af15-e634f51b2611', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', '2026-08-17 12:22:11', '2026-08-17 12:16:30'),
('30a51ae7-71da-4b19-957f-e607596b3248', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-21 07:30:12', '2026-09-21 07:29:59'),
('331a9579-799f-43c2-a27b-c7f9460720f3', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-21 06:50:11', '2026-09-21 05:54:30'),
('34e1d923-ad88-406b-b54e-efb6d2ce040b', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-21 07:28:05', '2026-09-21 07:19:52'),
('352c0577-ef96-4b11-8423-ac659e6ae27f', '1b514baf-ebde-4fcc-b838-902659c5c3e3', '04253', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 11:19:35'),
('35b98197-2548-4c31-91b3-3144e925aa9a', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-11 11:05:09'),
('3682a63d-f55d-486a-8c33-8cea36700dd8', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-07 06:41:42', '2026-09-07 06:32:38'),
('38976bbb-91f4-414d-8814-23834aed2817', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-17 03:54:32', '2026-09-17 03:52:14'),
('3d66bbaf-d738-41ed-9bae-aec56df44f56', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'LOCKED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 11:31:56'),
('3e18e467-1ce1-4160-813b-c7c2d5fc8ebc', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-31 12:09:27'),
('3fd548ea-d547-4fdd-8137-6cc9a624d046', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', NULL, '2026-09-16 11:27:53'),
('3fdfd9b8-cf7f-4f5d-97fc-daa40250963e', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-31 09:27:06'),
('400813d1-e346-458c-8191-2f628692cdfd', 'c96d5ee9-93ee-41cc-b9e6-f31ecba02f4e', '51837', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-21 05:41:25', '2026-09-21 05:41:18'),
('4015d68d-4f9a-40f8-9a70-2785043dfae4', 'c96d5ee9-93ee-41cc-b9e6-f31ecba02f4e', '51837', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-21 05:42:12', '2026-09-21 05:42:09'),
('40362ef6-da18-49b7-9f7a-37f127f00a23', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', NULL, '2026-09-10 11:42:09'),
('4040821b-b4a9-404b-8272-1d5af29715d0', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-17 11:16:24'),
('450aa649-3a23-46ad-b2b9-ac4b5aa5b5ca', 'user-slaf-admin', 'admin', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', NULL, '2026-10-05 11:59:19'),
('48539e2b-e534-40d2-9051-35c17e7e74c6', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', '2026-08-20 10:43:42', '2026-08-20 10:42:10'),
('48958309-c36d-4a2d-81ed-7f788c91a461', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-16 09:40:50', '2026-09-16 09:38:38'),
('4b9cf4f2-5fdf-4c5c-8d32-f956b9053931', 'c96d5ee9-93ee-41cc-b9e6-f31ecba02f4e', '51837', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-21 05:48:15', '2026-09-21 05:43:57'),
('4c52ee89-2a10-4de2-8521-a825a8663d3c', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-21 05:22:03', '2026-09-21 05:21:27'),
('4caeb4e1-61f5-49b7-bc6b-893c66e93a93', 'user-slaf-admin', 'admin', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-24 03:21:06'),
('4ccbc0c4-9033-4df2-a2d5-967627b1f94e', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-21 05:21:16', '2026-09-21 05:19:35'),
('50710762-d5ed-4a94-bb26-82301cc665d4', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 10:58:39'),
('527f0e14-4c2f-450a-b51d-b44389f6c68c', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-07 06:29:28', '2026-09-07 06:29:17'),
('52a3cccb-3f01-483f-a99b-2d84d876ee8a', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', '2026-09-21 11:58:30', '2026-09-21 11:55:01'),
('537fe759-0f48-4e40-876e-26a0bd8c6244', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-11 15:35:29'),
('54a79562-7bf7-4e67-89b0-3f45af67350a', 'c96d5ee9-93ee-41cc-b9e6-f31ecba02f4e', '51837', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-21 05:41:53', '2026-09-21 05:41:49'),
('56315124-3532-409f-a967-ead0798e1978', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', '2026-10-05 11:59:07', '2026-10-05 11:55:01'),
('5676e94e-0fd5-4cc0-b86f-8d9215162700', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 11:19:08'),
('57c93e0e-cafb-457a-b21d-7a81c8a628df', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-17 05:43:48'),
('5a35bfb5-bff2-4d35-ad40-247f9fff4eca', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 10:24:12'),
('5b93c0de-0f70-452e-afb8-9fcf3c5aaee7', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-17 09:47:04', '2026-09-17 09:46:26'),
('5bd935cb-4db4-4a15-9da1-a52fede77b87', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 10:03:37'),
('5da66cbc-81f7-46ab-8e27-016c6ddc08ab', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-17 09:45:40', '2026-09-17 09:45:14'),
('5f074316-2135-4f01-bd24-5c8b73d52ab9', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', NULL, '2026-09-15 11:26:43'),
('5fbbcd1a-698c-41bb-a8da-d9fa3f79fc82', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-18 10:10:11', '2026-09-18 10:09:57'),
('62f1b540-8680-4390-91b6-fdd85598a8c1', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-17 10:30:11', '2026-09-17 10:30:02'),
('633c9998-3f82-4881-99fa-62bc8ae6f330', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', '2026-08-17 11:32:12', '2026-08-17 11:19:57'),
('640df998-b46a-49e9-b17b-a0fb4c09b092', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', '2026-10-26 04:36:45', '2026-10-26 04:32:34'),
('6481b166-55da-4586-9474-390516e25a36', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-12 11:25:05'),
('67fa5821-a312-4127-a438-c326b79191b7', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-18 09:27:52', '2026-09-18 09:19:51'),
('68d91a14-1525-4059-a695-816856b66ac4', 'user-slaf-admin', 'admin', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36', NULL, '2026-10-26 04:05:19'),
('68db4af2-bf29-4ea7-86d1-59858043212e', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-14 11:44:55'),
('6a574d62-6eed-4280-9fc8-a861cc2934c7', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-07 06:30:42', '2026-09-07 06:29:41'),
('6bd76369-1bb8-4965-b6fb-53185d4dfe1f', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', NULL, '2026-09-15 12:31:14'),
('6c492625-d2db-4d1f-af84-2d50cd27dca7', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-21 05:54:17', '2026-09-21 05:48:39'),
('6c92d012-5d8e-4c9c-8cf2-97771c3dbd25', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-21 05:38:25', '2026-09-21 05:38:10'),
('6f661af2-9082-413d-9ab7-622389101bbd', '1b514baf-ebde-4fcc-b838-902659c5c3e3', '04253', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', '2026-08-24 10:29:59', '2026-08-24 10:29:26'),
('77df57bc-783b-48fe-a5c5-44dd406be09d', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', NULL, '2026-09-21 09:51:41'),
('78fd779c-a953-403e-8f0d-bb6dbf088617', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', NULL, '2026-09-24 02:59:40'),
('7934e008-927e-43d1-b9c1-6ba26216d984', 'user-slaf-admin', 'admin', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 09:49:42'),
('795df6d0-6596-4bb7-9623-3fa69cd52a9d', 'user-slaf-admin', 'admin', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-11 15:18:14'),
('7abab829-0cd6-42df-818f-633a73aa2194', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-21 05:40:53', '2026-09-21 05:39:33'),
('7b5cfa63-da19-4611-a7be-6d5285d94fa8', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-17 09:46:05', '2026-09-17 09:45:53'),
('7ba5fe8c-8bcf-4314-80d8-3df24e543941', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-11 15:16:21'),
('7c61ae3c-2476-4f08-8034-8d5538d36683', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', '2026-08-24 03:18:22', '2026-08-24 03:12:33'),
('8044e4d1-8ac0-4566-8b72-e8f1af325bb3', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-11 09:25:46'),
('80c7e8a9-796d-4aff-b9f4-1dfdd1559e18', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', '2026-08-17 11:32:53', '2026-08-17 11:32:31'),
('844f7b02-4e93-44b5-b397-3da9aa38596f', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 11:37:55'),
('84d600a2-30fa-40f1-a00c-8556b9fc2dc8', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-15 11:26:31', '2026-09-15 11:26:26'),
('881709b4-42ac-4a73-b519-0a0d57e3b814', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-18 09:32:38', '2026-09-18 09:28:43'),
('89368091-d3cb-425e-968e-104eb6f01111', NULL, '04152', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-17 10:51:06'),
('897768a2-ce78-49fe-8595-f0f75b7980aa', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-12 11:35:59'),
('8a6906c2-5d13-494a-9616-e759a71eaea1', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-16 10:33:32', '2026-09-16 09:41:06'),
('8ab2f21f-e4f7-4ac3-9f2e-19b0bcd27044', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', '2026-09-21 11:50:48', '2026-09-21 11:01:06'),
('8ba48444-f9bc-4cfb-b302-6b2bec36a6ea', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 11:24:13'),
('8bb5bc04-3c81-428e-b48c-8154bf587025', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-11 09:19:29', '2026-09-11 09:19:23'),
('8df77a4c-2c10-4379-8f87-d7708d7c8dc7', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-24 10:30:15'),
('8dff2620-14ab-4dfc-be6e-d833a2f4faf0', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-11 15:32:46'),
('8e110761-af6e-4d5d-adb2-faf95fec1ee3', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-17 10:23:39', '2026-09-17 10:14:25'),
('8e2fce7a-eeeb-4aaa-a273-4e37cd629f44', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-17 03:56:42', '2026-09-17 03:54:46'),
('90962e4c-e5eb-45b5-a5b2-960b36537bfb', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-12 10:15:41'),
('938afc27-e324-488a-b671-283e02a60ea8', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-09 11:22:50', '2026-09-09 11:17:05'),
('96cb9e70-0b60-403a-ac2c-85d6e231a893', 'user-slaf-admin', 'admin', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', NULL, '2026-09-21 05:17:05'),
('97ead365-b039-4ee4-9b4c-70a1cc995629', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', '2026-10-26 04:26:57', '2026-10-26 04:24:56'),
('9820f440-f06b-456a-bd07-51a5afa75a3b', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-17 03:51:47', '2026-09-17 03:43:56'),
('9963bcce-9e98-4bc0-ab37-dc3dd3f8cfd0', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', '2026-08-31 10:39:38', '2026-08-31 10:27:42'),
('99676ba8-5ef0-4d14-b3c4-e8f759215134', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', NULL, '2026-10-05 12:05:56'),
('999ff32f-0859-40b3-952e-23fd51ff92b9', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', NULL, '2026-09-11 11:25:57'),
('99b45267-41da-48b3-a41f-4eaa55c5cfbd', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', '2026-08-17 12:23:21', '2026-08-17 12:22:33'),
('9a7acc31-5e86-474e-8982-29d7ec8523ed', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-14 11:38:44'),
('9ad7cfd1-62b6-47da-baa0-ebaf1c365892', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-07 06:32:19', '2026-09-07 06:32:08'),
('9b8b4a37-985d-4247-8aee-7f996a82041c', '1b514baf-ebde-4fcc-b838-902659c5c3e3', '04253', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-17 10:51:59'),
('9ea41ad3-b771-4658-b141-b7f32af6f05a', 'user-slaf-admin', 'admin', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36', NULL, '2026-10-26 04:05:16'),
('9f548f5b-60d3-4124-8ebc-b58c1d9bb20c', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 11:07:06'),
('a0f9881d-d0df-4a33-844b-61b0049d2f80', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', NULL, '2026-09-11 10:24:58'),
('a1f401f5-fe73-49f0-90b4-e1228ff2159d', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', NULL, '2026-09-11 09:20:11'),
('a2736abc-2c8d-42d1-9592-dcb0c9d3407b', 'c96d5ee9-93ee-41cc-b9e6-f31ecba02f4e', '51837', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', '2026-09-21 09:51:12', '2026-09-21 09:50:11'),
('a50ebf43-dd74-4d65-8386-afb55c8a0ea6', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', '2026-10-26 04:30:11', '2026-10-26 04:27:16'),
('a66797b2-d61b-4b86-98c9-e0737ce4f904', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 11:00:49'),
('a811c261-59de-46d2-bc82-3cdffde9afeb', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-17 10:50:09'),
('a847e9d2-0b11-4935-943c-bd7da61c9158', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', NULL, '2026-09-21 12:00:26'),
('a84c4b4b-176d-4707-afe5-e251cc169454', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-21 05:37:57', '2026-09-21 05:35:54'),
('a8976e4e-76eb-46d8-affa-098c7ba45c7b', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-12 11:37:28'),
('ab23669d-f59d-4b82-8db9-f77b51f6e329', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-11 15:24:26'),
('ab4428ab-2870-4351-ba8a-32cd2d64affc', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'test', NULL, '2026-08-17 10:56:53'),
('ab988646-e8e9-42ff-85f1-5329b58b0f66', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', '2026-08-24 10:27:54', '2026-08-24 10:27:05'),
('ace22d0e-1065-45fa-ad33-a22209beeae3', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-10 10:52:32', '2026-09-09 11:52:17'),
('ada7fe6d-9d68-4a53-b0db-313e6f67de51', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', '2026-10-05 12:03:48', '2026-10-05 12:02:26'),
('adf299e5-9c01-4633-9fc2-14f2fe16f290', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-18 10:37:00', '2026-09-18 10:10:26'),
('adfc9977-9b54-42c1-b611-7e23a5072674', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', '2026-08-17 12:15:51', '2026-08-17 11:33:06'),
('af255ba1-1625-40ab-8d45-7d7508f64542', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-14 11:57:44'),
('b2c1574d-3107-4bf3-9ee3-9106132af529', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', '2026-10-26 04:43:13', '2026-10-26 04:37:06'),
('b35d4521-995b-4631-be3f-b25eacee31d8', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', '2026-10-05 12:05:43', '2026-10-05 12:04:09'),
('b37487d1-6870-4d5f-950b-9bba548e6aea', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-17 04:01:44', '2026-09-17 04:01:39'),
('b56f0afc-2d70-42d1-b068-443745678c18', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', NULL, '2026-09-17 10:14:02'),
('b7633a53-afea-4bbe-8807-43095f5054be', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-14 10:29:30'),
('b777e4ff-5d17-44f9-ac15-20787a841c13', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-17 10:13:43', '2026-09-17 09:47:30'),
('b8531849-3d34-4379-8d59-cb46acd8cc9b', '1b514baf-ebde-4fcc-b838-902659c5c3e3', '04253', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-17 10:53:17'),
('b9ef4324-998c-4d33-9a0d-625ef15473dc', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-17 10:30:56', '2026-09-17 10:30:43'),
('ba1b3d1d-329d-4595-95e9-3e3b370f817d', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-09 10:31:03', '2026-09-09 10:02:31'),
('bad10f7e-6b36-49d6-b8fd-a4f051d157d3', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-16 11:22:31', '2026-09-16 10:34:33'),
('bc5831d5-0cea-40f7-a9fe-de480eaa377b', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-17 10:26:28', '2026-09-17 10:25:23'),
('bc9bfac7-cefa-4ccc-8787-f32224b0fdcd', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-11 15:30:20'),
('bce856c4-53c2-41dc-a974-8201debf82e1', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-17 11:16:24'),
('bcfe9527-1960-4d1d-8c8e-8f1706d6a214', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-16 11:27:28', '2026-09-16 11:26:44'),
('c0df9c0a-6353-4cee-8d6f-3f90df05316d', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-17 04:00:43', '2026-09-17 03:57:03'),
('c1610687-ba42-4c9f-9d7c-e24c47665c7b', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-21 05:35:36', '2026-09-21 05:22:15'),
('c28683b7-f4cc-4498-86fd-ad57150e3a74', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36', NULL, '2026-10-26 03:53:54'),
('c46aaa1b-e5aa-4b11-8bf4-5f2a34a2f2ce', 'user-slaf-admin', 'admin', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36', NULL, '2026-10-26 03:53:48'),
('c473905b-19cc-4cba-8842-bdeadda87d31', 'user-slaf-admin', 'admin', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-24 11:41:19'),
('c4a181bf-5d1b-44e8-bdf7-a598661b416f', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', '2026-08-24 11:54:23', '2026-08-24 11:41:27'),
('c6503cec-4569-4366-af6f-d60dbad910ca', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', '2026-09-21 12:00:14', '2026-09-21 11:58:40'),
('c7e45b14-12af-4a82-abbe-0385ea75ec52', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36', '2026-10-26 04:12:00', '2026-10-26 04:05:24'),
('c98fb4ef-3f4e-4e0e-9d4e-11b2340587c3', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-12 09:59:04'),
('cc459eb9-979a-472e-b125-ab22e7d443e3', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', NULL, '2026-09-17 10:31:14'),
('cce9887a-cd1b-4560-88f7-1731f938fd78', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-11 15:34:17'),
('cd20a085-2a19-4cc9-a5a1-38782ecff8f7', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-21 05:19:23', '2026-09-21 05:17:08'),
('d12d18ec-b7d1-41cb-8d89-88d216c193e0', 'user-slaf-admin', 'admin', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', NULL, '2026-09-18 09:28:35'),
('d1728b58-9f2d-450e-9001-115d58f1b623', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', '2026-09-24 09:40:37', '2026-09-24 09:38:09'),
('d1f0f32b-1fc8-43ed-b208-cc182b7c2cfc', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', '2026-10-26 04:32:18', '2026-10-26 04:30:27'),
('d2318f32-4814-4642-88c1-79c8db89be68', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-21 05:16:52', '2026-09-21 05:01:42'),
('d2d5af51-7057-4661-b956-3530fe09ea1f', 'user-slaf-admin', 'admin', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 09:49:31'),
('d2e4c590-a876-40aa-8f39-fca67acb422d', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'LOCKED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 11:32:04'),
('d3505e45-26da-4468-bd28-72e1ebecc886', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', NULL, '2026-09-09 10:31:19'),
('d40994bc-c63f-410b-950f-5d6925765e01', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 09:34:44'),
('d6c72960-fea0-40b4-9792-5f5a680d02b4', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', NULL, '2026-09-09 09:51:11'),
('d7648c15-4291-478e-8b3f-e6c35bea5507', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', '2026-08-31 12:06:15', '2026-08-31 12:03:44'),
('d8292e85-3b24-4531-9703-46b04be1773f', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', NULL, '2026-09-17 10:24:59'),
('d9daa417-ba66-4a28-9b43-da40176aeb8c', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-16 10:34:25', '2026-09-16 10:33:45'),
('db061921-c138-4b75-ba47-e8a5882a0b2f', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-07 07:14:17', '2026-09-07 06:41:55'),
('db346d13-0dd4-49ef-918c-524f310c9725', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 11:29:03'),
('dc3e362c-244b-4e31-8e4e-5ed92e00840f', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-12 04:35:43'),
('dcf73a06-54ae-4035-a77d-50e8da3d18d7', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-07 06:28:13', '2026-09-07 06:28:03'),
('dde15697-fc9c-4bf4-81dd-1da709d6f4d2', NULL, '04153', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-17 10:51:51'),
('de0be3a6-553d-473b-aead-5e220abae6bc', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-16 11:22:59', '2026-09-16 11:22:41'),
('de9ca0a3-03f0-4c7b-a22b-6184201b0b11', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-17 04:03:14', '2026-09-17 04:01:55'),
('ded72c95-059b-4e26-90bf-3f9f557b4364', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', '2026-08-31 12:03:26', '2026-08-31 11:55:49'),
('dfa70712-7c84-4626-9338-5b67740969a4', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 11:23:41'),
('e1665bc9-093f-4afd-be34-fa80778cbdde', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-18 11:04:34', '2026-09-18 10:52:01'),
('e2e16ab6-3689-4f93-859c-7cf2949cec64', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-09 09:50:59', '2026-09-09 09:50:47'),
('e55755f4-47e6-4a2c-a872-7a38c06431ef', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', '2026-08-24 03:20:39', '2026-08-24 03:19:02'),
('e5805587-3200-4147-a987-5dedde9f6b70', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 11:21:22'),
('e66ac688-4812-4616-b138-b1de17b012ce', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36', '2026-10-26 03:52:58', '2026-10-26 03:52:17'),
('e813fe57-b189-4f34-9525-35b9cb668baf', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-14 11:50:29'),
('e86feab2-dff2-44bd-abb9-cdbc2dd67fae', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-21 05:43:37', '2026-09-21 05:42:26'),
('ea4ab306-4510-4b75-945b-481e77dcc580', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', NULL, '2026-09-09 11:23:09'),
('ed868f24-1de7-4319-a958-c88f54dedda1', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36', '2026-10-26 04:45:59', '2026-10-26 04:43:32'),
('eee72fb3-1fd0-4f13-9eeb-390f21b851d2', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-14 11:46:54'),
('efb26620-721a-47cf-9d9b-5f459039ac53', 'f6f853a0-a3db-481e-bb6b-95e469c45dc8', '51088', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-12 04:25:31'),
('eff0aaaf-234c-4ed1-9fac-333780e155fd', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-17 10:54:23'),
('f0752b04-18a1-46f7-ac03-10eb642306e2', '1b514baf-ebde-4fcc-b838-902659c5c3e3', '04253', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 11:08:27'),
('f095fcc5-0041-47c8-820d-7249be010b55', '1b514baf-ebde-4fcc-b838-902659c5c3e3', '04253', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-11 15:17:31'),
('f0ceb7fb-a671-45d6-b015-0f45a835a984', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 09:37:58'),
('f0f9c4e5-d932-4799-8f4e-fcb0290adcaa', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', '2026-09-21 11:53:44', '2026-09-21 11:53:10'),
('f50e279c-503e-49c5-9bc3-9e6ac97498ac', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-14 11:51:33'),
('f694edb6-2ff4-42fd-beb4-ad1651a8d128', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-12 05:29:46');
INSERT INTO `login_history` (`id`, `user_id`, `username`, `status`, `ip_address`, `user_agent`, `logout_time`, `created_at`) VALUES
('f833415a-f709-4955-a7a7-1c9c55416790', 'user-slaf-admin', 'admin', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36', NULL, '2026-10-26 03:53:29'),
('fab3a7aa-c7bc-4ffe-9189-f1822b5bc484', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36', '2026-09-21 09:50:01', '2026-09-21 09:48:17'),
('fb7b3a6e-a6ed-4022-8bcb-9e65a8a80542', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-31 10:39:54'),
('fb8c13cd-829c-4ab4-843a-9b85b19462bf', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-17 10:29:45', '2026-09-17 10:26:51'),
('fbc8b196-2f82-41ee-ade3-ece823830241', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-17 10:24:30', '2026-09-17 10:24:14'),
('fdada55f-b314-4fb6-8462-6a918da7ff3b', 'user-slaf-admin', 'admin', 'FAILED', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', NULL, '2026-09-18 09:28:29'),
('fe03afcf-93ff-4a94-b884-196fed9eabfe', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36', '2026-09-18 10:09:41', '2026-09-18 09:32:52'),
('fe088702-8d33-4e6a-b3e9-75178601053e', 'dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-10 11:33:39'),
('ff91af81-fdd3-403f-a150-dac169516791', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36', '2026-10-05 11:24:27', '2026-10-05 11:18:32'),
('ffb730bb-bd4c-4429-a788-539fd7b037ab', 'user-slaf-admin', 'admin', 'SUCCESS', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36', NULL, '2026-08-11 15:12:17');

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` varchar(36) NOT NULL,
  `user_id` varchar(36) DEFAULT NULL,
  `title` varchar(150) NOT NULL,
  `message` text NOT NULL,
  `type` varchar(20) DEFAULT NULL,
  `is_read` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`id`, `user_id`, `title`, `message`, `type`, `is_read`, `created_at`) VALUES
('0027552c-a2c2-4fa7-88c1-fbb1490cd4e8', '1b514baf-ebde-4fcc-b838-902659c5c3e3', 'Parade State Approval Required — Computer Technician (2026-08-17)', 'The Daily Parade State for trade \'Computer Technician\' on 2026-08-17 has been submitted by  SLAF Administrator for your approval. Total strength: 5 personnel.', 'ALERT', 0, '2026-08-17 10:50:49'),
('0a3b1262-4fc6-4ddd-9a54-97af97ed194b', 'user-slaf-admin', 'Parade State APPROVED — Computer Technician (2026-08-17)', 'Your parade state submission for trade \'Computer Technician\' on 2026-08-17 has been APPROVED by Flight Lieutenant Saman Kumara. ', 'INFO', 1, '2026-08-17 10:53:46'),
('312daa4a-3783-45fc-87ab-798745568863', 'user-slaf-admin', 'Parade State APPROVED — Computer Technician (2026-09-16)', 'Your parade state submission for trade \'Computer Technician\' on 2026-09-16 has been APPROVED by WO HFAI Fonseka. ', 'INFO', 1, '2026-09-16 11:27:17'),
('350169ea-e25c-458d-9264-704166f61397', 'user-slaf-admin', 'Parade State APPROVED — Computer Technician (2026-08-10)', 'Your parade state submission for trade \'Computer Technician\' on 2026-08-10 has been APPROVED by Flight Lieutenant Saman Kumara. ', 'INFO', 1, '2026-08-10 11:08:56'),
('45a0120c-04fd-4397-bc53-1603102cfdaa', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'Parade State Approval Required — Account Assistant (2026-09-21)', 'The Daily Parade State for trade \'Account Assistant\' on 2026-09-21 has been submitted by  SLAF Administrator for your approval. Total strength: 4 personnel.', 'ALERT', 0, '2026-09-21 05:22:52'),
('6168c8fb-fe26-4017-8a07-a29d8b935857', 'user-slaf-admin', 'CRITICAL STATE ALERT: Leading Aircraftman Rashmika', 'Student 50327 is officially confirmed as \'Hospital\' for 2026-08-24 (trade: Computer Technician). Parade approved by Officer I/C.', 'ALERT', 1, '2026-08-24 10:29:52'),
('71abb8a3-aa22-444b-a759-dedca6876979', 'user-slaf-admin', 'Parade State APPROVED — Computer Technician (2026-08-31)', 'Your parade state submission for trade \'Computer Technician\' on 2026-08-31 has been APPROVED by Warrant Officer HFAI Fonseka. ', 'INFO', 1, '2026-08-31 12:19:28'),
('8b223a78-d2fb-4256-ad10-36dcf8c4f699', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'Parade State Approval Required — Computer Technician (2026-09-16)', 'The Daily Parade State for trade \'Computer Technician\' on 2026-09-16 has been submitted by  SLAF Administrator for your approval. Total strength: 5 personnel.', 'ALERT', 1, '2026-09-16 11:23:48'),
('9cba3337-b996-4de2-a935-9e2c08d339b8', '1b514baf-ebde-4fcc-b838-902659c5c3e3', 'Parade State Approval Required — Computer Technician (2026-08-11)', 'The Daily Parade State for trade \'Computer Technician\' on 2026-08-11 has been submitted by  SLAF Administrator for your approval. Total strength: 5 personnel.', 'ALERT', 0, '2026-08-11 15:16:58'),
('ab2ca1f4-c32a-4eae-94bc-2667e14e46a1', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'Parade State Approval Required — Computer Technician (2026-08-31)', 'The Daily Parade State for trade \'Computer Technician\' on 2026-08-31 has been submitted by  SLAF Administrator for your approval. Total strength: 5 personnel.', 'ALERT', 1, '2026-08-31 12:06:00'),
('afd08786-e211-499c-86db-eabdc5022df6', '1b514baf-ebde-4fcc-b838-902659c5c3e3', 'Parade State Approval Required — Computer Technician (2026-08-10)', 'The Daily Parade State for trade \'Computer Technician\' on 2026-08-10 has been submitted by  SLAF Administrator for your approval. Total strength: 4 personnel.', 'ALERT', 1, '2026-08-10 11:08:11'),
('c5379b07-9588-4c0d-a145-50ac4b0eaafe', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'Parade State APPROVED — Computer Technician (2026-09-17)', 'Your parade state submission for trade \'Computer Technician\' on 2026-09-17 has been APPROVED by WO HFAI Fonseka. ', 'INFO', 0, '2026-09-17 10:28:47'),
('c7a1ab15-cfe3-4e94-9edb-ec7424e87b13', 'user-slaf-admin', 'Parade State APPROVED — Computer Technician (2026-08-24)', 'Your parade state submission for trade \'Computer Technician\' on 2026-08-24 has been APPROVED by Flight Lieutenant Saman Kumara. ', 'INFO', 1, '2026-08-24 10:29:52'),
('cc17f908-889a-4caf-85d7-eb4147b9b932', '1b514baf-ebde-4fcc-b838-902659c5c3e3', 'Parade State Approval Required — Computer Technician (2026-08-24)', 'The Daily Parade State for trade \'Computer Technician\' on 2026-08-24 has been submitted by  SLAF Administrator for your approval. Total strength: 5 personnel.', 'ALERT', 0, '2026-08-24 10:27:49'),
('d90922bf-c250-4351-9789-d88bdd8f9c11', 'user-slaf-admin', 'Parade State APPROVED — Computer Technician (2026-08-11)', 'Your parade state submission for trade \'Computer Technician\' on 2026-08-11 has been APPROVED by Flight Lieutenant Saman Kumara. ', 'INFO', 1, '2026-08-11 15:17:55'),
('de23185f-e3d5-40a5-90f6-11c1222a01ee', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'Parade State Approval Required — Computer Technician (2026-09-17)', 'The Daily Parade State for trade \'Computer Technician\' on 2026-09-17 has been submitted by WO HFAI Fonseka for your approval. Total strength: 5 personnel.', 'ALERT', 0, '2026-09-17 09:46:52'),
('e49f6fa4-7267-44ff-917a-69dffcca62ff', 'user-slaf-admin', 'Parade State APPROVED — Account Assistant (2026-09-21)', 'Your parade state submission for trade \'Account Assistant\' on 2026-09-21 has been APPROVED by  SLAF Administrator. ', 'INFO', 1, '2026-09-21 07:17:30'),
('eb225ab5-8d1c-4700-b01b-cab3aa3378e1', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'Parade State Approval Required — Computer Technician (2026-10-26)', 'The Daily Parade State for trade \'Computer Technician\' on 2026-10-26 has been submitted by  SLAF Administrator for your approval. Total strength: 7 personnel.', 'ALERT', 0, '2026-10-26 04:48:29'),
('f7103aa0-1e68-4568-8492-78b9a2991893', '1b514baf-ebde-4fcc-b838-902659c5c3e3', 'Parade State Approval Required — Computer Technician (2026-08-12)', 'The Daily Parade State for trade \'Computer Technician\' on 2026-08-12 has been submitted by  SLAF Administrator for your approval. Total strength: 5 personnel.', 'ALERT', 0, '2026-08-12 04:43:24'),
('f7a1741a-b421-46cb-9500-875f1dd029f5', '1b514baf-ebde-4fcc-b838-902659c5c3e3', 'CRITICAL STATE ALERT: Leading Aircraftman Rashmika', 'Student 50327 is officially confirmed as \'Hospital\' for 2026-08-24 (trade: Computer Technician). Parade approved by Officer I/C.', 'ALERT', 0, '2026-08-24 10:29:52'),
('notice-1', NULL, 'New Batch Registration', 'New batch registration starts next week. Please ensure all student documents are prepared.', 'INFO', 0, '2026-08-10 09:31:21'),
('notice-2', NULL, 'Timetable Release', 'Examination timetable for BA-AER-01 has been released on the portal.', 'INFO', 0, '2026-08-10 09:31:21'),
('notice-3', NULL, 'Accommodation Inspection', 'Billet inspection scheduled for Training Block Alpha this Friday at 0900 hrs.', 'WARNING', 0, '2026-08-10 09:31:21'),
('notice-4', NULL, 'Parade State Submission', 'Reminder: Daily parade state must be submitted before 0800 hrs daily.', 'ALERT', 0, '2026-08-10 09:31:21');

-- --------------------------------------------------------

--
-- Table structure for table `officer_in_charge`
--

CREATE TABLE `officer_in_charge` (
  `id` varchar(36) NOT NULL,
  `trade` varchar(50) NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `appointed_by` varchar(36) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `appointed_at` datetime DEFAULT current_timestamp(),
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `officer_in_charge`
--

INSERT INTO `officer_in_charge` (`id`, `trade`, `user_id`, `appointed_by`, `is_active`, `appointed_at`, `created_at`, `updated_at`) VALUES
('317890d8-306f-4f1e-a7d9-220cf7cf69b9', 'Computer Technician', '1b514baf-ebde-4fcc-b838-902659c5c3e3', 'user-slaf-admin', 0, '2026-08-10 11:07:43', '2026-08-10 11:07:43', '2026-08-31 10:30:24'),
('6caf2577-3e76-4047-a783-0ee799c7fae1', 'Administrative', 'ac814c9f-08ef-476f-8de4-15192d2e7f71', 'user-slaf-admin', 1, '2026-09-21 07:18:28', '2026-09-21 07:18:28', '2026-09-21 07:18:28');

-- --------------------------------------------------------

--
-- Table structure for table `parade_states`
--

CREATE TABLE `parade_states` (
  `id` varchar(36) NOT NULL,
  `student_id` varchar(36) NOT NULL,
  `date` date NOT NULL,
  `status` varchar(30) NOT NULL,
  `remarks` text DEFAULT NULL,
  `updated_by` varchar(36) DEFAULT NULL,
  `submission_id` varchar(36) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `parade_type` varchar(20) DEFAULT 'MORNING',
  `morning_status` varchar(30) DEFAULT NULL,
  `status_changed` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `parade_states`
--

INSERT INTO `parade_states` (`id`, `student_id`, `date`, `status`, `remarks`, `updated_by`, `submission_id`, `created_at`, `updated_at`, `parade_type`, `morning_status`, `status_changed`) VALUES
('0718748b-c836-45e1-9191-0ca16294ec44', '321a9e7c-95cc-4650-8147-afcf0757a5b3', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('09503525-1fa2-4b86-aa0f-5f86973800c7', 'd9f8c58f-5f7c-4f23-a51d-337fe13e7e40', '2026-09-21', 'Present', '', 'user-slaf-admin', '735f6744-4570-4854-8a7d-f1b84ef8fe3f', '2026-09-21 07:17:47', '2026-09-21 07:17:47', 'MORNING', NULL, 0),
('097ab181-09e4-4ea0-bd8d-97cba2833299', '56ab9898-66d0-4a4e-bbec-294e14953e4e', '2018-07-30', 'Active', 'Initial registration record', 'user-slaf-admin', NULL, '2026-10-26 04:22:34', '2026-10-26 04:22:34', 'MORNING', NULL, 0),
('09ff21fd-547b-4cdf-b77c-9a6e87736c44', '3b0e40ad-cfbf-4df7-804d-2c686c40ad2f', '2026-08-12', 'Leave', '', 'user-slaf-admin', 'e303ba0c-ae43-4cc3-9c83-7e5bd50b13e3', '2026-08-12 04:36:15', '2026-08-12 04:36:49', 'MORNING', NULL, 0),
('109660da-e435-4e6e-b077-add1b103cd70', '512aa119-c9ef-437e-90e3-eaf3af3c5173', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('10b0e1eb-f9ed-4fa6-a435-539f7be45cb3', '3b0e40ad-cfbf-4df7-804d-2c686c40ad2f', '2026-08-11', 'Present', '', 'user-slaf-admin', '8e60adda-1391-4592-b0c5-ef4bbad98862', '2026-08-11 15:16:58', '2026-08-11 15:16:58', 'MORNING', NULL, 0),
('11722abc-b664-4c38-b2c2-b8b730992c13', '20797436-0920-4880-99f6-10ed21333662', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('11ca75f4-a840-4f33-97ea-36117f0903ad', '85647492-ad67-4aa4-a1b4-1d1ac29b1c47', '2026-09-21', 'Present', '', 'user-slaf-admin', '735f6744-4570-4854-8a7d-f1b84ef8fe3f', '2026-09-21 07:17:47', '2026-09-21 07:17:47', 'MORNING', NULL, 0),
('1562383b-901e-4bd3-b175-c63555bd7f50', 'd9f8c58f-5f7c-4f23-a51d-337fe13e7e40', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('181b18b6-713a-4378-a548-8455583d2ec2', '9affc12f-83f3-41ae-b019-7ac9684da0e5', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('182c496e-bf0b-4369-b920-6d07d25351b9', '3b0e40ad-cfbf-4df7-804d-2c686c40ad2f', '2026-09-16', 'Present', '', 'user-slaf-admin', '30e8d3c9-7ebc-4890-ba9a-8f6d460e498f', '2026-09-16 11:23:48', '2026-09-16 11:23:48', 'MORNING', NULL, 0),
('1a4d0e4b-360f-415a-9120-82a0d8818465', 'e1650c87-f565-471c-85e8-a157df7dc81b', '2026-08-12', 'AWOL', '', 'user-slaf-admin', 'e303ba0c-ae43-4cc3-9c83-7e5bd50b13e3', '2026-08-12 04:36:15', '2026-08-12 04:36:49', 'MORNING', NULL, 0),
('1bba90e5-447c-447e-bf11-5dd0d778edc4', '5eca75db-051f-4ffb-b04b-b942fbc3d286', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('1dce7cd6-4b7b-44bb-8a2f-2de99820d4fe', 'e59d3871-3fa2-44db-bcb0-068ba53fe6e1', '2026-08-17', 'Present', '', 'user-slaf-admin', '873e9481-6a19-4cf9-9f47-021abd7a66ec', '2026-08-17 10:50:49', '2026-08-17 10:50:49', 'MORNING', NULL, 0),
('1df39284-b2d4-4194-8731-7b77f5734031', '5d9bb916-b83c-41bf-b8a7-acca66750e0f', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:46', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('20303f37-cc3b-47c2-a09f-19cff3f339ff', 'd0fca849-4bf5-4c56-be89-38a21d42a187', '2026-09-17', 'Present', '', 'dc5d99d0-d369-4487-a9df-27b663200f83', '37682c5a-5e8b-473b-9f3e-1b70b5df5274', '2026-09-17 09:46:52', '2026-09-17 09:46:52', 'MORNING', NULL, 0),
('20cef291-3152-4e32-91cc-d297cc35ad0d', 'b7b7149d-5fd8-4791-9cb1-fe6178f720f9', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('22dbe9ac-3b37-46d4-82b7-bccb9282b975', 'b65eb892-ab14-4968-b2c1-f3f4d52b809a', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('24056ab5-4a4c-4a15-8eaf-c56b279bc98b', '07c1e28f-a13f-438c-9e11-28092b66e6e6', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('2608a44d-612a-472b-a803-47bfc4831303', '56ab9898-66d0-4a4e-bbec-294e14953e4e', '2026-10-26', 'Course Visit', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Course Visit', 0),
('2831f6c6-5b13-47d4-b155-e99259de0e6a', 'a2c507d9-531e-468b-832c-a97071a1e777', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('28a630dd-0a2c-4ca8-8cfc-86159248e0d3', '3b0e40ad-cfbf-4df7-804d-2c686c40ad2f', '2026-10-26', 'Course Visit', '', 'user-slaf-admin', '79e43022-46e5-436d-bf32-624d33b1c36a', '2026-10-26 04:48:29', '2026-10-26 04:48:29', 'MORNING', NULL, 0),
('299af8a7-81b2-48e5-9397-a8665945335f', 'fc2fdbed-f23f-4463-b73f-f5c67cc043e5', '2026-09-21', 'Present', '', 'user-slaf-admin', '735f6744-4570-4854-8a7d-f1b84ef8fe3f', '2026-09-21 07:17:47', '2026-09-21 07:17:47', 'MORNING', NULL, 0),
('2b3d9597-ef4d-48d6-8dd2-95e220bb353b', '9affc12f-83f3-41ae-b019-7ac9684da0e5', '2026-09-21', 'Present', '', 'user-slaf-admin', '735f6744-4570-4854-8a7d-f1b84ef8fe3f', '2026-09-21 07:17:47', '2026-09-21 07:17:47', 'MORNING', NULL, 0),
('2d94efc6-8df8-4d06-b915-2a708de551e2', 'd0fca849-4bf5-4c56-be89-38a21d42a187', '2026-08-12', 'AWOL', '', 'user-slaf-admin', 'e303ba0c-ae43-4cc3-9c83-7e5bd50b13e3', '2026-08-12 04:36:15', '2026-08-12 04:36:49', 'MORNING', NULL, 0),
('31d8bd6f-ad49-4340-a0e8-61a81526a06b', '6539b613-e3e2-4d92-ada6-c1992fac9a7f', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:46', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('35b36666-0580-4667-85fe-f3ef59f3ebc8', 'e59d3871-3fa2-44db-bcb0-068ba53fe6e1', '2026-10-26', 'Course Visit', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Course Visit', 0),
('35c5ad81-da2c-4445-bfa1-dd099cbe5a4a', '512aa119-c9ef-437e-90e3-eaf3af3c5173', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('4040e9a3-6e42-4588-97fa-d6e04e9c865f', 'a39af54b-7f76-4c85-aa11-2ffa17cd9a36', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('4470dd7d-4b10-417e-b3a3-482b93fbe927', '4847c54d-9b0c-496f-9682-cf79cefe57e3', '2026-10-26', 'Course Visit', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Course Visit', 0),
('448b18dc-85c5-42f2-8a30-e4c3e535a9cb', '4847c54d-9b0c-496f-9682-cf79cefe57e3', '2026-10-02', 'Active', 'Initial registration record', 'user-slaf-admin', NULL, '2026-10-26 04:16:20', '2026-10-26 04:16:20', 'MORNING', NULL, 0),
('44c37c88-527f-4ddc-8d0e-7137419a90a4', '07c1e28f-a13f-438c-9e11-28092b66e6e6', '2026-09-21', 'Present', '', 'user-slaf-admin', 'ac931c09-9bcf-47be-969a-84dfcccb7c31', '2026-09-21 05:22:52', '2026-09-21 05:22:52', 'MORNING', NULL, 0),
('45e0d1d7-dea1-4f66-b4d5-276dfbeed0d9', '012f5d6a-01f0-4b01-8a83-51a3d0a7dd37', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('463766b4-6b50-4594-91c4-305298d3021b', 'e1650c87-f565-471c-85e8-a157df7dc81b', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('4788ee88-b7c3-4a35-9395-cea9b189f9f8', '0f382899-cd69-4a25-b18f-a7817a9d1b1e', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('48ffc5bd-d038-4fd4-9f2c-6989c8869958', 'b7b7149d-5fd8-4791-9cb1-fe6178f720f9', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:46', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('4c2b5701-cd3c-4f43-beee-41f460709049', '49599a29-88c3-4e4f-bad3-ef2d05785b27', '2026-08-31', 'Present', '', 'user-slaf-admin', 'e8d58de6-4072-4245-a900-50bcd5e460a9', '2026-08-31 12:06:00', '2026-08-31 12:06:00', 'MORNING', NULL, 0),
('50f2f397-e32e-45cb-b94d-051e44b6d8cf', 'b65eb892-ab14-4968-b2c1-f3f4d52b809a', '2026-09-21', 'Present', '', 'user-slaf-admin', 'ac931c09-9bcf-47be-969a-84dfcccb7c31', '2026-09-21 05:22:52', '2026-09-21 05:22:52', 'MORNING', NULL, 0),
('53d6f862-458c-4660-a800-5afb710f452b', '3b0e40ad-cfbf-4df7-804d-2c686c40ad2f', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('551c792a-e719-44c3-9f58-43058454fcdd', 'e278bced-fe8c-4e93-a6e5-9cba4911af21', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:46', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('57d5914b-36e6-4cf3-9e28-bb6fafaa0692', '82bcf39e-4c1b-4202-aec8-eed9a4cd857b', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('593f12c6-0dab-41ec-a522-66dc34e6507d', 'e59d3871-3fa2-44db-bcb0-068ba53fe6e1', '2026-08-10', 'Present', '', 'user-slaf-admin', '90b9f2ea-ea8b-48ac-b994-9aaccb1c91d6', '2026-08-10 11:08:11', '2026-08-10 11:08:11', 'MORNING', NULL, 0),
('5c6e0d18-914d-4fdc-8f13-250c234af65e', '07c1e28f-a13f-438c-9e11-28092b66e6e6', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:46', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('5c97b76c-ab4f-4614-9f86-f0b5d9573dbb', 'e1650c87-f565-471c-85e8-a157df7dc81b', '2026-10-26', 'Course Visit', '', 'user-slaf-admin', '79e43022-46e5-436d-bf32-624d33b1c36a', '2026-10-26 04:48:29', '2026-10-26 04:48:29', 'MORNING', NULL, 0),
('5d748b9a-3c8b-417e-8a43-6d0406af9ad4', '5eca75db-051f-4ffb-b04b-b942fbc3d286', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('5fa9f999-36d4-420b-8d24-a3c1347f1571', '3b0e40ad-cfbf-4df7-804d-2c686c40ad2f', '2026-08-17', 'Leave', '', 'user-slaf-admin', '873e9481-6a19-4cf9-9f47-021abd7a66ec', '2026-08-17 10:50:49', '2026-08-17 10:50:49', 'MORNING', NULL, 0),
('612deceb-4ab8-4ae2-8a70-db34d691248b', '3b0e40ad-cfbf-4df7-804d-2c686c40ad2f', '2026-10-26', 'Course Visit', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Course Visit', 0),
('69de3a69-4da7-4031-8de6-108b55f59f34', 'd0fca849-4bf5-4c56-be89-38a21d42a187', '2026-10-26', 'Course Visit', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Course Visit', 0),
('6bf50bd1-474f-47bd-bf2b-40cfbca43944', '3b0e40ad-cfbf-4df7-804d-2c686c40ad2f', '2026-08-31', 'Present', '', 'user-slaf-admin', 'e8d58de6-4072-4245-a900-50bcd5e460a9', '2026-08-31 12:06:00', '2026-08-31 12:06:00', 'MORNING', NULL, 0),
('6d16de5d-1ef5-496d-ab66-a0cc853b5912', 'e59d3871-3fa2-44db-bcb0-068ba53fe6e1', '2026-08-31', 'Present', '', 'user-slaf-admin', 'e8d58de6-4072-4245-a900-50bcd5e460a9', '2026-08-31 12:06:00', '2026-08-31 12:06:00', 'MORNING', NULL, 0),
('70fa163c-b5e2-4102-a397-d39dbdce1e43', '5d9bb916-b83c-41bf-b8a7-acca66750e0f', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('7457fcf9-8578-418a-9c86-427aaba8d824', 'a39af54b-7f76-4c85-aa11-2ffa17cd9a36', '2026-09-21', 'Present', '', 'user-slaf-admin', '735f6744-4570-4854-8a7d-f1b84ef8fe3f', '2026-09-21 07:17:47', '2026-09-21 07:17:47', 'MORNING', NULL, 0),
('757a5628-cbb1-4cfd-83c2-900092c90b1f', '95899396-0f2b-4d68-ba1b-00657ec9e7fd', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('79a0616d-3676-4350-b20a-002e465d41bb', 'fc2fdbed-f23f-4463-b73f-f5c67cc043e5', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('7a1aae34-c5ef-4083-b96a-ddcc6472a0ec', '49599a29-88c3-4e4f-bad3-ef2d05785b27', '2026-08-11', 'Present', '', 'user-slaf-admin', '8e60adda-1391-4592-b0c5-ef4bbad98862', '2026-08-11 15:16:58', '2026-08-11 15:16:58', 'MORNING', NULL, 0),
('7bba1fa4-1eed-423e-b0dd-07b32863b301', 'f439ed35-6970-4829-a862-a844cdbfa50f', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('7c56d402-9388-4a70-8f3e-2820eb2e9af2', 'd0fca849-4bf5-4c56-be89-38a21d42a187', '2026-08-10', 'Present', '', 'user-slaf-admin', '90b9f2ea-ea8b-48ac-b994-9aaccb1c91d6', '2026-08-10 11:08:11', '2026-08-10 11:08:11', 'MORNING', NULL, 0),
('7c9e242e-0f09-40c2-b08c-a93d1dee68b5', '49599a29-88c3-4e4f-bad3-ef2d05785b27', '2026-09-16', 'Present', '', 'user-slaf-admin', '30e8d3c9-7ebc-4890-ba9a-8f6d460e498f', '2026-09-16 11:23:48', '2026-09-16 11:23:48', 'MORNING', NULL, 0),
('7d78c713-6951-4750-9192-e626d52e7b03', '012f5d6a-01f0-4b01-8a83-51a3d0a7dd37', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('80306da3-2214-4646-8862-5bb8cffa741b', '0d938fdd-8a24-4ad9-8287-c4ae606c7f53', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('810e1b45-351c-43dd-a0ee-d5ad24af8c76', 'a39af54b-7f76-4c85-aa11-2ffa17cd9a36', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('812795f1-0370-4ed5-b537-351ea793115d', '7c03548a-fe20-40b5-9ac0-6f1ee3d1a886', '2026-09-21', 'Sick Report', 'Fever', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 1),
('83e26cfe-504e-4836-9bbb-f30b95e72b23', '95899396-0f2b-4d68-ba1b-00657ec9e7fd', '2026-09-21', 'Present', '', 'user-slaf-admin', '735f6744-4570-4854-8a7d-f1b84ef8fe3f', '2026-09-21 07:17:47', '2026-09-21 07:17:47', 'MORNING', NULL, 0),
('852b5e64-7fd4-45af-a9e7-f7bd9c81d481', 'd0fca849-4bf5-4c56-be89-38a21d42a187', '2026-08-11', 'Present', '', 'user-slaf-admin', '8e60adda-1391-4592-b0c5-ef4bbad98862', '2026-08-11 15:16:58', '2026-08-11 15:16:58', 'MORNING', NULL, 0),
('86c739eb-6842-4e19-a7c2-f23627031abf', '49599a29-88c3-4e4f-bad3-ef2d05785b27', '2026-10-26', 'Course Visit', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Course Visit', 0),
('8df61b15-2ac2-435b-bade-e13270d75f42', 'd0fca849-4bf5-4c56-be89-38a21d42a187', '2026-08-31', 'Present', '', 'user-slaf-admin', 'e8d58de6-4072-4245-a900-50bcd5e460a9', '2026-08-31 12:06:00', '2026-08-31 12:06:00', 'MORNING', NULL, 0),
('8ec968d5-0f4f-4ed0-9dea-b2b30930cf14', '49599a29-88c3-4e4f-bad3-ef2d05785b27', '2026-08-17', 'Leave', '', 'user-slaf-admin', '873e9481-6a19-4cf9-9f47-021abd7a66ec', '2026-08-17 10:50:49', '2026-08-17 10:50:49', 'MORNING', NULL, 0),
('8f91c76d-cdf7-4672-bc63-cd177d79e293', 'a1000f6d-0983-4dea-b2fd-ffd32faaf80a', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('9102e493-cdb9-4c69-b1e0-84f42fd58103', 'e59d3871-3fa2-44db-bcb0-068ba53fe6e1', '2026-08-24', 'Course Visit', '', 'user-slaf-admin', 'bebc58fe-0fd4-488d-8041-679441786665', '2026-08-24 10:27:49', '2026-08-24 10:27:49', 'MORNING', NULL, 0),
('9103e4d2-eda2-4fef-989f-ae02d87fb265', 'a2f87162-d63c-4c11-b4f5-3aefba9afded', '2026-09-21', 'Present', '', 'user-slaf-admin', '735f6744-4570-4854-8a7d-f1b84ef8fe3f', '2026-09-21 07:17:47', '2026-09-21 07:17:47', 'MORNING', NULL, 0),
('932a35e3-32bd-4eb6-a014-4684084782fe', 'e59d3871-3fa2-44db-bcb0-068ba53fe6e1', '2026-08-11', 'Present', '', 'user-slaf-admin', '8e60adda-1391-4592-b0c5-ef4bbad98862', '2026-08-11 15:16:58', '2026-08-11 15:16:58', 'MORNING', NULL, 0),
('96546301-df0e-4d87-85bb-59e5bb9e7138', 'd0fca849-4bf5-4c56-be89-38a21d42a187', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('9656720c-6d37-4e18-8d08-0a127fa02a2e', 'd0fca849-4bf5-4c56-be89-38a21d42a187', '2026-10-26', 'Course Visit', '', 'user-slaf-admin', '79e43022-46e5-436d-bf32-624d33b1c36a', '2026-10-26 04:48:29', '2026-10-26 04:48:29', 'MORNING', NULL, 0),
('98c7e394-5243-449d-8272-fa906ee1290b', 'a2c507d9-531e-468b-832c-a97071a1e777', '2026-09-21', 'Present', '', 'user-slaf-admin', '735f6744-4570-4854-8a7d-f1b84ef8fe3f', '2026-09-21 07:17:47', '2026-09-21 07:17:47', 'MORNING', NULL, 0),
('997e6891-47b6-4a3d-9de1-fd3ec7d03072', 'a2f87162-d63c-4c11-b4f5-3aefba9afded', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('9a0a5f83-b36f-49de-9280-14aa60736d94', 'e1650c87-f565-471c-85e8-a157df7dc81b', '2026-08-11', 'Present', '', 'user-slaf-admin', '8e60adda-1391-4592-b0c5-ef4bbad98862', '2026-08-11 15:16:58', '2026-08-11 15:16:58', 'MORNING', NULL, 0),
('9b4995ab-c429-4661-8d8f-a2dcc59b85ed', 'f439ed35-6970-4829-a862-a844cdbfa50f', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('9bc7617e-8b70-4220-9d7b-befad88195bc', '3b0e40ad-cfbf-4df7-804d-2c686c40ad2f', '2026-08-24', 'Leave', '', 'user-slaf-admin', 'bebc58fe-0fd4-488d-8041-679441786665', '2026-08-24 10:27:49', '2026-08-24 10:27:49', 'MORNING', NULL, 0),
('9becb142-14e0-4d73-a056-cfab965203fc', '0d938fdd-8a24-4ad9-8287-c4ae606c7f53', '2026-09-21', 'Present', '', 'user-slaf-admin', '735f6744-4570-4854-8a7d-f1b84ef8fe3f', '2026-09-21 07:17:46', '2026-09-21 07:17:46', 'MORNING', NULL, 0),
('9dad5498-c691-4682-96bf-f4886f203a4c', 'a1000f6d-0983-4dea-b2fd-ffd32faaf80a', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('a0ac7ad1-4688-4cac-a33a-69bcf1e19938', 'e278bced-fe8c-4e93-a6e5-9cba4911af21', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('a1547757-7ea8-4c19-ad7d-0849ed655de1', '6539b613-e3e2-4d92-ada6-c1992fac9a7f', '2026-09-21', 'Present', '', 'user-slaf-admin', '735f6744-4570-4854-8a7d-f1b84ef8fe3f', '2026-09-21 07:17:47', '2026-09-21 07:17:47', 'MORNING', NULL, 0),
('a2617e07-ef6e-48a1-a452-4e6e27a65a35', '4847c54d-9b0c-496f-9682-cf79cefe57e3', '2026-10-26', 'Course Visit', '', 'user-slaf-admin', '79e43022-46e5-436d-bf32-624d33b1c36a', '2026-10-26 04:48:29', '2026-10-26 04:48:29', 'MORNING', NULL, 0),
('a639ec7a-c3cf-42fb-8fbb-87f2faa00a8d', '9affc12f-83f3-41ae-b019-7ac9684da0e5', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('a8fdd41b-cfb7-4aed-b576-dc94ce9dff04', '49599a29-88c3-4e4f-bad3-ef2d05785b27', '2026-08-12', 'Leave', '', 'user-slaf-admin', 'e303ba0c-ae43-4cc3-9c83-7e5bd50b13e3', '2026-08-12 04:36:15', '2026-08-12 04:36:49', 'MORNING', NULL, 0),
('ab148238-1fad-49d0-8bc3-69238a6ca022', '56ab9898-66d0-4a4e-bbec-294e14953e4e', '2026-10-26', 'Course Visit', '', 'user-slaf-admin', '79e43022-46e5-436d-bf32-624d33b1c36a', '2026-10-26 04:48:29', '2026-10-26 04:48:29', 'MORNING', NULL, 0),
('ae3b1b9e-1986-4843-b6b3-feea07cafd9d', 'e1650c87-f565-471c-85e8-a157df7dc81b', '2026-09-16', 'Present', '', 'user-slaf-admin', '30e8d3c9-7ebc-4890-ba9a-8f6d460e498f', '2026-09-16 11:23:48', '2026-09-16 11:23:48', 'MORNING', NULL, 0),
('af0e28fb-8087-40e4-bf9b-b36ae06bb195', '85647492-ad67-4aa4-a1b4-1d1ac29b1c47', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('afd8835d-fd78-4ee8-bb45-0af1e645750a', 'd0fca849-4bf5-4c56-be89-38a21d42a187', '2026-09-16', 'Present', '', 'user-slaf-admin', '30e8d3c9-7ebc-4890-ba9a-8f6d460e498f', '2026-09-16 11:23:48', '2026-09-16 11:23:48', 'MORNING', NULL, 0),
('b3ffb169-2d47-4f23-a78b-963c642fb18d', 'e1650c87-f565-471c-85e8-a157df7dc81b', '2026-08-17', 'Present', '', 'user-slaf-admin', '873e9481-6a19-4cf9-9f47-021abd7a66ec', '2026-08-17 10:50:49', '2026-08-17 10:50:49', 'MORNING', NULL, 0),
('b45c5006-2741-4f0d-b4ae-5c131d166e4e', '012f5d6a-01f0-4b01-8a83-51a3d0a7dd37', '2026-09-21', 'Present', '', 'user-slaf-admin', '735f6744-4570-4854-8a7d-f1b84ef8fe3f', '2026-09-21 07:17:46', '2026-09-21 07:17:46', 'MORNING', NULL, 0),
('b51730c2-51ef-4226-825a-ae267021a37f', '07c1e28f-a13f-438c-9e11-28092b66e6e6', '2025-03-01', 'Active', 'Initial registration record', 'user-slaf-admin', NULL, '2026-09-10 11:26:07', '2026-09-10 11:26:07', 'MORNING', NULL, 0),
('b527afca-f325-4eb9-9c25-1d8badee21a3', '82bcf39e-4c1b-4202-aec8-eed9a4cd857b', '2026-09-21', 'Present', '', 'user-slaf-admin', 'ac931c09-9bcf-47be-969a-84dfcccb7c31', '2026-09-21 05:22:52', '2026-09-21 05:22:52', 'MORNING', NULL, 0),
('b752be54-9b74-480a-8cab-a2cac2a37e80', '0d938fdd-8a24-4ad9-8287-c4ae606c7f53', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('b7e3d8c8-0670-45b3-9505-d4a5d5764aaa', 'e1650c87-f565-471c-85e8-a157df7dc81b', '2026-08-31', 'Present', '', 'user-slaf-admin', 'e8d58de6-4072-4245-a900-50bcd5e460a9', '2026-08-31 12:06:00', '2026-08-31 12:06:00', 'MORNING', NULL, 0),
('b8612ee5-1f4f-4558-b0ad-9e3650716bad', '321a9e7c-95cc-4650-8147-afcf0757a5b3', '2026-09-21', 'Present', '', 'user-slaf-admin', '735f6744-4570-4854-8a7d-f1b84ef8fe3f', '2026-09-21 07:17:46', '2026-09-21 07:17:46', 'MORNING', NULL, 0),
('bd52b4ca-adaa-4f93-acb2-a524a1bd9889', '49599a29-88c3-4e4f-bad3-ef2d05785b27', '2026-10-26', 'Course Visit', '', 'user-slaf-admin', '79e43022-46e5-436d-bf32-624d33b1c36a', '2026-10-26 04:48:29', '2026-10-26 04:48:29', 'MORNING', NULL, 0),
('bd793a04-cfc3-46fd-ad8e-029da76c98b5', 'e1650c87-f565-471c-85e8-a157df7dc81b', '2026-10-26', 'Present', 'Course visit', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Course Visit', 1),
('c2047090-4bbd-4006-b772-3f6838374813', 'a1000f6d-0983-4dea-b2fd-ffd32faaf80a', '2026-09-21', 'Present', '', 'user-slaf-admin', '735f6744-4570-4854-8a7d-f1b84ef8fe3f', '2026-09-21 07:17:47', '2026-09-21 07:17:47', 'MORNING', NULL, 0),
('c20c2a7d-a0d9-40b4-8e37-84ffd52c46c3', '82bcf39e-4c1b-4202-aec8-eed9a4cd857b', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:46', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('c608fe46-85da-4e9e-9170-8217f4066ce8', 'b65eb892-ab14-4968-b2c1-f3f4d52b809a', '2025-03-01', 'Active', 'Initial registration record', 'user-slaf-admin', NULL, '2026-09-10 11:32:31', '2026-09-10 11:32:31', 'MORNING', NULL, 0),
('c64e867a-5e1b-45a5-b7bf-d7552380dad3', '20797436-0920-4880-99f6-10ed21333662', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('c6eedc2b-7b0e-4e14-a735-b2099d3e6d35', '5eca75db-051f-4ffb-b04b-b942fbc3d286', '2026-09-21', 'Present', '', 'user-slaf-admin', '735f6744-4570-4854-8a7d-f1b84ef8fe3f', '2026-09-21 07:17:47', '2026-09-21 07:17:47', 'MORNING', NULL, 0),
('c7264914-b765-4602-82ab-077279d59478', '82bcf39e-4c1b-4202-aec8-eed9a4cd857b', '2025-03-01', 'Active', 'Initial registration record', 'user-slaf-admin', NULL, '2026-09-10 11:30:03', '2026-09-10 11:30:03', 'MORNING', NULL, 0),
('c72b6be1-9a5a-47ac-8db7-fe097984f48f', '5d9bb916-b83c-41bf-b8a7-acca66750e0f', '2025-03-01', 'Active', 'Initial registration record', 'user-slaf-admin', NULL, '2026-09-10 11:35:05', '2026-09-10 11:35:05', 'MORNING', NULL, 0),
('c7dc01f3-3a31-4d97-b4c0-6e1c7a3f5e8f', '49599a29-88c3-4e4f-bad3-ef2d05785b27', '2026-09-17', 'Present', '', 'dc5d99d0-d369-4487-a9df-27b663200f83', '37682c5a-5e8b-473b-9f3e-1b70b5df5274', '2026-09-17 09:46:52', '2026-09-17 09:46:52', 'MORNING', NULL, 0),
('c7e046cd-b958-4022-bea4-c8a86c6c552a', 'b7b7149d-5fd8-4791-9cb1-fe6178f720f9', '2026-09-21', 'Present', '', 'user-slaf-admin', '735f6744-4570-4854-8a7d-f1b84ef8fe3f', '2026-09-21 07:17:47', '2026-09-21 07:17:47', 'MORNING', NULL, 0),
('c94a8611-487a-48e5-bbd1-4d8e54729ac9', '3b0e40ad-cfbf-4df7-804d-2c686c40ad2f', '2026-09-17', 'Present', '', 'dc5d99d0-d369-4487-a9df-27b663200f83', '37682c5a-5e8b-473b-9f3e-1b70b5df5274', '2026-09-17 09:46:52', '2026-09-17 09:46:52', 'MORNING', NULL, 0),
('cf9226e2-47f1-4b11-a99e-ed8fa064b0f2', '49599a29-88c3-4e4f-bad3-ef2d05785b27', '2026-08-10', 'Present', '', 'user-slaf-admin', '90b9f2ea-ea8b-48ac-b994-9aaccb1c91d6', '2026-08-10 11:08:11', '2026-08-10 11:08:11', 'MORNING', NULL, 0),
('d28afc43-9f62-4bb1-9b5e-4e12255b0179', '6539b613-e3e2-4d92-ada6-c1992fac9a7f', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('d3a06acf-2b73-4858-82a9-77b53e80f00b', '49599a29-88c3-4e4f-bad3-ef2d05785b27', '2026-08-24', 'Present', '', 'user-slaf-admin', 'bebc58fe-0fd4-488d-8041-679441786665', '2026-08-24 10:27:49', '2026-08-24 10:27:49', 'MORNING', NULL, 0),
('d4f25f26-9c6d-4cd1-9d8f-7624727a2a07', 'b65eb892-ab14-4968-b2c1-f3f4d52b809a', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:46', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('d74ad27f-0ac6-43d5-b8a0-92bf59569650', 'a2c507d9-531e-468b-832c-a97071a1e777', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('d8564edb-546a-4d62-9157-5fb61f3c5f71', 'e3ab5331-1cd2-407e-a1e3-c357abc0263e', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('dadaf554-47c0-4a7c-a4bd-6bb7e5524664', 'e1650c87-f565-471c-85e8-a157df7dc81b', '2026-09-17', 'Present', '', 'dc5d99d0-d369-4487-a9df-27b663200f83', '37682c5a-5e8b-473b-9f3e-1b70b5df5274', '2026-09-17 09:46:52', '2026-09-17 09:46:52', 'MORNING', NULL, 0),
('db674028-4049-4d60-af2b-daf28a6673ab', '49599a29-88c3-4e4f-bad3-ef2d05785b27', '2026-09-21', 'Leave', 'leave', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 1),
('db6c4369-c69f-44ff-9936-6a6d036140e5', '3b0e40ad-cfbf-4df7-804d-2c686c40ad2f', '2026-08-10', 'Present', '', 'user-slaf-admin', '90b9f2ea-ea8b-48ac-b994-9aaccb1c91d6', '2026-08-10 11:08:11', '2026-08-10 11:08:11', 'MORNING', NULL, 0),
('de9761fd-b58b-4977-bbd8-2ace26f4d538', 'e1650c87-f565-471c-85e8-a157df7dc81b', '2026-05-02', 'Active', 'Initial registration record', 'user-slaf-admin', NULL, '2026-08-11 15:15:23', '2026-08-11 15:15:23', 'MORNING', NULL, 0),
('e26e287a-eaf9-42f3-a280-a15c5679b3fb', 'd0fca849-4bf5-4c56-be89-38a21d42a187', '2026-08-17', 'Present', '', 'user-slaf-admin', '873e9481-6a19-4cf9-9f47-021abd7a66ec', '2026-08-17 10:50:49', '2026-08-17 10:50:49', 'MORNING', NULL, 0),
('e357cb66-68b4-4e22-b5cd-0ae629b3d224', '0f382899-cd69-4a25-b18f-a7817a9d1b1e', '2026-09-21', 'Present', '', 'user-slaf-admin', '735f6744-4570-4854-8a7d-f1b84ef8fe3f', '2026-09-21 07:17:46', '2026-09-21 07:17:46', 'MORNING', NULL, 0),
('e39373c4-52f3-48d0-b097-007e0df72062', 'd0fca849-4bf5-4c56-be89-38a21d42a187', '2026-08-24', 'Present', '', 'user-slaf-admin', 'bebc58fe-0fd4-488d-8041-679441786665', '2026-08-24 10:27:49', '2026-08-24 10:27:49', 'MORNING', NULL, 0),
('e52a2c05-ab0f-4aef-b4a6-4584295acda7', '5d9bb916-b83c-41bf-b8a7-acca66750e0f', '2026-09-21', 'Present', '', 'user-slaf-admin', 'ac931c09-9bcf-47be-969a-84dfcccb7c31', '2026-09-21 05:22:52', '2026-09-21 05:22:52', 'MORNING', NULL, 0),
('e645b51b-3703-479b-abc9-4e0f7bd37ea7', 'd9f8c58f-5f7c-4f23-a51d-337fe13e7e40', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('e86c4a2c-6793-401b-9644-d8eaba98a6e3', 'a2f87162-d63c-4c11-b4f5-3aefba9afded', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('e8a8d241-3147-46c8-bb0d-e965df924afe', '321a9e7c-95cc-4650-8147-afcf0757a5b3', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('e8be4661-cc65-4d79-b7ac-f552de8291b9', '0f382899-cd69-4a25-b18f-a7817a9d1b1e', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('e90f4c95-07af-40b4-91b1-bf8d24a86838', 'e59d3871-3fa2-44db-bcb0-068ba53fe6e1', '2026-09-21', 'Hospital', 'Fever', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 1),
('ee69f7fa-69ca-4f2c-ae06-2b03be9b0e59', '95899396-0f2b-4d68-ba1b-00657ec9e7fd', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('f06ab516-34cf-447a-98f6-42c47f025bdc', '85647492-ad67-4aa4-a1b4-1d1ac29b1c47', '2026-09-21', 'Present', '', 'user-slaf-admin', '4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21 11:40:48', '2026-09-21 11:49:29', 'NIGHT', 'Present', 0),
('f0f1e0d6-d41d-49f4-8b07-3dde99526287', 'e59d3871-3fa2-44db-bcb0-068ba53fe6e1', '2026-10-26', 'Course Visit', '', 'user-slaf-admin', '79e43022-46e5-436d-bf32-624d33b1c36a', '2026-10-26 04:48:29', '2026-10-26 04:48:29', 'MORNING', NULL, 0),
('f13db4c2-680d-4806-8fe6-8524aff4424a', '7c03548a-fe20-40b5-9ac0-6f1ee3d1a886', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('f39a46b9-d223-4683-af1e-4a59876f0909', 'e3ab5331-1cd2-407e-a1e3-c357abc0263e', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:46', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('f7b34e82-9234-4283-9ee8-def7507bafb6', 'e59d3871-3fa2-44db-bcb0-068ba53fe6e1', '2026-09-16', 'Present', '', 'user-slaf-admin', '30e8d3c9-7ebc-4890-ba9a-8f6d460e498f', '2026-09-16 11:23:48', '2026-09-16 11:23:48', 'MORNING', NULL, 0),
('faff9716-a819-4dae-a9d4-31ef7d2a36e5', 'e1650c87-f565-471c-85e8-a157df7dc81b', '2026-08-24', 'Hospital', '', 'user-slaf-admin', 'bebc58fe-0fd4-488d-8041-679441786665', '2026-08-24 10:27:49', '2026-08-24 10:27:49', 'MORNING', NULL, 0),
('fb704d20-7339-4b4e-abaf-5ac3f0286525', 'e59d3871-3fa2-44db-bcb0-068ba53fe6e1', '2026-08-12', 'Hospital', '', 'user-slaf-admin', 'e303ba0c-ae43-4cc3-9c83-7e5bd50b13e3', '2026-08-12 04:36:15', '2026-08-12 04:36:49', 'MORNING', NULL, 0),
('fc2471e9-d006-4283-b0f4-990613d8ffb5', 'e3ab5331-1cd2-407e-a1e3-c357abc0263e', '2026-09-21', 'Present', '', 'user-slaf-admin', '735f6744-4570-4854-8a7d-f1b84ef8fe3f', '2026-09-21 07:17:47', '2026-09-21 07:17:47', 'MORNING', NULL, 0),
('fc46157b-a3a9-4bb3-80e3-88ed728f2159', 'fc2fdbed-f23f-4463-b73f-f5c67cc043e5', '2026-10-26', 'Present', '', 'user-slaf-admin', '64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26 04:49:45', '2026-10-26 04:51:13', 'NIGHT', 'Present', 0),
('fc53e76f-d5d1-4e72-8cf5-24575f46f7ac', 'e59d3871-3fa2-44db-bcb0-068ba53fe6e1', '2026-09-17', 'Present', '', 'dc5d99d0-d369-4487-a9df-27b663200f83', '37682c5a-5e8b-473b-9f3e-1b70b5df5274', '2026-09-17 09:46:52', '2026-09-17 09:46:52', 'MORNING', NULL, 0),
('fd563c74-7b93-45cb-b57f-14417c2ee528', '512aa119-c9ef-437e-90e3-eaf3af3c5173', '2026-09-21', 'Present', '', 'user-slaf-admin', '735f6744-4570-4854-8a7d-f1b84ef8fe3f', '2026-09-21 07:17:46', '2026-09-21 07:17:46', 'MORNING', NULL, 0);

-- --------------------------------------------------------

--
-- Table structure for table `parade_status_types`
--

CREATE TABLE `parade_status_types` (
  `id` varchar(36) NOT NULL,
  `code` varchar(50) NOT NULL,
  `label` varchar(100) NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `can_sit_exam` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `parade_status_types`
--

INSERT INTO `parade_status_types` (`id`, `code`, `label`, `is_active`, `created_at`, `updated_at`, `can_sit_exam`) VALUES
('3411d4f9-fab4-4ca1-baed-e6c26fbf5acf', 'COURSE_VISIT', 'Course Visit', 1, '2026-08-10 09:31:21', '2026-08-10 09:31:21', 0),
('3b15c2d5-90ab-45da-828c-2d61149b442d', 'AWOL', 'AWOL', 1, '2026-08-10 09:31:21', '2026-08-10 09:31:21', 0),
('9cd0c75f-c98b-40b2-b62c-feb1cfcd111c', 'TEMPORARY_DUTY', 'Temporary Duty', 1, '2026-08-10 09:31:21', '2026-08-10 09:31:21', 1),
('9d6e6df9-7108-409f-bbc9-f71e073eb19c', 'PRESENT', 'Present', 1, '2026-08-10 09:31:21', '2026-08-10 09:31:21', 1),
('9d95e6b2-46b0-40ab-b0bb-020e0057cff2', 'LEAVE', 'Leave', 1, '2026-08-10 09:31:21', '2026-08-10 09:31:21', 0),
('bb5e9617-73d8-4e69-97f2-55349dbdec0a', 'DETACHED_DUTY', 'Detached Duty', 1, '2026-08-10 09:31:21', '2026-08-10 09:31:21', 0),
('ddc9c225-ca7f-4fd6-8a9e-9dfe7d6cf5e0', 'SICK_REPORT', 'Sick Report', 1, '2026-08-10 09:31:21', '2026-08-10 09:31:21', 0),
('ee410901-cc42-4e15-a1f5-16168d220a7e', 'HOSPITAL', 'Hospital', 1, '2026-08-10 09:31:21', '2026-08-10 09:31:21', 0);

-- --------------------------------------------------------

--
-- Table structure for table `parade_submissions`
--

CREATE TABLE `parade_submissions` (
  `id` varchar(36) NOT NULL,
  `date` date NOT NULL,
  `trade` varchar(50) NOT NULL,
  `submitted_by` varchar(36) DEFAULT NULL,
  `approving_officer_id` varchar(36) DEFAULT NULL,
  `status` enum('DRAFT','SUBMITTED','APPROVED','REJECTED') NOT NULL DEFAULT 'DRAFT',
  `submitter_remarks` text DEFAULT NULL,
  `approver_remarks` text DEFAULT NULL,
  `rejection_reason` text DEFAULT NULL,
  `submitted_at` datetime DEFAULT NULL,
  `reviewed_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `course_id` varchar(36) DEFAULT NULL,
  `batch` varchar(30) DEFAULT NULL,
  `returned_by` varchar(36) DEFAULT NULL,
  `returned_at` datetime DEFAULT NULL,
  `parade_type` varchar(20) DEFAULT 'MORNING'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `parade_submissions`
--

INSERT INTO `parade_submissions` (`id`, `date`, `trade`, `submitted_by`, `approving_officer_id`, `status`, `submitter_remarks`, `approver_remarks`, `rejection_reason`, `submitted_at`, `reviewed_at`, `created_at`, `updated_at`, `course_id`, `batch`, `returned_by`, `returned_at`, `parade_type`) VALUES
('0e97b4ae-f50a-42eb-a7cb-ffeccad658bb', '2026-09-21', 'All', 'user-slaf-admin', 'dc5d99d0-d369-4487-a9df-27b663200f83', '', '', NULL, NULL, NULL, NULL, '2026-09-21 11:40:48', '2026-09-21 11:40:48', NULL, NULL, NULL, NULL, 'NIGHT'),
('2e40b81f-ea10-483b-a8a5-ad62ed096256', '2026-09-21', 'All', 'user-slaf-admin', 'dc5d99d0-d369-4487-a9df-27b663200f83', '', '', NULL, NULL, '2026-09-21 11:41:12', '2026-09-21 11:41:12', '2026-09-21 11:41:11', '2026-09-21 11:41:12', NULL, NULL, NULL, NULL, 'NIGHT'),
('30e8d3c9-7ebc-4890-ba9a-8f6d460e498f', '2026-09-16', 'Computer Technician', 'user-slaf-admin', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'APPROVED', '', '', NULL, '2026-09-16 11:23:48', '2026-09-16 11:27:17', '2026-09-16 11:23:48', '2026-09-16 11:27:17', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '169', NULL, NULL, 'MORNING'),
('37682c5a-5e8b-473b-9f3e-1b70b5df5274', '2026-09-17', 'Computer Technician', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'APPROVED', '', '', NULL, '2026-09-17 09:46:52', '2026-09-17 10:28:47', '2026-09-17 09:46:52', '2026-09-17 10:28:47', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '169', NULL, NULL, 'MORNING'),
('4ff92b2c-7eb8-49e8-b774-f99511504874', '2026-09-21', 'All', 'user-slaf-admin', 'dc5d99d0-d369-4487-a9df-27b663200f83', '', '', NULL, NULL, '2026-09-21 11:49:29', '2026-09-21 11:49:29', '2026-09-21 11:49:29', '2026-09-21 11:49:29', NULL, NULL, NULL, NULL, 'NIGHT'),
('64883a03-c3fd-4d42-bddf-8923276d535f', '2026-10-26', 'All', 'user-slaf-admin', 'dc5d99d0-d369-4487-a9df-27b663200f83', '', '', NULL, NULL, '2026-10-26 04:51:13', '2026-10-26 04:51:13', '2026-10-26 04:51:13', '2026-10-26 04:51:13', NULL, NULL, NULL, NULL, 'NIGHT'),
('6e4223ff-0743-4372-980e-d66a6566c351', '2026-09-21', 'All', 'user-slaf-admin', 'dc5d99d0-d369-4487-a9df-27b663200f83', '', '', NULL, NULL, '2026-09-21 11:42:32', '2026-09-21 11:42:32', '2026-09-21 11:42:32', '2026-09-21 11:42:32', NULL, NULL, NULL, NULL, 'NIGHT'),
('735f6744-4570-4854-8a7d-f1b84ef8fe3f', '2026-09-21', 'Administrative', 'user-slaf-admin', NULL, 'SUBMITTED', '', NULL, NULL, '2026-09-21 07:17:47', NULL, '2026-09-21 07:17:46', '2026-09-21 07:17:47', NULL, '174 D', NULL, NULL, 'MORNING'),
('79e43022-46e5-436d-bf32-624d33b1c36a', '2026-10-26', 'Computer Technician', 'user-slaf-admin', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'SUBMITTED', '', NULL, NULL, '2026-10-26 04:48:29', NULL, '2026-10-26 04:48:29', '2026-10-26 04:48:29', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '169', NULL, NULL, 'MORNING'),
('873e9481-6a19-4cf9-9f47-021abd7a66ec', '2026-08-17', 'Computer Technician', 'user-slaf-admin', '1b514baf-ebde-4fcc-b838-902659c5c3e3', 'APPROVED', '', '', NULL, '2026-08-17 10:50:49', '2026-08-17 10:53:46', '2026-08-17 10:50:49', '2026-08-17 10:53:46', NULL, NULL, NULL, NULL, 'MORNING'),
('8e60adda-1391-4592-b0c5-ef4bbad98862', '2026-08-11', 'Computer Technician', 'user-slaf-admin', '1b514baf-ebde-4fcc-b838-902659c5c3e3', 'APPROVED', 'NA', '', NULL, '2026-08-11 15:16:58', '2026-08-11 15:17:55', '2026-08-11 15:16:58', '2026-08-11 15:17:55', NULL, NULL, NULL, NULL, 'MORNING'),
('90b9f2ea-ea8b-48ac-b994-9aaccb1c91d6', '2026-08-10', 'Computer Technician', 'user-slaf-admin', '1b514baf-ebde-4fcc-b838-902659c5c3e3', 'APPROVED', 'Parade state', '', NULL, '2026-08-10 11:08:11', '2026-08-10 11:08:56', '2026-08-10 11:08:11', '2026-08-10 11:08:56', NULL, NULL, NULL, NULL, 'MORNING'),
('9df52d15-15da-47a4-a1c4-0186b6bd30ef', '2026-10-26', 'All', 'user-slaf-admin', 'dc5d99d0-d369-4487-a9df-27b663200f83', '', '', NULL, NULL, NULL, NULL, '2026-10-26 04:51:11', '2026-10-26 04:51:11', NULL, NULL, NULL, NULL, 'NIGHT'),
('ac931c09-9bcf-47be-969a-84dfcccb7c31', '2026-09-21', 'Account Assistant', 'user-slaf-admin', 'user-slaf-admin', 'APPROVED', '', '', NULL, '2026-09-21 05:22:52', '2026-09-21 07:17:30', '2026-09-21 05:22:52', '2026-09-21 07:17:30', '0b7a2bcf-5ac0-4590-a777-05febce54289', '2/2026', NULL, NULL, 'MORNING'),
('bebc58fe-0fd4-488d-8041-679441786665', '2026-08-24', 'Computer Technician', 'user-slaf-admin', '1b514baf-ebde-4fcc-b838-902659c5c3e3', 'APPROVED', '', '', NULL, '2026-08-24 10:27:49', '2026-08-24 10:29:52', '2026-08-24 10:27:49', '2026-08-24 10:29:52', NULL, NULL, NULL, NULL, 'MORNING'),
('e303ba0c-ae43-4cc3-9c83-7e5bd50b13e3', '2026-08-12', 'Computer Technician', 'user-slaf-admin', '1b514baf-ebde-4fcc-b838-902659c5c3e3', 'SUBMITTED', 'dfd', NULL, NULL, '2026-08-12 04:43:24', NULL, '2026-08-12 04:36:15', '2026-08-12 04:43:24', NULL, NULL, NULL, NULL, 'MORNING'),
('e8d58de6-4072-4245-a900-50bcd5e460a9', '2026-08-31', 'Computer Technician', 'user-slaf-admin', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'APPROVED', 'thyuykf', '', NULL, '2026-08-31 12:06:00', '2026-08-31 12:19:28', '2026-08-31 12:06:00', '2026-08-31 12:19:28', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '169', NULL, NULL, 'MORNING'),
('fb8945d7-0f0b-4921-8e7a-7d33c340f8f4', '2026-10-26', 'All', 'user-slaf-admin', 'dc5d99d0-d369-4487-a9df-27b663200f83', '', '', NULL, NULL, NULL, NULL, '2026-10-26 04:49:45', '2026-10-26 04:49:45', NULL, NULL, NULL, NULL, 'NIGHT');

-- --------------------------------------------------------

--
-- Table structure for table `password_history`
--

CREATE TABLE `password_history` (
  `id` varchar(36) NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `hashed_password` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `password_history`
--

INSERT INTO `password_history` (`id`, `user_id`, `hashed_password`, `created_at`) VALUES
('19886d85-c9a9-4857-936c-0ef1f68030d4', '1b514baf-ebde-4fcc-b838-902659c5c3e3', '$2b$12$Ly.4HmnyZ6pXwwhYszCwBOGmzSNyghXl2.Djh8rqWj0b8CRWP5Vxi', '2026-08-10 11:06:34'),
('1a5d6d69-365d-497a-8c1e-26bd2382dc52', 'c5f0985e-45f7-4086-9bb7-06019de7cea3', '$2b$12$tx7PjhuM88cE9rybDVgeGufWRXsszTvA3ZSzS/r83fYWB2qc8jdmK', '2026-10-26 04:45:55'),
('c5395c57-b828-49d0-8772-d9643fc8f144', 'f6f853a0-a3db-481e-bb6b-95e469c45dc8', '$2b$12$zwNigOZ3O9heds1wiBurUevacRWsaZRtr7vi793cOoI5eFmAgiCdK', '2026-08-11 15:32:32'),
('e6e843e6-fa8c-4b16-a58f-5717ea8c0abc', 'c96d5ee9-93ee-41cc-b9e6-f31ecba02f4e', '$2b$12$IC6Jk4iBB8p7tYHuC2q8yOIMlCd9VDkgXWHybZSNU7kBIviYnVQlm', '2026-09-21 05:40:48'),
('f4ee0c51-0105-44e7-9ebe-7458662c0d9d', 'dc5d99d0-d369-4487-a9df-27b663200f83', '$2b$12$jyb5sjFwZYCgxNE3AZ8tRudeKBJyczgzxUQwClxWrPNU2lDPWu8ee', '2026-08-10 11:23:21');

-- --------------------------------------------------------

--
-- Table structure for table `permissions`
--

CREATE TABLE `permissions` (
  `id` varchar(36) NOT NULL,
  `name` varchar(100) NOT NULL,
  `code` varchar(100) NOT NULL,
  `module` varchar(50) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `permissions`
--

INSERT INTO `permissions` (`id`, `name`, `code`, `module`, `description`, `created_at`) VALUES
('perm-academic-read', 'Read Grades & Timetable', 'academic:read', 'General', 'Ability to view schedules and marks', '2026-08-10 09:31:20'),
('perm-academic-write', 'Manage Academics', 'academic:write', 'General', 'Ability to record marks and edit timetables', '2026-08-10 09:31:20'),
('perm-audit-read', 'Read Audit Logs', 'system:audit', 'General', 'Ability to review security logs', '2026-08-10 09:31:20'),
('perm-occurrence-delete', 'Delete Personal Occurrences', 'personal_occurrence:delete', 'General', 'Ability to delete personal occurrence records', '2026-08-14 11:42:49'),
('perm-occurrence-read', 'Read Personal Occurrences', 'personal_occurrence:read', 'General', 'Ability to view trainee personal occurrence records', '2026-08-14 11:42:49'),
('perm-occurrence-write', 'Create/Edit Personal Occurrences', 'personal_occurrence:write', 'General', 'Ability to record or edit personal occurrences', '2026-08-14 11:42:49'),
('perm-parade-approve', 'Approve Parade State', 'parade:approve', 'General', 'Ability to approve or reject submitted parade states as Officer I/C', '2026-08-10 09:31:20'),
('perm-parade-officers', 'Manage Officer I/C Assignments', 'parade:manage_officers', 'General', 'Ability to appoint and remove Officer I/C assignments by trade', '2026-08-10 09:31:20'),
('perm-parade-read', 'Read Parade State', 'parade:read', 'General', 'Ability to view daily parade state strength', '2026-08-10 09:31:20'),
('perm-parade-write', 'Update Parade State', 'parade:write', 'General', 'Ability to record daily status boards', '2026-08-10 09:31:20'),
('perm-reports-read', 'Read Reports & Analytics', 'reports:read', 'General', 'Ability to generate reports and analytics', '2026-08-10 11:16:25'),
('perm-room-read', 'Read Accommodation Map', 'room:read', 'General', 'Ability to inspect vacancy charts', '2026-08-10 09:31:20'),
('perm-room-write', 'Allocate Accommodation', 'room:write', 'General', 'Ability to edit room registers and transfers', '2026-08-10 09:31:20'),
('perm-student-read', 'Read Student Profile', 'student:read', 'General', 'Ability to view trainee data', '2026-08-10 09:31:20'),
('perm-student-write', 'Create/Edit Student Profile', 'student:write', 'General', 'Ability to add or edit trainee data', '2026-08-10 09:31:20');

-- --------------------------------------------------------

--
-- Table structure for table `personal_occurrences`
--

CREATE TABLE `personal_occurrences` (
  `id` varchar(36) NOT NULL,
  `trainee_id` varchar(36) NOT NULL,
  `occurrence_type` varchar(30) NOT NULL,
  `occurrence_date` date NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `remarks` text DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  `created_by` varchar(36) DEFAULT NULL,
  `updated_by` varchar(36) DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `personal_occurrences`
--

INSERT INTO `personal_occurrences` (`id`, `trainee_id`, `occurrence_type`, `occurrence_date`, `title`, `description`, `remarks`, `status`, `created_by`, `updated_by`, `deleted_at`, `created_at`, `updated_at`) VALUES
('047610ca-fa41-4da6-8d20-ff286394d418', '012f5d6a-01f0-4b01-8a83-51a3d0a7dd37', 'ACHIEVEMENT', '2026-09-15', 'Test Achievement Automated Verification', 'Outstanding performance in technical examination', 'Commendation recommended', 'Archived', '1b514baf-ebde-4fcc-b838-902659c5c3e3', '1b514baf-ebde-4fcc-b838-902659c5c3e3', '2026-09-15 11:14:57', '2026-09-15 11:14:57', '2026-09-15 11:14:57'),
('0c6d823b-67af-43b7-b9f7-3f8bd208a4f7', '012f5d6a-01f0-4b01-8a83-51a3d0a7dd37', 'ACHIEVEMENT', '2026-09-15', 'Test REST Endpoint Occurrence', 'Verified via REST API TestClient', 'Testing remarks', 'Archived', 'user-slaf-admin', 'user-slaf-admin', '2026-09-15 11:20:47', '2026-09-15 11:20:47', '2026-09-15 11:20:47'),
('6c9dbe05-270a-4149-ab4e-c29ec7cb2b52', '56ab9898-66d0-4a4e-bbec-294e14953e4e', 'MISCONDUCT_OFFENSE', '2020-10-26', 'Absent', 'Unauthorized exit from camp', '7 Detention', 'Active', 'user-slaf-admin', NULL, NULL, '2026-10-26 04:24:05', '2026-10-26 04:24:05');

-- --------------------------------------------------------

--
-- Table structure for table `ranks`
--

CREATE TABLE `ranks` (
  `id` varchar(36) NOT NULL,
  `code` varchar(50) NOT NULL,
  `label` varchar(100) NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ranks`
--

INSERT INTO `ranks` (`id`, `code`, `label`, `is_active`, `created_at`, `updated_at`) VALUES
('rank-ac', 'AC', 'AC', 1, '2026-08-10 09:31:21', '2026-09-15 12:07:12'),
('rank-acm', 'ACM', 'ACM', 1, '2026-09-15 12:07:12', '2026-09-15 12:07:12'),
('rank-aircdre', 'AIRCDRE', 'AIRCDRE', 1, '2026-09-15 12:07:12', '2026-09-15 12:07:12'),
('rank-am', 'AM', 'AM', 1, '2026-09-15 12:07:12', '2026-09-15 12:07:12'),
('rank-avm', 'AVM', 'AVM', 1, '2026-09-15 12:07:12', '2026-09-15 12:07:12'),
('rank-cpl', 'CPL', 'CPL', 1, '2026-08-10 09:31:21', '2026-09-15 12:07:12'),
('rank-fgoff', 'FGOFF', 'FGOFF', 1, '2026-09-15 12:07:12', '2026-09-15 12:07:12'),
('rank-fltlt', 'FLTLT', 'FLTLT', 1, '2026-09-15 12:07:12', '2026-09-15 12:07:12'),
('rank-fsgt', 'FSGT', 'FSGT', 1, '2026-08-10 09:31:21', '2026-09-15 12:07:12'),
('rank-gpcapt', 'GP CAPT', 'GP CAPT', 1, '2026-09-15 12:07:12', '2026-09-15 12:07:12'),
('rank-lac', 'LAC', 'LAC', 1, '2026-08-10 09:31:21', '2026-09-15 12:07:12'),
('rank-mwo', 'MWO', 'MWO', 1, '2026-09-15 12:07:12', '2026-09-15 12:07:12'),
('rank-ocdt', 'O/CADET', 'O/CADET', 1, '2026-09-15 12:07:12', '2026-09-15 12:07:12'),
('rank-pltoff', 'PLTOFF', 'PLTOFF', 1, '2026-09-15 12:07:12', '2026-09-15 12:07:12'),
('rank-sgt', 'SGT', 'SGT', 1, '2026-08-10 09:31:21', '2026-09-15 12:07:12'),
('rank-sqnldr', 'SQNLDR', 'SQNLDR', 1, '2026-09-15 12:07:12', '2026-09-15 12:07:12'),
('rank-wgcdr', 'WG CDR', 'WG CDR', 1, '2026-09-15 12:07:12', '2026-09-15 12:07:12'),
('rank-wo', 'WO', 'WO', 1, '2026-08-10 09:31:21', '2026-09-15 12:07:12');

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `id` varchar(36) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`id`, `name`, `description`, `is_active`, `created_at`, `updated_at`) VALUES
('role-academic', 'Academic Section', 'Manages courses, subject syllabus, lesson plans, exams, and marks entry.', 1, '2026-08-10 09:31:20', '2026-08-10 09:31:20'),
('role-accommodation', 'Accommodation Officer', 'Manages billets, rooms, beds, and trainee room allocations.', 1, '2026-08-10 09:31:20', '2026-08-10 09:31:20'),
('role-co', 'Commanding Officer', 'High-level dashboard visibility, executive reports, and approval rights.', 1, '2026-08-10 09:31:20', '2026-08-10 09:31:20'),
('role-discipline', 'Discipline Section', 'Manages daily parade state, student profiles, statuses, and logs.', 1, '2026-08-10 09:31:20', '2026-08-10 09:31:20'),
('role-instructor', 'Instructor', 'Manages class registers, lesson plans, and marks entry.', 1, '2026-08-10 09:31:20', '2026-08-10 09:31:20'),
('role-off i/c', 'Officer In Commanding', 'High-level dashboard visibility, executive reports, and approval rights.', 1, '2026-08-10 09:31:20', '2026-08-10 09:31:20'),
('role-super-admin', 'Super Administrator', 'Full control over users, security configurations, backups, and settings.', 1, '2026-08-10 09:31:20', '2026-08-10 09:31:20'),
('role-sys-admin', 'System Administrator', 'Manages core database entries, logs, and system operations.', 1, '2026-08-10 09:31:20', '2026-08-10 09:31:20'),
('role-viewer', 'Viewer', 'Read-only access to dashboard data and reports.', 1, '2026-08-10 09:31:20', '2026-08-10 09:31:20');

-- --------------------------------------------------------

--
-- Table structure for table `role_permissions`
--

CREATE TABLE `role_permissions` (
  `role_id` varchar(36) NOT NULL,
  `permission_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `role_permissions`
--

INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES
('role-academic', 'perm-academic-read'),
('role-academic', 'perm-academic-write'),
('role-academic', 'perm-parade-read'),
('role-academic', 'perm-reports-read'),
('role-academic', 'perm-student-read'),
('role-accommodation', 'perm-parade-read'),
('role-accommodation', 'perm-reports-read'),
('role-accommodation', 'perm-room-read'),
('role-accommodation', 'perm-room-write'),
('role-accommodation', 'perm-student-read'),
('role-co', 'perm-occurrence-delete'),
('role-co', 'perm-occurrence-read'),
('role-co', 'perm-occurrence-write'),
('role-co', 'perm-parade-approve'),
('role-co', 'perm-parade-officers'),
('role-co', 'perm-parade-read'),
('role-co', 'perm-parade-write'),
('role-co', 'perm-reports-read'),
('role-co', 'perm-student-read'),
('role-co', 'perm-student-write'),
('role-discipline', 'perm-occurrence-delete'),
('role-discipline', 'perm-occurrence-read'),
('role-discipline', 'perm-occurrence-write'),
('role-discipline', 'perm-parade-approve'),
('role-discipline', 'perm-parade-officers'),
('role-discipline', 'perm-parade-read'),
('role-discipline', 'perm-parade-write'),
('role-discipline', 'perm-reports-read'),
('role-discipline', 'perm-student-read'),
('role-discipline', 'perm-student-write'),
('role-instructor', 'perm-academic-read'),
('role-instructor', 'perm-academic-write'),
('role-instructor', 'perm-occurrence-read'),
('role-instructor', 'perm-occurrence-write'),
('role-instructor', 'perm-parade-approve'),
('role-instructor', 'perm-parade-read'),
('role-instructor', 'perm-parade-write'),
('role-instructor', 'perm-reports-read'),
('role-instructor', 'perm-student-read'),
('role-super-admin', 'perm-academic-read'),
('role-super-admin', 'perm-academic-write'),
('role-super-admin', 'perm-audit-read'),
('role-super-admin', 'perm-occurrence-delete'),
('role-super-admin', 'perm-occurrence-read'),
('role-super-admin', 'perm-occurrence-write'),
('role-super-admin', 'perm-parade-approve'),
('role-super-admin', 'perm-parade-officers'),
('role-super-admin', 'perm-parade-read'),
('role-super-admin', 'perm-parade-write'),
('role-super-admin', 'perm-reports-read'),
('role-super-admin', 'perm-room-read'),
('role-super-admin', 'perm-room-write'),
('role-super-admin', 'perm-student-read'),
('role-super-admin', 'perm-student-write'),
('role-sys-admin', 'perm-academic-read'),
('role-sys-admin', 'perm-academic-write'),
('role-sys-admin', 'perm-audit-read'),
('role-sys-admin', 'perm-occurrence-delete'),
('role-sys-admin', 'perm-occurrence-read'),
('role-sys-admin', 'perm-occurrence-write'),
('role-sys-admin', 'perm-parade-approve'),
('role-sys-admin', 'perm-parade-officers'),
('role-sys-admin', 'perm-parade-read'),
('role-sys-admin', 'perm-parade-write'),
('role-sys-admin', 'perm-reports-read'),
('role-sys-admin', 'perm-room-read'),
('role-sys-admin', 'perm-room-write'),
('role-sys-admin', 'perm-student-read'),
('role-sys-admin', 'perm-student-write'),
('role-viewer', 'perm-parade-read'),
('role-viewer', 'perm-reports-read'),
('role-viewer', 'perm-student-read');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` varchar(36) NOT NULL,
  `service_number` varchar(30) NOT NULL,
  `initials` varchar(30) DEFAULT NULL,
  `full_name` varchar(255) NOT NULL,
  `nic` varchar(20) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `rank` varchar(50) DEFAULT NULL,
  `trade` varchar(50) DEFAULT NULL,
  `course_id` varchar(36) DEFAULT NULL,
  `batch` varchar(30) DEFAULT NULL,
  `joining_date` date DEFAULT NULL,
  `passing_out_date` date DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `emergency_contact_name` varchar(100) DEFAULT NULL,
  `emergency_contact_phone` varchar(20) DEFAULT NULL,
  `blood_group` varchar(10) DEFAULT NULL,
  `medical_category` varchar(50) DEFAULT NULL,
  `religion` varchar(30) DEFAULT NULL,
  `nationality` varchar(30) DEFAULT NULL,
  `permanent_address` text DEFAULT NULL,
  `temporary_address` text DEFAULT NULL,
  `profile_photo_path` varchar(255) DEFAULT NULL,
  `qr_code_data` text DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `service_number`, `initials`, `full_name`, `nic`, `dob`, `gender`, `rank`, `trade`, `course_id`, `batch`, `joining_date`, `passing_out_date`, `status`, `phone`, `email`, `emergency_contact_name`, `emergency_contact_phone`, `blood_group`, `medical_category`, `religion`, `nationality`, `permanent_address`, `temporary_address`, `profile_photo_path`, `qr_code_data`, `created_at`, `updated_at`, `deleted_at`) VALUES
('012f5d6a-01f0-4b01-8a83-51a3d0a7dd37', '50833', 'SLY', 'LAKSHAN', '200003103357', '2000-01-31', 'Male', 'CPL', 'Administrative', '66e284eb-945e-48d7-8c5f-f1d3de0965af', '170', '2026-08-04', NULL, 'Active', NULL, NULL, 'CHANDANA', '0770709587', 'O+', 'A4G1', 'Buddhist', 'Sri Lankan', 'GALKETIYA,KURUWAMBA,BIBILE', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACF0lEQVR4nO1aS47bMAx9pAVkqdwgR7Fv0CMVvZl1lDnAAPYyQAIWpGQ3QbtQB5gJW/MBCSTlLQhSpPgJCTpRuJcJBJVDWYjr0g0OKkJZ3eCgQkENCTThTjStRMC6HU+hLFfXZRTFoskEnQTlPAhNGOxUnMnaA/6/qWtzIZHlTkC+kh2bv3mT9bjU9PvRcAPWBMH6FQJwUPFha5F+/lyDcegVTi5hFpFZF6PcYO+WHYvo9isE6AD3kI5ALZb7nXW5noS+L2jZocKZrDh6JJTHI8sy1KOy+JKVD0/FlqMPGgkt/mnevgAPgdHy+zmUxW58606CrAWXokzDjZDfk6jxPlUADir+1rfGzU7mTNW3ZDEvGyR8y5e1pAbBrDFRs8MKs+C+nV8uKwcV+PU8vVn+1/qE1nmyOjmU5ey6FE3ey2X3supqV5LZskNXsh6YipYT5vZ41YeqZvCWJ9oPEQk9UUUsCKqNyuVKGN9Ou8m0/PIk65Gpyb6bQdazrk5C1UYr6VsW75a7nHDHVh23vP2BMr9cVg4qnmfHdb5VzuZbqbYxYnbsrToWxfLUea++lbVYDt9yOjue6zbVvny8Wy6t9Qwtv6zUkh+XqLd8z4436KRLGTTOLmQNamqasFmW/REjvyeMW99dyre938uhV3iZbxmGp4ZG3UYP3u/sWOpGn6y2bSu8XlYOKkJZ3eCgIpTVDQ4q/h1l/QRtDTnGM4o+wQAAAABJRU5ErkJggg==', '2026-08-04 04:32:17', '2026-09-15 12:28:05', NULL),
('07c1e28f-a13f-438c-9e11-28092b66e6e6', 'TA/40216', 'AMMD', 'Senevirathne', '200323800102', '2003-08-25', 'Male', 'AC', 'Account Assistant', '0b7a2bcf-5ac0-4590-a777-05febce54289', '2/2026', '2025-03-01', '2026-05-21', 'Present', '0761383328', 'senevirathne@gmail.com', 'Senevirathne', '0761383328', 'O+', 'A4G1', 'Buddhist', 'Sri Lankan', '42/2 KemmalaPitiya, Padiyatalawa', 'NA', NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACLUlEQVR4nO1aS2rEMAx9VgxdOtAD9CiZm/VqyVHmAIV4OZCiIllJKIViCk1NrbcIjucthBT9JzAqsVAtE3AqubLgn0s1yKlwZVWDnApBMESEm15kOeX9utyRKwttfFkTC1Y9v4dwS5ucBr3lxmStAf1vat5daBkH1le9Vn+7RIAKEHqnxi83OW6MPGzhGgHIqfixsngWjyqJyvXaqm8lyU4ZMI9KG1heuSVZyalQLFr7jVJvrEdNKPWGwJXVlm/x8a4eBaRH4M+ehb+XlZwKgbrVWf/xnJ9Yfas4nfdbjXwuKC3VDKnbJVsxb6X90n6rnLQbm/9cVuqeGlUDYVqfJQhGqzKW8S2y9MlAft4sIFL3yqJWNJAeAcuLTDDUwdYzMIrJ3FotWYtLJMxPjGkdWAcaZ3S8QIAqEHqnwiaBJWVpBhMkNruVk+etlqzFEvp2Q1kkNLdKRmCvMtAWNbGFQzOZzODvxxaFmpK1Y2oI48Dh9R5tliF5y3ZbWnm0JGvP1KhPrdEZ2I4iMG6YZhkb5tCMrNQ9NaoGdosMsixRu1mrpSZzZbW6Ow462j2S17mXRDOy1oA62R1DuyyBjAitY75AgApQDakrKs/pIXZ7D9Ydn8tJukSAb0DonRq/3OQIXjQcprfAyy3uixP6FQHIqfj57nhax/1x10GUGs712oQG9slTga1IymhDuuNSavjkqdnd8elq+ueM80dCNcipcGVVg5wKV1Y1yKnoXVkfs3UATnt1QCkAAAAASUVORK5CYII=', '2026-09-10 11:26:07', '2026-09-21 07:17:30', NULL),
('0d938fdd-8a24-4ad9-8287-c4ae606c7f53', 'AW/4946', 'EMPB', 'GUNARATHNE', '995340062V', '1999-03-02', 'Female', 'LAC', 'Administrative', '66e284eb-945e-48d7-8c5f-f1d3de0965af', '170', '2026-08-04', NULL, 'Active', NULL, NULL, 'ISHAN PRADEEP', '0773747985', 'B+', 'A4G1', 'Buddhist', 'Sri Lankan', 'NO;36/3,MOLAGODA,HARANKAHWA,KANDY', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACMElEQVR4nO1ZS27jMAx9pAV4qQA9QI8i36zokXqD+Cg9QAFrOUAMDkjJSZtF4SzScibkQrbstyD4RPFHgp0y814kEFAOYyGOy27hgCKMtVs4oFChLknfEmiqtmyfpzCWj+OS2qMcda1PbSfASZ+DraB7KsABxc3GqpsLlWUl2zai1NXCrm5P1vzc3Er+AV0fDpqu9kqSONWVA4omWUQ0dtGElWjKJ9hWRFrsQhgLbo7LbLnfQV/rKIDlhMqbSrDl6yaU815a3Mp/SK6vRL6LAhxQ3GgsUrdq+V/PCUcx32pOF/WWM9+q6QTkBZinQQj5pLfjIFQk6i0/bEFUYPSUpacVctQswxKMsgyGEDn+uq788NDUKANW62AkKm9PQmVZtw4GVo1gYSxPFpg1bk11bGm8vB4GfRu60wVbvm7CYnedFV2NnkHsErRCrP/l39aVHx6KHpWUGY1bG4OWxtvSARJswQ1bcqHnkm+caQy2PGUZhLwI5snaGKNgfpYty4i45Y4tsXWrrQjIfeZFqORGVw4ovs6Oe5Zh862qrQ27BMNYro5LaTEKoBcLWS0dNN6sv+tJ14DiPDs2jzLRFqENJ8O3vB4XebU6WTsYrTq2cdcPKvCNMB4dmq4/FFmTaGsDyB8k85S2wQnfRQEOKG5mKysltffbqSwHUHkftWI24sKuLiyw9eCb2NWnTfevqUZUx15nx7i4mo5NPv3kuyjAAUUYa7dwQBHG2i0cUPyXxvoL/BcTxdaQCTEAAAAASUVORUSCYII=', '2026-08-04 04:14:41', '2026-09-15 12:28:05', NULL),
('0f382899-cd69-4a25-b18f-a7817a9d1b1e', 'AW/5000', 'NLSD', 'SANDEEPANI DILTHATA SENRATHNE', '997210549V', '1999-08-08', 'Female', 'LAC', 'Administrative', '66e284eb-945e-48d7-8c5f-f1d3de0965af', '170', '2026-08-04', NULL, 'Active', NULL, NULL, 'SUBHASH', '0778430058', 'B+', 'A4G1', 'Buddhist', 'Sri Lankan', '197/C, DORANAGODA EAST BEMMULLA', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACF0lEQVR4nO1ZQW7jMAwcygJ6dIA+IE9xnm4/aIHoGCAGiyHltJuTewjK1uRBtuw5EKSGGkqi2GlL2YsEEloyWMjlsttKQpHB2m0loaBJt8q3Crk0G7bPlwxWjOVS/THNHNu7zxS48znYCHmlAyWh+Haw2kah6bqKTT1RpFrGNezKWs5OK/0Fvh4OWp/mTJIG9bUkFG6jqnLvkgtWkct4h01V1fcuZLAQZrkspv1OfG1vCpgmZN5oma1YlVAfc/V9a7yJPpfE8hIHSkLxzWAJaeX6r2vCNzVuOemy34rHLeUglIOC8c7qOKhMmv1WnGxBzaw5NpuUAoMqwwTGdB0cofOP+1oOD60WAcH4r3ZutZOVw+0EAyt3sAxWpAhM135YqDMb4+U0kG9skVkTM1uhKiGs4M3WdHl6Bv9mjRimrISxVEbjo9W78JOy/mE537waZiUMpjL0+mAZVcZjqkqCJbei9VuD2q2WF8HlrNrvtvyQN5CvR4bW//oty8xagbHfeQmahPG1HB4Kr3/drLfqB7quMqwIZr8Va7lM2+bl5bDLQVLNz3cj+XpgKDYFv5HJCeZvNKr65FZQqKreeIy79j6ZWj65FTVbWE7bYNcmc6t9G0M8Xw8HxdZlPXorr4m9MH7pvOYf97UcHoonTfipN/rmRamR3XHUu2OYjXzy2uTLz/ISB0pCkcHabSWhyGDttpJQ/MlgfQBsHDLgbbyVtwAAAABJRU5ErkJggg==', '2026-08-04 04:24:25', '2026-09-15 12:28:05', NULL),
('20797436-0920-4880-99f6-10ed21333662', '42617', 'HMNL', 'HERATH', '901191697V', '1990-02-04', 'Male', 'FSGT', 'Engine', '66e284eb-945e-48d7-8c5f-f1d3de0965af', '149', '2011-02-21', '2026-08-20', 'Active', '0718089945', 'lakshanmk@gmail.com', 'RAK Ranasinghe', '0812421284', 'O+', 'A4G1', 'Buddhist', 'Sri Lankan', 'No:44, Sampath uyana Pallakele', 'NA', NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACE0lEQVR4nO1ZQW7DQAicJZZ6dKU+IE9Zf60/i5/SB1Syj5YcUQG7bpLT5uCGJnCwF+8cELOwGBKjUUZqRQIBpXAW4rg0CwUU4axmoYBCJBXpZNUhDbM+6uchnOXjuHT2yid5zh+mMbDK+6BPpD0NoIDibmfNNYTydE6qGlESauFXtydrPFpY8T+w9eWg3Y0uJLFTWymgMOmZWe6uNOCc0tCvUJWZ7e5COAtujsuotd+7LOc3BrQmFN5Egi1fmZA3ne3e6pfEtymRdjGAAop2YRHNhFpbaOpjng6MLCut7LN8PoVfyQtbkCLQbislqn7TVbDlii1WjrbYMt50lSf9FrHlgq2tJiz0aNOJefr9MZafZV+2Ngg9N3QuLUINsDTMbzXe+qjgnVYZvaQ+zXqiShK0jbi3XLFlYvWfXlSTLDWs+m2XHm0rvTwUhYtKjypWvJeNUhhysAUnxyWlo2RCaWNIV0NXZbZlTd442i48cJkJLayubivDRGy56jyloh1WBhbRzp0MJ9cyptzRAAoo7nVWrpdXGrSDYQEmSXCOaaTj2THk7/gkHOkNVoaTrmwNaBX+PC5SWyypdqNk3KVbhGahgOIvZsfIX13Nf/134nHo6uCEggL46GXki3+r64butDV+6dG20stDYWwVKcV74WgrNaKC9zo7hkrPpbVxsUm7GEABRTirWSigCGc1CwUUT+msHxWHXr5HrVWtAAAAAElFTkSuQmCC', '2026-08-06 04:33:48', '2026-09-15 12:28:06', NULL),
('321a9e7c-95cc-4650-8147-afcf0757a5b3', '51066', 'PDR', 'KAVINGA', '199932112418', '1999-11-16', 'Male', 'LAC', 'Administrative', '66e284eb-945e-48d7-8c5f-f1d3de0965af', '170', '2026-08-04', NULL, 'Active', NULL, NULL, 'WR Vinitha', '0716405679', 'O+', 'A4G1', 'Buddhist', 'Sri Lankan', 'Siyabalagahawatta,Galahitiya,Kataragama', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACJUlEQVR4nO1aS07EMAx9TiLNMr3BHKVzM8SRuEFzFA6A1CyRWhnZacqAhFQWgFH9FjNN+xaWnc/rc4lxECUcZQJODZ4s+HQ5jOBUeLIOIzgVAtqQZLAS3SoRUPvtmyfL1HQZWTCLmKAL8+MQmW6IepeNxXpiatr+6wCMT1o3gMZ5IEYFCIiLlViDU/ER266Xl37lyTK4tnaUYQaX4QX2Yg2np6YtA1lOpwowsMq9C/ehJ8vcdCmq/QbZCeuFMc66J65NEhqLFWdfW7yPGXUlBpa+3n46gOBUfDNZJMtKFxjKdZHDa6W7B55XawqemngHEJmQI6NIwcantNA4mYjVqaElQg6qZl48PCfwpIaGPsmvfm6ZVPDlyvKzyNuxHmVrEkHPZCTW4FQ0ZLGYnjefsK0yVYeoutQ8WSYygO4ERlYHozmDPMcm43nKzM1FnP481nB6Klq1xl6eBi0Uvw+9WsbOrZW4XJekXgbrG1i5xUWPLDYSa3AqGmTDQ71wMzRoUE24ki4r729ZmS7gj9DybBvj3tryndBy7xjNy6ipFcpWrIcQztI7HnaBke89KJiJ9cRUdE2oSjAyT9Lfn6RQd2V0TWiVml+JHnbxrq0U/4rGbLWqOBiC97fj3w3gSwScnZo+9Y4J+UX6W+LBi2344wEEp+I4+O4bNKnRyGI/iYJvw67l2Z0nGOwdozuG23C7wt/HGpwKT9ZhBKfCk3UYwan4P8l6AydZGQgKN0K3AAAAAElFTkSuQmCC', '2026-08-04 04:01:14', '2026-09-15 12:28:05', NULL),
('3b0e40ad-cfbf-4df7-804d-2c686c40ad2f', '51840', 'THD', 'KAVINDA', '984562482V', '1998-04-04', 'Male', 'LAC', 'Computer Technician', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '171', '2026-08-04', NULL, 'Present', NULL, NULL, 'htrhh', '175', 'O+', 'A4G4', 'Buddhist', 'Sri Lankan', 'xvfh', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACJUlEQVR4nO1aS27jMAx9pAV06QA5QI9i36xXs4/SAwxgLQMk4ICk1GmzKDyLtGzNt7Al5y2IR0n8KCTYiZX3MoGkcoqFXC67wUlFirUbnFQoqKHoqIDmao/+eU6xYiyX4q9p0Wc9+0yAq74He4IeaQAnFf8tVu1baNpuZFN3lG611DXsylqffVvJD7D1cNRyN1cnSVBbOalwjCKisYtm3Ijm8QqbiojHLqRYCLNcVsv9TjqsTwJYTqh+U6S3Yp2E8jYXj1vjheT+SOSHGMBJxX6Iwk5Cyy3s6BPZBsGkI8vsJ/28pK4cw1siW3OKp4N3o/RWqJOQvBKu56sAN8J6+lN81L6FsDWpbDr4gachy5pOttV6YawuS7EiLRd62TRvr+aeQWiuT5rQa4k8ZgYfL8tAr608RmnSMWmqYelHxq1Q3jK06Ta0pMO3lZbNhuXbbeWkwmGH4ChCZMHrn99erU5OsQIpQPR8IUyvpffgNXg5vMkbyNYjU8uHXq56pp6FrKGhd16ESmFs5cNTiynQPTJcZT1Bm063YqVWu6ZMsUItl8kSCa2yXqzpbq1dyzI8q49ka1Lxdnfsjup9+X45mWKFVECW8aL3Wxdq1bFdd32hAZ+AP/vxmNT11BtRdm2yaCNqCWrrUXsZk8et3mrSyxLrZVgsy+o4mLcaWqup+eid87KXoYh3dwzDqG/9c8a7H/khBnBSkWLtBicVKdZucFLxK8X6CxKJLUeo3bkJAAAAAElFTkSuQmCC', '2026-08-04 05:21:11', '2026-09-15 12:28:05', NULL),
('4847c54d-9b0c-496f-9682-cf79cefe57e3', '51098', 'MPS', 'Kithmal', '982370523V', '1998-08-24', 'Male', 'LAC', 'Computer Technician', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '2026/01', '2026-10-02', '2021-10-27', 'Active', '0742557379', 'pshanilka080@gmail.com', 'Sumeka', '0765653395', 'O+', 'A4G1', 'Buddhist', 'Sri Lankan', 'Radawana', 'NA', '/static/uploads/photos/51098.JPG', 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACI0lEQVR4nO1ZS2rEMAx9cgJdJtAD9CjJzcocqTdIjtIDFOJlwUFFsj1pBwa8aas2eotJ7HkLIUe/Z2I0Yg2tTMCpwZ0F/1yaEZwKd1YzglMhoIIeNGMnmiMREOv27M4y9blMLNgAvtAD8zIw04xOd9mYrS0I/5saawhNWwk13dZ4+xEDGhBaSCejDklCLf2eAXcR7v91Vuo67sSXI6J+3ID7CDg7tS/PQapTlEz4+sAEdElTIVuyNTgVilVL1QgcxQuQ7vBaweDOgpHY4s9bO/E6djXevtuA4FS0g3OPrr3F1jEveS+BWZb6r/b3i/s1GPmypq2TI3snmmXUorFj7Tdojt7Bm8uEK3WJER9ZJi/wOpOc4CgpMpmxNZyeiprrElTB0EyoqS9nR4VnQmN1C/ImytOSK9g1O1b5ib1uwQx10GDSc+uYL09XdXBIpauHGVvPS+3LM/aJppfHRBh22atDFqDL7zPAqaHdWX1+TMtO2hPqKsdVHrpiX6ex4EcAI13GpnXr6xWJQPVd7zJMndaBvKkNRmkMfTq2e3fM2sHLYKxJsCqGhmx1Kq53x1XVkFFLfvK5ubPM1S2UAavohBmqHSqWX7c1OBU30Jv+PGAJsljozrLxufQ3a15H6eDjWDeGN5+3LGoZLA0GPbOIF0cn6Bq8TZ0QIjoVYbBKhEcvz163YO7umPNjSPlNb0xcy7ByWsGpcGc1IzgV7qxm/CVnfQDduDAXpvuH8AAAAABJRU5ErkJggg==', '2026-10-26 04:16:20', '2026-10-26 04:16:20', NULL),
('49599a29-88c3-4e4f-bad3-ef2d05785b27', '51836', 'GKM', 'Sathruwan', '199812345678', '1998-04-10', 'Male', 'LAC', 'Computer Technician', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '171', '2026-08-03', NULL, 'Present', NULL, NULL, 'sanka adikaram', '0766932107', 'O+', 'A4G4', 'Buddhist', 'Sri Lankan', 'No:60/B, Madadeniya,Kapuliyadda\n20206', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACIklEQVR4nO1aQY7CMAwcu5U4tj/gKe3XeNL+IH0KD1ipvVN5ZSctCAkplwXv1nOAJMzBcuJ47ECCSkxcywSCyuEsxHGpBgcV4axqcFChoIIWNGIlGhciYNmWx3CWq+MyiGIG5EInkdSJ0IjGVsWZrTXg/01dthAa5hJqtmzx9hYDKsA1pINRu5uG2u1zBrwEv/7pqNSpX0ku94h6uwGvwTg6tS3fnWanRW/C60kIaG52FYonWzmoMEyWqnrgnrwAVYd7BkM4C05iSx6XVpKpb7Z4+20DOKioh2SNbtpibkRSXrtBRKf2q+n7FH5lLydrOYlczqoEtdSivhHTGzQuoeDdxdawS3ZNWRZgeRSx5W+3JF99e99i2G/HfSpxE8JLn3BEI9YdlGR7pH1C1fKAtp+SJ1uPTG23wdpiOgsInaYsGxm6GTQkF7YGlbMjJjoJhmsLSdYxtB58xhr1lrfYGr56ksk04V5+5aJrabdqjD9tKx+eirvqs3rLFPyDV0wshsrwpgkLyvbovhVhGNWx37djSVoOa2Fsl+DWMXRka1Cxvx1j6rU6NhmvH3nfwlm+8tZszYuSt6xYzrDeoSF93FYOKp4wXMvbSUZuFoazfByX9mku+iQplrIyuu/Wi60cVJRN0bvO9MZZ/+50V4LRg3d0XJDzVoHp9vK0VaablpfIW3D3diy2RyoHbU2AMsLnbeWgIpxVDQ4qwlnV4KDi7zjrB3EdNh+FwedjAAAAAElFTkSuQmCC', '2026-08-03 04:12:04', '2026-09-15 12:28:05', NULL),
('4ae38410-0c6f-4091-b88a-f2c271e038bb', 'S-1789363674', '', 'Test Trainee Expiration', NULL, NULL, 'Male', 'AC', 'Airframe', '631f5810-ac42-4f45-954f-5c886f4ce601', 'Batch-TEST-EXP-1789363673', NULL, '2026-09-14', 'Passed Out', NULL, NULL, NULL, NULL, 'O+', 'A4G4', 'Buddhist', 'Sri Lankan', NULL, NULL, NULL, NULL, '2026-09-14 10:57:54', '2026-09-17 03:59:39', '2026-09-17 03:59:39'),
('512aa119-c9ef-437e-90e3-eaf3af3c5173', 'AW/4988', 'WAT', 'AMANDIKA', '200069300471', '2000-07-11', 'Female', 'LAC', 'Administrative', '66e284eb-945e-48d7-8c5f-f1d3de0965af', '170', '2026-08-04', NULL, 'Active', NULL, NULL, 'WITHARANA ARACHICHIGE ROHANA', '0715205447', 'A+', 'A4G1', 'Buddhist', 'Sri Lankan', 'NO:67/2/1 -A , MADOLA ,AVISSAWELLA', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACEklEQVR4nO1aQY6DMAwcG6QeqbQP2KfA1/oz+pT+AI4rgbyyk7RVpVa5lHoXz4FCmINlY3vilASVOHMtEwgqh7MQn0s1OKgIZ1WDgwoFZbSgASvRMBMBc1kewlmuPpdeFBMgJzqIjJ0IDWhsVZzZWgP+39S5pFA/5VSzZcu3TQyoANeQdkbtFk215XMGPAU/f7VX6vm4kpxuGbW5Ac/B2Du1zb+ddqdZK+HlIAQ0i5VC8WQrBxWGs7WqI3BrXoCqw2sHQzgLTnJL7pdWkvOxKfn2bgM4qKiHJI1u2mJqREZdVJUhoo/21vT9GH5lJ9HqrfR1Frd8yXGbmoiW39yS1LJy84rcchst2EWhpe/hUaISwkm0Eqz0pSJYUg0o4yeJaMGJJiS79rK26MdV12zTZcGbQP3owtagcvaEVb251Z3XQYvgT9llYY39lpvPBVblkmTXyfu9CIRVwlIsx4/byrunokRLYfst7VtynerafDdUhkOVoTBZcUuwtP2KaDlUGUCziE2eAO1b89eCJDDeaAAHFfWQh0qYEiwdcuW7tDiGX9nb2TEp0kBD5/J2gLKJARXgGtLOqN1yf76vh5PxLxqv0RK5aKCuQ6e7O97EgBfgVy93Re3y5InoWxuV1r+kBHXH7MzW/VJRdLvhuh0uI8I4MXF9dizpR5Vgfsx3+LytHFSEs6rBQUU4qxocVPwdZ/0C/YZdOc72+KIAAAAASUVORUSCYII=', '2026-08-04 04:22:13', '2026-09-15 12:28:05', NULL),
('56ab9898-66d0-4a4e-bbec-294e14953e4e', 'aw/4618', 'RSM', 'Ranasinghe', '985820740V', '1998-03-22', 'Female', 'LAC', 'Computer Technician', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '2026/01', '2018-07-30', '2018-12-27', 'Active', '0765653995', 'dfghjhkl@gmail.com', 'Kithmal', '0742557379', 'O+', 'A1G1', 'Buddhist', 'Sri Lankan', 'Angoda', 'NA', '/static/uploads/photos/aw_4618.jpg', 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACMElEQVR4nO1bQWrlMAx9UgyzTKAH6FGSG/RMPVJv8HOUHqCQLAsJGiTFoZRO8RSamlpvEb6dtxCynyxL+SQoxMylTCCoHM5CbJdicFARzioGBxUKOpBA05pANOxE05qnp3BWVdtlFMUCyOOwE4BOs4/OZqUyW0vAv5u6HhKiSdfotiafNr1dYkABGK1T00eTNC53EKxXGMBBxdedNcorYR5MZeHXSrXV6+m0QhU16OPOp6UmWzmoMMyW+7miOsmy2j0lDGfVpS05x29PK9PbdxvAQUU55MzRRZZOMGoab7j19kLnbMjhV9SirT0B/atdtbYc+wgyPyzfawAHFf+rrVFlddyJAbm5ojaYwA6pcfgVVWxCueXk3RcK/aYp4h+xQtQFBhSB0To15R87WfKef2kQHEAyP7yQVGIrN0/FEeZMYGfUs3zDBdZvmcLNO4tr8UBvoY+OMgbdb/CzTFPESwwoAKN1arInjQuE0OelGZ9Ib8zdFrWMqlYLOfTlVOOIf2efJCJhjZFQ/BJsA++YnMNLDCgAl5Ca6h2LPGveDm1J2pI9az+5JluLwG30jh16MfaYON9H77je3jE0J/SqhtblXWBXGFAALiE1RaVJi4W6ZH4HE21OXmnAJ+DPXrZJHXN2SFO/+ZF1JIt8jQH/BqN1anrXO7YgSEDaLAjKTEelFz9vKzdPxdtv0M7v0rwG5Z0urWpE5amO7ULxrwX88BJwUBHOKgYHFeGsYvxSZ/0FOcARJ3QG7GMAAAAASUVORK5CYII=', '2026-10-26 04:22:34', '2026-10-26 04:22:34', NULL),
('5d9bb916-b83c-41bf-b8a7-acca66750e0f', 'TA/40219', 'HMDKN', 'HERATH', '200517101349', '2005-06-19', 'Male', 'AC', 'Account Assistant', '0b7a2bcf-5ac0-4590-a777-05febce54289', '2/2026', '2025-03-01', '2026-05-21', 'Present', '0789585291', 'kosala@gmail.com', 'HMD Hearth', '.', 'O+', 'A4G1', 'Buddhist', 'Sri Lankan', 'Alaha,Maspanna', 'NA', NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACHklEQVR4nO1ZS4rDMAx9VgxdJjAHmKOkN5grJ0fpAQbi5YCLBsl2p0M3ptBWNHqLYDtvISTL+gVGJ1bqZQJOJVcW/Lp0g5wKV1Y3yKkQhIqIcNSDJKvUjssZubJg42bNLNh0fQ7hOGZZDXrKxmTtAb03NTUXWqeBdavH6m9PEaADhL1T481JipmRhhyeIwA5FXcrixfxqBKoXK9WfWuU6JQA9SgGMli2bElWcioUq+Z+k+Qbm/iW5oSSbwhcWbZ8iy97RjoHBn7kw7ZkJadCoG51nf+lA6tvFafzesvIdUEpqXiTvF2qrJn1o1XWwGWl1djycllp91Q0a9WQVTFm+SF222qJzG4tvPy6xLYYpHuRIzB+RwbOJTvU1gYbkZWcCkGJURKtypsoDQ1e0F5HV5aplxD1wculOpbyq5zVlb+E5uIWi6F40ZClEUzdaqwE9rgFM9TxXyZYsgz1t9NlikJWZN07NYRw4NK3mE+xNOLrbOvT45Y1a7GGLEHpN0nnqbpam53Aiqx7pkb9NoMMmddJO06aIn5kzMuDBSCn4u7ZcaiT/kNL3t23LM+OZ83bBdIixOpxy6C1GnjRuCUdjFId/w0nCd0gp+Ipk/71K0cNXtKDCrweYxuckJsA9mbHEWHeJoT5dJCGhhrOrWVCA7XzVFFHJKW1cT1F8V6GCWvdzo7/XE0aGlc/6SECkFPhyuoGORWurG6QU/GWyvoFfv0Y8VPUknwAAAAASUVORK5CYII=', '2026-09-10 11:35:05', '2026-09-21 07:17:30', NULL),
('5eca75db-051f-4ffb-b04b-b942fbc3d286', 'AW/5009', 'PT', 'PAWANI THARUSHI SAMARAPPULI', '997270835V', '1999-08-14', 'Female', 'LAC', 'Administrative', '66e284eb-945e-48d7-8c5f-f1d3de0965af', '170', '2026-08-04', NULL, 'Active', NULL, NULL, 'NILANTHI WIJERATHNE', '0772125041', 'O+', 'A4G1', 'Buddhist', 'Sri Lankan', 'RUKSEWANA THALALLA EAST KAKENADURA MATARA', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACBUlEQVR4nO1aUW7DMAh9kEj9TG/QoyQ3m3az5Ci9Qfw5qRET2Gmybh/WPlq2gFTJdt4HAgMPUxJUysS1SCCgHMZCXJdq4YAijFUtHFCoUJEWNGAhGhIRkNbjIYzl6rr0ojIrmaCTYDo3QgMaOxVnutYI/29oKiEkMi8EdB9kxxZv3nQ9LrT9ftTcgNRCkJ6hAAcUv/YW6e/nHozDrnByCTsRGXXRyw1Wt+xYRLfPUKBCuAZ0BOhk3O+sy3QSeptR2KGKM11x9Ewo+yNjGRpRnfjSlQ8PxcrRG82Elv8aQT8Du8Ro/H4MY7EPb5mYZ8xlxW/dbfdVwltw4i30855WWJ8sMmt3rB8itlx5S0YtVJb1jB3K/Wlj244v15UPD0WOrUwrcv67Oy/HW3l+kvAWnFwXKXFkdWuh4qjug7Lf4mr744QwJpj9lkX5Rmf0I2LLhbceY4voYiWrcMLSfnnS9chQrLG1bTUd3vOfxlvEli9vbVK6rJW37yDjy3XlgOLr7FjGpANkm2+lNodVzI69dceyVStblfyXi1ewDLez4+v66K7v8uivGm++dK0QPgh00rHJdClUQ94v0W85nh3381mZ4FImXYqgfnSha0D5cXac/+6UToUOanccmdBnv9XcHzS2SVe8wfudHUveaMkq27LC63XlgCKMVS0cUISxqoUDir9jrE/KwHaYywU7lgAAAABJRU5ErkJggg==', '2026-08-04 04:28:56', '2026-09-15 12:28:05', NULL),
('6539b613-e3e2-4d92-ada6-c1992fac9a7f', 'AW/5024', 'AS', 'GUNATHILAKA', '200065802848', '2000-06-06', 'Female', 'LAC', 'Administrative', '66e284eb-945e-48d7-8c5f-f1d3de0965af', '170', '2026-08-04', NULL, 'Active', NULL, NULL, 'THARINDU KUMRA', '0779482177', 'O+', 'A4G1', 'Buddhist', 'Sri Lankan', 'NO:62/3 MATIWALA,THELWATTA, AMBALANGODA', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACF0lEQVR4nO1aQW7DQAgcsKUc7R/kKfbPovzMfkp/sD5WckQFu05cpYdVDwmtQbIUr+eAYIEBQoJKmbkWCQSUw1iI61ItHFCEsaqFAwoVKtKCRtyIxoUIWLbjMYzl6roMopKUTNBJMPeN0IjGTsWZrjXC/xu6lBASSTcCuk+yY4s3b7oeF9o+HzUrsLQQLK9QgAOKX3uL9Pm5B+OwK5xcwk5EJv0xyAqrW3Ysoq+vUKBCuAZ0BOhs3K/Xn8tJ6JJQ2KGKM11x9Ewo+yNjGRpRnfjSlQ8PxcbRG82Elv8awZCAXWI0fj+FsdiHt8QcZZ7Z+a1by9cM4XfryoeHIsfW3VElmDS2JGl3nOwsvOXiuuwYfK5Sc5+ESskqFUyc6MoBRRFNfTYdxI3k2uuwMJ/FLMNf3eoKmbBM+MiOMmkjFnXL1wx+1DjSpsuCKXdZNt8tXx3pGlDRWW6eW8x9IRil6bLiFcbydF0or7aWEkyYzzqD17n85SPqlh9vYddR5Wq1kfdcxh6Q6e26ckDxfXcs114Lle23lA6qy6Juebku2Pif7Y5t6GQ9cdkn5+IV3bEzbyV1jznKGLy+muTEGJnQK3RplWVYq7VCrufYb3neHXdriyHdyqZLETRMLnQNKD/tjpP+3Wnj8nmWYR8QxmI3+y2T+54kPTZdMYP3uzuW/GyTdwFiBu/HWxxQhLGqhQOKMFa1/CVjfQGADlaEo1yQ/gAAAABJRU5ErkJggg==', '2026-08-04 04:36:27', '2026-09-15 12:28:05', NULL),
('7c03548a-fe20-40b5-9ac0-6f1ee3d1a886', '32853', 'HFAI', 'Fonseka', '862710070V', '1986-09-27', 'Male', 'WO', 'Airframe', 'course-basic-safety', '117', '2026-08-03', NULL, 'Active', NULL, NULL, 'DA Thirimanna', '0382295009', 'O+', 'A4G4', 'Buddhist', 'Sri Lankan', '105/4, Delgahawatta,Wadduwa', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACPklEQVR4nO1ZXWqEQAz+Egf20YUeoEcZb1Z6pN7AOcoeoKCPBSUlibplYcGX1qHme1Bn/B5CJsnkhwQ7UXgvEwgqh7IQ5rIbHFSEsnaDgwoFLUigDjNRNxIB47rdhbKqMpcsigGQd7qI9K0IdWhsVyqTdQ/4f1PH1YXysLiabZu//YkAO8B7SCejtpO62nScAE/Bz3+dlVquM8n73aP+XIDnYJydmpZ3q7fTqJHwdhECmslCodQkKwcVhmJX1RW4X16AZofbDYZQFirxLfm5NZOUa7P6228LwEHFfojn6JZbDI1I73sTRHRpfy2/70OvXIdlidwufmTUaalF10Ys36BujAy+ttMi71ZoByPfiKTX8utNi+Vena4qWc9MhQc7D31b3yJv0XFbSkRC1EQl71vYGbmXaXTEcpehKllPSk32JLSDu5U+BeVVsCTu7QDKfRWyBpXvyrDOuz/ehnmtsrB9cegVB1tW8lf+SJOU12krvywn1KJrTGs1xkfLykGFo/3SgdbFgqCsU62ZrL8b863qcsIFvql18poYRnVc7+xYLJfv7bbSwnjpGFYka1CxzY7tjKy/67m8NjRCWbWYCzz+mQtZ/LMCSx3MYb1DQ3+4rBxUPCAPOicx31J4szCUVYe5pIe1pfFiV5aj/Uy1yMqnp6aH2THlYfaldzBKFz34eswl+at4KqHlsGF8mVComSgPLz7zx/Gy8umpyTRwHxJ7G0PTQdsTYPlCKAthLnx6h+HQACK+7gYHFb+hrG8irAZlJHXVbAAAAABJRU5ErkJggg==', '2026-08-03 05:09:32', '2026-09-15 12:28:06', NULL),
('82bcf39e-4c1b-4202-aec8-eed9a4cd857b', 'TA/40217', 'HMI ', 'Chinthaka', '200419000712', '2004-07-08', 'Male', 'AC', 'Account Assistant', '0b7a2bcf-5ac0-4590-a777-05febce54289', '2/2026', '2025-03-01', '2026-05-21', 'Present', NULL, NULL, 'HM Dasanayake', '0765407188', 'O+', 'A4G1', 'Buddhist', 'Sri Lankan', 'Kahatagasyaya Namaloya', 'NA', NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACOUlEQVR4nO1aUYrjMAx9kg39TKAH6FGSm/VMe4P6KD3AQPJZSNAi2WnLDFMyH90xaz2GOEnfh3iKZFkaEuxE4r1MwKnsYsE/l91gp8LF2g12KhRUEIFERMBcLhmji1XV5zKIYrK7BUR9EBoR7K1UZuse8P9NnbcQShQhMq0klxx0sTpbd4DboNJ5AmjsFpT8968NeAF+9WOr1CBI/W8a8B0YrVNjWTvdnWZAUh8gaTxIfny7AexU7Ic81REaVsP0uGyvrQa5uK5cR2zJ/VnS6UYCLFu8vdsAdip+KBaRblTlqHXQfWulpx9c16oyoYhYMC1avOvbTlOf3uSc6JmwKmqig2C4RhCdzFHr1sHoblSZrQ1TY1m76V4YxoWGybayNSL1k1AltnLz1FgUmNUl83HRhST1HxHDn6OQOq8UG9y8WFyHAnTO+9aNrG6n81XPW9D206OrwXXY2jI1lnU+CpIGVuqDBthKoqdjsr9KbOXmqXFTQN1jmxeseA8L0mh+u5/GuHmxuBoFgraadL7Vh3tNuJIV754JqztvFdihy3yULwY/b9U6Ox6ujwGyPvo0subZMXJrV280yp5mJ/xOA/aA0ToVOf+Ze7TLJKIXrdszdPCfc+Tl123l5qnxqwJWE27vtaqnwVqG3LxYXKECYastJkAunf8XTb2zY7JGvPagkE4+36rTWyl3LELuGJqXCND+7jUutdjKzVPj59lxXizA8mO5g4sF/1y4+YBhVwCeX3eDnYp3iPUX4rwFSBJSl84AAAAASUVORK5CYII=', '2026-09-10 11:30:03', '2026-09-21 07:17:30', NULL),
('85647492-ad67-4aa4-a1b4-1d1ac29b1c47', 'AW/5007', 'WMD', 'DASUNI HANSIKA', '200073103166', '2000-08-18', 'Male', 'LAC', 'Administrative', '66e284eb-945e-48d7-8c5f-f1d3de0965af', '170', '2026-08-04', NULL, 'Active', NULL, NULL, 'DDKD RAJAPAKASHA', '0713505633', 'O+', 'A4G4', 'Buddhist', 'Sri Lankan', '487,NARAGODAPALUWA,BATUWATTA', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACAElEQVR4nO1aQXKDMAxcC2ZyTH7Qp4Sv5WfwlP4Ajp0Jo45kgWlm0vpSohbtwQGzB40XeYWVxKjEQLVMIKgUi4V4XapBQUUsVjUoqBAkQ4vUYU6pm1ICpmW6i8Vy9bpcWTACfEsn5v7MnDo0OsvOYq0B/W/qtKTQdbRU02nNt10CqADVkA5GPd8l1e6vC+Ap6Pmjo1KHy5z4VjJq9wCeg3B0amu/Z3GnSXbC9xMnoLnrVsieYqWgQjGoVV2AYl6AVIergyEWC05yi7dTc+Lh0iz59tsBUFBRD841utYWY8Pcy6RUGcxyq0+1vu9jXcmHWtyjEcl4M5huYxNqeVOLpWRXt5JhEWrJvMgtV2pBtz45wQDKCYbsjopQy5VaLB5lvnVW3czGingcvgUnakFEsWTKGWXiZRuL3PJGnROu7y24n06i0UfaPNglgJ9BODoV5ltaW+RKcC0CNd9K2UivjpUOT0Wp+rJvSXWYS0SFnu/GTuitgjdsLEsVDN/y3DvmXi1Lh6ldTwwdxXpkKnJGWe/4y6eW5ZZujOFbLtR67B3roD1/PZfXBsouAVSAakgHo062J5bmZPyLxqtafHtbzjIyyhXtEsA3IBydigffMqMqJ+/CiQrel1qG9XN4OSKMjonr3jHnH0kwu7UrvD5WCipisapBQUUsVjUoqPg7i/UJRf1+kLCJ3U4AAAAASUVORUSCYII=', '2026-08-04 04:26:47', '2026-09-15 12:28:05', NULL),
('95899396-0f2b-4d68-ba1b-00657ec9e7fd', 'AW/4978', 'HMDK', 'HERATH', '199957802162', '1999-03-18', 'Female', 'LAC', 'Administrative', '66e284eb-945e-48d7-8c5f-f1d3de0965af', '170', '2026-08-04', NULL, 'Active', NULL, NULL, 'RMAD RATHNAYAKE', '0771985235', 'B+', 'A4G1', 'Buddhist', 'Sri Lankan', '151/C,24 WESTERTERN SETTERN EAST DEMANGANDIYA', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACIklEQVR4nO1ZQW6DQAwcG6Qclx/0KfC1/gyekgdUgmMlkCt72VBVirQ9JHGL50CyyxwsL/Z4bRJUYuJaJhBUDmchPpdqcFARzqoGBxUK2tGCBmxEw0IELGV7CGe5+lx6UcyAvNNFZEwiNKCxXXFmaw34f1OXEkL9vIeabVu8PcWACnAN6WTUtGqora8z4C74/quzUqduI3k/IurpBtwH4+zUdv9Nqk6LZsLrRQhoVkuF4slWDioMk0lVBxziBWh1eFMwhLPgJLbk+9ZGMnVNibdHG8BBRT0k1+hWW8yNyKibWmWI6NLeWn0/hl/Zx5cl46JBlj6JhiSCqWv0YffkqOD9nFZrT0L6aIGlg2BRndJHP+sSqxtb+fRU5GRnWW9MK0omLNnREJnQl271plH5yFSjiowBpf0koVt4+Wm1+Wd6+6QSTJvu2aVLkWZQP7qwNai8e2JpIXK1ZqEFmB5exhb3LZeZcDTd0kdOfbBMWKRtfLmtfHoqyo2qCFW+at26uvlFnJavmrDAyopyblYYxu3Y7+xYVLJ23dKL8d4xdGRrUHGbHVtsWX83l4g2QLGSEOEsdlNloOiWjvu/6VZpFkpUGfA5O6Zjvp+bhU814C4YZ6e2P9aizULktqHh+McPMYCDil87K9kFS+uNTjPh9VLmJNGDdzjfyrjpVmkRHrW8hG7B3exY8kIbGvty/4fX28pBRTirGhxUhLOqwUHF33HWF1qWSe/PBGxZAAAAAElFTkSuQmCC', '2026-08-04 04:19:50', '2026-09-15 12:28:05', NULL),
('9affc12f-83f3-41ae-b019-7ac9684da0e5', 'AW/5010', 'EAM', 'MALKA SAMADHI', '988081043V', '1998-11-03', 'Female', 'LAC', 'Administrative', '66e284eb-945e-48d7-8c5f-f1d3de0965af', '170', '2026-08-04', NULL, 'Active', NULL, NULL, 'ARUNI PEREA', '0717960803', 'B+', 'A4G1', 'Buddhist', 'Sri Lankan', '106,KURUDUWATTA,MAWALA WADDUWA', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACGElEQVR4nO1aS46DMAx9MUhdgjQH6FHgaj3S3ACO0hvAciQqj+yE0Fm0yqatNfFbUEjewrLjT+wGRiFmKmUCTiVXFvy4FIOcCldWMcipEISEFmHELYRxDQFY9+XRlWXquAwsWAC+hBPz1DGHEY2usjFZS0D/m7ruLjQsydV0Wf3tLQIUgEpIlVG7TVxt+5wAD0GPt2qlzv0t8OXwqLcL8BiE2qlt+u0kO60SCa8nDkCzaShkS7KSU6GYNVX1wJG8AKkOcwaDKwtGfIvvl26B577Z/e3VApBTUQ6ONbrWFkvDPMmiVBnM8qm7Wt9PrlcyYq1haZLJ0KnxeLebbLi1bEXC+SyGWltg+JY8tQYxVC8hcjMjK1VPxX2sOzwqR0eF+5a1vMXSeZK81W3QR4qOe/uJPW/BirUGLdklZaU2RpNzmVcZ9u5bZzHatQVfenWwn/2WhZvftyzWhBGTulV+yxT2SAgz1uIc//Sqlbu6uuFVhilrHbhLWakw9Lxld3bMvEii0ryl16/Fmqw1UxE9Ks2OtcDIjaj90hW9bvq4rORU/J0d60Nn/tqX1wGKK8vucVlTTDyGk/4vGqvWYikHYy8j4nijtwjwBPRssypql1qEYdTaQuJfrNvl05is9VLb+DPHhoXOILe81mxhWL7izB+fl5Wqp7aqgWNIzHrf0kowfaY3uLLgx4WqdxhyDcDjazHIqXiFsn4B45Nag+l5NjMAAAAASUVORUSCYII=', '2026-08-04 04:30:31', '2026-09-15 12:28:05', NULL),
('a1000f6d-0983-4dea-b2fd-ffd32faaf80a', '50845', 'AK', 'PRASANNA', '973070100v', '1997-11-02', 'Male', 'LAC', 'Administrative', '66e284eb-945e-48d7-8c5f-f1d3de0965af', '170', '2026-08-04', NULL, 'Active', NULL, NULL, 'AS ANANDA', '0754079435', 'AB+', 'A4G1', 'Buddhist', 'Sri Lankan', 'ALUTHAGEDARA,BULATGAMA,BALANGODA', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAAB90lEQVR4nO1bwWrDMAx9knN3YR/QT0k/3f6UfUAhOQ4SNKQ43TrGMDu0otE7hNh5ByH52ZLVkqATlXuZQFA5nIVYLt3goCKc1Q0OKhTUMAD1ZMMBwLxPX8JZrpbLKIpJ396JME6rxijZrDiztQf82tS5SYjolATILUZNZb5sPS51+DGWellJKqVFMD/CAA4q/u+scVJthV9dr6wsIkVf6nnRkK1k0yKyPMaADjCOTsX3PAJJNm21xz5tOUh5uq18eCrkHlvIkFVg919KOIvdaCs1gamipGjybg+ZWhovES24iVZeICW3oqtVXhYj/RDRchUtsfB8zzdMW6ayOLe81VuEvAxAvg4YyzoI8pUESAuNokMftvLhqWjb3K6jX4+x2Ak9LpcsgnqyUksftidqdvgwA/4G4+hUbGJqtZUlge2g2mW15/Ll6bby4anDFrJ63ivkekkLVbvJsLMMSbZrDYSz2I22UhPYTWU7QT+EtpzeZYxbdfy1HUZ17Lh3jNtlIWZtJZ8/onfst3cMrESkF/HbZaFqq7iytQd8jN4xLDEsJisiQo3esefeMbRjPE5vEHe2clBxDyL9zdPlS2/zsA85nAUn2soqJfshRr6S5RamLQHaGyJa8Nc7xq3nH71jd9Gi+NcCnhwCDirCWd3goCKc1Y0XddYnb+xeKD2xgMMAAAAASUVORUSCYII=', '2026-08-04 04:09:08', '2026-09-15 12:28:05', NULL),
('a2c507d9-531e-468b-832c-a97071a1e777', 'AW/4945', 'APD', 'MILONI', '200077002898', '2000-09-26', 'Female', 'LAC', 'Administrative', '66e284eb-945e-48d7-8c5f-f1d3de0965af', '170', '2026-08-04', NULL, 'Active', NULL, NULL, 'CHANDIMA KUMARI', '0772659817', 'AB+', 'A4G1', 'Buddhist', 'Sri Lankan', '263/A,BELIATTAKUBURA,DENIYAYA', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACJ0lEQVR4nO1aQWrsMAx9cgJdJvAPMEdxbtAjld4sPkoPMBAvCwn6SFGmU9qF6aKj/yPBhNjzFkKypGcpxGiUklqRQEBTGAtxXJolBRRhrGZJAYUImfSgCRvRVImAemxPYSxXxyWzyCJkgp4YZeyYJnS6y850bZH0f0OrhRDzshEwvJNua7x50/W80P7rVrcCtQej/oYCKaD4sbdIft/fwVLYFU4O4cDMs7xkXqF1S7eZZfkbCjRIagGdAVqU+43yWp+YXhYYOxRxpivOngn5fktZhkTUwL50TaeH4uDonWRCzX8dIy/AXWJUfj+HsZKT2CrPV2IM1z3rcRm7lTBce1bnxdF2FVusF2ONKKEVumRe5Ha8SKhFbHnyFrJ4Zh4kJ8rjo7WhZFFlfriuKaAw0e5gL9VqI34dZalJsEYvw10mnPeeoDLB9Yg3yYkSbxFbvryF3UeaDu/+O7Jj1C1XULYa9W75T8qYXbr0+uVJ1zNDe33uDimT3pM34nKRHnwlIL9F3fLH4A+xvYO330Hmh+uaAorPs2OrWzrfEjooLovZsbPjkjV8pJf7stx4u9StMkbdcng7hvQyjAQa6cBHfyMyoQtvfYHmNyKUi161VvDrJeZbjmfHeV57ystmky5BUJ5d6BrQ3iyhsyz5EKNQx4T6x+hgeb4lxRR2hZf5lsox2lIGb8vowfudHfO+kJJlS3vD43VNAUUYq1lSQBHGapYUUPw7xvoLhzVaTlFbH6sAAAAASUVORUSCYII=', '2026-08-04 04:11:43', '2026-09-15 12:28:05', NULL),
('a2f87162-d63c-4c11-b4f5-3aefba9afded', '50702', 'WMWLP', 'WASALA', '981682602v', '1998-12-06', 'Male', 'LAC', 'Administrative', '66e284eb-945e-48d7-8c5f-f1d3de0965af', '170', '2026-08-04', NULL, 'Active', NULL, NULL, 'YML Manike', '0743308429', 'B-', 'A4G1', 'Buddhist', 'Sri Lankan', '327/A, Udawela,Barawardhanaoya', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACLElEQVR4nO1aQW7cMAwc0gb26AXygDxF+4M+qciT8gP7KfmBfQywAQtS0sab9qAEaMxWJOCFpJ0DwREtcmQSNNrCrUggoBzBQmyXZuOAIoLVbBxQqFGxEXTBG9FlIwK2unyJYLnaLknUVi0m6CRYzoPQBYOtijNfW4z/b+hWUkhkfSNgeiVbtnzz5mu/0PH3peEKbCME23c4wAHFl9kiff7cg3HEFU424SQisw6SXGHnli2L6PQ7HGgwbgH1AF2s9jvrcDsJ/VxRqkM1Z76i9zeh7JesytCMmsSXr9w9FLVGH/RNaO8/rdtXYPditPp+jmCxE7ZS/THKCm/TNf+bbT7cV+4eivf+N3fHmkw5t2S1LBsqjdx9sNhLbq2aUZPyptVhNiXvfTof7it3D0XJLS0rUqanjpTBcowFW562i+TTynKrlhomP8ls1aEnX3uG4u7cqgdVruBvDMa55Su31CyZrCdGejndKNP2y5OvPUNH+yVMKyg9n7VPFhULlaONgPQSGrwftiD3lqvDW92+g8yH+8oBxf3dsTw9vqpiaLk1Zhkj7o4dahlSMsoUjKI37QSN+XBfOaD4cHc8a0ZZWqkuH+eW7+2yPJYGy1oteapTOPS1O+j4YU66RGm+jvmmq0z/ngMB5c+zNWn5px9ipOcH/S7joZSDyw+ToyKuLiKw0zKq3mQafJWfTCwMLcPp3bHkRykr0zLC8b5yQBHBajYOKCJYzcYBxb8TrF/lWGk9fCYwwQAAAABJRU5ErkJggg==', '2026-08-04 03:58:10', '2026-09-15 12:28:05', NULL),
('a39af54b-7f76-4c85-aa11-2ffa17cd9a36', '54444', 'DDD', 'Dasanayake Dushan Duminda', '908260090V', '2003-07-17', 'Male', 'AC', 'Administrative', '66e284eb-945e-48d7-8c5f-f1d3de0965af', '174C ', '2026-03-05', '2026-11-14', 'Active', '076456783', 'isanaga32853@gmail.com', 'Aravinda Isanga', '097918 71190', 'O+', 'A4G4', 'Buddhist', 'Sri Lankan', 'Air Force station jalahalli (west)', 'N/A', NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACFElEQVR4nO1ay23DMAx9lA3kaG+QUZTNio7UDeRRMkAB+xjABgtSktMUKOAe2rAQ38GWlXcgSJHiJ8Q4iCkcZQJODa4s+HE5jOBUuLIOIzgVAiro5WMjuixEwFK3L64sU8clsmCWZIJOzK9jx3RBp7tsTNaGqX15LyMQ39RuAMV5JMYCENCtVmQNTsUjStQb1rpyZRn0rR3TOIOn8R32ZA3NU/uigUFupwVgYJO9E9dPV5a54zJp7jdKJFxOjDhrTNxySmhMVrTuW7x/M5aNGFirv/22AMGp+KGySNxKHQzTeZXLa6NPP7hejZws5JIq6XpYwWmQAmuoe3HuOFdj6emyhuapyNaSwph5lnJYHmmoRVbktdTOyZUVbFgLcX+IW5XWhhjq/pmeLmtonorSW9IgKMZTt5KcMAdB1PYTu7VgxlqPUU/CoZosX2PuW7asFcWZ1I9KbqHXWOW4tex1nlge0tCVFQPTpVs1j2cjsobmqahZxn5vqUo+5YQeCe1l8BUaDu9VVuZ4JDQ7Ox5u0tC4yey4L75lStZDCI3MjuP1VFYaDvceFMzI2jAVOf7tBRYnTQwf7q2M9HRZg1PxFcON6GVP3nWU4v+isXpc4lUHkXJl7dXxnwrwPQJap/ZfZscU01rrrbPPtwx3niDJe96rLUKfmBifHSukyStvnSJ7L8OKtYJT4co6jOBUuLIO4z8p6wPu6lk93muCtAAAAABJRU5ErkJggg==', '2026-08-05 05:25:39', '2026-09-15 12:28:05', NULL),
('b65eb892-ab14-4968-b2c1-f3f4d52b809a', 'TA/40218', 'RAK', 'Tharanga', '200227604425', '2002-02-21', 'Male', 'AC', 'Account Assistant', '0b7a2bcf-5ac0-4590-a777-05febce54289', '2/2026', '2025-03-01', '2026-05-21', 'Present', '.', 'tharanga@gmail.com', 'Gamini Ranjith', '.', 'O+', 'A4G1', 'Buddhist', 'Sri Lankan', 'Padavi Parackramapura', 'NA', NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACB0lEQVR4nO1aS2rDQAx9UgxZ2jfIUZyr9Wb2UXqAgGcZGKMizThuKYWhpamo9RZhPHkLIfnN6GMSNGLmViYQVA5nIV6XZnBQEc5qBgcVCqroQFfbSLpK23bZ43AWfLxZoygWW69E1z7r6mS74szWFvD/pqZNQvNwEnu0bdPbUwxoAOPo1O7TTuqyIJ0yPccADiq+7SyZVFHlogq/etVWr7dTAqqi+gzRR/FkKwcVhtlyv0HzjeWRE2q+oQhn+dKWPJ4FaSUB7vojvmzloEJhsnqf/6WzmLaK6KLecvK6oJRUIhky9SIYJZfyy+qtsrJqbPpzW/nwVJRYaSb4HpplaAQxLrVElogW/Lwupy0oFqhlPxjXyDKcaQtFTLuOetObnYSmstCWp2jV66nKSssvsUOwriJanqIlKisrtfaT0PRm0QptOewTynyxhsbZDsZO19rf7TKNkwtbg4ov763qojgJXfYyxEJG6G+612WoogiJ3NjKQcXH2bFMqVO93cmahTXBCGf5nB1TGRvXy6uMKZ9hQAu4iXWo2fH4qoFSaIsQ8yU/x4AGcAvpUFR5GfS7DKxUqmNFdHXdTvrHZYDMOulCfyOZr902OOFfMYCDip/NjklDRnYm6ir86q3eKqgjEss3Sn/DUo3oPLmdHe9Ss48z9j8ZzeCgIpzVDA4qwlnN4KDi6M56A6zWPsdB+mCXAAAAAElFTkSuQmCC', '2026-09-10 11:32:31', '2026-09-21 07:17:30', NULL),
('b7b7149d-5fd8-4791-9cb1-fe6178f720f9', 'tw 4988', 'I.k .G.I.N', 'karunathilaka', '200579903281', '2005-10-25', 'Female', 'AC', 'Administrative', NULL, '174 D', '2026-08-03', NULL, 'Active', NULL, NULL, 'siril kaarunathilaka', '0779459485', 'O+', 'A4G4', 'Buddhist', 'Sri Lankan', 'ihala abathale ,labunoruwa,maradankadawala', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACCElEQVR4nO1bQU7EMAwcO5E4ZiUewFOyP+BJfK15Cg9Aao8rdWVkN2EXThUSYFH70KbpHCy79o7tLAl2SuO9SCCgHMZCfC67hQOKMNZu4YBChbpkoJ3sMQNYxvY5jOXqc6miMuvqlQh1vqqPku2KM133CP9v6NJDiOiUBCjdRz3KfOl6XGj+8iztfCVplFbB8hsKcEDxfWPVWWMr7Or6yyoiMumiPa3qsivZtoisv6PADmEcHYp7HoEkW2z1y9g2DjL9ua58eCjks2wuQ9EA+/xmCmOxm9hKPcB6RCVNjMrg507jJbwFT5xQttuiq+VEqLrRni8kTnTlw0PzcJTRirQSioB0hUbmtwyqxj/48MZiN79ba8+JVVdT0YuRjvFCIhPCC7TduoObJKGzxdsSvQw/3sr9vjzc03gsmheLEY41e9GVDw/FyH+9Or49GjvcquOot3yxjKaMQkkg1emapZ3eshZd+jYJOdGVDw/NZgGq8+NqTHDkwySkHtzYYRjLcy9DjLH3dBjVsePZcTVqYfMtpYPt6RKzY7+zY5TL4O3WLLwNUNiJrgeGopNAG/KbZz4K4y6RCR3PjmGVV5lH2/CnFeCA4tvGItKuxsvrOPN01j5hnHlyFltFQ8kOYpQ3Mm5hsSVA9OCdz45lY/AxO/bmLYp/LeCPXcABRRhrt3BAEcbaLf/UWO/OtkT/DN1C4gAAAABJRU5ErkJggg==', '2026-08-03 05:17:16', '2026-09-15 12:28:05', NULL),
('b92a011e-8967-4e81-9456-93b923d19866', 'S-1789362557', '', 'Test Trainee Expiration', NULL, NULL, 'Male', 'AC', 'Airframe', '8116f096-d83b-4000-9308-6b6b7ddf7e05', 'Batch-TEST-EXP-1789362557', NULL, '2026-09-14', 'Passed Out', NULL, NULL, NULL, NULL, 'O+', 'A4G4', 'Buddhist', 'Sri Lankan', NULL, NULL, NULL, NULL, '2026-09-14 10:39:17', '2026-09-15 12:28:05', NULL),
('bbd307bd-5dff-4d7e-9da6-701db2ee5c72', 'S-1789362528', '', 'Test Trainee Expiration', NULL, NULL, 'Male', 'AC', 'Airframe', '9ef4c9a9-ad44-49d0-a514-b3c533af66d1', 'Batch-TEST-EXP-1789362528', NULL, '2026-09-14', 'Passed Out', NULL, NULL, NULL, NULL, 'O+', 'A4G4', 'Buddhist', 'Sri Lankan', NULL, NULL, NULL, NULL, '2026-09-14 10:38:48', '2026-09-15 12:28:05', NULL),
('d0fca849-4bf5-4c56-be89-38a21d42a187', '51873', 'NWAMSP', 'Adikaram NWAMSP', '984562484V', '1996-12-17', 'Male', 'AC', 'Computer Technician', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '171', '2026-08-04', NULL, 'Present', NULL, 'sankaadikaram1996@gmail.com', 'htrhh', '175', 'O+', 'A4G4', 'Buddhist', 'Sri Lankan', 'sdfdgf', 'fewaet', NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACJUlEQVR4nO1aS47jQAh9YEtZ2jeYo5Rv0Edq9c3so/QBWrKXkWwxApc//VmUZpHQY5DiVPBbICiKVxASFMrApUggoBzOQmyXYuGAIpxVLBxQqFCWGtRhIeomImDa1F04y9V2SaIyKpmgm2BoK6EOlWnFma0lwv83dMopJDIuBDR3MrXlmzdbrwutv6uqGZhqCKZHGMABxT9Hi/Tz8x2Mw69wsgkbEel1kWSG1S1Ti+jPRxhQIFwCugJ0MO7X6nK6Cb2OyOxQxZmtuPpJKGeVsQzNqEZ82cqXh2Lj6JWehHb+KW8fgdPBaPy+D2exj2hJ38zb6ojbrltf8LNt5ctDsebWmj0aI02mNbdktCwzXUTLxXbZGfxSI8lCMrSjbCUrVzBxYitfHop8zmkeWaEygpG0B5XGvYxFbvnaLo22mprMN/KjuZMVtIcYUCCMq0Nx4oR7jcoM3viGRjDqliuoiNyJOouRDkvS+20PmRYvT7ZeGVrbk9B8QAbSe/JUzbTGaCIgvUcP3k+0cLpRHVz+dCYeVzJ+tq0cUHyeHctbuxAGfejYxEIWs2OPt2OxjFovxnmefGpo9E+3lQOKL7Pjtz8bZde+fNStX7Bdhla7uppWR/Dg1NZLz47TQQJ10qUISr0LWwNaZ09YY9D+iNHMNaVtsiXDi5awcJazXobJPt/fWoRrszB6GU5nx7J+bZ13AaIH7ydaHFCEs4qFA4pwVrH8Jmf9BX62VNmFjdzlAAAAAElFTkSuQmCC', '2026-08-04 05:38:25', '2026-09-15 12:28:05', NULL),
('d9f8c58f-5f7c-4f23-a51d-337fe13e7e40', '50870', 'IGKGP', 'RAJAPAKSHA', '200028300936', '2000-10-09', 'Male', 'LAC', 'Administrative', '66e284eb-945e-48d7-8c5f-f1d3de0965af', '170', '2026-08-04', NULL, 'Active', NULL, NULL, 'IGW RAJAPAKSHA', '0776295268', 'B+', 'A4G1', 'Buddhist', 'Sri Lankan', 'A-98/5 ALUTHNUWARA,MAWANELLA', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAAB/0lEQVR4nO1bMW7DMAw8SgY6ykAfkKc4P8vXrKfkB/YYwAELUnTSZCiMDgkRk4MqyzcQPNHiiSkxNlpNW5FAQFMEC7FdNlsKKCJYmy0FFGJk1gG118cOwLwuHyNYrrbLwGKTzM5EGKarcJR1lZ35usXSZ0NnSyGiPjNQjCPLMl++7hfaPT1zPV6JK+WFMb/CgRRQ/D9YwyS5FXF1vbMKM48yqYdFKLuSLjPz8hoHNljC3qH4XUcgc8stG9ZlrUHGt/uadg8FP1qjDEUS7PHNGMFKbnIrW4JJRvEoxbsOPFkZz8EWnLDFemRJRqnoMuWlL3Qt2HLFFjeOTGqtuaVZFueWu5unIzLTsdzKwXKRmjAznXgxyuDE1z1DOx1VCZsmFo6ALxmEt7l342sKKNRqf88olVr6aOdWBMtZTTg0baVFoB1UrTpUdRx6y9eXsB6sgCcUBlW9ySiLvNUPowtfA9o1joZztwDztwxKTl6UMpJZBMvtXcbQ1PH9cxjq2HHvGIWZTqq8ZmklHy7RO3ZXZbBKZLsi5FG6kS234p7Qce8Y7cZQ04qIUKN37JCt1ezIasW7Wugtv2yRJdgt3+ZuXUsvceAPS9g7tLO/RfTW+kMMklsNFWAM2Azv9zXtHorn3vG95x+9Y3fbheK/FvBmClJAEcHabCmgiGBttg8N1g//yl/CL2c7cwAAAABJRU5ErkJggg==', '2026-08-04 04:06:49', '2026-09-15 12:28:05', NULL),
('e1650c87-f565-471c-85e8-a157df7dc81b', '50327', 'MS', 'Rashmika', '199804700695', '1998-02-16', 'Male', 'LAC', 'Computer Technician', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '169', '2026-05-02', '2027-07-01', 'Present', '0764188538', 'srrashmika98@gmail.com', 'Mother-Sanjeewani', '0757241388', 'AB+', 'A4G1', 'Buddhist', 'Sri Lankan', '360/102 Samagi MW , Dangedara,Galle', 'NA', NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACB0lEQVR4nO1bwW3DMAw80gL6dIAOkFHUzTpTN7BGyQAF7GcBBSxIyWmSR2H0kRA1+TAk5R4EzydStEKCjVZ4KxIIKEewEK/LZuOAIoK12TigUKNuCSgHmyYAy7r8FsFy9bpkUZt1dCJCns/K0WCr4szXLcb/G7p0CREdBgHGzlFXmS9f9wtNd3Mpb2eSQkMVLI9wgAOKvwcrz6qtiKvrN2sUkUkH5ViVsjPZsojUxziwwRh7h+K6jsAgTVv9sS5bDTI93VfePRRya40yjCqw21+mCBa70dbQBaaKkkmLd3vI3Mt4Cbbgha08rzmqjezkZRyNtctverqvvHsoOhWtyuhHrVVbprLIW97OW5RPBMm6GebpnATjJwkwVMqiUx++8u6hqUWgHAUorR84CAEv+tAyfjlEsPzthHU9dNnITKeayyJv+WILWlHcHbCuK4+oMjzthFIOM6Qca0L+eK1UrJMx1rRujC58DWi6rjJOmq3GL2VnaJSRjiJYjnsZuKrbrQcVecsXW+hmDY3ewejd+EsPanq6rxxQ3H87lgoibcQ3olRbJjVEsNhR5wldTJeuRrPYCf1CZbpPaPF9yy9b9H5K6Jec7K7GcpnyQxz4xRh7h+LndNxqi8tXZEtj0cvwCC12b9BagktvHfYrUBTa8sMWxb8W8GQKOKCIYG02DigiWJvtnwbrG+AXhcOrzlmsAAAAAElFTkSuQmCC', '2026-08-11 15:15:23', '2026-09-15 12:28:05', NULL),
('e278bced-fe8c-4e93-a6e5-9cba4911af21', 'SN-90001', 'W A', 'Sanka Adikaram', '199612349001', '1996-12-17', 'Male', 'LAC', 'Airframe', NULL, 'Intake 171', '2026-08-01', NULL, 'Active', '0771234567', 'sanka90001@slaf.gov.lk', 'Parent Name', '0711234567', 'O+', 'A4G4', 'Buddhist', 'Sri Lankan', '123 Main Street, Ekala', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACFklEQVR4nO1aS26EMAx9NpG6BKkHmKMwN6t6pN6AHGVuAMtKjFw5CZ9WmipdTOsOfotA4C0sGzv+QIJKRK5lAk5lVxb8c6kGOxWurGqwU6GgggBEIgKmsmScXVmmPpdeFGO6m0HUNUJnNOmpGJO1BvzY1GlxoUgBIuOVZMhOF8zJWgE+BpVeRoDO7YwS/35bgG/A3708KrURxO4vBbgFxtGpoVxbPZ0mQGLXQOL5SfL27gKwU1EP2eUR6lb9uC3L45SDDK5XtuFbsu4lnmZ1tbSILVnZqVAQ6UFVSq0Aee2utHvhyjIWCdvsTEv8azX06U2OiR4JTWUZ/VtIyyzxJCDguqYf72RFVj48FYtvqVvJvHcm0W154VmGic+lWGszVHo2tNu2tJ/Ec0JYooraKPebXi5ab0HbT1tXgw3JenDfGkuBtSUducmb4JHQGLUtZ1RO2ZPxYrcGRluyVoAfmzppDqhTrf4SIENuyV8puZVHQivWgnzGvvJaW1IeCa3OjhP6UXsZ6m+byWBE1irwQWbHmFI6qFAv281O+J4C1IBxdCqWnLDkFqW2SuFQoYWY11tmqTH9NpOSjrwNXm/ZtRba9X8aLb8GzTd+V4CbYBydGr7MjkltRP1bM0P7u/cXgJ2Kn1or5kZ7oyZ7niXZDQgz9ZewHGHseoW12TFQZseybsWIrOxUuLKqwU6FK6sa7FT8H2V9AFvoL0Ex1VRCAAAAAElFTkSuQmCC', '2026-08-04 05:53:16', '2026-09-15 12:28:05', NULL),
('e3ab5331-1cd2-407e-a1e3-c357abc0263e', 'AW/5023', 'NHPND', 'NANAYAKKARA', '200072200699', '2000-08-09', 'Female', 'LAC', 'Administrative', '66e284eb-945e-48d7-8c5f-f1d3de0965af', '170', '2026-08-04', NULL, 'Active', NULL, NULL, 'SOMAWATHI', '0766484292', 'A+', 'A4G1', 'Buddhist', 'Sri Lankan', '118C2 BULATHWELDENIYA,NIKAHETIKANDA', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACNklEQVR4nO1aS47bMAx9pAVkaQNzgDmKc4MeqejN7KP0AANYywAOWDxK9nxWnkUatSYXjuS8BcEnfkRaDAdl1qNIIKAaxkIcl8OiAUUY67BoQEGRKomrBLlmf2yvr2GsNo5LKj/jxGd+KTsDVv52/oQ8UgENKL5trLy50LjcxbeFKLpa2LXZkzW/Freyf0DX00HTlz1JskZ11YCiSG9mzF1yxV3k2q/wrZmV3IUwFpo5LrPXfgOX+WKA14TkjRJstRUJbd9byVv9TexrSNSHKKABxTeNJXSrUv/VmvBi7lvF6eK+1dbJGn/Tyfob6WEk7FdGx4vJTzNrTNcTQ9O2uIt5thqNHjW8JeM73phXa0RXPT007dkqyTgZBPmF7Ny3DobTGMZqLhLar71vMQ8dC/quxsS/oMARUZwdCqN8WI3lgtUZxsXZ8ne8jT1dVw0oClGLX7roWzmRN9Ybr7cSDf2ejDAWWuo8Cfo3qZ33PGw9qJxWKR16fbauenpo2ohak9eE5XY8/2C94RJ5q8lehjFHkSPS1NeZlyBLM7pqQPF5duwZzCafb2W2NrzACGM1dVxGLwgX9uAZ+mo5yOqw9Hdb0vXEUNS6nTVh4QgdedunkRyluExP11UDis9itnC+xQ5GuR37uCuM1ehxmYft4WOTiXVi5K1G2MLWwfC8tWWrPTCWoiMiYVtsVan9psrRO3mRtxqdHcM/Jez5hh9nfPhTH6KABhRhrMOiAUUY67BoQPFfGusPlGYJC5gNooMAAAAASUVORUSCYII=', '2026-08-04 04:34:15', '2026-09-15 12:28:05', NULL),
('e59d3871-3fa2-44db-bcb0-068ba53fe6e1', '51837', 'NWAMSP', 'Nawarathane wasla adikaram mudiyanselage sanka prabhath adikaram', '963521219V', '1996-12-17', 'Male', 'LAC', 'Computer Technician', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '171', '2026-07-23', '2025-02-05', 'Present', NULL, NULL, 'sanka adikaram', '0766932107', 'O+', 'A4G4', 'Buddhist', 'Sri Lankan', 'No:60/B, Madadeniya,Kapuliyadda\n20206', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACMUlEQVR4nO1aQW6EMAwcm0h7BKkP2KeEr/Vn8JT9weZYCeTKTljaA1JUabdp8RyAhDlYThxP4pCgEjPXMgGnsjsLPl2qwU6FO6sa7FQoqCCARqxEYyIC0tY9urOami5RFHdA3ukiMvUiNKKzXmnM1hrw/6amLYTivYSadVu8vcSACnAN6WTUftFQW37PgEPw8a+zUudhJXnfI+rlBhyDcXZqKO9es1PSlfB2EQK6xZZCaclWdioMs6WqAdiTF6Dq8JHB4M5CI7ElX7tWknnotnh7tgHsVNRDskY3bXHvRKbct0BEm/bX9P3kfuVGZla0pa//II0oIRo6Mb1BY3IF385ohfJOb0IzdULxRpB5JB3BQZfIpRlb+fTUUDzQf5CUlAVQFIDm6xI2heHOaskDOkaY6VIymB5tmJYHUHIZmrH1xNSwf1KUVfOWpqyroIRVfwfFqQlbnRqKJ9JFMJNp+VX79iXQmu6sJjxQFHzRhEVRZOE+oZOvTf5tW9mp2BFvIddOtqrWSna+6/WtVqYL5Dv2fbKNm22/fHfcymgFe25ZqlsEKUBlvNaO3xZkgfFEA9ip+HHtuMAymD70QKP0MarBTsWzVUbU9U+XPjsnzLCzQ1cZzU7CVGonGfmw8KUGHIKPf52UKnaVRlQdZmyqHu3Zel5qbxssvTZz1etOuxL0M/gG61sZj+2wZTBtPrS8+O4YzdWOJb/6JX9ZxUQasZWdCndWNdipcGdVg52Kv+OsT+J3E3bLUfDHAAAAAElFTkSuQmCC', '2026-07-23 05:41:22', '2026-09-15 12:28:05', NULL),
('f439ed35-6970-4829-a862-a844cdbfa50f', '51050', 'WMDNG', 'RATHNAYAKE', '982051819V', '1998-07-23', 'Male', 'LAC', 'Airframe', '66e284eb-945e-48d7-8c5f-f1d3de0965af', '170', '2026-08-04', NULL, 'Active', NULL, NULL, 'Nilanthi Kumari', '0714086475', 'O+', 'A4G1', 'Buddhist', 'Sri Lankan', 'Bulugahawatta, Ihala medagama,Kumbukgete', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACQUlEQVR4nO1Zy23kMAx9lATM0QZSwJSi6SAlLbak6cAqZQoIYB0D2GBAWvbkgyDOYRNizXcYW553IEjxT4ydKGEvE3BqcGXBr8tuBKfClbUbwakQUEOSw0x0qURAXT9fXFmmrktmwSjFBJ2Y//aR6YKoX9mYrAempvasPZCvajeA8tgTowIExMmKrMGpeIsW9bppfXNlGfStDaUfwaV/gj1Zw+GpqWmgk+xUAQZm+Xbi9ejKMndditZ+vUTCemLkUWPivJSExmTF0X2LtzOjzsTAtPrbvxYgOBXfVBaJW6mDoZwnSV4zvfrD9WrNt+aEzJqyIhO6yChisHxNE+XBhKxOTaoHytceXCgy5VuauDyq3QTds+ctexV8nAidFO/nSbpjTWVzkoKeyYis4fBULMMl5gk8rI2x1oTIYxSTtfETD66sYOO60DbBYB4j8wA11Ew83KcawYasuxD+f2q+Jem3dOguhlIz6jT+hwT4AgFHp6b2rD0oDyxjXC0RGSgXyWX3biz8tqzh8FQsOxFJVOpMr5LXtkpZ9imDKyuYqTIaZIIhxouLje4mY7cW7O2O800GGjrLqHL0baTl3TGkHNQKXsPhNoOCGVkPTMUS/7YGq1Xwb/LWguHXZQ1OxTuU8zPRn8XL1lWK91t2r0uU7lhdTUpEKTp+WIDPEHB0anq3OyYgSRSUGfzZ91s2rVWWUiLKj2wj64M0xrIsuanxTMjq1PRhd7xNDNuxvcGVBb8uwX0LHl12IzgVrqzd+IayXgDZpAjbxZsnAAAAAABJRU5ErkJggg==', '2026-08-04 04:03:49', '2026-09-15 12:28:05', NULL),
('fc2fdbed-f23f-4463-b73f-f5c67cc043e5', 'AW/4967', 'PMSM', 'PATHIRAJA', '200054303466', '2000-02-12', 'Female', 'LAC', 'Administrative', '66e284eb-945e-48d7-8c5f-f1d3de0965af', '170', '2026-08-04', NULL, 'Active', NULL, NULL, 'NIROSHA GANGANI', '0712655970', 'O+', 'A4G1', 'Buddhist', 'Sri Lankan', 'NO:70,THMANNAWATIYA,NAWAGATHTHEGAMA.', NULL, NULL, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAACIUlEQVR4nO1aQWrEMAwcKYE9JtAH9CnJ1/qz+Cl9QCE5LiSoSLaTbWHBFNKaRjpsYu8chMYjyXZIUGiBS5GAQ9mDBV8uxcYOhQer2NihUKNkLWjERjQuRMCSp0cPVlXLZRC1GZA3uolMnQiNaGxWKvO1xPh/Q5csoWFOUrNp09uvOFBgXAK6GLRbVWrr3znw1Pj5X1eFhn4jeTsU9esOPDfG1aFtenZanRbNhO83IaBZLRVKTb6yQ2EWrFT1wFG8AO0O9woGDxYq0ZY8Tm0koW+y3s52gB2KcpPYo1tvMTcik05qlyGiQ/vX+vvJ48p1sCXGzKSUoTPyJPM2N85WbWxNthM2MekWORGVlefaqg9K9HonhD6JCeF1fdgnoypfLwpFUk8sWSkdxpxoSRD5+Em8bqEWtgBT1HGMoUNjS8uYZ8LKoJ1ytGg/v9yUo3vOf9g8E9aYCbF3gkfncUDEMyGqYUu0WuV0KLKf6qbs6GydR8EP9lvZ0gYr77K8blV48kRp1KwC3Ml+gOVlxTCd7AA7FOUmUVH2yG18vuRKR1JRdZPHlavpMpA3WN3XupUPC8XZQn3Q4b19vN/Xy0n/iqYWttpvYwm9PrqP/Zpyf+NTHGCH4sd3xzTI1opukckajDD6VzT1rKw2PkLsCvUOcjFx2Vyz0jC/xDt//L2vfHloaxE4LoklDrTVSMP0Bg8WfLnw5QXDHgF4fi02dijOCNYnxLpiNI34yR8AAAAASUVORK5CYII=', '2026-08-04 04:17:31', '2026-09-15 12:28:05', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `student_status_types`
--

CREATE TABLE `student_status_types` (
  `id` varchar(36) NOT NULL,
  `code` varchar(50) NOT NULL,
  `label` varchar(100) NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student_status_types`
--

INSERT INTO `student_status_types` (`id`, `code`, `label`, `is_active`, `created_at`, `updated_at`) VALUES
('ss-active', 'ACTIVE', 'Active', 1, '2026-08-10 09:31:21', '2026-08-10 09:31:21'),
('ss-awol', 'AWOL', 'AWOL', 1, '2026-08-10 09:31:21', '2026-08-10 09:31:21'),
('ss-leave', 'LEAVE', 'Leave', 1, '2026-08-10 09:31:21', '2026-08-10 09:31:21'),
('ss-passed-out', 'PASSED_OUT', 'Passed Out', 1, '2026-08-10 09:31:21', '2026-08-10 09:31:21'),
('ss-sick-report', 'SICK_REPORT', 'Sick Report', 1, '2026-08-10 09:31:21', '2026-08-10 09:31:21'),
('ss-suspended', 'SUSPENDED', 'Suspended', 1, '2026-08-10 09:31:21', '2026-08-10 09:31:21');

-- --------------------------------------------------------

--
-- Table structure for table `subjects`
--

CREATE TABLE `subjects` (
  `id` varchar(36) NOT NULL,
  `course_id` varchar(36) NOT NULL,
  `code` varchar(30) NOT NULL,
  `name` varchar(150) NOT NULL,
  `description` text DEFAULT NULL,
  `periods` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `subjects`
--

INSERT INTO `subjects` (`id`, `course_id`, `code`, `name`, `description`, `periods`, `created_at`, `updated_at`, `deleted_at`) VALUES
('005b5e66-2fa6-4568-88c9-13cc8817326c', '0b7a2bcf-5ac0-4590-a777-05febce54289', '16', 'SLAF Non Public Funds', '', 6, '2026-09-09 10:49:25', '2026-09-09 10:49:25', NULL),
('02c8dadc-756f-47f7-ac46-8a3de12c98b9', 'ca0ae649-cffd-4712-b156-8209ffd159d4', 'DAD', 'Desktop Application Development', '', 40, '2026-08-17 10:19:44', '2026-08-17 10:19:44', NULL),
('12517d10-edbd-4ee9-96de-4b4d0f6f1a46', '0b7a2bcf-5ac0-4590-a777-05febce54289', '08', 'Bank Accounts public Imprests', '', 6, '2026-09-09 10:42:04', '2026-09-09 10:42:04', NULL),
('159f77c9-e545-46eb-bca6-49503136353c', '0b7a2bcf-5ac0-4590-a777-05febce54289', '09', 'Public Imprests', '', 24, '2026-09-09 10:42:28', '2026-09-09 10:42:28', NULL),
('20b7a2c2-d14f-4d8c-94d5-34b2a89def3a', '0b7a2bcf-5ac0-4590-a777-05febce54289', '01', 'Public Account', '', 60, '2026-09-09 10:35:24', '2026-09-09 10:35:24', NULL),
('294a13c2-da21-4208-b925-23af2b0fb371', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', 'SDLC', 'Software Deveopment life Cycle', '', 4, '2026-08-12 10:18:39', '2026-08-12 10:18:39', NULL),
('3b8ca667-ee94-4eeb-ab4e-458561596270', '0b7a2bcf-5ac0-4590-a777-05febce54289', '14', 'Travelling Claims and combined allowances', '', 6, '2026-09-09 10:47:25', '2026-09-09 10:47:25', NULL),
('3ffa680a-7a95-4520-9712-979cc000e392', 'course-basic-admin', 'BA-ADM-01-MOD1', 'Basic Administrative Assistant Course Core Modules', NULL, 40, '2026-09-17 10:49:16', '2026-09-17 10:49:16', NULL),
('40f9d52c-b752-4d93-bb54-e09192a03e4a', '0b7a2bcf-5ac0-4590-a777-05febce54289', '03', 'Computer Awareness', '', 60, '2026-09-09 10:38:18', '2026-09-09 10:38:18', NULL),
('44243c82-8ffb-41f0-9cfd-0955261e87c1', '0b7a2bcf-5ac0-4590-a777-05febce54289', '23', 'Service Writing and Abbrevations', '', 36, '2026-09-09 10:56:09', '2026-09-09 10:56:09', NULL),
('4fef96ad-0eb8-4cfd-97ff-002c189ec485', '0b7a2bcf-5ac0-4590-a777-05febce54289', '12', 'Loans/Advance under the Advance Granted Accounts \"B\"', '', 6, '2026-09-09 10:46:08', '2026-09-09 10:46:08', NULL),
('5e9acac5-a8fa-4362-ae55-4a9d80ef0ad6', '0b7a2bcf-5ac0-4590-a777-05febce54289', '07', 'Register other Documents and Payment Procudures', '', 6, '2026-09-09 10:40:40', '2026-09-09 10:40:40', NULL),
('5ea56f2b-bcf7-4e6c-93c0-aadfbaee1c5c', '0b7a2bcf-5ac0-4590-a777-05febce54289', '04', 'Role and Task Of the AF', '', 12, '2026-09-09 10:38:59', '2026-09-09 10:38:59', NULL),
('68a7987d-6be2-4980-8829-8a23f85309b2', '0b7a2bcf-5ac0-4590-a777-05febce54289', '17', 'SLAF non Public Accounts Procedures', '', 36, '2026-09-09 10:50:12', '2026-09-09 10:50:12', NULL),
('692c4ef9-f995-4b05-81ba-29f81d75eb1b', '0b7a2bcf-5ac0-4590-a777-05febce54289', '22', 'Administration of Leave Officers and Other Ranks', '', 18, '2026-09-09 10:55:42', '2026-09-09 10:55:42', NULL),
('69c35932-0fd5-43f2-9da2-38a793aece74', '0b7a2bcf-5ac0-4590-a777-05febce54289', '10', 'Pay And Allowances', '', 18, '2026-09-09 10:43:24', '2026-09-09 10:43:24', NULL),
('736ebc24-5a3d-44b2-9012-39e71ac9b333', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', 'MAD', 'Mobile Application Development', '', 7, '2026-08-12 10:26:28', '2026-08-12 10:26:28', NULL),
('7d7af610-49df-4a58-882e-166d212fd6ba', '0b7a2bcf-5ac0-4590-a777-05febce54289', '21', 'Absent Without Officials leave and desertion', '', 24, '2026-09-09 10:55:04', '2026-09-09 10:55:04', NULL),
('7fd8a821-2fd1-432d-9e9c-b1af15c066fd', '0b7a2bcf-5ac0-4590-a777-05febce54289', '19', 'Essentail Resource Managment', '', 36, '2026-09-09 10:53:36', '2026-09-09 10:53:36', NULL),
('805b4507-676a-426c-a1eb-5a94e8ddf14d', '0b7a2bcf-5ac0-4590-a777-05febce54289', '18', 'Gagana Viru Sawiya Walfare Scheme', '', 6, '2026-09-09 10:52:39', '2026-09-09 10:52:39', NULL),
('894bd95e-b757-4975-8e6b-5e21f9e90201', '0b7a2bcf-5ac0-4590-a777-05febce54289', '06', 'Responsiblities of Admin Officers at SLAF', '', 6, '2026-09-09 10:40:03', '2026-09-09 10:40:03', NULL),
('90d50500-01db-4003-8299-ad1817ec00b0', '0b7a2bcf-5ac0-4590-a777-05febce54289', '15', 'Introdution of Accounting & Basic Concepts', '', 12, '2026-09-09 10:48:02', '2026-09-09 10:48:02', NULL),
('9624828d-62c0-431f-9494-d54aec8ae306', 'ca0ae649-cffd-4712-b156-8209ffd159d4', 'DBMS', 'Database Managment System', '', 40, '2026-08-17 10:11:57', '2026-08-17 10:11:57', NULL),
('a63d0f08-0f60-47c0-91e4-93e0780c6a4f', '0b7a2bcf-5ac0-4590-a777-05febce54289', '20', 'Registries and Filing system', '', 30, '2026-09-09 10:54:15', '2026-09-09 10:54:15', NULL),
('bf89db32-42b8-42e7-8a39-ae30cf395c7d', '0b7a2bcf-5ac0-4590-a777-05febce54289', '02', 'Non-Public Accounts', '', 12, '2026-09-09 10:36:42', '2026-09-09 10:36:42', NULL),
('cca882ce-0993-475e-8f02-908b239e14e5', '0b7a2bcf-5ac0-4590-a777-05febce54289', '11', 'Salary Payment Procedures', '', 6, '2026-09-09 10:45:17', '2026-09-09 10:45:17', NULL),
('cdf0b002-1b8f-4de3-afce-f32d0c1400e2', '0b7a2bcf-5ac0-4590-a777-05febce54289', '24 ', 'Routing Orders', '', 18, '2026-09-09 10:56:31', '2026-09-09 10:56:31', NULL),
('dfa0b877-ea20-422c-a7b3-7738fbe35e60', '0b7a2bcf-5ac0-4590-a777-05febce54289', '05', 'AF Accounts Administration', '', 6, '2026-09-09 10:39:29', '2026-09-09 10:39:29', NULL),
('ebc66534-457f-430e-bb3b-4a2747015e8c', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', 'DBMS', 'Data Base Management System', '', 5, '2026-08-12 10:17:12', '2026-08-12 10:17:12', NULL),
('f67d16bb-36ce-4b25-8c6c-77109ff4e041', '0b7a2bcf-5ac0-4590-a777-05febce54289', '13', 'Recoveries', '', 6, '2026-09-09 10:46:49', '2026-09-09 10:46:49', NULL),
('fafb3737-e8b6-4270-b01d-912335afc118', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', 'DAD', 'Desktop Application Development', '', 4, '2026-08-12 10:19:56', '2026-08-12 10:19:56', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `timetables`
--

CREATE TABLE `timetables` (
  `id` varchar(36) NOT NULL,
  `course_id` varchar(36) NOT NULL,
  `date` date NOT NULL,
  `period_number` int(11) NOT NULL,
  `subject_id` varchar(36) NOT NULL,
  `lesson_id` varchar(36) NOT NULL,
  `instructor_id` varchar(36) NOT NULL,
  `location` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `timetables`
--

INSERT INTO `timetables` (`id`, `course_id`, `date`, `period_number`, `subject_id`, `lesson_id`, `instructor_id`, `location`, `created_at`, `updated_at`) VALUES
('03616d16-aed7-4f6c-824b-91b77691d6c8', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '2026-09-16', 3, 'ebc66534-457f-430e-bb3b-4a2747015e8c', '04673170-69a7-4a12-8679-7184c9e6294c', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'H-05', '2026-09-17 10:49:55', '2026-09-17 10:49:55'),
('073a8462-01ea-40c7-ae4f-22cfecc67588', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '2026-09-17', 3, 'ebc66534-457f-430e-bb3b-4a2747015e8c', '04673170-69a7-4a12-8679-7184c9e6294c', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'H-05', '2026-09-17 11:44:12', '2026-09-17 11:44:12'),
('09e828e4-c106-413a-a179-417d53058b79', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '2026-08-31', 4, 'fafb3737-e8b6-4270-b01d-912335afc118', '98e1933c-53d1-4a2d-8560-20d0222631fe', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'H-05', '2026-08-31 10:43:14', '2026-08-31 10:43:14'),
('1587b89a-80cc-45f3-8167-13d070c1b67b', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '2026-09-16', 2, '736ebc24-5a3d-44b2-9012-39e71ac9b333', '5da752f1-0dd1-461a-a310-35bc05031e59', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'H-05', '2026-09-17 10:49:55', '2026-09-17 10:49:55'),
('37d59bc0-8167-4e28-886b-a95b6a913993', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '2026-09-17', 2, '736ebc24-5a3d-44b2-9012-39e71ac9b333', '5da752f1-0dd1-461a-a310-35bc05031e59', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'H-05', '2026-09-17 11:44:12', '2026-09-17 11:44:12'),
('55651f7b-8e23-4698-8993-d79d1c85fc7f', '0b7a2bcf-5ac0-4590-a777-05febce54289', '2026-09-11', 1, '005b5e66-2fa6-4568-88c9-13cc8817326c', '2b4e2908-405e-47d0-bed0-f6337cab72a3', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'E-18', '2026-09-11 09:26:02', '2026-09-11 09:26:02'),
('5a3a9b85-3bf7-458a-8bc2-198ccae458b5', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '2026-09-16', 4, 'fafb3737-e8b6-4270-b01d-912335afc118', '98e1933c-53d1-4a2d-8560-20d0222631fe', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'H-05', '2026-09-17 10:49:55', '2026-09-17 10:49:55'),
('5dd5f988-9cef-4170-9af8-8487f2cb67d4', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '2026-09-16', 1, '294a13c2-da21-4208-b925-23af2b0fb371', 'bac287ab-d947-4c0d-851f-d77003831682', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'H-05', '2026-09-17 10:49:55', '2026-09-17 10:49:55'),
('6c84cdf5-9385-4209-b84d-36839a5271dd', '0b7a2bcf-5ac0-4590-a777-05febce54289', '2026-09-11', 3, '159f77c9-e545-46eb-bca6-49503136353c', 'e7d7cd40-510f-4aac-b2ee-0ebf305424b6', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'E-18', '2026-09-11 09:26:02', '2026-09-11 09:26:02'),
('7b3e4652-19ba-4599-815d-670fc99b0bb3', '0b7a2bcf-5ac0-4590-a777-05febce54289', '2026-09-11', 2, '12517d10-edbd-4ee9-96de-4b4d0f6f1a46', '5db47a16-e3a7-46c9-a9df-96e0d61f7bff', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'E-18', '2026-09-11 09:26:02', '2026-09-11 09:26:02'),
('7ddf528e-dab3-4b34-9b33-2a40a35bb934', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '2026-09-17', 1, '294a13c2-da21-4208-b925-23af2b0fb371', 'bac287ab-d947-4c0d-851f-d77003831682', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'H-05', '2026-09-17 11:44:12', '2026-09-17 11:44:12'),
('81fbdb90-25f7-45c0-94b8-5f405bf923e0', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '2026-08-31', 2, '736ebc24-5a3d-44b2-9012-39e71ac9b333', '5da752f1-0dd1-461a-a310-35bc05031e59', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'H-05', '2026-08-31 10:43:14', '2026-08-31 10:43:14'),
('99dc4d29-6bda-4f99-9996-3c796e92fcdd', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '2026-08-17', 1, '294a13c2-da21-4208-b925-23af2b0fb371', 'bac287ab-d947-4c0d-851f-d77003831682', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'H-05', '2026-08-17 11:30:13', '2026-08-17 11:30:13'),
('ac5af7cd-d7d9-481d-88f3-15091727bc86', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '2026-08-17', 3, 'ebc66534-457f-430e-bb3b-4a2747015e8c', '04673170-69a7-4a12-8679-7184c9e6294c', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'H-05', '2026-08-17 11:30:13', '2026-08-17 11:30:13'),
('b7ee6234-1dde-4a3d-bd41-069f858eb1d7', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '2026-08-31', 3, 'ebc66534-457f-430e-bb3b-4a2747015e8c', '04673170-69a7-4a12-8679-7184c9e6294c', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'H-05', '2026-08-31 10:43:14', '2026-08-31 10:43:14'),
('bb31b987-51f2-4f32-8157-f2f7e4e94577', '0b7a2bcf-5ac0-4590-a777-05febce54289', '2026-09-11', 4, '20b7a2c2-d14f-4d8c-94d5-34b2a89def3a', '21464371-1c1d-44c3-a81c-7ea70dcb9222', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'E-18', '2026-09-11 09:26:02', '2026-09-11 09:26:02'),
('bc4a0d1e-cfee-4e24-9a0d-8282c043d20f', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '2026-08-17', 2, '736ebc24-5a3d-44b2-9012-39e71ac9b333', '5da752f1-0dd1-461a-a310-35bc05031e59', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'H-05', '2026-08-17 11:30:13', '2026-08-17 11:30:13'),
('d7050f4c-71c4-40a7-8589-4f0608ab7382', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '2026-08-31', 1, '294a13c2-da21-4208-b925-23af2b0fb371', 'bac287ab-d947-4c0d-851f-d77003831682', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'H-05', '2026-08-31 10:43:14', '2026-08-31 10:43:14'),
('e59d4518-8bcc-48d3-8485-fc082c5540e7', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '2026-08-17', 4, 'fafb3737-e8b6-4270-b01d-912335afc118', '98e1933c-53d1-4a2d-8560-20d0222631fe', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'H-05', '2026-08-17 11:30:13', '2026-08-17 11:30:13'),
('e63fe3f4-c683-42a5-93ef-ff7cd8deb324', '544f0ae2-2ee5-403b-84cf-58ac0aa193af', '2026-09-17', 4, 'fafb3737-e8b6-4270-b01d-912335afc118', '98e1933c-53d1-4a2d-8560-20d0222631fe', 'dc5d99d0-d369-4487-a9df-27b663200f83', 'H-05', '2026-09-17 11:44:12', '2026-09-17 11:44:12');

-- --------------------------------------------------------

--
-- Table structure for table `trades`
--

CREATE TABLE `trades` (
  `id` varchar(36) NOT NULL,
  `code` varchar(50) NOT NULL,
  `label` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `trades`
--

INSERT INTO `trades` (`id`, `code`, `label`, `description`, `is_active`, `created_at`, `updated_at`) VALUES
('04748ef0-2827-4f70-915b-2c07078074fc', 'TELEPHONIST', 'Telephone Operator', '', 1, '2026-10-26 04:28:10', '2026-10-26 04:28:10'),
('26b9799b-914a-4414-8ae4-3be16e56c74e', 'ACCT_ASST', 'Account Assistant', '', 1, '2026-09-09 09:51:50', '2026-09-09 09:51:50'),
('5c162d3f-e913-4568-8372-844975e54bff', 'OPS AIR', 'Operation ', '', 1, '2026-08-11 15:25:40', '2026-08-11 15:25:40'),
('5d312046-1f95-4bbd-adbe-cda9e70c44bd', 'COMP TECH', 'Computer Technician', '', 1, '2026-08-10 09:38:42', '2026-08-10 09:38:42'),
('b260e0d3-c8f9-4857-aad2-e05b9b5a6257', 'TEST_AIR', 'Test Airframe', NULL, 1, '2026-09-14 10:38:48', '2026-09-14 10:38:48'),
('e840b87f-54f1-46d9-bcd4-8f9e4cf82eeb', 'TEST_TRADE_01', 'Test Trade - Avionics', 'Testing Trade', 1, '2026-08-13 11:42:59', '2026-08-13 11:42:59'),
('trade-admin', 'ADMINISTRATIVE', 'Administrative', NULL, 1, '2026-08-10 09:31:21', '2026-08-10 09:31:21'),
('trade-airframe', 'AIRFRAME', 'Airframe', NULL, 1, '2026-08-10 09:31:21', '2026-08-10 09:31:21'),
('trade-avionics', 'A E & I', 'Aeronuatical Electrical Instrument', 'Electrical Instrumental', 1, '2026-08-10 09:31:21', '2026-08-11 09:38:53'),
('trade-engine', ' AERO ENGINE', 'Aero Engine', '', 1, '2026-08-10 09:31:21', '2026-08-11 09:42:48'),
('trade-logistical', 'LOGISTICS', 'Log Asssitant', '', 1, '2026-08-10 09:31:21', '2026-08-11 09:43:38'),
('trade-safety', 'SAFETY EQUIPMENT', 'Safety Equipment', '', 1, '2026-08-10 09:31:21', '2026-08-11 09:43:50');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` varchar(36) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `service_number` varchar(50) DEFAULT NULL,
  `rank` varchar(50) DEFAULT NULL,
  `full_name` varchar(100) NOT NULL,
  `mobile_number` varchar(20) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `designation` varchar(100) DEFAULT NULL,
  `assigned_module` varchar(100) DEFAULT NULL,
  `hashed_password` varchar(255) NOT NULL,
  `profile_photo` varchar(255) DEFAULT NULL,
  `role_id` varchar(36) NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `is_locked` tinyint(1) DEFAULT NULL,
  `must_change_password` tinyint(1) DEFAULT NULL,
  `failed_login_attempts` int(11) DEFAULT NULL,
  `password_changed_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `service_number`, `rank`, `full_name`, `mobile_number`, `department`, `designation`, `assigned_module`, `hashed_password`, `profile_photo`, `role_id`, `is_active`, `is_locked`, `must_change_password`, `failed_login_attempts`, `password_changed_at`, `deleted_at`, `created_at`, `updated_at`) VALUES
('1b514baf-ebde-4fcc-b838-902659c5c3e3', '04253', 'saman@slaf.lk', '04253', 'FLTLT', 'Saman Kumara', '075986331', 'Commanding Section', 'OFF I/C', 'Daily Parade', '$2a$12$Bm/f.TJ1NrCfH6QANDt3euDHgoyzlOpGRIkD9YQG7gIKVOGfWURuK', NULL, 'role-co', 1, 0, 1, 0, '2026-08-10 11:06:34', NULL, '2026-08-10 11:06:34', '2026-09-15 12:28:06'),
('ac814c9f-08ef-476f-8de4-15192d2e7f71', 'test_inst_01', 'inst01@slaf.lk', 'S/12345', 'Sgt', 'Sgt A. Perera', NULL, NULL, NULL, NULL, 'dummy_password', NULL, 'role-academic', 1, 0, 0, 0, NULL, NULL, '2026-08-13 11:43:21', '2026-08-13 11:43:21'),
('c5f0985e-45f7-4086-9bb7-06019de7cea3', '51098', 'pshanilka080@gmail.com', '51098', 'LAC', 'Kithmal MPS', '0742557973', 'Academic Section', 'Instructor', 'Academic Activities', '$2b$12$tx7PjhuM88cE9rybDVgeGufWRXsszTvA3ZSzS/r83fYWB2qc8jdmK', NULL, 'role-instructor', 1, 0, 0, 0, '2026-10-26 04:45:55', NULL, '2026-10-26 04:45:55', '2026-10-26 04:45:55'),
('c96d5ee9-93ee-41cc-b9e6-f31ecba02f4e', '51837', 'sankaadikaram1996@gmail.com', '51837', 'LAC', 'sanka adikaram', '+94766932107', 'Accommodation Section', 'Clerk', 'Daily Parade', '$2b$12$IC6Jk4iBB8p7tYHuC2q8yOIMlCd9VDkgXWHybZSNU7kBIviYnVQlm', NULL, 'role-academic', 1, 0, 1, 0, '2026-09-21 05:40:48', NULL, '2026-09-21 05:40:48', '2026-09-21 05:43:34'),
('dc5d99d0-d369-4487-a9df-27b663200f83', '32853', 'fonseka@gmail.com', '32853', 'WO', 'HFAI Fonseka', '0719129215', 'Academic Section', 'Instructor', 'Academic Activities', '$2a$12$0drfccQ/ejnf2n3izPR3eudCND71i.vm3MuKO7MkJAd15.bStxFwS', NULL, 'role-instructor', 1, 0, 0, 0, '2026-08-10 11:23:21', NULL, '2026-08-10 11:23:21', '2026-09-17 10:25:23'),
('f6f853a0-a3db-481e-bb6b-95e469c45dc8', '51088', '51088@gamil.com', '51088', 'LAC', 'Dayanada', '0766880015', 'Academic Section', 'JNCO', 'Academic Activities', '$2a$12$PD4fVjzgKgoK7Kioh1sshOP1qusVd5Zy5/NRqfZj5DaKBIIuwTpg.', NULL, 'role-instructor', 1, 0, 1, 0, '2026-08-11 15:32:32', NULL, '2026-08-11 15:32:32', '2026-09-15 12:28:06'),
('user-slaf-admin', 'admin', 'admin@slaf.lk', NULL, NULL, 'SLAF Administrator', NULL, NULL, NULL, NULL, '$2b$12$mtZ8.IsD3Dt60K8x73tpgOC8sWZRzKKx0sU.O5zvzsfAzyOSNc4kG', NULL, 'role-super-admin', 1, 0, 0, 0, NULL, NULL, '2026-08-10 09:31:20', '2026-10-26 04:05:24');

-- --------------------------------------------------------

--
-- Table structure for table `user_permissions`
--

CREATE TABLE `user_permissions` (
  `user_id` varchar(36) NOT NULL,
  `permission_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_permissions`
--

INSERT INTO `user_permissions` (`user_id`, `permission_id`) VALUES
('1b514baf-ebde-4fcc-b838-902659c5c3e3', 'perm-parade-approve'),
('dc5d99d0-d369-4487-a9df-27b663200f83', 'perm-academic-read'),
('dc5d99d0-d369-4487-a9df-27b663200f83', 'perm-audit-read'),
('dc5d99d0-d369-4487-a9df-27b663200f83', 'perm-parade-read'),
('dc5d99d0-d369-4487-a9df-27b663200f83', 'perm-parade-write'),
('dc5d99d0-d369-4487-a9df-27b663200f83', 'perm-reports-read'),
('dc5d99d0-d369-4487-a9df-27b663200f83', 'perm-student-read'),
('dc5d99d0-d369-4487-a9df-27b663200f83', 'perm-student-write'),
('f6f853a0-a3db-481e-bb6b-95e469c45dc8', 'perm-academic-write'),
('f6f853a0-a3db-481e-bb6b-95e469c45dc8', 'perm-parade-write'),
('f6f853a0-a3db-481e-bb6b-95e469c45dc8', 'perm-reports-read');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `academic_attendance`
--
ALTER TABLE `academic_attendance`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `idx_unique_timetable_student` (`timetable_id`,`student_id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `idx_academic_att_status` (`status`);

--
-- Indexes for table `accommodation_allocations`
--
ALTER TABLE `accommodation_allocations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bed_id` (`bed_id`),
  ADD KEY `allocated_by` (`allocated_by`),
  ADD KEY `vacated_by` (`vacated_by`),
  ADD KEY `idx_alloc_student_status` (`student_id`,`status`);

--
-- Indexes for table `accommodation_beds`
--
ALTER TABLE `accommodation_beds`
  ADD PRIMARY KEY (`id`),
  ADD KEY `billet_id` (`billet_id`);

--
-- Indexes for table `accommodation_bed_positions`
--
ALTER TABLE `accommodation_bed_positions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_pos_bunk` (`bunk_bed_id`),
  ADD KEY `idx_pos_status` (`status`);

--
-- Indexes for table `accommodation_billets`
--
ALTER TABLE `accommodation_billets`
  ADD PRIMARY KEY (`id`),
  ADD KEY `building_id` (`building_id`);

--
-- Indexes for table `accommodation_buildings`
--
ALTER TABLE `accommodation_buildings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `accommodation_bunk_beds`
--
ALTER TABLE `accommodation_bunk_beds`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_bunk_billet` (`billet_id`);

--
-- Indexes for table `audit_logs`
--
ALTER TABLE `audit_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_audit_logs_user_id` (`user_id`),
  ADD KEY `ix_audit_logs_created_at` (`created_at`);

--
-- Indexes for table `batches`
--
ALTER TABLE `batches`
  ADD PRIMARY KEY (`id`),
  ADD KEY `trade_id` (`trade_id`),
  ADD KEY `idx_batches_status_passing_out_date` (`status`,`passing_out_date`),
  ADD KEY `idx_batches_course_status` (`course_id`,`status`),
  ADD KEY `idx_batches_classroom_status` (`classroom_id`,`status`),
  ADD KEY `idx_batches_instructor_status` (`instructor_id`,`status`);

--
-- Indexes for table `classrooms`
--
ALTER TABLE `classrooms`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `courses`
--
ALTER TABLE `courses`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD KEY `idx_courses_status_end_date` (`status`,`end_date`),
  ADD KEY `idx_courses_is_active_end_date` (`is_active`,`end_date`),
  ADD KEY `idx_courses_trade_status` (`trade_id`,`status`);

--
-- Indexes for table `course_calendar`
--
ALTER TABLE `course_calendar`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_course_calendar_course_id` (`course_id`),
  ADD KEY `idx_course_calendar_instructor_id` (`instructor_id`),
  ADD KEY `idx_course_calendar_commencement` (`commencement_date`),
  ADD KEY `idx_course_calendar_completion` (`completion_date`),
  ADD KEY `idx_course_calendar_status` (`status`);

--
-- Indexes for table `exams`
--
ALTER TABLE `exams`
  ADD PRIMARY KEY (`id`),
  ADD KEY `course_id` (`course_id`),
  ADD KEY `subject_id` (`subject_id`);

--
-- Indexes for table `exam_marks`
--
ALTER TABLE `exam_marks`
  ADD PRIMARY KEY (`id`),
  ADD KEY `exam_id` (`exam_id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `entered_by` (`entered_by`);

--
-- Indexes for table `lessons`
--
ALTER TABLE `lessons`
  ADD PRIMARY KEY (`id`),
  ADD KEY `subject_id` (`subject_id`);

--
-- Indexes for table `lesson_plans`
--
ALTER TABLE `lesson_plans`
  ADD PRIMARY KEY (`id`),
  ADD KEY `lesson_id` (`lesson_id`),
  ADD KEY `instructor_id` (`instructor_id`);

--
-- Indexes for table `lesson_plan_documents`
--
ALTER TABLE `lesson_plan_documents`
  ADD PRIMARY KEY (`id`),
  ADD KEY `lesson_id` (`lesson_id`),
  ADD KEY `ix_lesson_plan_documents_uploaded_at` (`uploaded_at`),
  ADD KEY `ix_lesson_plan_documents_uploaded_by` (`uploaded_by`),
  ADD KEY `ix_lesson_plan_documents_status` (`status`),
  ADD KEY `ix_lesson_plan_documents_course_id` (`course_id`);

--
-- Indexes for table `login_history`
--
ALTER TABLE `login_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_login_history_user_id` (`user_id`),
  ADD KEY `ix_login_history_created_at` (`created_at`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `officer_in_charge`
--
ALTER TABLE `officer_in_charge`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_oic_trade` (`trade`),
  ADD KEY `idx_oic_user` (`user_id`);

--
-- Indexes for table `parade_states`
--
ALTER TABLE `parade_states`
  ADD PRIMARY KEY (`id`),
  ADD KEY `updated_by` (`updated_by`),
  ADD KEY `ix_parade_states_date` (`date`),
  ADD KEY `idx_parade_student_date` (`student_id`,`date`),
  ADD KEY `idx_parade_submission_status` (`submission_id`,`status`);

--
-- Indexes for table `parade_status_types`
--
ALTER TABLE `parade_status_types`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `parade_submissions`
--
ALTER TABLE `parade_submissions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_ps_date` (`date`),
  ADD KEY `idx_ps_trade` (`trade`),
  ADD KEY `idx_ps_officer` (`approving_officer_id`);

--
-- Indexes for table `password_history`
--
ALTER TABLE `password_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_password_history_user_id` (`user_id`);

--
-- Indexes for table `permissions`
--
ALTER TABLE `permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `personal_occurrences`
--
ALTER TABLE `personal_occurrences`
  ADD PRIMARY KEY (`id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `updated_by` (`updated_by`),
  ADD KEY `ix_personal_occurrences_status` (`status`),
  ADD KEY `idx_trainee_occ_date` (`trainee_id`,`occurrence_date`),
  ADD KEY `ix_personal_occurrences_occurrence_date` (`occurrence_date`),
  ADD KEY `ix_personal_occurrences_trainee_id` (`trainee_id`),
  ADD KEY `ix_personal_occurrences_occurrence_type` (`occurrence_type`);

--
-- Indexes for table `ranks`
--
ALTER TABLE `ranks`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `role_permissions`
--
ALTER TABLE `role_permissions`
  ADD PRIMARY KEY (`role_id`,`permission_id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_students_service_number` (`service_number`),
  ADD UNIQUE KEY `nic` (`nic`),
  ADD KEY `idx_students_course_status` (`course_id`,`status`),
  ADD KEY `idx_students_batch_status` (`batch`,`status`),
  ADD KEY `idx_students_status_deleted` (`status`,`deleted_at`);

--
-- Indexes for table `student_status_types`
--
ALTER TABLE `student_status_types`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `subjects`
--
ALTER TABLE `subjects`
  ADD PRIMARY KEY (`id`),
  ADD KEY `course_id` (`course_id`);

--
-- Indexes for table `timetables`
--
ALTER TABLE `timetables`
  ADD PRIMARY KEY (`id`),
  ADD KEY `course_id` (`course_id`),
  ADD KEY `subject_id` (`subject_id`),
  ADD KEY `lesson_id` (`lesson_id`),
  ADD KEY `instructor_id` (`instructor_id`);

--
-- Indexes for table `trades`
--
ALTER TABLE `trades`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_users_username` (`username`),
  ADD UNIQUE KEY `ix_users_email` (`email`),
  ADD KEY `role_id` (`role_id`),
  ADD KEY `ix_users_service_number` (`service_number`),
  ADD KEY `ix_users_deleted_at` (`deleted_at`);

--
-- Indexes for table `user_permissions`
--
ALTER TABLE `user_permissions`
  ADD PRIMARY KEY (`user_id`,`permission_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `academic_attendance`
--
ALTER TABLE `academic_attendance`
  ADD CONSTRAINT `academic_attendance_ibfk_1` FOREIGN KEY (`timetable_id`) REFERENCES `timetables` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `academic_attendance_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `accommodation_allocations`
--
ALTER TABLE `accommodation_allocations`
  ADD CONSTRAINT `accommodation_allocations_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `accommodation_allocations_ibfk_2` FOREIGN KEY (`bed_id`) REFERENCES `accommodation_beds` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `accommodation_allocations_ibfk_3` FOREIGN KEY (`allocated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `accommodation_allocations_ibfk_4` FOREIGN KEY (`vacated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `accommodation_beds`
--
ALTER TABLE `accommodation_beds`
  ADD CONSTRAINT `accommodation_beds_ibfk_1` FOREIGN KEY (`billet_id`) REFERENCES `accommodation_billets` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `accommodation_billets`
--
ALTER TABLE `accommodation_billets`
  ADD CONSTRAINT `accommodation_billets_ibfk_1` FOREIGN KEY (`building_id`) REFERENCES `accommodation_buildings` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `audit_logs`
--
ALTER TABLE `audit_logs`
  ADD CONSTRAINT `audit_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `batches`
--
ALTER TABLE `batches`
  ADD CONSTRAINT `batches_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `batches_ibfk_2` FOREIGN KEY (`trade_id`) REFERENCES `trades` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `batches_ibfk_3` FOREIGN KEY (`classroom_id`) REFERENCES `classrooms` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `batches_ibfk_4` FOREIGN KEY (`instructor_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `courses`
--
ALTER TABLE `courses`
  ADD CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`trade_id`) REFERENCES `trades` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `exams`
--
ALTER TABLE `exams`
  ADD CONSTRAINT `exams_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `exams_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `exam_marks`
--
ALTER TABLE `exam_marks`
  ADD CONSTRAINT `exam_marks_ibfk_1` FOREIGN KEY (`exam_id`) REFERENCES `exams` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `exam_marks_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `exam_marks_ibfk_3` FOREIGN KEY (`entered_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `lessons`
--
ALTER TABLE `lessons`
  ADD CONSTRAINT `lessons_ibfk_1` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `lesson_plans`
--
ALTER TABLE `lesson_plans`
  ADD CONSTRAINT `lesson_plans_ibfk_1` FOREIGN KEY (`lesson_id`) REFERENCES `lessons` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `lesson_plans_ibfk_2` FOREIGN KEY (`instructor_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `lesson_plan_documents`
--
ALTER TABLE `lesson_plan_documents`
  ADD CONSTRAINT `lesson_plan_documents_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `lesson_plan_documents_ibfk_2` FOREIGN KEY (`lesson_id`) REFERENCES `lessons` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `lesson_plan_documents_ibfk_3` FOREIGN KEY (`uploaded_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `login_history`
--
ALTER TABLE `login_history`
  ADD CONSTRAINT `login_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `parade_states`
--
ALTER TABLE `parade_states`
  ADD CONSTRAINT `parade_states_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `parade_states_ibfk_2` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `parade_states_ibfk_3` FOREIGN KEY (`submission_id`) REFERENCES `parade_submissions` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `password_history`
--
ALTER TABLE `password_history`
  ADD CONSTRAINT `password_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `personal_occurrences`
--
ALTER TABLE `personal_occurrences`
  ADD CONSTRAINT `personal_occurrences_ibfk_1` FOREIGN KEY (`trainee_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `personal_occurrences_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `personal_occurrences_ibfk_3` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `students`
--
ALTER TABLE `students`
  ADD CONSTRAINT `students_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `subjects`
--
ALTER TABLE `subjects`
  ADD CONSTRAINT `subjects_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `timetables`
--
ALTER TABLE `timetables`
  ADD CONSTRAINT `timetables_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `timetables_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `timetables_ibfk_3` FOREIGN KEY (`lesson_id`) REFERENCES `lessons` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `timetables_ibfk_4` FOREIGN KEY (`instructor_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
