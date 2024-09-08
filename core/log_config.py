import sys
from functools import wraps

from halo import Halo
from loguru import logger

# Configure loguru
logger.remove()
logger.add(sys.stdout, format="{time} - {name} - {level} - {message}", level="INFO")

# Define emojis for different log levels
EMOJIS = {
    "DEBUG": "🐛",
    "INFO": "ℹ️",
    "SUCCESS": "✅",
    "WARNING": "⚠️",
    "ERROR": "❌",
    "CRITICAL": "🔥"
}


# Custom log function to include emojis
def log(level, message):
    emoji = EMOJIS.get(level, "")
    logger.log(level, f"{emoji} {message}")


# Decorator for logging
def log_decorator(level="INFO"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log(level, f"Calling function {func.__name__}")
            result = func(*args, **kwargs)
            log(level, f"Function {func.__name__} completed")
            return result

        return wrapper

    return decorator


# Decorator for spinner
def spinner_decorator(text="Processing"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            spinner = Halo(text=text, spinner='dots')
            spinner.start()
            try:
                result = func(*args, **kwargs)
                spinner.succeed("Done")
                return result
            except Exception as e:
                spinner.fail("Failed")
                log("ERROR", f"An error occurred: {e}")
                raise e

        return wrapper

    return decorator
