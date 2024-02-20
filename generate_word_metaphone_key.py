import json
from doublemetaphone import doublemetaphone

def generate_metaphone_keys(input_file, output_dict_file, output_key_file):

    # 入力ファイルを読み込む
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # metaphoneキーを計算し、新しい辞書に保存
    word_metaphone_dict = {}
    word_metaphone_key = []
    for word in data:
        metaphone_key = doublemetaphone(word)[0]  # DMetaphone()でメタフォンキーを生成
        metaphone_key = metaphone_key.decode('utf-8') if isinstance(metaphone_key, bytes) else metaphone_key
        word_metaphone_dict[metaphone_key] = word
        word_metaphone_key.append(metaphone_key)

    # 結果を新しいJSONファイルに書き込む
    with open(output_dict_file, 'w', encoding='utf-8') as f:
        json.dump(word_metaphone_dict, f, indent=4, ensure_ascii=False)

    with open(output_key_file, 'w', encoding='utf-8') as f:
        json.dump(word_metaphone_key, f, indent=4, ensure_ascii=False)

# 実行例
generate_metaphone_keys('./registered_json/word_register.json', './generated_json/word_metaphone_dict.json', './generated_json/word_metaphone_key.json')
