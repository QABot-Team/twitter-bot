import inspect
import logging


def get_logger():
    frm = inspect.stack()[2]
    mod = inspect.getmodule(frm[0])
    return logging.getLogger(mod.__name__)


class Logger:

    @staticmethod
    def config(loglevel):
        numeric_level = getattr(logging, loglevel.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % loglevel)
        logging.basicConfig(level=numeric_level)

    @staticmethod
    def debug(message):
        get_logger().debug(message)

    @staticmethod
    def info(message):
        get_logger().info(message)

    @staticmethod
    def warning(message):
        get_logger().warning(message)

    @staticmethod
    def error(message):
        get_logger().error(message)

    @staticmethod
    def critical(message):
        get_logger().critical(message)
