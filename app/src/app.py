# -*- coding: utf-8 -*-
from logging import getLogger, config, DEBUG, NOTSET
import os

from typing import Any, Dict, Callable, TypeVar, Union, Type, TypeVar, Protocol, List
from typing_extensions import ParamSpec

# import sys
from logutil import LogUtil
from importenv import ImportEnvKeyEnum

from util.sample import Util
from controller import SampleController

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME', '..')
LOG_CONFIG_FILE = ['config', 'log_config.json']

logger = getLogger(__name__)
log_conf = LogUtil.get_log_conf(os.path.join(PYTHON_APP_HOME, *LOG_CONFIG_FILE))
config.dictConfig(log_conf)
logger.setLevel(DEBUG)
logger.propagate = False

# 型変数の定義
T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")

def apply_logger(target: Union[Type[T], Callable[..., Any]]) -> Any:
    # クラスの場合
    if isinstance(target, type):
        for attr_name, attr_value in target.__dict__.items():
            if callable(attr_value):  # メソッドかどうか確認
                logger_name = f"{__name__}.{target.__name__}.{attr_name}"
                decorated = LogUtil.dynamic_logger(logger_name)(attr_value)
                setattr(target, attr_name, decorated)
        return target
    # 関数の場合
    elif callable(target):
        # 関数名からロガー名を取得
        logger_name = f"{__name__}.{target.__name__}"
        return LogUtil.dynamic_logger(logger_name)(target)
    return target

@apply_logger
def sample_func() -> None:
    logger.info('hoge')
    logger.debug('hoge')

if __name__ == '__main__':
    # 起動引数の取得
    # args = sys.argv
    # args[0]はpythonのファイル名。
    # 実際の引数はargs[1]から。
    
    logger.info('Sample Start!!')
    logger.info('This is logger message!!')
    logger.debug('This is logger message!!')

    # environment.jsonの取得
    logger.info(f'ImportEnvKeyEnum.SAMPLE.value : {ImportEnvKeyEnum.SAMPLE.value}')

    sample_func()

    Util.print()
    Util.print2()
    
    SampleController().print_log_info_only()
    SampleController().print_log_debug()
    
    SampleController().public_method()
    logger.info('Sample Finish!!')
