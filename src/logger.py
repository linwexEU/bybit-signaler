from functools import wraps
import logging
from typing import Callable, TypeVar, Any

R = TypeVar("R")


def log(func: Callable[..., R]) -> Callable[..., R]: 
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> R: 
        try:
            logging.info(f"Do: {func.__name__}, Args: {args}, Kwargs: {kwargs}")
            return func(*args, **kwargs) 
        except Exception as ex: 
            logging.error(f"Args: {args}, Kwargs: {kwargs}, Error: {str(ex)}")
            raise
    return wrapper


def configure_logging(level: int = logging.INFO) -> None: 
    logging.basicConfig(
        level=level, 
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
        handlers=[
            logging.FileHandler("../app.log"),
            logging.StreamHandler()
        ]
    )
