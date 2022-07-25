import datetime
from sklearn.ensemble import RandomForestRegressor

from database import get_db
from models_energy import DbModbusDataTmp
from settings import FORECASTENERGY_TRAIN_DAYS


# %% Forecast energy missing data
def fill_gaps(logger, modbus_type_id,
            start_forecast=datetime.date.today()+datetime.timedelta(days=-10),
            stop_forecast=datetime.date.today(),
            db=None):
    '''
    Fill the gaps of data (empty ones, or already filled ones)
    For test:
    modbus_type_id = 1
    start_forecast = datetime.date(2022,1,10)
    stop_forecast = datetime.date(2022,1,12)
    '''
    # input
    start_all = start_forecast + datetime.timedelta(days=-FORECASTENERGY_TRAIN_DAYS)  # for training
    stop_all = stop_forecast
    start_forecast_dt = datetime.datetime(start_forecast.year, start_forecast.month, start_forecast.day)
    stop_forecast_dt = datetime.datetime(stop_forecast.year, stop_forecast.month, stop_forecast.day)
    idx_to_upload = []
    logger.info(f'Fill data gaps for n {modbus_type_id} from {start_forecast} to {stop_forecast}')
    
    # Get all data
    logger.info(f'FillGaps: download data data for n {modbus_type_id}')
    if db == None:
        db_present = False
        db = next(get_db())
    else:
        db_present = True
    statement = f"""SELECT c15.Vtime 
                        , EXTRACT(month FROM c15.Vtime) AS mese
                        , EXTRACT(day FROM c15.Vtime) AS giorno
                        , VTS_AEEG
                        , Vclass_2
                        , Vnowork
                        , V_hGME
                        , V_VnW
                        , V_VnG
                        , case when e15.reale = true then e15.value else null end AS value
                        , e15.reale AS reale
                        , case when md.reale = true then md.value else NULL end AS md_value
                        , md.reale AS md_reale
                    FROM calendario_15m c15
                    LEFT JOIN energy_15m e15 
                        ON c15.Vtime = e15.Vtime
                        AND e15.modbus_type_id = 1
                    LEFT JOIN modbus_data md
                        ON c15.Vtime = md.ins_date
                        AND e15.modbus_type_id = md.modbus_type_id
                    WHERE c15.Vtime >= '{start_all.strftime('%Y/%m/%d')}'
                        AND c15.Vtime < '{stop_all.strftime('%Y/%m/%d')}' 
                """
    dati_db = db.execute(statement)
    dati = [dict(val) for val in dati_db]

    # train & test
    train_idx, x_train, y_train = [], [], []
    test_idx, x_test = [], []
    col_train = ['mese','giorno','VTS_AEEG','Vclass_2','Vnowork','V_hGME','V_VnW','V_VnG']
    for idx, d in enumerate(dati):
        tmp = [d[k] for k in col_train]
        if d['value'] == None or d['reale'] == 0:
            if d['Vtime'] >= start_forecast_dt and d['Vtime'] < stop_forecast_dt and len(train_idx)>0:
                # TEST data
                test_idx.append(idx)
                x_test.append(tmp)
        else:
            # TRAIN data
            train_idx.append(idx)
            x_train.append(tmp)
            y_train.append(d['value'])

    if len(test_idx) > 0:
        logger.info(f'FillGaps: Forecast and calculation for n {modbus_type_id} of {len(test_idx)} gaps')

        model = RandomForestRegressor()
        model.fit(x_train, y_train)
        prev = model.predict(x_test)
        for n_idx, t_idx in enumerate(test_idx):
            prev_i = prev[n_idx] if prev[n_idx]>= 0 else 0
            dati[t_idx]['value'] = prev_i
            dati[t_idx]['reale'] = 0
            dati[t_idx]['value_normalize'] = prev_i

        # Move to Raw data
        logger.info('Calculation for obtaining modbus raw data')
        start_idx = test_idx[0] # index of the 1st forecast
        end_idx = min(test_idx[-1]+1, len(dati)) + 1 #the last in range is not used
        idx_list_tmp, value_list_tmp = [], []
        for cur_idx in range(start_idx, end_idx):
            if (dati[cur_idx]['reale'] == 1 and dati[cur_idx-1]['reale'] == 0):
                # If the reale=0 string finished
                if start_idx != cur_idx:
                    logger.debug(dati[idx_list_tmp[0]])
                    real_energy = dati[idx_list_tmp[-1]+1]['md_value'] - dati[idx_list_tmp[0]]['md_value']

                    for cur_idx_2 in idx_list_tmp:
                        # calculate new consumption
                        value_normalize = dati[cur_idx_2]['value'] * real_energy / sum(value_list_tmp) if sum(value_list_tmp)!=0 else 0
                        dati[cur_idx_2]['value_normalize'] = round(value_normalize, 2)
                        # calculate new readings (modbus) as estimated
                        if dati[cur_idx_2]['md_reale'] == 0 or dati[cur_idx_2]['md_value'] == None:
                            logger.debug(f"FillGaps: gap for n {modbus_type_id} on {dati[cur_idx_2]['Vtime']}")
                            dati[cur_idx_2]['md_value'] = round(dati[cur_idx_2-1]['md_value'] + dati[cur_idx_2]['value_normalize'],2)
                            dati[cur_idx_2]['md_reale'] = 0
                            idx_to_upload.append(cur_idx_2)

                # start of a new hole
                idx_list_tmp, value_list_tmp = [], []
            if dati[cur_idx]['reale'] == 0:
                idx_list_tmp.append(cur_idx)
                value_list_tmp.append(dati[cur_idx]['value'])

        # Upload to DB
        logger.info(f'FillGaps: Upload on DB for n {modbus_type_id} of {len(idx_to_upload)} gaps')
        for idx in idx_to_upload:

            data = DbModbusDataTmp(modbus_type_id=modbus_type_id, ins_date=dati[idx]['Vtime'], 
                            reale=False, value=dati[idx]['md_value'])
            db.add(data)
            db.commit()
            db.execute('CALL modbus_data_updater()')
            db.commit()
    else:
        logger.info(f'FillGaps: NO forecast for n {modbus_type_id}: there are {len(test_idx)} gaps')

    # Close DB
    if not db_present:
        db.close()
    
    if len(idx_to_upload) > 0:
        return len(idx_to_upload), dati[idx_to_upload[0]]['Vtime'], dati[idx_to_upload[-1]]['Vtime']
    else:
        return len(idx_to_upload), None, None
