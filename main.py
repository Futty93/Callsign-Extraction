import json
import time
from word_processing import replace_words_spell, extract_callsigns, get_closest_callsign
from sentence_formatter import format_sentence, word_combination_formatter
from extractor import Extractor
from restoration import Restoration

def extraction_flight_number(input_text: str) -> list:
    """
    Extract and identify the flight callsign from the transcribed ATC communication.

    Parameters
    ----------
    input_text : str
        Transcribed ATC communication.

    Returns
    -------
    list
        A list containing the closest callsign match and its confidence (edit distance).
        If no callsign is found, it returns ["Callsign is not Found", 128].
    """
    # start_time: float = time.time()
    
    formatted_text = format_sentence(input_text)
    extractor = Extractor()

    replaced_array = replace_words_spell(formatted_text)
    # print("1. ", replaced_array)
    restoration_sentence = [word[0] if isinstance(word, list) else word for word in replaced_array]
    # print("2. ", restoration_sentence)
    restoration_callsign = Restoration().restoration_callSign(restoration_sentence)
    # print("3. ", restoration_callsign)
    extracted_callsigns = extractor.extract_pattern(restoration_callsign)
    # print("4. ", extracted_callsigns)

    if extracted_callsigns:
        closest_callsign = get_closest_callsign(extracted_callsigns, extractor)
        if closest_callsign[1] < 2:
            # end_time: float = time.time()
            # print(f"Execution time: {end_time - start_time} seconds")
            return closest_callsign

    # # スペルのみでの抽出テスト
    # # return ["Callsign is not Found", 128]

    callsign_metaphone = extract_callsigns(formatted_text, "metaphone")
    callsign_g2p = extract_callsigns(formatted_text, "g2p")
    
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
        closest_callsign = get_closest_callsign(extracted_callsigns, extractor)
        if closest_callsign[1] < 2:
            # end_time: float = time.time()
            # print(f"Execution time: {end_time - start_time} seconds")
            return closest_callsign
        
    # 1回目の音声符号化のみでの抽出テスト
    # return ["Callsign is not Found", 128]

    extra_formated_text = word_combination_formatter(formatted_text)

    callsign_metaphone_1 = extract_callsigns(extra_formated_text[0], "metaphone")
    callsign_metaphone_2 = extract_callsigns(extra_formated_text[1], "metaphone")
    callsign_g2p_1 = extract_callsigns(extra_formated_text[0], "g2p")
    callsign_g2p_2 = extract_callsigns(extra_formated_text[1], "g2p")
    
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
        closest_callsign = get_closest_callsign(extracted_callsigns, extractor)
        if closest_callsign[1] < 2:
            # end_time: float = time.time()
            # print(f"Execution time: {end_time - start_time} seconds")
            return closest_callsign
    
    # end_time: float = time.time()
    # print(f"Execution time: {end_time - start_time} seconds")
    return ["Callsign is not Found", 128]

if __name__ == '__main__':
    input_text: str = "I picked 903 bar decent and maintain 4200 feet clear for uploads."
    print(extraction_flight_number(input_text))