# これはスクレイピングから電車の時刻表を取得するテストファイルです
import requests
from bs4 import BeautifulSoup

# 百草園駅の時刻表のURL
url = "https://www.navitime.co.jp/poi?node=00007813&from=view.transfer.searchlist.poi"

# リクエストを送信
response = requests.get(url)

# レスポンスが正常か確認
if response.status_code == 200:
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
                shinjuku_times.append((departure_time, train_type, destination_name))

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
                keio_hachioji_times.append((departure_time, train_type, destination_name))

    # 結果を表示
    print("新宿方面の出発時刻:")
    for time, train_type, destination in shinjuku_times:
        print(f"時刻: {time}, 種別: {train_type}, 目的地: {destination}")

    print("\n京王八王子方面の出発時刻:")
    for time, train_type, destination in keio_hachioji_times:
        print(f"時刻: {time}, 種別: {train_type}, 目的地: {destination}")

else:
    print("Webページの取得に失敗しました。")
