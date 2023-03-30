import logging

# Define a decorator function to add logging to a method
def log_method(func):
    def wrapper(*args, **kwargs):
        class_name = args[0].__class__.__name__
        method_name = func.__name__
        logger = logging.getLogger(class_name)
        logger.debug(f"Calling {method_name}() with arguments {args} {kwargs}")
        result = func(*args, **kwargs)
        method_name = result.fget.__name__
        logger.debug(f"{method_name}() returned {result}")
        return result

    return wrapper

logging.basicConfig(filename='cost.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# import logging as logger
#
#
# class Logger:
#     def __init__(self, log_file, log_level=logger.INFO):
#         self.logger = logger.getLogger(__name__)
#         self.logger.setLevel(log_level)
#         handler = logger.FileHandler(log_file)
#         handler.setLevel(log_level)
#         formatter = logger.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#         handler.setFormatter(formatter)
#         self.logger.addHandler(handler)
#
#     def log(self, message, log_level=logger.INFO):
#         if log_level == logger.DEBUG:
#             self.logger.debug(message)
#         elif log_level == logger.WARNING:
#             self.logger.warning(message)
#         elif log_level == logger.ERROR:
#             self.logger.error(message)
#         elif log_level == logger.CRITICAL:
#             self.logger.critical(message)
#         else:
#             self.logger.info(message)
