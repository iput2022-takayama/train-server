# これはAPIから天気のデータを取得するテストファイルです
import requests

# Open-Meteo APIのエンドポイント
BASE_URL = "https://api.open-meteo.com/v1/forecast"
LATITUDE = 35.682839  # 東京の緯度
LONGITUDE = 139.759455  # 東京の経度

# 取得する時刻（24時間形式）
target_hours = ['03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00', '00:00']

# 天気コードの説明
weather_description = {
    0: "晴れ",
    1: "主に晴れ",
    2: "曇り",
    3: "小雨",
    61: "雨",
    63: "雷雨",
    71: "雪"
}

# リクエストURL
url = f"{BASE_URL}?latitude={LATITUDE}&longitude={LONGITUDE}&hourly=temperature_2m,precipitation,weathercode&timezone=Asia%2FTokyo"

def get_weather():
    """指定された時刻の天気情報を取得して表示する"""
    response = requests.get(url)

    # レスポンスが成功した場合
    if response.status_code == 200:
        data = response.json()
        
        hourly_data = data['hourly']
        times = hourly_data['time']
        temperatures = hourly_data['temperature_2m']
        precipitations = hourly_data['precipitation']
        weather_codes = hourly_data['weathercode']

        # 指定時刻ごとの天気データを表示
        for target_hour in target_hours:
            found = False  # 各時刻に対応するデータが見つかったか
            for i, time in enumerate(times):
                # 時刻部分（HH:MM）を抽出して比較
                if time.endswith(target_hour):
                    temp = temperatures[i]
                    precip = precipitations[i]
                    weather = weather_description.get(weather_codes[i], "不明")
                    
                    print(f"{time} - 温度: {temp}°C, 降水量: {precip}mm, 天気: {weather}")
                    found = True
                    break
            
            if not found:
                print(f"{target_hour} のデータは見つかりませんでした。")
    else:
        print("天気情報の取得に失敗しました。")

# 実行
if __name__ == "__main__":
    get_weather()
