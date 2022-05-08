'''
Endpoint for getting data on load, production in the future, and so on
'''

from distutils.command.install_data import install_data
import logging
import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
import traceback

from settings import LOG_CONF, EMAIL_ADMIN, ACTIVE_MODBUS_DATA_TYPE
from models_energy import DbModbusData, DbModbusDataTypes, ForecastDates, ModbusData
from forecast_energy import fill_gaps
from database import get_db
from utils import send_mail

# %% Init
NAMESPACE = "energy"

logger = logging.getLogger(NAMESPACE)
logging.config.fileConfig(LOG_CONF, disable_existing_loggers=False)

router = APIRouter(prefix="/energy", tags=["energy"])


# %% Test endpoint

@router.get('/ping', tags=[NAMESPACE])
def ping():
    '''Test function server is active'''
    logger.info('Ping function called!')
    return {'status': 'active', 'message': f'pong from {NAMESPACE}', 'current_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    

# %% Endpoints
@router.post('/save_modbus_data', tags=[NAMESPACE])
def save_modbus_data(modbus_data: ModbusData, db: Session = Depends(get_db)):
    '''
    Get the incremental energy from modbus in input and save it on DB
    and save it on database
    '''
    logger.info(f'Save incremental energy from modbus: {modbus_data}')
    adesso = datetime.datetime.now()

    # Check presence
    d = db.query(DbModbusData).filter(DbModbusData.modbus_type_id == modbus_data.modbus_type_id) \
                .filter(DbModbusData.ins_date == modbus_data.ins_date).first()
    if not d:
        logger.info('Data already on database')
        return {'on_db': True, 'uploaded': False}

    # Save on DB
    try:
        data = DbModbusData(**modbus_data.dict())
        db.add(data)
        db.commit()
    except Exception as err:
        logger.error(f"{err} - {err.args} - {type(err)}")
        logger.error('Error incremental energies save')
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="upload in DB failed")

    logger.info('incremental energies saved - finish')
    return {'on_db': True, 'uploaded': True}



@router.post('/fill_gaps/{modbus_type_id}', tags=[NAMESPACE])
def fill_gaps_endpoint(modbus_type_id: int, dates: ForecastDates, db: Session = Depends(get_db)):
    '''Fill gaps'''
    logger.info('Fill gaps endpoint called')
    adesso = datetime.datetime.now()

    dict_mail = {'modbus_type_id': modbus_type_id}

    try:
        if dates.start_date is not None and dates.stop_date is not None:
            logger.info(f'Call function for filling gaps for {modbus_type_id} from {dates.start_date} to {dates.stop_date}')
            dict_mail.update({'Start date': dates.start_date, 'Stop date': dates.stop_date})
            gaps_n, gaps_start, gaps_stop = fill_gaps(logger, modbus_type_id, start_forecast=dates.start_date, 
                                                    stop_forecast=dates.stop_date, db=db)
        else:
            logger.info(f'Call function for filling gaps for {modbus_type_id} with no dates')
            gaps_n, gaps_start, gaps_stop = fill_gaps(logger, modbus_type_id, db=db)
        dict_mail.update({'Gaps number': gaps_n, 'Gaps start': gaps_start, 'Gaps stop': gaps_stop})
    except Exception as err:
        logger.error(f"{err} - {err.args} - {type(err)}")
        logger.error(f'Error call function for filling gaps for {modbus_type_id}')
        traceback.print_exc()
    
    if 'Gaps number' in dict_mail.keys() and dict_mail['Gaps number'] > 0:
        try:
            logger.info(f'Launch procedure update_15_minutes and update_hourly for {modbus_type_id}')
            # Update 15 minutes and hourly
            db.execute(f"CALL scivolo.update_15_minutes({modbus_type_id})")
            dict_mail.update({'update 15 minutes': 1})
            
            db.execute(f"CALL scivolo.update_hourly({modbus_type_id}, '{dates.start_date}')")
            dict_mail.update({'update 1 hour': 1})
        except Exception as err:
            logger.error(f"{err} - {err.args} - {type(err)}")
            logger.error(f'Error launch procedures for {modbus_type_id}')
            traceback.print_exc()
    
    db.close()
        
    return dict_mail


# %% Scheduled jobs
scheduler_load = BackgroundScheduler()


@scheduler_load.scheduled_job('cron', id='update_energy_hourly', hour='*', minute='5') # pay attention: it's in UTC
def update_energy_hourly():
    '''
    Calculate the energy from raw data
    '''
    logger.info('Launch procedure for calculating energy')
    db = next(get_db())
    adesso = datetime.datetime.now()

    for modbus_type_id in ACTIVE_MODBUS_DATA_TYPE:
        try:
            logger.info(f'Launch procedure update_15_minutes and update_hourly for {modbus_type_id}')
            # Update 15 minutes and hourly
            db.execute(f"CALL scivolo.update_15_minutes({modbus_type_id})")
            db.execute(f"CALL scivolo.update_hourly({modbus_type_id}, NULL)")
        except Exception as err:
            logger.error(f"{err} - {err.args} - {type(err)}")
            logger.error(f'Error launch procedures for {modbus_type_id}')
            traceback.print_exc()
    
    db.close()

    logger.info('Procedure for update energy - finish')


@scheduler_load.scheduled_job('cron', id='check_energy_daily', hour='2, 15', minute='20') # pay attention: it's in UTC
def check_energy_daily():
    '''
    Check the data are present, and fill gaps
    '''
    if datetime.datetime.now().hour < 14:
        date_check = datetime.date.today()+datetime.timedelta(days=-1)
        hour_to_have = 96
    else:
        date_check = datetime.date.today()
        hour_to_have = 96/2
    logger.info(f'Check modbus data for {date_check}')
    db = next(get_db())

    mail_flag = False
    dict_result = {}
    for modbus_type_id in ACTIVE_MODBUS_DATA_TYPE:
        modbus_tcp_type = db.query(DbModbusDataTypes).filter(DbModbusDataTypes.modbus_type_id == modbus_type_id).first()
        statement = f"SELECT count(*) AS n FROM scivolo.modbus_data WHERE modbus_type_id = {modbus_type_id} AND date(ins_date) = '{date_check}' AND reale = 1"
        n_data = db.execute(statement).fetchone()[0]
        dict_result[modbus_tcp_type.readable_name] = n_data
        if n_data < hour_to_have:
            mail_flag = True
            logger.warning(f'There are only {n_data}/{hour_to_have} data for {modbus_type_id} on {date_check}')
    if mail_flag:
        logger.info(f'Send mail after check data for {date_check}')
        oggetto = "SmartScivolo: alcune ore mancanti"
        testo = f"Ci sono delle ore mancanti per {date_check}.\n\nOre presenti:\n"
        for modbus_type in dict_result.keys():
            testo += f"- {modbus_type} = {dict_result[modbus_type]}/{hour_to_have}\n"
        send_mail([EMAIL_ADMIN], oggetto, testo)

    db.close()


# @scheduler_load.scheduled_job('cron', id='fill_gaps', hour='18', minute='18') # pay attention: it's in UTC
def fill_all_gaps():
    '''
    Fill all gaps in the energy modbus table with estimated data
    '''

    logger.info('Fill gaps in the last days')
    adesso = datetime.datetime.now()
    dict_names = ['modbus_type_id', 'Gaps number', 'Gaps start', 'Gaps stop', 'update 15 minutes', 'update 1 hour']
    list_mail = []

    db = next(get_db())

    for modbus_type_id in ACTIVE_MODBUS_DATA_TYPE:
        dict_mail = {'modbus_type_id': modbus_type_id}

        try:
            logger.info(f'Call function for filling gaps for {modbus_type_id}')
            gaps_n, gaps_start, gaps_stop = fill_gaps(logger, modbus_type_id, db=db)
            dict_mail.update({'Gaps number': gaps_n, 'Gaps start': gaps_start, 'Gaps stop': gaps_stop})
        except Exception as err:
            logger.error(f"{err} - {err.args} - {type(err)}")
            logger.error(f'Error call function for filling gaps for {modbus_type_id}')
            traceback.print_exc()
        
        try:
            logger.info(f'Launch procedure update_15_minutes and update_hourly for {modbus_type_id}')
            # Update 15 minutes and hourly
            db.execute(f"CALL scivolo.update_15_minutes({modbus_type_id})")
            dict_mail.update({'update 15 minutes': True})
            
            db.execute(f"CALL scivolo.update_hourly({modbus_type_id}, NULL)")
            dict_mail.update({'update 1 hour': True})
        except Exception as err:
            logger.error(f"{err} - {err.args} - {type(err)}")
            logger.error(f'Error launch procedures for {modbus_type_id}')
            traceback.print_exc()
        
        list_mail.append(dict_mail)
    
    db.close()
    logger.info('Fill gaps in the last days - finish')

    # Send mail
    str_list_mail = '<tr><th>'+'</th><th>'.join(dict_names)+'</th></tr>'
    for dict_mail in list_mail:
        dict_list = []
        for i in dict_names:
            if i in dict_mail.keys():
                dict_list.append(str(dict_mail[i]))
            else:
                dict_list.append('')
        str_list_mail += '<tr><td>'+'</td><td>'.join(dict_list)+'</td></tr>'
    testo = f'<table border=1>{str_list_mail}<table>'
    send_mail([EMAIL_ADMIN], f'Fill gaps on Smartscivolo at {adesso}', testo, mailType='HTML')
    logger.info('Fill gaps in the last days - mail sent')


# ---------------
scheduler_load.start()        
