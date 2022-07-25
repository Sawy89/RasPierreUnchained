-- SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
/* SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'; */

-- -----------------------------------------------------
-- Schema
-- -----------------------------------------------------

/* CREATE DATABASE scivolo
WITH 
   ENCODING = 'UTF8'
   OWNER = hello_django
   CONNECTION LIMIT = 100; */

-- Set the server to My timezone
SET timezone = 'Europe/Rome';

-- -----------------------------------------------------
-- Type
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS modbus_data_types (
  modbus_type_id SERIAL PRIMARY KEY,
  modbus_tcp_address VARCHAR(4) NOT NULL,
  modbus_ip INT NOT NULL,
  readable_name VARCHAR(100) NOT NULL,
  description VARCHAR(5000)
  );


INSERT INTO modbus_data_types
  (modbus_type_id, modbus_tcp_address, modbus_ip, readable_name, description)
VALUES
  (1, '1074', 1, 'Consumo dalla rete [kWh]', 'energia acquistata dalla rete'),
  (2, '1076', 1, 'Consumo dal fv/accumulo [kWh]', 'energia prodotta dal dv'),
  (3, '1078', 1, 'Consumo dalla caldaia [kWh]', 'parziale di consumo dal locale caldaia'),
  (4, '10B0', 1, 'Produzione in rete [kWh]', 'energia regalata alla rete'),
  (5, '10B2', 1, 'Produzione in fv/accumulo [kWh]', 'questo è il consumo del sistema fv/accumulo'),
  (6, '1030', 1, 'Potenza attiva istantanea dalla rete [kW]', 'questo è la potenza attiva istantanea prelevata o immessa in rete'),
  (7, '1032', 1, 'Potenza attiva istantanea dal fotovoltaico e accumulo [kW]', 'questo è la potenza attiva istantanea prelevata o immessa nel sistema fv/accumulo'),
  (8, '1034', 1, 'Potenza attiva istantanea caldaia [kW]', 'questo è la potenza attiva istantanea prelevata dal locale caldaia'),
  (11, '1074', 2, 'Consumo dalla wallbox [kWh]', 'parziale di consumo dalla wallbox'),
  (12, '1076', 2, 'Consumo dalla piscina [kWh]', 'parziale di consumo dalla piscina, dai miei'),
  (16, '1030', 2, 'Potenza attiva istantanea dalla wallbox [kW]', 'questo è la potenza attiva istantanea prelevata dalla wallbox'),
  (17, '1032', 2, 'Potenza attiva istantanea dalla piscina [kW]', 'questo è la potenza attiva istantanea prelevata dalla piscina');



-- -----------------------------------------------------
-- Value
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS modbus_data (
  modbus_type_id INT NOT NULL,
  ins_date TIMESTAMP NOT NULL,
  value NUMERIC NOT NULL,
  reale BOOLEAN NOT NULL,
  merged BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (modbus_type_id, ins_date),
    FOREIGN KEY (modbus_type_id)
    REFERENCES modbus_data_types (modbus_type_id)
    );


CREATE TABLE IF NOT EXISTS modbus_data_temp (
  modbus_type_id INT NOT NULL,
  ins_date TIMESTAMP NOT NULL,
  value NUMERIC NOT NULL,
  reale BOOLEAN NOT NULL
    );


CREATE TABLE IF NOT EXISTS calendario (
  Vtime TIMESTAMP NOT NULL,
  Vtime_pure TIMESTAMP NOT NULL,
  VTS_AEEG INT NOT NULL,
  Vclass_2 INT NOT NULL,
  Vnowork INT NOT NULL,
  V_hGME INT NOT NULL,
  V_VnW INT NOT NULL,
  V_VnG INT NOT NULL,
  PRIMARY KEY (Vtime)
  );


  CREATE TABLE IF NOT EXISTS calendario_15m (
  Vtime TIMESTAMP NOT NULL,
  Vtime_pure TIMESTAMP NOT NULL,
  VTS_AEEG INT NOT NULL,
  Vclass_2 INT NOT NULL,
  Vnowork INT NOT NULL,
  V_hGME INT NOT NULL,
  V_VnW INT NOT NULL,
  V_VnG INT NOT NULL,
  PRIMARY KEY (Vtime)
  );


  CREATE TABLE IF NOT EXISTS energy_15m (
  modbus_type_id INT NOT NULL,
  Vtime TIMESTAMP NOT NULL,
  value NUMERIC NOT NULL,
  reale BOOLEAN NOT NULL,
  insertdate TIMESTAMP NOT NULL,
  PRIMARY KEY (modbus_type_id, Vtime),
    FOREIGN KEY (modbus_type_id)
    REFERENCES modbus_data_types (modbus_type_id)
    );


    CREATE TABLE IF NOT EXISTS energy_1h (
  modbus_type_id INT NOT NULL,
  Vtime TIMESTAMP NOT NULL,
  value NUMERIC NOT NULL,
  reale BOOLEAN NOT NULL,
  insertdate TIMESTAMP NOT NULL,
  PRIMARY KEY (modbus_type_id, Vtime),
    FOREIGN KEY (modbus_type_id)
    REFERENCES modbus_data_types (modbus_type_id)
    );
