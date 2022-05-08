-- SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema
-- -----------------------------------------------------

CREATE SCHEMA IF NOT EXISTS `scivolo` DEFAULT CHARACTER SET utf8;
USE `scivolo`;

-- Set the server to My timezone
SET GLOBAL time_zone = 'Europe/Rome';
SET time_zone = 'Europe/Rome';

-- -----------------------------------------------------
-- Type
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `scivolo`.`modbus_data_types` (
  `modbus_type_id` INT NOT NULL AUTO_INCREMENT,
  `modbus_tcp_address` VARCHAR(4) UNIQUE NOT NULL,
  `readable_name` VARCHAR(100) NOT NULL,
  `description` VARCHAR(5000),
  PRIMARY KEY (`modbus_type_id`)
  ) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;


INSERT INTO `scivolo`.`modbus_data_types`
  (`modbus_type_id`, `modbus_tcp_address`, `readable_name`, `description`)
VALUES
  (1, '1074', 'Consumo dalla rete [kWh]', 'energia acquistata dalla rete'),
  (2, '1076', 'Consumo dal fv/accumulo [kWh]', 'energia prodotta dal dv'),
  (3, '1078', 'Consumo dalla caldaia [kWh]', 'parziale di consumo dal locale caldaia'),
  (4, '10B0', 'Produzione in rete [kWh]', 'energia regalata alla rete'),
  (5, '10B2', 'Produzione in fv/accumulo [kWh]', 'questo è il consumo del sistema fv/accumulo'),
  (6, '1030', 'Potenza attiva istantanea dalla rete [kW]', 'questo è la potenza attiva istantanea prelevata o immessa in rete'),
  (7, '1032', 'Potenza attiva istantanea dal fotovoltaico e accumulo [kW]', 'questo è la potenza attiva istantanea prelevata o immessa nel sistema fv/accumulo'),
  (8, '1034', 'Potenza attiva istantanea  caldaia [kW]', 'questo è la potenza attiva istantanea prelevata dal locale caldaia');



-- -----------------------------------------------------
-- Value
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `scivolo`.`modbus_data` (
  `modbus_type_id` INT NOT NULL,
  `ins_date` DATETIME NOT NULL,
  `value` DOUBLE NOT NULL,
  `reale` BOOLEAN NOT NULL,
  `merged` BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (`modbus_type_id`, `ins_date`),
  CONSTRAINT `FK_modbusdata_modbustypeid`
    FOREIGN KEY (`modbus_type_id`)
    REFERENCES `scivolo`.`modbus_data_types` (`modbus_type_id`)
    ) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;


CREATE TABLE IF NOT EXISTS `scivolo`.`modbus_data_temp` (
  `modbus_type_id` INT NOT NULL,
  `ins_date` DATETIME NOT NULL,
  `value` DOUBLE NOT NULL,
  `reale` BOOLEAN NOT NULL
    ) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;


CREATE TABLE IF NOT EXISTS `scivolo`.`calendario` (
  `Vtime` DATETIME NOT NULL,
  `Vtime_pure` DATETIME NOT NULL,
  `VTS_AEEG` INT NOT NULL,
  `Vclass_2` INT NOT NULL,
  `Vnowork` INT NOT NULL,
  `V_hGME` INT NOT NULL,
  `V_VnW` INT NOT NULL,
  `V_VnG` INT NOT NULL,
  PRIMARY KEY (`Vtime`)
  ) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;


  CREATE TABLE IF NOT EXISTS `scivolo`.`calendario_15m` (
  `Vtime` DATETIME NOT NULL,
  `Vtime_pure` DATETIME NOT NULL,
  `VTS_AEEG` INT NOT NULL,
  `Vclass_2` INT NOT NULL,
  `Vnowork` INT NOT NULL,
  `V_hGME` INT NOT NULL,
  `V_VnW` INT NOT NULL,
  `V_VnG` INT NOT NULL,
  PRIMARY KEY (`Vtime`)
  ) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;



  CREATE TABLE IF NOT EXISTS `scivolo`.`energy_15m` (
  `modbus_type_id` INT NOT NULL,
  `Vtime` DATETIME NOT NULL,
  `value` DOUBLE NOT NULL,
  `reale` BOOLEAN NOT NULL,
  `insertdate` DATETIME NOT NULL,
  PRIMARY KEY (`modbus_type_id`, `Vtime`),
  CONSTRAINT `FK_energy15m_modbustypeid`
    FOREIGN KEY (`modbus_type_id`)
    REFERENCES `scivolo`.`modbus_data_types` (`modbus_type_id`)
    ) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;


    CREATE TABLE IF NOT EXISTS `scivolo`.`energy_1h` (
  `modbus_type_id` INT NOT NULL,
  `Vtime` DATETIME NOT NULL,
  `value` DOUBLE NOT NULL,
  `reale` BOOLEAN NOT NULL,
  `insertdate` DATETIME NOT NULL,
  PRIMARY KEY (`modbus_type_id`, `Vtime`),
  CONSTRAINT `FK_energy1h_modbustypeid`
    FOREIGN KEY (`modbus_type_id`)
    REFERENCES `scivolo`.`modbus_data_types` (`modbus_type_id`)
    ) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;
