from main import main as main
import json
import re

from whispercpp import Whisper

w = Whisper('small')

if __name__ == "__main__":
    with open("transcript.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    pattern = r'\b([A-Z]{3})(\d+)\b'  # AAA111 のパターン
    count = 0
    RANGE = 159 # sound fileの番号
    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0
    count_5 = 0

    for i in range(RANGE + 1):
        match = re.search(pattern, data[i]["text"])
        if match:
            callsign = match.group(0)
        else:
            callsign = "Callsign is not found"

        result = w.transcribe(f"../../音源ファイル/soundFiles/{data[i]['sound-file']}")

        text = w.extract_text(result)

        extracted_callsigns:list[str, int] = main(text[0])

        print(i)

    #     if extracted_callsign[0][0] == callsign:
    #         count += 1
    #         print("success!")
    #         print(callsign, extracted_callsign[0])
    #     else:
    #         print("False!!")
    #         print(callsign, extracted_callsign)
    #         print(data[i]["text"])
    #         print(data[i]["transcript-result"])
    #
    # success_rate = count / (RANGE + 1)
    #
    # print(success_rate, '(',  count, '/',  RANGE + 1, ')' )

        if any(extracted_callsign[0] == callsign for extracted_callsign in extracted_callsigns):
            # 二つ目の要素を抽出
            second_elements = [item[1] for item in extracted_callsigns]

            # 条件に応じた処理
            if all(value == 0 for value in second_elements):
                # 全てが 0 の場合の処理1
                count_1 += 1
            elif any(value == 0 for value in second_elements) and any(value != 0 for value in second_elements):
                # 0と0以外が混在する場合の処理2
                count_2 += 1
            elif all(value != 0 for value in second_elements):
                # 全てが 0 以外の場合の処理3
                count_3 += 1
            count += 1
            print("success!")
            print(callsign, [extracted_callsign for extracted_callsign in extracted_callsigns if
                             extracted_callsign[0] == callsign])
        else:
            if extracted_callsigns[0][1]:
                count_4 += 1
            else:
                count_5 += 1
            print("False!!")
            print(callsign, extracted_callsigns)
            print(data[i]["text"])
            print(text[0])

    success_rate = count / (RANGE + 1)

    print(success_rate, '(', count, '/', RANGE + 1, ')')
    print("count_1:", count_1)
    print("count_2:", count_2)
    print("count_3:", count_3)
    print("count_4:", count_4)
    print("count_5:", count_5)
    