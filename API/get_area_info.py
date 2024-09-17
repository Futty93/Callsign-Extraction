import requests
import re

def get_callsigns_from_api():
    # APIエンドポイントにアクセス
    url = "http://localhost:8080/aircraft/location/all"  # 適切なAPIエンドポイントに置き換えてください
    response = requests.get(url)
    
    if response.status_code == 200:
        # レスポンステキストを取得
        response_text = response.text
        
        # 正規表現でコールサインを抽出
        callsigns = re.findall(r'callsign=([A-Z0-9]+)', response_text)
        
        return callsigns
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []


if __name__ == "__main__":
  # 使用例
  callsigns = get_callsigns_from_api()
  print(callsigns)