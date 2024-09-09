import asyncio
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
        async def async_wrapper(*args, **kwargs):
            log(level, f"Calling function {func.__name__}")
            result = await func(*args, **kwargs)
            log(level, f"Function {func.__name__} completed")
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            log(level, f"Calling function {func.__name__}")
            result = func(*args, **kwargs)
            log(level, f"Function {func.__name__} completed")
            return result

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


# Decorator for spinner
def spinner_decorator(text="Processing"):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            spinner = Halo(text=text, spinner='dots')
            spinner.start()
            try:
                result = await func(*args, **kwargs)
                spinner.succeed("Done")
                return result
            except Exception as e:
                spinner.fail("Failed")
                log("ERROR", f"An error occurred: {e}")
                raise e

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
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

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
