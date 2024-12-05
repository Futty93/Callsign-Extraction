import requests

def highlight_aircrafts(aircraft_data, callsign_status):
    # 配列が空の場合はリクエストを行わない
    if not aircraft_data:
        print("No data to send.")
        return
    
    url = "http://localhost:8080/highlight/"  # エンドポイントを適切に置き換えてください
    
    # AircragtHighlightDtoオブジェクトのリストを作成
    highlight_dtos = []
    
    if callsign_status == "SUCCESS":
        
        if aircraft_data[0][0] == "Callsign is not Found":
            if aircraft_data[0][1]:
                callsign_status = "CALLSIGN_NOT_FOUND"
            else:
                callsign_status = "FAILURE"
        
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
        
    params = {'callsignStatus': callsign_status}

    # POSTリクエストを送信
    response = requests.post(url, json=highlight_dtos, params=params)

    # レスポンスの確認
    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print(f"Failed with status code {response.status_code}: {response.text}")

# 使用例
if __name__ == "__main__":
    aircraft_data = [['ANA123', 1], ['SKY514', 0]]
    # aircraft_data = [['Callsign is not Found', 128]]
    highlight_aircrafts(aircraft_data, "NO_VALUE") # コールサインのハイライトをリセット
    # highlight_aircrafts(aircraft_data, "SUCCESS") # コールサインのハイライトを更新