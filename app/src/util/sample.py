# -*- coding: utf-8 -*-
from logging import getLogger, config, StreamHandler, DEBUG, NOTSET
import os

from logutil import LogUtil

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME')
LOG_CONFIG_FILE = ['config', 'log_config.json']

logger = getLogger(__name__)
log_conf = LogUtil.get_log_conf(os.path.join(PYTHON_APP_HOME, *LOG_CONFIG_FILE))
config.dictConfig(log_conf)
logger.setLevel(DEBUG)
logger.propagate = False

def apply_logger(cls):
    logger_name = f"{__name__}.{cls.__name__}"
    cls.logger = getLogger(logger_name)  # クラスレベルの logger を定義

    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):  # メソッドかどうか確認
            method_logger_name = f"{logger_name}.{attr_name}"
            decorated = LogUtil.dynamic_logger(method_logger_name)(attr_value)
            setattr(cls, attr_name, decorated)
    return cls


@apply_logger
class Util:
    @staticmethod
    def print():
        logger.info('Hello Util.')
        logger.debug('Hello Util.')
        return 'This is Util'
    
    @classmethod
    def print2(cls):
        cls.logger.info('Hello Util.')
        cls.logger.debug('Hello Util.')
        return 'This is Util'