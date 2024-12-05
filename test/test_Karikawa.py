import sys
import os

# プロジェクトのルートディレクトリをsys.pathに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

script_dir = os.path.dirname(os.path.abspath(__file__))
transcript_path = "../../修論/狩川先生読み上げ音声/読み上げ音声文字起こしデータ.json"

from main import extraction_flight_number as extractor
import json
import re

if __name__ == "__main__":
    with open(transcript_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    pattern = r'\b([A-Z]{3})(\d+)\b'  # AAA111 のパターン
    count = 0
    RANGE = 122 #len(data) # sound fileの番号
    
    for i in range(RANGE):
        match = re.search(pattern, data[i]["instruction"])
        if match:
            callsign = match.group(0)
        else:
            callsign = "Callsign is not found"

        extracted_callsigns:list[str, int] = extractor(data[i]["text"][0])

        if any(extracted_callsign[0] == callsign for extracted_callsign in extracted_callsigns):
            count += 1
        else:
            print("False!!", i)
            print(callsign, extracted_callsigns)
            print(data[i]["instruction"])
            print(data[i]["text"])
            
    success_rate = count / (RANGE + 1)
    
    print(success_rate, '(',  count, '/',  RANGE + 1, ')' )
    