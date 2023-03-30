import logging
import functools

# Define a decorator function to add logging to a method
def log_method(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        class_name = args[0].__class__.__name__
        method_name = func.__name__
        logger = logging.getLogger(class_name)
        result = func(*args, **kwargs)
        logger.info(f"{class_name}'s {method_name} is: {result:.2g} ")
        logger.info(f"{method_name} returned {result}")
        return result
    return wrapper


logging.basicConfig(filename='cost.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
