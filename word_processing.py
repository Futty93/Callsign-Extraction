import json
from Levenshtein import distance
# from levenshtein import restricted_distance as distance
from g2p import G2PClass
from metaphone import MetaphoneClass
from restoration import Restoration
from extractor import Extractor

class WordReplacement:
    def __init__(self):
        with open('registered_json/word_register.json', 'r') as f:
            self.register_word_list = json.load(f)

    def replace_words_spell(self, sentence: str) -> list:
        """
        Replace words in the given sentence with registered words based on spelling similarity.

        Parameters
        ----------
        sentence : str
            Formatted sentence.

        Returns
        -------
        list
            A list containing the replaced words (if similar) or the original words.
            Replaced words are represented as [replaced_word, distance].
        """
        word_list: list[str] = sentence.split()
        replaced_words: list[str] = []

        for word in word_list:
            if word.isdigit():
                replaced_words.append(word)
                continue
            min_distance = float('inf')
            closest_word = word

            for register_word in self.register_word_list:
                d = distance(word, register_word)
                if d < min_distance:
                    min_distance = d
                    closest_word = register_word

            if len(word) * 2 / 3 > min_distance:
                replaced_words.append([closest_word, min_distance])
            else:
                replaced_words.append(word)

        return replaced_words

    def replace_words_metaphone(word_list: list[str]) -> list:
        """
        与えられた単語のmetaphone keyの配列に対して、./generated_json/word_metaphone_key.jsonに登録されている
        単語との距離を計算し、最も近い単語に置き換える。

        Parameters
        ---
            word_list: list[str]
                metaphone key化された文章の単語ごとの配列
        
        Returns
        ---
            replaced_words: list[str]
                単語を置き換えた場合は[置き換えた単語, 元の単語]の配列を返す
                単語の距離が一定以上ある場合は単語をそのまま返す
        """

        # JSONファイルから単語とそれに対応するメタフォンキーを読み込む
        with open('./generated_json/word_metaphone_list.json', 'r') as f:
            register_metaphone_list = json.load(f)

        replaced_words: list[str] = []

        # 各単語に対してループを実行し、最も近い単語に置き換える
        for word in word_list:
            if isinstance(word, list) == False:
                replaced_words.append(word)
                continue
            min_distance = float('inf')
            closest_word = word[0]

            # 単語のメタフォンキーに対応する単語との距離を計算し、最小距離を見つける
            for metaphone_key_word in register_metaphone_list:
                d = distance(word[0], metaphone_key_word)
                if d < min_distance:
                    min_distance = d
                    closest_word = metaphone_key_word

            if len(word) * 2 / 3 > min_distance:
                replaced_words.append([closest_word, word[1]])
            else:
                replaced_words.append(word[1])

        return replaced_words

    def replace_words_g2p(word_list: list[str]) -> list:
        """
        与えられたg2p化された単語の配列に対してそれぞれ登録されている単語のg2pと距離を計算し、最も近い単語に置き換えた配列を返す

        Parameters
        ---
            word_list: list[str]
                g2p化された文章の単語ごとの配列
        
        Returns
        ---
            replaced_words: list[str]
                単語を置き換えた場合は[置き換えた単語, 元の単語]の配列を返す
                単語の距離が一定以上ある場合は単語をそのまま返す
        """
        # JSONファイルから登録されている単語のg2pを読み込む
        with open('./generated_json/word_g2p_list.json', 'r') as f:
            register_g2p_list = json.load(f)

        replaced_words: list[str] = []
        # 各単語に対してループを実行し、最も近い単語に置き換える
        for word in word_list:
            if isinstance(word, list) == False:
                replaced_words.append(word)
                continue
            min_distance = float('inf')
            closest_word = word[0]

            # 単語のメタフォンキーに対応する単語との距離を計算し、最小距離を見つける
            for g2p_word in register_g2p_list:
                d = distance(word[0], g2p_word)
                if d < min_distance:
                    min_distance = d
                    closest_word = g2p_word

            if len(word) * 2 / 3 > min_distance:
                replaced_words.append([closest_word, word[1]])
            else:
                replaced_words.append(word[1])

        return replaced_words

def replace_words_spell(sentence: str) -> list:
    """
    Wrapper function to call the replace_words_spell method from the WordReplacement class.
    """
    word_replacement = WordReplacement()
    return word_replacement.replace_words_spell(sentence)

def extract_callsigns(sentence: str, processing_type: str) -> list:
    """
    Extract callsigns from the given sentence using the specified processing type.

    Parameters
    ----------
    sentence : str
        Formatted sentence.
    processing_type : str
        The processing type ("metaphone" or "g2p").

    Returns
    -------
    list
        A list of extracted callsigns.
    """
    if processing_type == "metaphone":
        key_array = MetaphoneClass().generate_metaphone_key_list(sentence)
        replaced_array = WordReplacement.replace_words_metaphone(key_array)
    elif processing_type == "g2p":
        key_array = G2PClass().generate_g2p_list(sentence)
        replaced_array = WordReplacement.replace_words_g2p(key_array)
    else:
        raise ValueError("Invalid processing_type. Must be 'metaphone' or 'g2p'.")

    restoration_sentence = Restoration().restoration_sentence(replaced_array, processing_type)
    restoration_callsign = Restoration().restoration_callSign(restoration_sentence)
    callsign = Extractor().extract_pattern(restoration_callsign)

    return callsign

def get_closest_callsign(extracted_callsigns: list, extractor: Extractor) -> list:
    """
    Find the closest callsign match from the extracted callsigns by comparing with known area information.

    Parameters
    ----------
    extracted_callsigns : list
        A list of extracted callsigns.
    extractor : Extractor
        An instance of the Extractor class.

    Returns
    -------
    list
        A list containing the closest callsign match and its confidence (edit distance).
    """
    callsigns = []
    print(extracted_callsigns)
    for item in extracted_callsigns:
        callsigns.append(extractor.reference_area_info(item))

    callsign = ""
    min_distance = float('inf')
    for item in callsigns:
        if item[1] < min_distance:
            min_distance = item[1]
            callsign = item[0]

    return [callsign, min_distance]