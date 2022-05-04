import logging
from datetime import datetime
from fastapi import FastAPI
# from fastapi.responses import FileResponse
import os

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

@app.get('/forecast/fill_gaps', tags=[NAMESPACE])
def fill_gaps():
    '''Fill gaps forecast'''
    logger.info('Ping function called!')
    return {'status': 'active', 'message': f'pong from {NAMESPACE}', 'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}


