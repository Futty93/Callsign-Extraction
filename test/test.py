import sys
import os

# プロジェクトのルートディレクトリをsys.pathに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

script_dir = os.path.dirname(os.path.abspath(__file__))
transcript_path = os.path.join(script_dir, "../transcript.json")

from main import extraction_flight_number as extractor
import json
import re

if __name__ == "__main__":
    with open(transcript_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    pattern = r'\b([A-Z]{3})(\d+)\b'  # AAA111 のパターン
    count = 0
    RANGE = 159 # sound fileの番号
    
    for i in range(RANGE + 1):
        match = re.search(pattern, data[i]["text"])
        if match:
            callsign = match.group(0)
        else:
            callsign = "Callsign is not found"
            
        extracted_callsigns:list[str, int] = extractor(data[i]["transcript-result"])
        
        print(i)

        if any(extracted_callsign[0] == callsign for extracted_callsign in extracted_callsigns):
            count += 1
            print("success!")
            print(callsign, [extracted_callsign for extracted_callsign in extracted_callsigns if
                             extracted_callsign[0] == callsign])
        else:
            print("False!!")
            print(callsign, extracted_callsigns)
            print(data[i]["text"])
            print(data[i]["transcript-result"])
            
    success_rate = count / (RANGE + 1)
    
    print(success_rate, '(',  count, '/',  RANGE + 1, ')' )
    