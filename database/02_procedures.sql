
USE `scivolo`;


-- ----------------------------------------------------------
-- Procedures for processing energy data
-- ----------------------------------------------------------
DELIMITER $$
CREATE PROCEDURE update_15_minutes(
  IN _current_modbus_type_id INT
)
BEGIN

  START TRANSACTION;

    -- Save for insertdate
    SET @adesso = now();

    -- Extract the date to start from: the first not merged date
    SELECT min(ins_date) INTO @current_min_ins_date
    FROM scivolo.modbus_data md 
    WHERE modbus_type_id = _current_modbus_type_id
    AND merged = 0;

    -- Table with starting lecture
    DROP TABLE IF EXISTS scivolo.tmp_data;
    CREATE TEMPORARY TABLE scivolo.tmp_data
    SELECT ins_date 
        , value
        , reale
    FROM scivolo.modbus_data md 
    WHERE modbus_type_id = _current_modbus_type_id
    AND ins_date >= @current_min_ins_date;

    -- Table with ending (shifted by 15m back) lecture
    DROP TABLE IF EXISTS scivolo.tmp_data_shifted;
    CREATE TEMPORARY TABLE scivolo.tmp_data_shifted
    SELECT ins_date - INTERVAL 15 MINUTE AS ins_date
        , value
        , reale
    FROM scivolo.modbus_data md 
    WHERE modbus_type_id = _current_modbus_type_id
    AND ins_date >= @current_min_ins_date;

    -- JOIN calendar with starting and ending lecture of 15 minutes slots
    DROP TABLE IF EXISTS scivolo.tmp_data_15m;
    CREATE TEMPORARY TABLE scivolo.tmp_data_15m
    SELECT Vtime
        , tds.value - td.value AS consumption
        , if(td.reale = 1 and tds.reale = 1, 1, 0) AS reale
    FROM scivolo.calendario_15m c 
    LEFT JOIN scivolo.tmp_data td
    ON c.Vtime = td.ins_date
    LEFT JOIN scivolo.tmp_data_shifted tds
    ON c.Vtime = tds.ins_date
    WHERE Vtime >= @current_min_ins_date
    AND Vtime < @adesso
    AND td.value IS NOT NULL 
    AND tds.value IS NOT NULL;

    -- Insert into 15 minutes table
    INSERT INTO scivolo.energy_15m (modbus_type_id, Vtime, value, reale, insertdate)
    SELECT _current_modbus_type_id AS modbus_type_id
        , Vtime
        , consumption
        , reale
        , @adesso AS insertdate
    FROM scivolo.tmp_data_15m
    ON DUPLICATE KEY UPDATE 
    energy_15m.value = tmp_data_15m.consumption,
    energy_15m.reale = tmp_data_15m.reale,
    energy_15m.insertdate = @adesso;

    -- Set as merged in the raw table
    UPDATE scivolo.modbus_data md 
    SET merged = 1
    WHERE modbus_type_id = _current_modbus_type_id
    AND ins_date in (SELECT Vtime 
                    FROM scivolo.tmp_data_15m);

  COMMIT;

END;
$$
DELIMITER ;



DELIMITER $$
CREATE PROCEDURE update_hourly(
  IN _current_modbus_type_id INT,
  IN _start_date DATETIME
)
BEGIN

  START TRANSACTION;

    -- Save for insertdate
    SET @adesso = now();

    -- Check input date
    IF _start_date IS NULL THEN
        SET @_start_date = now() - INTERVAL 10 DAY;
    ELSE
        SET @_start_date = _start_date;
    END IF;

    -- Create hourly table
    DROP TABLE IF EXISTS tmp_data;
    CREATE TEMPORARY TABLE tmp_data
    SELECT min(Vtime) AS Vtime
        , date(Vtime) AS datat
        , hour(Vtime) AS ora
        , sum(value) AS value 
        , count(*) AS n
        , if(sum(reale-1) = 0, 1, 0) AS reale
    FROM energy_15m
    WHERE modbus_type_id = _current_modbus_type_id
        AND Vtime > @_start_date
    GROUP BY datat, ora;

    -- Insert into 15 minutes table
    INSERT INTO scivolo.energy_1h (modbus_type_id, Vtime, value, reale, insertdate)
    SELECT _current_modbus_type_id AS modbus_type_id
        , Vtime
        , value
        , reale
        , @adesso AS insertdate
    FROM scivolo.tmp_data
    WHERE n = 4
    ON DUPLICATE KEY UPDATE 
    energy_1h.value = if(energy_1h.value = tmp_data.value AND energy_1h.reale = tmp_data.reale, energy_1h.value, tmp_data.value),
    energy_1h.reale = if(energy_1h.value = tmp_data.value AND energy_1h.reale = tmp_data.reale, energy_1h.reale, tmp_data.reale),
    energy_1h.insertdate = if(energy_1h.value = tmp_data.value AND energy_1h.reale = tmp_data.reale, energy_1h.insertdate, @adesso);

  COMMIT;

END;
$$
DELIMITER ;




DELIMITER $$
CREATE PROCEDURE modbus_data_updater()
BEGIN

  START TRANSACTION;

    INSERT INTO modbus_data (modbus_type_id, ins_date, value, reale, merged)
    SELECT modbus_type_id
          , ins_date
          , value
          , reale
          , 0 AS merged
    FROM modbus_data_temp mdt
    ON DUPLICATE KEY UPDATE
    -- update values only if the new is not null and the old is not reale
      modbus_data.value = if(mdt.value IS NULL OR modbus_data.reale = 1, modbus_data.value, mdt.value)
      , modbus_data.reale = if(mdt.value IS NULL OR modbus_data.reale = 1, modbus_data.reale, mdt.reale)
      , modbus_data.merged = if(mdt.value IS NULL OR modbus_data.reale = 1, modbus_data.merged, 0);

    DELETE
    FROM modbus_data_temp;

    COMMIT;

  END;
$$
DELIMITER ;