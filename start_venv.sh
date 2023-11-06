#!/bin/bash

source $1/bin/activate

pushd app > /dev/null
# 引数の数に応じて変更する
# bash start.sh $2 $3 ...
bash start.sh

popd > /dev/null

deactivate