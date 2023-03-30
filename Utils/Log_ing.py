import logging as logger


class Logger:
    def __init__(self, log_file, log_level=logger.INFO):
        self.logger = logger.getLogger(__name__)
        self.logger.setLevel(log_level)
        handler = logger.FileHandler(log_file)
        handler.setLevel(log_level)
        formatter = logger.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log(self, message, log_level=logger.INFO):
        if log_level == logger.DEBUG:
            self.logger.debug(message)
        elif log_level == logger.WARNING:
            self.logger.warning(message)
        elif log_level == logger.ERROR:
            self.logger.error(message)
        elif log_level == logger.CRITICAL:
            self.logger.critical(message)
        else:
            self.logger.info(message)
