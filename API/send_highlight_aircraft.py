import requests

def highlight_aircrafts(aircraft_data):
    # 配列が空の場合はリクエストを行わない
    if not aircraft_data:
        print("No data to send.")
        return
    
    url = "http://localhost:8080/highlight/"  # エンドポイントを適切に置き換えてください

    # AircragtHighlightDtoオブジェクトのリストを作成
    highlight_dtos = []
    
    for data in aircraft_data:
        callsign = data[0]
        rank = data[1]

        # rankを修正
        if rank == 0:
            rank = 2
        elif rank == 1:
            rank = 1
        elif rank == 2:
            rank = 0

        highlight_dtos.append({"callsign": callsign, "rank": rank})

    # POSTリクエストを送信
    response = requests.post(url, json=highlight_dtos)

    # レスポンスの確認
    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print(f"Failed with status code {response.status_code}: {response.text}")

# 使用例
aircraft_data = [['SKY514', 0]]
highlight_aircrafts(aircraft_data)