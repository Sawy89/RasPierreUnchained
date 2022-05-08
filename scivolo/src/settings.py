import os

# SPECIFIC
ACTIVE_MODBUS_DATA_TYPE = [1, 2, 3, 4, 5]

# CONSTANT
LOG_CONF = os.environ.get("LOG_CONF", default="/usr/src/app/logging.conf") # need the env variable for vscode debug
LOG_PATH = os.environ.get("LOG_PATH", default="/usr/data/app/log") # need the env variable for vscode debug

# FROM ENV
DATABASE_IP = os.environ.get("DATABASE_IP", default="database:3306")
DATABASE_NAME = "scivolo"
DATABASE_USER = os.environ.get("DATABASE_USER", default="root")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", default="admin")

# # Mail
EMAIL_HOST = os.environ.get("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = os.environ.get("EMAIL_PORT", default="587")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_ADMIN = os.environ.get("EMAIL_ADMIN")

# Forecast
FORECASTENERGY_TRAIN_DAYS = 365