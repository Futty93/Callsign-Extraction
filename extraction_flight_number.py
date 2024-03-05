from sentenceFormat import SentenceFormatter
from g2p_metaphone_gen  import G2PClass, MetaphoneClass
from word_replace import WordReplaceClass
from restoration_sentence import Restoration
from reference_callsign import Extractor
import json


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


def extraction_flight_number(input_text: str) -> list:
    """
    音声認識による文字起こしの結果の原文を引数とし、そこから空域情報と照会したコールサインを確信度(編集距離)とともに返す
    
    Parameters
    ---
        input_text: str
            音声認識した管制官の命令文
            
    Return
    ---
        [callsign: str, min_distance: int]: list
            抽出したコールサインを空域情報と照会し、最も近いものとその確信度(編集距離)のリスト
    """
    
    formated_text = SentenceFormatter().format_sentence(input_text)
    
    extractor = Extractor()

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
    extracted_callsigns = extractor.extract_pattern(restoration_callsign)
    
    if extracted_callsigns:
        return extractor.get_closest_callsign(extracted_callsigns)

    callsign_metaphone = process_extract_callsign(formated_text, "metaphone")
    callsign_g2p = process_extract_callsign(formated_text, "g2p")
    
    # callsign_metaphone と callsign_g2p の値を検証して、抽出したコールサインのリストを作成する
    extracted_callsigns: list = []
    if callsign_metaphone and callsign_g2p:
        extracted_callsigns = callsign_metaphone + callsign_g2p
    elif callsign_metaphone:
        extracted_callsigns = callsign_metaphone
    elif callsign_g2p:
        extracted_callsigns = callsign_g2p
    else:
        extracted_callsigns = []


    if extracted_callsigns:
        return extractor.get_closest_callsign(extracted_callsigns)

    extra_formated_text = SentenceFormatter().word_combination_formatter(formated_text)

    callsign_metaphone_1 = process_extract_callsign(extra_formated_text[0], "metaphone")
    callsign_metaphone_2 = process_extract_callsign(extra_formated_text[1], "metaphone")
    callsign_g2p_1 = process_extract_callsign(extra_formated_text[0], "g2p")
    callsign_g2p_2 = process_extract_callsign(extra_formated_text[1], "g2p")
    
    extracted_callsigns:list = []

    # callsign_metaphone_1 と callsign_metaphone_2 の値を検証して、抽出したコールサインのリストを作成する
    if callsign_metaphone_1 and callsign_metaphone_2:
        extracted_callsigns += callsign_metaphone_1 + callsign_metaphone_2
    elif callsign_metaphone_1:
        extracted_callsigns += callsign_metaphone_1
    elif callsign_metaphone_2:
        extracted_callsigns += callsign_metaphone_2

    # callsign_g2p_1 と callsign_g2p_2 の値を検証して、抽出したコールサインのリストを作成する
    if callsign_g2p_1 and callsign_g2p_2:
        extracted_callsigns += callsign_g2p_1 + callsign_g2p_2
    elif callsign_g2p_1:
        extracted_callsigns += callsign_g2p_1
    elif callsign_g2p_2:
        extracted_callsigns += callsign_g2p_2

    if extracted_callsigns:
        return extractor.get_closest_callsign(extracted_callsigns)
    
    else:
        return ["Callsign is not Found", 128]

if __name__ == '__main__':
    input_text: str = "IMAX456 Hold position. Traffic on final"
    print(extraction_flight_number(input_text))