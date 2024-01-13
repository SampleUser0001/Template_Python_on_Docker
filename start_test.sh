#!/bin/bash

source venv/bin/activate

pushd app > /dev/null
# 引数の数に応じて変更する
# bash start.sh $1 $2 ...
bash unittest.sh

popd > /dev/null

deactivate