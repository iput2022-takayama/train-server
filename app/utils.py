# utils.py

import requests
from datetime import datetime
from bs4 import BeautifulSoup

# Open-Meteo APIのエンドポイント
BASE_URL = "https://api.open-meteo.com/v1/forecast"
LATITUDE = 35.682839  # 東京の緯度
LONGITUDE = 139.759455  # 東京の経度

last_status = "京王線は通常運転です"

def send_to_slack(message):
    """Slackにメッセージを送信する関数"""
    # SlackのWebhook URLを設定（実際のURLに置き換えてください）
    webhook_url = "https://hooks.slack.com/services/XXXXXXXXX/XXXXXXXXX/XXXXXXXXX"
    
    # Slackメッセージのペイロードを作成
    payload = {
        "text": message  # 送信するメッセージ
    }
    
    # POSTリクエストでメッセージを送信
    response = requests.post(webhook_url, json=payload)
    
    if response.status_code != 200:
        print(f"Slackへのメッセージ送信に失敗しました: {response.status_code}")
    else:
        print("Slackへのメッセージ送信に成功しました")


def get_keio_delay_info():
    """京王線の遅延情報を取得し、遅延詳細を表示"""
    global last_status  # グローバル変数を使用する宣言
    url = "https://transit.yahoo.co.jp/diainfo/102/0"  # 京王線遅延情報のURL

    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTPエラーが発生した場合例外を送出
    except requests.RequestException as e:
        print(f"遅延情報の取得に失敗しました: {e}")
        return "遅延情報の取得に失敗しました"

    soup = BeautifulSoup(response.text, 'html.parser')
    delay_info = soup.find('dd', class_='trouble')

    if delay_info:
        # 遅延が発生している場合
        delay_details = delay_info.find('p')
        if delay_details:
            delay_text = delay_details.get_text(strip=True)  # 遅延詳細テキスト（サイト表示用）
            slack_message = (
                f"京王線は遅延しています。詳細: {delay_text}\n"
                f"遅延証明書: https://www.keio.co.jp/train/delay/"
            )  # Slack通知用
            if slack_message != last_status:  # 前回のSlackメッセージと異なる場合にのみ送信
                send_to_slack(slack_message)
                last_status = slack_message  # 最新状態をSlack通知用に保存
            return f"京王線は遅延しています。詳細: {delay_text}"  # サイト表示用メッセージを返す
        else:
            slack_message = (
                "京王線は遅延していますが、詳細は確認できませんでした。\n"
                f"遅延証明書: https://www.keio.co.jp/train/delay/"
            )  # Slack通知用
            if slack_message != last_status:  # 前回のSlackメッセージと異なる場合にのみ送信
                send_to_slack(slack_message)
                last_status = slack_message  # 最新状態をSlack通知用に保存
            return "京王線は遅延していますが、詳細は確認できませんでした。"  # サイト表示用メッセージを返す
    else:
        # 遅延が解消され、現在通常運転の場合
        if last_status != "京王線は通常運転です":
            resolved_message = "京王線は通常運転に戻りました。問題は解決しました。"
            # 遅延情報から通常運転への変更時にのみ送信
            send_to_slack(resolved_message)

        # 状態を通常運転に更新
        last_status = "京王線は通常運転です"
        return "京王線は通常運転です"




def get_departure_times():
    """百草園駅の新宿方面と京王八王子方面の出発時刻を取得"""
    # 百草園駅の時刻表のURL
    url = "https://www.navitime.co.jp/poi?node=00007813&from=view.transfer.searchlist.poi"
    
    # リクエストを送信
    response = requests.get(url)
    
    if response.status_code != 200:
        return None, None  # エラー時にはNoneを返す
    
    # BeautifulSoupでHTMLを解析
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 新宿方面の出発時刻を取得
    shinjuku_times = []
    shinjuku_section = soup.find('span', class_='name', string='新宿方面')  # 新宿方面を探す
    if shinjuku_section:
        # 新宿方面の出発時刻リストを取得
        time_list = shinjuku_section.find_parent('dd').find_all('li', class_='time-list__time')
        destination_list = shinjuku_section.find_parent('dd').find_all('li', class_='destination-area')
        
        # 時刻と目的地を取得
        for time, destination in zip(time_list[:3], destination_list[:3]):  # 最初の3つの時刻と目的地
            departure_time = time.get_text().strip()
            destination_info = destination.find('div', class_='destination')
            if destination_info:
                train_type = destination_info.find('span').text.strip()  # 「各停」など
                # 目的地名を格納している部分を変更
                destination_name = destination_info.get_text().strip().replace(train_type, "").strip()
                shinjuku_times.append({
                    'time': departure_time,
                    'train_type': train_type,
                    'destination': destination_name
                })

    # 京王八王子方面の出発時刻を取得
    keio_hachioji_times = []
    keio_hachioji_section = soup.find('span', class_='name', string='京王八王子方面')  # 京王八王子方面を探す
    if keio_hachioji_section:
        # 京王八王子方面の出発時刻リストを取得
        time_list = keio_hachioji_section.find_parent('dd').find_all('li', class_='time-list__time')
        destination_list = keio_hachioji_section.find_parent('dd').find_all('li', class_='destination-area')
        
        # 時刻と目的地を取得
        for time, destination in zip(time_list[-3:], destination_list[-3:]):  # 最後の3つの時刻と目的地
            departure_time = time.get_text().strip()
            destination_info = destination.find('div', class_='destination')
            if destination_info:
                train_type = destination_info.find('span').text.strip()  # 「各停」など
                # 目的地名を格納している部分を変更
                destination_name = destination_info.get_text().strip().replace(train_type, "").strip()
                keio_hachioji_times.append({
                    'time': departure_time,
                    'train_type': train_type,
                    'destination': destination_name
                })

    return shinjuku_times, keio_hachioji_times

def get_weather_data():
    target_hours = ['03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00', '00:00']

    # 天気コードの説明（関数内に移動）
    weather_description = {
        0: "晴れ",
        1: "主に晴れ",
        2: "曇り",
        3: "小雨",
        61: "雨",
        63: "雷雨",
        71: "雪"
    }

    url = f"{BASE_URL}?latitude={LATITUDE}&longitude={LONGITUDE}&hourly=temperature_2m,precipitation,weathercode&timezone=Asia%2FTokyo"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        hourly_data = data['hourly']

        # 時間とデータを整理
        times = hourly_data['time']
        temperatures = hourly_data['temperature_2m']
        precipitations = hourly_data['precipitation']
        weather_codes = hourly_data['weathercode']

        # 今日の日付を取得
        today_date = datetime.now().strftime('%Y-%m-%d')

        # 今日のデータのみを抽出
        weather_data = [
            {
                "time": time.split('T')[1],  # 時刻のみ
                "temperature": temp,
                "precipitation": precip,
                "weather": weather_description.get(code, "不明")
            }
            for time, temp, precip, code in zip(times, temperatures, precipitations, weather_codes)
            if time.startswith(today_date) and time.split('T')[1] in target_hours
        ]

        return weather_data
    else:
        return []