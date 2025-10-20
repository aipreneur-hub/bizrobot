from loguru import logger
logger.remove()
logger.add(lambda msg: print(msg, end=""))
__all__ = ["logger"]
