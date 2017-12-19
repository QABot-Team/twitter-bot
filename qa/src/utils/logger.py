import inspect
import logging


def get_logger():
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    return logging.getLogger(mod.__name__)