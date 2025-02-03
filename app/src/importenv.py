# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
import json
from enum import Enum

env_path = join(dirname(__file__), 'environment.json')
with open(env_path, 'r') as json_open:
    env_data = json.load(json_open)

class ImportEnvKeyEnum(Enum):
    """ .envファイルのキーを書く """
    SAMPLE = env_data['SAMPLE']
