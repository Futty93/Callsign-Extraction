import re
import json
from Levenshtein import distance

class Extractor:
    def __init__(self):
        # 空域情報の読み込み
        with open("./area_info.json", 'r', encoding='utf-8') as f:
            self.area_info = json.load(f)

    def extract_pattern(self, sentence: str) -> list:
        """
        受け取った文章から正規表現に一致する部分を抽出する
        Parameter
        ---
            sentence: str
                便名などを3レターに置き換えた後の文章を受け取る
        Return
        ---
            extracted_patterns: list
                正規表現に一致した部分を全て抜き出し、配列として返す。
                1つも見つからなかった場合はFalseを返す。
        """
        pattern = r'\b([A-Z]{3})\s(\d+)\b'  # AAA 111 のパターン
        matches = re.findall(pattern, sentence)
        if matches:
            extracted_patterns = [''.join(match) for match in matches]
            return extracted_patterns
        else:
            return False
        

    ##########################################################################
    # 空域情報と抽出したコールサインの参照を行う関数を作成する
    def reference_area_info(self, extracted_callsign: str) -> list:
        """
        抽出したコールサインと空域に存在するコールサインを比較し、最も距離の近いものとその距離を返す関数
        """
        min_distance: int = 128 # 十分に大きい数字を初期値とする
        closest_callsign = ""
        for area_callsign in self.area_info:
            d = distance(extracted_callsign, area_callsign)
            if d < min_distance:
                min_distance = d
                closest_callsign = area_callsign
        
        return [closest_callsign, min_distance]
        
        
    def get_closest_callsign(self, extracted_callsigns: list) -> list:
        callsigns = []
        for item in extracted_callsigns:
            callsigns.append(self.reference_area_info(item))

        callsign = ""
        min_distance = float('inf')
        for item in callsigns:
            if item[1] < min_distance:
                min_distance = item[1]
                callsign = item[0]

        return [callsign, min_distance]

if __name__ == "__main__":
    # クラスのインスタンス化
    extractor = Extractor()

    # テスト用の文章
    sample_text = "ANA 133 Hold position Traffic from final approach"

    # パターンを抽出
    extracted_patterns = extractor.extract_pattern(sample_text)

    # 抽出されたパターンの表示
    print("Extracted patterns:", extracted_patterns)
