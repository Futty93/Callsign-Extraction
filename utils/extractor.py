import json
import os
import re
from utils.levenshtein import distance
from API.get_area_info import get_callsigns_from_api

script_dir = os.path.dirname(os.path.abspath(__file__))
area_info_path = os.path.join(script_dir, "../ATC_area_info.json")

# area_info_path = os.path.join(script_dir, "../area_info.json")

class Extractor:
    def __init__(self):
        # テスト用の空域情報の利用はこっち
        with open(area_info_path, 'r', encoding='utf-8') as f:
            self.area_info = json.load(f)
        
        # # Horusの空域情報の利用はこっち
        # self.area_info = get_callsigns_from_api()

    def extract_pattern(self, tokens: list) -> list | bool:
        """
        Extract patterns where the current element is a tuple and the next element is a number.

        Parameters
        ----------
        sentence : str
            The sentence to be processed.

        Returns
        -------
        list
            A list of matched patterns, or False if no patterns are found.
        """
        # # トークンを分割
        # tokens = sentence.split()

        # 結果を格納するリスト
        matched_patterns = []

        # 各要素をチェック
        for i in range(len(tokens) - 1):  # 最後の要素は次の要素がないためスキップ
            current = tokens[i]
            next_item = tokens[i + 1]

            # current がタプルであり、next_item が数字かを判定
            if isinstance(current, tuple) and next_item.isdigit():
                matched_patterns.append(current[0] + next_item)

        # パターンが見つかった場合はリストを返し、見つからなかった場合は False を返す
        return matched_patterns if matched_patterns else False
    
    def reference_area_info(self, extracted_callsign: str) -> list:
        """
        Find the closest callsign matches from the known area information.

        Parameters
        ----------
        extracted_callsign : str
            The extracted callsign to be compared.

        Returns
        -------
        list
            A list of lists containing the closest callsign matches and their edit distance.
            If min_distance == 0, the list will contain one entry [[closest_callsign, min_distance]].
            If min_distance > 0, the list will contain all matches with the same min_distance.
        """
        min_distance: int = 128
        closest_callsigns = []

        # 空域に存在するすべてのコールサインと比較を行う。
        # 3レターコードと便名に分けて、3レターコードは完全一致、便名は編集距離を計算する。
        for area_callsign in self.area_info:
            # Extract alphabetic part
            area_alpha_part = ''.join(filter(str.isalpha, area_callsign))
            extracted_alpha_part = ''.join(filter(str.isalpha, extracted_callsign))

            # Check if alphabetic parts match
            if area_alpha_part != extracted_alpha_part:
                continue

            # Calculate edit distance for numeric parts
            area_num_part = ''.join(filter(str.isdigit, area_callsign))
            extracted_num_part = ''.join(filter(str.isdigit, extracted_callsign))
            d = distance(extracted_num_part, area_num_part)

            # # コースサインが最も近い航空機と、その編集距離を返す
            # if d < min_distance:
            #     min_distance = d
            #     closest_callsigns = [[area_callsign, d]]
            # elif d == min_distance:
            #     closest_callsigns.append([area_callsign, d])
            if d <= 1:
                closest_callsigns.append([area_callsign, d])

        return closest_callsigns