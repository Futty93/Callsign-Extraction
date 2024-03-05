import re

class Extractor:
    def __init__(self):
        pass

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
    def reference_area_info(self, extracted_callsign: str, area_info: list[str]) -> list:
        """
        抽出したコールサインと空域に存在するコールサインを比較し、最も距離の近いものとその距離を返す関数
        """
        

if __name__ == "__main__":
    # クラスのインスタンス化
    extractor = Extractor()

    # テスト用の文章
    sample_text = "ANA 133 Hold position Traffic from final approach"

    # パターンを抽出
    extracted_patterns = extractor.extract_pattern(sample_text)

    # 抽出されたパターンの表示
    print("Extracted patterns:", extracted_patterns)
