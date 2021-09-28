# Template Python on Docker

## 使い方

1. Dockerfileのimageを変更する。
2. 必要に応じてDockerfileにpipを書く。
3. 必要に応じてdocker-compose.ymlを修正する。
4. 下記実行。
    ``` sh
    docker-compose build
    docker-compose up
    ```

### 起動引数を渡したい場合

1. docker-compose.ymlのpython serviceの名前を変更する。
2. 下記実行。
    ``` sh
    docker-compose build
    docker-compose run ${サービス名} ${起動引数}
    ```

### 依存モジュールの取得

コンテナ内で```pip freeze```を実行する。  
ファイルは```app/requirements/requirements.txt```に出力される。

``` sh
docker-compose build
docker-compose -f docker-compose_getRequirements.yml up
```

### 非Dockerコンテナ環境で実行する

作成済みのプログラムのパスについては意識している（ファイルの読み書きを行おうとしたときに、パスや権限が存在しないみたいなことは発生しない）想定。  

1. 事前に依存モジュールを取得する。
    - 取得したファイルは何らかの方法で保存しておく。
2. 実行環境でcloneする。
3. ```pip install -r app/requirements/requirements.txt```
4. ```start.sh```を必要に応じて修正する。
    - ```python```コマンドを```python3```コマンドに修正
5. ```app/config/log_config.json```を修正する。
    - 下記の```filename```を修正する。
    ``` json
      "fileHandler": {
        "class": "logging.FileHandler",
        "level": "DEBUG",
        "formatter": "simple",
        "filename": "/opt/app/log/app.log"  
      }
    ```
    - AWS CloudShellだったら…
    ``` json
        "filename": "/home/cloudshell-user/Template_Python_on_Docker/app/log/app.log"  
    ```

## 参考

- [Qiita:Docker を使う（python のイメージで色々確認してみる）](https://qiita.com/landwarrior/items/fd918da9ebae20486b81)
- [Future Tech Blog:仕事でPythonコンテナをデプロイする人向けのDockerfile (1): オールマイティ編](https://future-architect.github.io/articles/20200513/)
