# -*- coding: utf-8 -*-
from logging import getLogger, NOTSET
import json
import os

from functools import wraps

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
                # インスタンスが渡された場合にのみロガーを設定
                # staticmethodの場合は、インスタンスが渡されないため、ロガーを設定しない
                if args:
                    logger = getLogger(logger_name)

                    # ロガーの設定が見つかるまで、設定ファイルを遡る
                    _logger_name = logger_name
                    while logger.level == NOTSET:
                        splited = _logger_name.split('.')
                        _logger_name = '.'.join(splited[:-1])
                        logger = getLogger(_logger_name)

                    setattr(args[0], 'logger', logger)
                    logger.propagate = False
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
