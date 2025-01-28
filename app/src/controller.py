# -*- coding: utf-8 -*-
from logging import getLogger, config, DEBUG, NOTSET
import os

# import sys
from logutil import LogUtil, apply_logger

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME')
LOG_CONFIG_FILE = ['config', 'log_config.json']

logger = getLogger(__name__)
log_conf = LogUtil.get_log_conf(os.path.join(PYTHON_APP_HOME, *LOG_CONFIG_FILE))
config.dictConfig(log_conf)
logger.setLevel(DEBUG)
logger.propagate = False

@apply_logger
class SampleController():
    def __init__(self) -> None:
        self.logger = getLogger(__name__)
    
    def print_log_info_only(self) -> None:
        self.logger.info("print log")
        self.logger.debug("print log")

    def print_log_debug(self) -> None:
        self.logger.info("print log")
        self.logger.debug("print log")
        
