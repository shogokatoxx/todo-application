# TODO

task management app

## Description

Task management application using Django.
lists,details,edits and 3 views.

## Features
- lists view
- detail view
- edit view

## Requirement

<<<<<<< HEAD
- Python3.6
- Django2.2.1
=======
- Python3
- Django2.2.6
- pytz2019.1
>>>>>>> develop
- sqlparse0.3.0

## Usage

Undecided

## Installation

Undecided


## Anything Else

Undecided

## Docker

### Dockerfileでやってること
* python, pipが入ってる環境にpipenvをいれる
* 作業ディレクトリとPYTHONPATHの設定
* pipenvを使って依存するパッケージのインストール

### docker-composeでやってること
* port 8000をホスト側の8000にマウント
* コンテナ起動時にstart.shを実行

### start.shでやってること
* マイグレーション
* 開発用サーバの起動
