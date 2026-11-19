import logging

class CSVFormatter(logging.Formatter):
    def format(self, record):
        service = getattr(record, "service", "GENERAL")
        return f'"{self.formatTime(record)}","{record.levelname}","{record.name}","{service}","{record.getMessage()}"'


def start_logger():
    logger = logging.getLogger("CofreSeguro")
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(r"data\log.csv", encoding="utf-8")
    handler.setFormatter(CSVFormatter())
    
    logger.addHandler(handler)
    return logger

logger = start_logger()