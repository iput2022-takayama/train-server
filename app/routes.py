from flask import render_template, Blueprint
from app.utils import get_departure_times, get_keio_delay_info, get_weather_data  # 必要な関数をインポート

# Blueprintを使用してルーティングを定義
main = Blueprint('main', __name__)

@main.route('/')
def index():
    # 百草園駅の出発時刻を取得
    shinjuku_times, keio_hachioji_times = get_departure_times()

    # 京王線の遅延情報を取得
    keio_delay_info = get_keio_delay_info()

    # 天気データを取得
    weather_data = get_weather_data()
    
    # 結果が取得できなかった場合
    if shinjuku_times is None or keio_hachioji_times is None:
        message = "Webページの取得に失敗しました。"
        return render_template('index.html', message=message)
    
    # 取得した時刻とデータをテンプレートに渡す
    return render_template('index.html', 
        shinjuku_times=shinjuku_times, 
        keio_hachioji_times=keio_hachioji_times,
        keio_delay_info=keio_delay_info,
        weather_data=weather_data) 
