import logging
from datetime import datetime
import traceback
from fastapi import FastAPI, HTTPException
# from fastapi.responses import FileResponse
import os
from sklearn.ensemble import RandomForestRegressor
from models import ForecastData

from settings import LOG_CONF, LOG_PATH


# %% Init
NAMESPACE = 'root'

logger = logging.getLogger(NAMESPACE)
logging.config.fileConfig(LOG_CONF, disable_existing_loggers=False)

app = FastAPI()


# %% Test endpoint
@app.get('/ping', tags=[NAMESPACE])
def ping():
    '''Test function server is active'''
    logger.info('Ping function called!')
    return {'status': 'active', 'message': f'pong from {NAMESPACE}', 'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}


# %% Production endpoint
# @app.get('/log', tags=[NAMESPACE])
# def ping(errorflag: bool):
#     '''Download current log file: error or normal'''
#     filename = "Error.log" if errorflag else "Log.log"
#     logger.info(f'Return log {filename} file')
#     return FileResponse(os.path.join(LOG_PATH, filename), filename=filename)

@app.post('/forecast/fill_gaps', tags=[NAMESPACE])
def fill_gaps(data: ForecastData):
    '''Fill gaps forecast'''
    logger.info('Fill gaps endpoint called!')

    try:
        model = RandomForestRegressor()
        logger.info('Train with Random Forecast Regressor')
        model.fit(data.x_train, data.y_train)
        logger.info('Predict with Random Forecast Regressor')
        prev = model.predict(data.x_test)
        logger.info('Prediction done')
    except Exception as err:
        logger.error(f"{err} - {err.args} - {type(err)}")
        logger.error('Error fill gaps endpoint')
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error in ML model processing")

    return {'status': 'done', 'data': prev.tolist()}


