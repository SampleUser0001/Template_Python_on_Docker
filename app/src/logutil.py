# -*- coding: utf-8 -*-
from logging import getLogger, NOTSET
import json
import os

from functools import wraps

def apply_logger(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):  # メソッドかどうか確認
            logger_name = f"{__name__}.{cls.__name__}.{attr_name}"
            decorated = LogUtil.dynamic_logger(logger_name)(attr_value)
            setattr(cls, attr_name, decorated)
    return cls

class LogUtil:

    @classmethod
    def get_log_conf(cls, log_conf_path):
        """ ログ設定ファイルを読み込む
        """
        with open(log_conf_path, mode='r') as f:
            log_conf = json.loads(f.read())
            log_conf['handlers']['fileHandler']['filename'] = os.getenv('PYTHON_APP_HOME') + '/' + log_conf['handlers']['fileHandler']['filename']
            log_conf['handlers']['testFileHandler']['filename'] = os.getenv('PYTHON_APP_HOME') + '/' + log_conf['handlers']['testFileHandler']['filename']
            
            # テストファイルのログ設定を更新する。
            test_config = log_conf['loggers']['test']
            for name in cls.find_test_file():
                log_conf['loggers'][name] = test_config
        return log_conf

    @classmethod
    def dynamic_logger(cls, logger_name):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # インスタンスの有無を判断
                instance = args[0] if args and isinstance(args[0], cls) else None
                
                if instance:
                    original_logger = getattr(instance, 'logger', None)

                    logger = getLogger(logger_name)

                    # ロガーの設定が見つかるまで、設定ファイルを遡る
                    while logger.level == NOTSET and '.' in logger_name:
                        logger_name = '.'.join(logger_name.split('.')[:-1])
                        logger = getLogger(logger_name)

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
    def find_test_file(cls):
        """ テスト用のファイルを探す
        """
        test_files = []
        app_dir = os.path.join(os.getenv('PYTHON_APP_HOME'), *['src'])
        for root, dirs, files in os.walk(app_dir):
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    test_files.append(file.replace('.py', ''))
        return test_files

