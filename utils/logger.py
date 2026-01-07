import os
import time
from loguru import logger
from config import LogConfig


class Logger:
    logger: logger = logger
    if LogConfig.path is not None:
        if not os.path.exists(LogConfig.path):
            os.mkdir(LogConfig.path)
        logger.add("{}/log_{}.log".format(LogConfig.path, time.strftime("%Y_%m_%d")), rotation="00:00", encoding="utf-8",
                retention="300 days")

    @staticmethod
    def info(message: str):
        logger.info(message)

    @staticmethod
    def error(message: str):
        Logger.logger.error(message)

    @staticmethod
    def debug(message: str):
        Logger.logger.debug(message)

    @staticmethod
    def warning(message: str):
        Logger.logger.warning(message)

    @staticmethod
    def critical(message: str):
        Logger.logger.critical(message)

    @staticmethod
    def exception(message: str):
        Logger.logger.exception(message)

    @staticmethod
    def trace(message: str):
        Logger.logger.trace(message)

    @staticmethod
    def success(message: str):
        Logger.logger.success(message)


if __name__ == '__main__':
    Logger.info("测试消息")
    Logger.error("测试消息")
    Logger.debug("测试消息")
    Logger.warning("测试消息")
    Logger.critical("测试消息")
    Logger.exception("测试消息")
    Logger.trace("测试消息")
    Logger.success("测试消息")
