import logging
from datetime import datetime, timezone

from pythonjsonlogger.json import JsonFormatter

from app.config import settings

logger = logging.getLogger(__name__)

logHandler = logging.StreamHandler()

class CustomJsonFormatter(JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname

formatter = CustomJsonFormatter(
    "%(timestamp)s %(level)s %(message)s %(module)s  %(funcName)s"
)

logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

try:
    logger.setLevel(settings.LOG_LEVEL)
except ValueError:
    logger.setLevel(logging.INFO)  # Уровень по умолчанию
    logger.warning(f"Invalid log level: {settings.LOG_LEVEL}. Using INFO.")