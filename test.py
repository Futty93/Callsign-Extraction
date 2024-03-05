from extraction_flight_number import extraction_flight_number as main
import json
import re

if __name__ == "__main__":
    with open("./fixed_output.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    pattern = r'\b([A-Z]{3})(\d+)\b'  # AAA111 のパターン
    count = 0
    RANGE = 60
    
    for i in range(RANGE):
        match = re.search(pattern, data[i]["text"])
        if match:
            callsign = match.group(0)
        else:
            callsign = "Callsign is not found"
            
        extracted_callsign:list[str, int] = main(data[i]["transcript-result"])

        if extracted_callsign[0] == callsign:
            count += 1
            print("success!")
            print(callsign, extracted_callsign[0], extracted_callsign[1])
        else:
            print("False!!")
            print(callsign, extracted_callsign)
            print(data[i]["text"])
            print(data[i]["transcript-result"])
            
    success_rate = count / RANGE
    
    print(success_rate)
    