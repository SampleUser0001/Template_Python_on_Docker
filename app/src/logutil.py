# -*- coding: utf-8 -*-
from logging import getLogger, NOTSET, Logger
from typing import Any, Dict, Callable, TypeVar, Union, Type, TypeVar, Protocol, List
from typing_extensions import ParamSpec
import json
import os
import inspect
from functools import wraps


# 型変数の定義
T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")

class HasName(Protocol):
    __name__: str

def apply_logger(cls: Type[T]) -> Type[T]:
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):  # メソッドかどうか確認
            logger_name = f"{__name__}.{cls.__name__}.{attr_name}"
            decorated = LogUtil.dynamic_logger(logger_name)(attr_value)
            setattr(cls, attr_name, decorated)
    return cls


def get_current_function_name() -> str:
    """現在実行中の関数名を取得する"""
    # スタックを1つ戻って呼び出し元の関数名を取得
    frame = inspect.currentframe()
    if frame is None:
        return "<unknown>"
    caller_frame = frame.f_back
    if caller_frame is None:
        return "<unknown>"
    return caller_frame.f_code.co_name


def find_appropriate_logger(logger_name: str) -> Logger:
    """ロガーの設定が見つかるまで、設定ファイルを遡る共通関数
    
    Args:
        logger_name (str): ロガー名
        
    Returns:
        Logger: 適切なロガーインスタンス
    """
    logger = getLogger(logger_name)
    
    # ロガーの設定が見つかるまで、設定ファイルを遡る
    while logger.level == NOTSET and '.' in logger_name:
        logger_name = '.'.join(logger_name.split('.')[:-1])
        logger = getLogger(logger_name)
    
    return logger


def get_class_method_logger(cls: Union[Type[Any], Any]) -> Logger:
    """現在のクラスとメソッドのロガーを自動的に取得する
    
    Args:
        cls: クラスまたはクラスオブジェクト
        
    Returns:
        Logger: 適切なロガーインスタンス
    """
    # スタックフレームを取得して呼び出し元の情報を収集
    frame = inspect.currentframe()
    if frame is None:
        return getLogger("fallback")
    caller_frame = frame.f_back
    if caller_frame is None:
        return getLogger("fallback")
    
    method_name = caller_frame.f_code.co_name
    
    # クラス名を取得
    if isinstance(cls, type):
        # クラスメソッドの場合
        class_name = cls.__name__
    else:
        # インスタンスメソッドの場合
        class_name = cls.__class__.__name__
    
    # モジュール名を取得
    module = inspect.getmodule(caller_frame)
    module_name = "<unknown>" if module is None else module.__name__
    
    # ロガー名を構築
    logger_name = f"{module_name}.{class_name}.{method_name}"
    
    # 適切なロガーを返す
    return find_appropriate_logger(logger_name)


class LogUtil:

    @classmethod
    def get_log_conf(cls: Type["LogUtil"], log_conf_path: str) -> Dict[str, Any]:
        """ ログ設定ファイルを読み込む
        """
        with open(log_conf_path, mode='r') as f:
            log_conf: Dict[str, Any] = json.loads(f.read())
            file_handler_filename: str = log_conf['handlers']['fileHandler']['filename']
            log_conf['handlers']['fileHandler']['filename'] = os.getenv('PYTHON_APP_HOME', '..') + '/' + file_handler_filename
            
            test_file_handler_filename: str = log_conf['handlers']['testFileHandler']['filename']
            log_conf['handlers']['testFileHandler']['filename'] = os.getenv('PYTHON_APP_HOME', '..') + '/' + test_file_handler_filename
            
            # テストファイルのログ設定を更新する。
            test_config = log_conf['loggers']['test']
            for name in cls.find_test_file():
                log_conf['loggers'][name] = test_config
        return log_conf

    @classmethod
    def dynamic_logger(cls: Type["LogUtil"], logger_name: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
        def decorator(func: Callable[P, R]) -> Callable[P, R]:
            @wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                # インスタンスの有無を判断
                instance = args[0] if args and hasattr(args[0], '__class__') and not isinstance(args[0], type) else None
                
                if instance:
                    original_logger = getattr(instance, 'logger', None)

                    # 共通関数を使用して適切なロガーを取得
                    logger = find_appropriate_logger(logger_name)
                    
                    setattr(instance, 'logger', logger)
                    logger.propagate = False
                    
                    try:
                        return func(*args, **kwargs)
                    finally:
                        # 元のself.loggerを復元
                        setattr(instance, 'logger', original_logger)
                
                # インスタンスがない場合（staticmethodなど）、直接関数を呼び出す
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    @classmethod
    def find_test_file(cls: Type["LogUtil"]) -> List[str]:
        """ テスト用のファイルを探す
        """
        test_files: List[str] = []
        app_dir = os.path.join(os.getenv('PYTHON_APP_HOME', '..'), *['src'])
        for root, dirs, files in os.walk(app_dir):
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    test_files.append(file.replace('.py', ''))
        return test_files