from sentenceFormat import SentenceFormatter
from g2p_metaphone_gen  import G2PClass, MetaphoneClass
from word_replace import WordReplaceClass
from restoration_sentence import Restoration
from reference_callsign import Extractor


def process_extract_callsign(sentence, processing_type):
    """
    テキストの処理を行います。

    Args:
    - sentence (str): 処理するテキスト
    - processing_type (str): 処理タイプ（"metaphone"または"g2p"）

    Returns:
    - list: テキストの処理結果
    """
    # テキストのフォーマット
    formated_text = SentenceFormatter().format_sentence(sentence)

    if processing_type == "metaphone":
        # metaphoneプロセス
        key_array = MetaphoneClass().generate_metaphone_key_list(formated_text)
    elif processing_type == "g2p":
        # g2pプロセス
        key_array = G2PClass().generate_g2p_list(formated_text)
    else:
        raise ValueError("Invalid processing_type. Must be 'metaphone' or 'g2p'.")

    # 単語の置換
    if processing_type == "metaphone":
        # metaphoneプロセス
        replaced_array = WordReplaceClass.replace_words_metaphone(key_array)
    elif processing_type == "g2p":
        # g2pプロセス
        replaced_array = WordReplaceClass.replace_words_g2p(key_array)
    

    # 単語の復元
    restoration_sentence = Restoration().restoration_sentence(replaced_array, processing_type)

    # コールサインの抽出
    restoration_callsign = Restoration().restoration_callSign(restoration_sentence)
    callsign = Extractor().extract_pattern(restoration_callsign)

    return callsign


def main(input_text: str):
    formated_text = SentenceFormatter().format_sentence(input_text)

    replaced_array = WordReplaceClass.replace_words_spell(formated_text)
    restoration_sentence = []
    for word in replaced_array:
        # もしwordがlistだったら辞書を利用して元の単語に置き換える
        if isinstance(word, list):
            restoration_sentence.append(word[0])
        else:
            restoration_sentence.append(word)

    restoration_sentence = ' '.join(restoration_sentence)
    restoration_callsign = Restoration().restoration_callSign(restoration_sentence)
    callsign = Extractor().extract_pattern(restoration_callsign)

    if callsign:
        print(callsign)
        return

    callsign_metaphone = process_extract_callsign(formated_text, "metaphone")
    callsign_g2p = process_extract_callsign(formated_text, "g2p")

    if callsign_metaphone or callsign_g2p:
        print(callsign_metaphone)
        print(callsign_g2p)
        return

    extra_formated_text = SentenceFormatter().word_combination_formatter(formated_text)

    callsign_metaphone_1 = process_extract_callsign(extra_formated_text[0], "metaphone")
    callsign_metaphone_2 = process_extract_callsign(extra_formated_text[1], "metaphone")
    callsign_g2p_1 = process_extract_callsign(extra_formated_text[0], "g2p")
    callsign_g2p_2 = process_extract_callsign(extra_formated_text[1], "g2p")

    if callsign_metaphone_1 or callsign_metaphone_2 or callsign_g2p_1 or callsign_g2p_2:
        if callsign_metaphone_1:
            print(callsign_metaphone_1)
        if callsign_metaphone_2:
            print(callsign_metaphone_2)
        if callsign_g2p_1:
            print(callsign_g2p_1)
        if callsign_g2p_2:
            print(callsign_g2p_2)
    else:
        print("Callsign not Found")

    return

if __name__ == '__main__':
    input_text: str = "5x456 Hold position. Traffic on final"
    main(input_text)