import logging
class Logger:
    def log_info(self, log_file):
        # Create a logger instance with a unique name
        self.logger = logging.getLogger('car_logger')
        self.logger.setLevel(logging.DEBUG)

        # Create a file handler that logs to the specified file
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Create a formatter for the log messages
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        self.logger.addHandler(file_handler)
        return self.logger