import os
from pathlib import Path

from dotenv import load_dotenv
from ocpp.v16.enums import Action

from core.fields import ConnectionStatus

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG', True))

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S %Z'

RABBITMQ_PORT = int(os.environ.get('RABBITMQ_PORT', 5672))
RABBITMQ_UI_PORT = int(os.environ.get('RABBITMQ_UI_PORT', 15672))
RABBITMQ_USER = os.environ.get('RABBITMQ_USER', 'guest')
RABBITMQ_PASS = os.environ.get('RABBITMQ_PASS', 'guest')
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')

EVENTS_EXCHANGE_NAME = os.environ.get('EVENTS_EXCHANGE_NAME', 'events')
TASKS_EXCHANGE_NAME = os.environ.get('TASKS_EXCHANGE_NAME', 'tasks_models')

MAX_MESSAGE_PRIORITY = 10
REGULAR_MESSAGE_PRIORITY = 5
LOW_MESSAGE_PRIORITY = 1

WS_SERVER_PORT = int(os.environ.get('WS_SERVER_PORT', 8001))

HTTP_SERVER_HOST = os.environ.get('HTTP_SERVER_HOST', 'http://localhost')
HTTP_SERVER_PORT = int(os.environ.get('HTTP_SERVER_PORT', 8000))

ALLOWED_SERVER_SENT_EVENTS = [
    ConnectionStatus.LOST_CONNECTION,
    Action.Heartbeat,
    Action.StatusNotification,
    Action.StartTransaction,
    Action.StopTransaction,
]

LOCK_FOLDER = '/tmp/lock'

OCPP_VERSION = os.environ.get('OCPP_VERSION', '1.6')
