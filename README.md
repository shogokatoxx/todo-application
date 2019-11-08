# TaskChanger

タスク管理アプリ

## 概要

Djangoで開発しました。途中までですが、tsuchinagaさんというかたと
共同開発という形でやってました。
タイトル、本文、状態、作成時間で1タスクとなります。


## 機能
- 一覧ビュー
- 詳細ビュー
- 編集ビュー
- 追加ビュー
- 状態変化(ボタン)
- 削除機能
- モーダルウインドウ

## 開発環境

<<<<<<< HEAD
- Python3.6
- Django2.2.1
=======
- Python3
- Django2.2.6
- pytz2019.1
>>>>>>> develop
- sqlparse0.3.0

## 使用方法
- Python、git環境を用意
- 「https://github.com/shogokatoxx/todo-application.git」をクローン
- pipというパッケージ管理ライブラリで「pipenv」というパッケージ管理ライブラリをインストール
- django-todo(プロジェクトファイル)でターミナル「$pipenv sync」を実行
- 「$pipenv run start」で「https://192.168.33.10:8080」にTaskChangerが展開されます

※Dockerを使っても環境の準備が可能です(詳細は下に記述)

## Version
- Version 1.0 ：現バージョン
- Version 1.5 ：予定中(タスクの上にリレーション追加追加、フォーム欄の改善)

### Docker

## Dockerfileでやってること
* python, pipが入ってる環境にpipenvをいれる
* 作業ディレクトリとPYTHONPATHの設定
* pipenvを使って依存するパッケージのインストール

## docker-composeでやってること
* port 8000をホスト側の8000にマウント
* コンテナ起動時にstart.shを実行

## start.shでやってること
* マイグレーション
* 開発用サーバの起動
