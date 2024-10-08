# 計算アプリ (Vue.js + Flask)

このプロジェクトは、Vue.jsを使用したフロントエンドとFlaskを使用したバックエンドからなるシンプルな計算アプリです。Dockerを使用して、フロントエンドとバックエンドをコンテナ化し、簡単に起動できるようにしています。

## 機能

- 掛け算と割り算の練習モードを提供
- 入力された数値をバックエンド（Flask）に送信し、サーバー側で計算結果を返す
- Vue.jsを使用したシンプルでインタラクティブなフロントエンド

## 技術スタック

- フロントエンド: [Vue.js](https://vuejs.org/)
- バックエンド: [Flask](https://flask.palletsprojects.com/)
- コンテナ化: [Docker](https://www.docker.com/)
- 開発環境の管理: [docker-compose](https://docs.docker.com/compose/)

## 必要条件

- [Docker](https://www.docker.com/) と [Docker Compose](https://docs.docker.com/compose/) がインストールされていること

## セットアップ方法

1. このリポジトリをクローンします。

   ```bash
   git clone https://github.com/your-repository/calculation-app.git
   cd calculation-app
   ```

2. docker-compose を使用してアプリケーションをビルドし、起動します。
    ```sudo docker-compose up --build```

3. 以下のURLでアプリケーションにアクセスします:
    フロントエンド (Vue.js): http://localhost:8080
    バックエンド (Flask): http://localhost:5000

## 使用方法
1. フロントエンド画面が表示されたら、2つの数値を入力し、「計算」ボタンをクリックします。
2. 計算結果が画面に表示されます。

