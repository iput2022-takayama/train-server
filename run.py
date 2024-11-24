from app import create_app  # 'create_app' をインポート

# Flask アプリケーションのインスタンスを作成
app = create_app()

# アプリケーションを実行
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # `debug=True` にして開発時に便利に
