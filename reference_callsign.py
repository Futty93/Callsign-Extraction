import re

class Extractor:
    def __init__(self):
        pass

    def extract_pattern(self, text):
        pattern = r'\b([A-Z]{3})\s(\d+)\b'  # AAA 111 のパターン
        matches = re.findall(pattern, text)
        if matches:
            extracted_patterns = [''.join(match) for match in matches]
            return extracted_patterns
        else:
            return "Pattern not found."

if __name__ == "__main__":
    # クラスのインスタンス化
    extractor = Extractor()

    # テスト用の文章
    sample_text = "This is a sample text with patterns like AAA 123, BBB 4567, and CC 78901."

    # パターンを抽出
    extracted_patterns = extractor.extract_pattern(sample_text)

    # 抽出されたパターンの表示
    print("Extracted patterns:", extracted_patterns)
