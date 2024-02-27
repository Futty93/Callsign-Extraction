import json
from Levenshtein import distance

def replace_with_closest_words(words):
    """
    与えられた単語の配列に対して、./generated_json/word_metaphone_key.jsonに登録されている
    単語との距離を計算し、最も近い単語に置き換える。

    Args:
    - words (list): 置き換える単語が含まれる配列

    Returns:
    - replaced_words (list): 置き換えられた単語が含まれる配列
    """

    # JSONファイルから単語とそれに対応するメタフォンキーを読み込む
    with open('./generated_json/word_metaphone_key.json', 'r') as f:
        word_metaphone_key = json.load(f)

    replaced_words = []

    # 各単語に対してループを実行し、最も近い単語に置き換える
    for word in words:
        if word.isdigit():
            replaced_words.append(word)
            continue
        min_distance = float('inf')
        closest_word = word

        # 単語のメタフォンキーに対応する単語との距離を計算し、最小距離を見つける
        for metaphone_key_word in word_metaphone_key:
            d = distance(word, metaphone_key_word)
            if d < min_distance:
                min_distance = d
                closest_word = metaphone_key_word

        if len(word)*2/3 > min_distance:
            replaced_words.append([closest_word, min_distance])
        else:
            replaced_words.append(word)

    return replaced_words
