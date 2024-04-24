from main import extraction_flight_number as main
import json
import re

from whispercpp import Whisper

w = Whisper('small')

if __name__ == "__main__":
    with open("./transcript.json", 'r', encoding='utf-8') as f:
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
            
        result = w.transcribe(f"../音源ファイル/soundFiles/{data[i]['sound-file']}")
        
        text = w.extract_text(result)
            
        extracted_callsign:list[str, int] = main(text[0])
        
        print(i)

        if extracted_callsign[0] == callsign:
            count += 1
            print("success!")
            print(callsign, extracted_callsign[0], extracted_callsign[1])
        else:
            print("False!!")
            print(callsign, extracted_callsign)
            print(data[i]["text"])
            print(data[i]["transcript-result"])
            
    success_rate = count / (RANGE + 1)
    
    print(success_rate, '(',  count, '/',  RANGE + 1, ')' )
    