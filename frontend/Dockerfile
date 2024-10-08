# ベースイメージ
FROM node:14

# 作業ディレクトリを設定
WORKDIR /app

# package.json と package-lock.json をコピー
COPY package*.json ./

# 依存関係をインストール
RUN npm install

# アプリケーションのコードをコピー
COPY . .

# 開発サーバーを開始
CMD ["npm", "run", "serve"]
