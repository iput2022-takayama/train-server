import os
import socket
import threading
from app import create_app
from app.utils import send_to_slack

# Flask アプリケーションのインスタンスを作成
app = create_app()

def get_local_ip():
    """ローカルIPアドレスを取得"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    finally:
        s.close()
    return local_ip

def notify_slack_on_start():
    """Flask サーバー起動時に Slack に通知する"""
    local_ip = get_local_ip()
    server_url = f'http://{local_ip}:5000'
    message = f"アプリケーションが起動しました: {server_url}"
    send_to_slack(message)

if __name__ == '__main__':
    # デバッグモードによるリロード時の重複通知を防ぐ
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':  # デバッグリロード時のメインスレッドのみ実行
        threading.Thread(target=notify_slack_on_start).start()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
