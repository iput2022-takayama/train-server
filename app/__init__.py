from flask import Flask
from .routes import main  # Blueprint をインポート

def create_app():
    app = Flask(__name__)  # アプリケーションインスタンスを作成
    app.register_blueprint(main)  # Blueprint を登録
    return app