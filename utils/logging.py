from loguru import logger

from core import settings

log_file_path = settings.BASE_DIR / 'logs/log.out'

logger.add(
    log_file_path,
    format='[{time}] [{level}] [{file.name}:{line}]  {message}',
    level='DEBUG' if settings.DEBUG else 'INFO',
    rotation='1 week',
    compression='zip',
)
