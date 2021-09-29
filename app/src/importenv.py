# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
from dotenv import load_dotenv
from enum import Enum

class ImportEnvKeyEnum(Enum):
  """ .envファイルのキーを書く """

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ENV_DIC = {}
# ImportEnvKeyEnumの値を書く
ENV_KEYS = []

for e in ImportEnvKeyEnum:
  ENV_DIC[e.value] = os.environ.get(e.value)