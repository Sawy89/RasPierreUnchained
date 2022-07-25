-- ----------------------------------------------------------
-- Procedures for processing energy data
-- ----------------------------------------------------------

CREATE OR REPLACE PROCEDURE update_15_minutes(
  _current_modbus_type_id INT
)  AS $$
DECLARE _adesso TIMESTAMP;  
DECLARE _current_min_ins_date TIMESTAMP;
BEGIN

    -- Save for insertdate
    _adesso := now();

    -- Extract the date to start from: the first not merged date
    SELECT min(ins_date) INTO _current_min_ins_date
    FROM modbus_data md 
    WHERE modbus_type_id = _current_modbus_type_id
    AND merged = false; 

    -- Table with starting lecture
    DROP TABLE IF EXISTS tmp_data;
    CREATE TEMP TABLE tmp_data AS 
    SELECT ins_date 
        , value
        , reale
    FROM modbus_data md 
    WHERE modbus_type_id = _current_modbus_type_id
    AND ins_date >= _current_min_ins_date;

    -- Table with ending (shifted by 15m back) lecture
    DROP TABLE IF EXISTS tmp_data_shifted;
    CREATE TEMP TABLE tmp_data_shifted AS 
    SELECT ins_date - (15 * interval '1 minute') AS ins_date
        , value
        , reale
    FROM modbus_data md 
    WHERE modbus_type_id = _current_modbus_type_id
    AND ins_date >= _current_min_ins_date;

    -- JOIN calendar with starting and ending lecture of 15 minutes slots
    DROP TABLE IF EXISTS tmp_data_15m;
    CREATE TEMP TABLE tmp_data_15m AS 
    SELECT Vtime
        , tds.value - td.value AS consumption
        , CASE WHEN (td.reale = true AND tds.reale = true) THEN true ELSE false END AS reale
    FROM calendario_15m c 
    LEFT JOIN tmp_data td
    ON c.Vtime = td.ins_date
    LEFT JOIN tmp_data_shifted tds
    ON c.Vtime = tds.ins_date
    WHERE Vtime >= _current_min_ins_date
    AND Vtime < _adesso
    AND td.value IS NOT NULL 
    AND tds.value IS NOT NULL;

    -- Insert into 15 minutes table
    INSERT INTO energy_15m (modbus_type_id, Vtime, value, reale, insertdate)
    SELECT _current_modbus_type_id AS modbus_type_id
        , Vtime
        , consumption
        , reale
        , _adesso AS insertdate
    FROM tmp_data_15m
    ON CONFLICT ON CONSTRAINT energy_15m_pkey 
    DO UPDATE
    SET 
    value = EXCLUDED.value,
    reale = EXCLUDED.reale,
    insertdate = _adesso;

    -- Set as merged in the raw table
    UPDATE modbus_data md 
    SET merged = true
    WHERE modbus_type_id = _current_modbus_type_id
    AND ins_date in (SELECT Vtime 
                    FROM tmp_data_15m);

END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE PROCEDURE update_hourly(
  _current_modbus_type_id INT
  , _start_date_in TIMESTAMP
)  AS $$
DECLARE _adesso TIMESTAMP;  
DECLARE _start_date TIMESTAMP;  
BEGIN

    -- Save for insertdate
    _adesso := now();


    -- Check input date
    IF _start_date_in IS NULL THEN
        _start_date := now() - INTERVAL '10' DAY;
    ELSE
        _start_date := _start_date_in;
    END IF;


    -- Create hourly table
    DROP TABLE IF EXISTS tmp_data;
    CREATE TEMP TABLE tmp_data as 
    SELECT min(Vtime) AS Vtime
        , date(Vtime) AS datat
        , EXTRACT(HOUR from Vtime) AS ora
        , sum(value) AS value 
        , count(*) AS n
         , CASE WHEN sum((CASE WHEN reale THEN 1 ELSE 0 end) -1) = 0 THEN true ELSE false END AS reale
    FROM energy_15m
    WHERE modbus_type_id = 1
    group by datat, ora;


    -- Insert into 15 minutes table
    INSERT INTO energy_1h (modbus_type_id, Vtime, value, reale, insertdate)
    SELECT _current_modbus_type_id AS modbus_type_id
        , Vtime
        , value
        , reale
        , _adesso AS insertdate
    FROM tmp_data
    WHERE n = 4
    ON CONFLICT ON CONSTRAINT energy_1h_pkey 
    do update 
    set 
    value = EXCLUDED.value,
    reale = EXCLUDED.reale,
    insertdate = EXCLUDED.insertdate;

END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE PROCEDURE modbus_data_updater(
)  AS $$
BEGIN

    INSERT INTO modbus_data (modbus_type_id, ins_date, value, reale, merged)
    SELECT modbus_type_id
          , ins_date
          , value
          , reale
          , false AS merged
    FROM modbus_data_temp mdt
    ON CONFLICT ON CONSTRAINT modbus_data_pkey 
    DO UPDATE SET 
    -- update values only if the new is not null and the old is not reale
      value = EXCLUDED.value
      , reale = EXCLUDED.reale
      , merged = EXCLUDED.merged 
     where modbus_data.reale = false;

    DELETE
    FROM modbus_data_temp;


END;
$$ LANGUAGE plpgsql;