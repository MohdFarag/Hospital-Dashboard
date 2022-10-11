-- Host: 127.0.0.1    Database: almazadb
-- ------------------------------------------------------
-- Server version	8.0.29

CREATE SCHEMA IF NOT EXISTS `almazadb`;
USE `almazadb`;

-- Drops
DROP TABLE IF EXISTS `admin`;
DROP TABLE IF EXISTS `equipment`;
DROP TABLE IF EXISTS `model`;
DROP TABLE IF EXISTS `location`;
DROP TABLE IF EXISTS `manufacturer`;
DROP TABLE IF EXISTS `device`;
DROP TABLE IF EXISTS `service`;

-- Creates
CREATE TABLE `admin` (
  `admin_id` int NOT NULL auto_increment,
  `username` varchar(55) DEFAULT NULL,
  `passwd` varchar(55) DEFAULT NULL,
  PRIMARY KEY (`admin_id`)
);

CREATE TABLE `equipment` (
  `equipment_id` int NOT NULL,
  `equipment_name` varchar(55) NOT NULL,
  PRIMARY KEY (`equipment_id`)
); 

CREATE TABLE `model` (
  `model_id` int NOT NULL,
  `model_name` varchar(55) NOT NULL,
  `equipment_id` int DEFAULT NULL,
  PRIMARY KEY (`model_id`),
  KEY `equipment_id` (`equipment_id`),
  CONSTRAINT `model_equipment` FOREIGN KEY (`equipment_id`) REFERENCES `equipment` (`equipment_id`) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE `manufacturer` (
  `manufacturer_id` int NOT NULL,
  `manufacturer_name` varchar(55) NOT NULL,
  PRIMARY KEY (`manufacturer_id`)
);

CREATE TABLE `location` (
  `location_id` int NOT NULL,
  `location_name` varchar(55) NOT NULL,
  PRIMARY KEY (`location_id`)
);

CREATE TABLE `device` (
  `device_sn` varchar(100) NOT NULL,
  `category` varchar(30) NOT NULL,
  `equipment_id` int DEFAULT NULL,
  `model_id` int DEFAULT NULL,
  `manufacturer_id` int DEFAULT NULL,
  `device_production_date` date,
  `device_supply_date` date,
  `location_id` int DEFAULT NULL,
  `device_country` varchar(55) NOT NULL,
  `image` varchar(2083),
  `device_contract_type` varchar(55) NOT NULL,
  `contract_start_date` date DEFAULT NULL,
  `contract_end_date` date DEFAULT NULL,
  `terms` longtext,
  `terms_file` varchar(2083),
  `inspection_list` varchar(2083),
  `inspection_checklist` longtext,
  `ppm_list` varchar(2083),
  `ppm_checklist` longtext,
  `ppm_external` tinyint(1) DEFAULT NULL,
  `calibration_list` varchar(2083),
  `calibration_checklist` longtext,
  `calibration_external` tinyint(1) DEFAULT NULL,
  `technical_status` varchar(55) NOT NULL,
  `problem` longtext NOT NULL,
  `TRC` int NOT NULL,
  `Code` varchar(150) NOT NULL,
  `qrCode` longtext NOT NULL,
  `createdAt` date NOT NULL,
  `updatedAt` date DEFAULT NULL,
  PRIMARY KEY (`device_sn`),
  KEY `equipment_id` (`equipment_id`),
  KEY `model_id` (`model_id`),
  KEY `manufacturer_id` (`manufacturer_id`),
  KEY `location_id` (`location_id`),
  FULLTEXT KEY `device_sn` (`device_sn`),
  CONSTRAINT `device_equipment` FOREIGN KEY (`equipment_id`) REFERENCES `equipment` (`equipment_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `device_model` FOREIGN KEY (`model_id`) REFERENCES `model` (`model_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `device_manufacturer` FOREIGN KEY (`manufacturer_id`) REFERENCES `manufacturer` (`manufacturer_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `device_location` FOREIGN KEY (`location_id`) REFERENCES `location` (`location_id`) ON DELETE SET NULL
);

CREATE TABLE `service` (
  `service_id` int NOT NULL AUTO_INCREMENT,
  `service_type` varchar(55) NOT NULL,
  `device_sn` varchar(55) DEFAULT NULL,
  `scheduled_date` date NOT NULL,
  `done_date` date DEFAULT NULL,
  PRIMARY KEY (`service_id`),
  KEY `device_sn` (`device_sn`),
  CONSTRAINT `service_device` FOREIGN KEY (`device_sn`) REFERENCES `device` (`device_sn`) ON DELETE CASCADE ON UPDATE CASCADE
);


-- Inserts
INSERT INTO `admin` VALUES (0,'Admin','Admin');
