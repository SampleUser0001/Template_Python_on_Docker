#!/bin/bash

source common.sh

pushd src > /dev/null

# mypyを実行
PYTHON_FILES=$(find $PYTHON_APP_HOME/src -name "*.py" -not -name 'test*.py')
shift # 最初の引数を削除して残りの引数をmypyのオプションとして扱う
# mypyを実行（追加の引数があれば渡す）
mypy $PYTHON_FILES $@
MYPY_RESULT=$?

# mypyの戻り値をチェック
if [ $MYPY_RESULT -eq 0 ]; then
    echo "mypy チェック成功！Pythonスクリプトを実行します..."
    python app.py
else
    echo "mypy エラーが検出されました。修正してください。"
    exit $MYPY_RESULT
fi
# 起動引数を渡したい場合は下記。
# python app.py $1 $2 ...

popd > /dev/null