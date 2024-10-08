# ベースイメージ
FROM python:3.8-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なPythonモジュールをインストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# Flaskアプリケーションを実行
CMD ["python", "app.py"]