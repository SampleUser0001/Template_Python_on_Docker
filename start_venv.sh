#!/bin/bash

source venv/bin/activate

pushd app > /dev/null

ln -s ./src/$1.env ./src/.env

# 引数の数に応じて変更する
# bash start.sh $1 $2 ...
bash start.sh

unlink ./src/.env

popd > /dev/null

deactivate