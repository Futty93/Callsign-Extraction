# from typing import List
#
# from utils.word_processing import replace_words_spell, extract_callsigns, get_closest_callsigns
# from utils.sentence_formatter import format_sentence, word_combination_formatter
# from utils.extractor import Extractor
# from utils.restoration import Restoration
#
# def main(input_text: str) -> list | list[list[str | int]]:
#     """
#     Extract and identify the flight callsign from the transcribed ATC communication.
#
#     Parameters
#     ----------
#     input_text : str
#         Transcribed ATC communication.
#
#     Returns
#     -------
#     list
#         A list containing the closest callsign match and its confidence (edit distance).
#         If no callsign is found, it returns ["Callsign is not Found", 128].
#     """
#     is_callsign_found: bool = False
#
#     # start_time: float = time.time()
#
#     formatted_text = format_sentence(input_text.lower())
#
#     extractor = Extractor()
#
#     print("0. ", formatted_text)
#
#     replaced_array = replace_words_spell(formatted_text)
#     print("1. ", replaced_array)
#     # restoration_sentence = [word[0] if isinstance(word, list) else word for word in replaced_array]
#     # print("2. ", restoration_sentence)
#     restoration_callsign = Restoration().restoration_callsign(replaced_array)
#     print("3. ", restoration_callsign)
#     extracted_callsigns = extractor.extract_pattern(restoration_callsign)
#
#     print("4. ", extracted_callsigns)
#
#     # if extracted_callsigns:
#     #     closest_callsigns = get_closest_callsigns(extracted_callsigns, extractor)
#     #     is_callsign_found = True
#     #
#     #     # closest_callsigns が空でないか確認
#     #     if closest_callsigns and closest_callsigns[0][1] < 2:
#     #         # end_time: float = time.time()
#     #         # print(f"Execution time: {end_time - start_time} seconds")
#     #         return closest_callsigns
#
#     # # スペルのみでの抽出テスト
#     # return [["Callsign is not Found", is_callsign_found]]
#
#     callsign_metaphone = extract_callsigns(formatted_text, "metaphone")
#     callsign_g2p = extract_callsigns(formatted_text, "g2p")
#
#     # callsign_metaphone と callsign_g2p の値を検証して、抽出したコールサインのリストを作成する
#     extracted_callsigns: list = []
#     # if callsign_metaphone and callsign_g2p:
#     #     extracted_callsigns = callsign_metaphone + callsign_g2p
#     # elif callsign_metaphone:
#     #     extracted_callsigns = callsign_metaphone
#     # elif callsign_g2p:
#     #     extracted_callsigns = callsign_g2p
#     # else:
#     #     extracted_callsigns = []
#     extracted_callsigns = list(set(callsign_metaphone) | set(callsign_g2p))
#
#     if extracted_callsigns:
#         closest_callsigns = get_closest_callsigns(extracted_callsigns, extractor)
#         is_callsign_found = True
#
#         # closest_callsigns が空でないか確認
#         # print(closest_callsigns)
#         if closest_callsigns and closest_callsigns[0][1] < 2:
#             # end_time: float = time.time()
#             # print(f"Execution time: {end_time - start_time} seconds")
#             return closest_callsigns
#
#     # # # 1回目の音声符号化のみでの抽出テスト
#     # return [["Callsign is not Found", is_callsign_found]]
#
#     extra_formated_text = word_combination_formatter(formatted_text)
#
#     callsign_metaphone_1 = extract_callsigns(extra_formated_text[0], "metaphone")
#     callsign_metaphone_2 = extract_callsigns(extra_formated_text[1], "metaphone")
#     callsign_g2p_1 = extract_callsigns(extra_formated_text[0], "g2p")
#     callsign_g2p_2 = extract_callsigns(extra_formated_text[1], "g2p")
#
#     extracted_callsigns: list = []
#
#     # callsign_metaphone_1 と callsign_metaphone_2 の値を検証して、抽出したコールサインのリストを作成する
#     if callsign_metaphone_1 and callsign_metaphone_2:
#         extracted_callsigns += callsign_metaphone_1 + callsign_metaphone_2
#     elif callsign_metaphone_1:
#         extracted_callsigns += callsign_metaphone_1
#     elif callsign_metaphone_2:
#         extracted_callsigns += callsign_metaphone_2
#
#     # callsign_g2p_1 と callsign_g2p_2 の値を検証して、抽出したコールサインのリストを作成する
#     if callsign_g2p_1 and callsign_g2p_2:
#         extracted_callsigns += callsign_g2p_1 + callsign_g2p_2
#     elif callsign_g2p_1:
#         extracted_callsigns += callsign_g2p_1
#     elif callsign_g2p_2:
#         extracted_callsigns += callsign_g2p_2
#
#     if extracted_callsigns:
#         closest_callsigns = get_closest_callsigns(extracted_callsigns, extractor)
#         is_callsign_found = True
#
#         # 追加: closest_callsigns が空でないか確認
#         if closest_callsigns and closest_callsigns[0][1] < 2:
#             # end_time: float = time.time()
#             # print(f"Execution time: {end_time - start_time} seconds")
#             return closest_callsigns
#
#     # end_time: float = time.time()
#     # print(f"Execution time: {end_time - start_time} seconds")
#     return [["Callsign is not Found", is_callsign_found]]
#
# if __name__ == '__main__':
#     input_text: str = "Skymark 1 2 3. Descend and maintain 5500 feet. Creanfall uploads."
#     print(main(input_text))

import re
import json
import os
import g2p_en as G2p
from doublemetaphone import doublemetaphone

g2p = G2p.G2p()
script_dir = os.path.dirname(os.path.abspath(__file__))

def levenshtein_distance(s1: str, s2: str) -> int:
    """2つの文字列の編集距離を計算する"""
    len1, len2 = len(s1), len(s2)
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)

    return dp[len1][len2]

def generate_g2p(word: str) -> str:
    return "".join(g2p(word))

def format_sentence(text: str) -> str:
    """文章を整形する（記号削除、数字とアルファベットの間のスペース挿入）"""
    original_text = text.lower()
    modified_text = re.sub(r'[.,\'"/]', '', original_text)
    modified_text = modified_text.replace('-', ' ')
    modified_text = re.sub(r'\b(\d+)\s+(\d+)\b', r'\1\2', modified_text)
    modified_text = re.sub(r'([a-zA-Z]+)(\d+)', r'\1 \2', modified_text)
    modified_text = re.sub(r'(\d+)([a-zA-Z])', r'\1 \2', modified_text)

    return modified_text if modified_text == original_text else format_sentence(modified_text)

def load_json(filepath: str) -> dict:
    """JSONファイルを読み込む"""
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_element(item, index: int) -> str:
    """ リストの指定したインデックスの要素を取得。リストでなければそのまま返す """
    return item[index] if isinstance(item, list) and len(item) > index else item

def replace_to_three_letter_code(replaced_words: list[str]) -> list[str]:
    """航空会社名を3文字コードに置換"""
    airline_codes = load_json(os.path.join(script_dir, './registered_json/airline_code_dict.json'))
    restoration_three_letter_code = []
    index = 0

    while index < len(replaced_words) - 1:
        current_word = get_element(replaced_words[index], 0)
        next_word = get_element(replaced_words[index + 1], 0)
        combined_word = f"{current_word} {next_word}"

        if current_word in airline_codes:
            restoration_three_letter_code.append((airline_codes[current_word], get_element(replaced_words[index], 1)))
            index += 1
        elif combined_word in airline_codes:
            restoration_three_letter_code.append((airline_codes[combined_word], [
                get_element(replaced_words[index], 1),
                get_element(replaced_words[index + 1], 1)
            ]))
            index += 2
        else:
            restoration_three_letter_code.append(get_element(replaced_words[index], 1))
            index += 1

    if index == len(replaced_words) - 1:
        restoration_three_letter_code.append(get_element(replaced_words[index], 1))

    return restoration_three_letter_code

def extract_callsigns_and_restore_sentence(restoration_three_letter_code: list) -> tuple[list[str], list[str]]:
    """
    3文字コードのリストを処理し、コールサインを抽出し、復元された文章を作成する。

    Parameters
    ----------
    restoration_three_letter_code : list
        変換対象のリスト。要素は文字列またはタプル (3文字コード, 元の単語)。

    Returns
    -------
    Tuple[list[str], list[str]]
        - 抽出されたコールサインのリスト
        - 復元された文章のリスト（"CALLSIGN" に置き換えられたものを含む）
    """
    found_callsigns: list[str] = []
    restored_sentence: list[str] = []
    index = 0

    while index < len(restoration_three_letter_code) - 1:
        current = restoration_three_letter_code[index]
        next_item = restoration_three_letter_code[index + 1]

        if isinstance(current, tuple) and isinstance(next_item, str) and next_item.isdigit():
            found_callsigns.append(current[0] + next_item)
            restored_sentence.append("CALLSIGN")
            index += 2  # 次の要素をスキップ
        else:
            restored_sentence.append(current[1] if isinstance(current, tuple) else current)
            index += 1

    # 最後の要素を追加（リストが空でない場合のみ）
    if restoration_three_letter_code:
        restored_sentence.append(restoration_three_letter_code[-1])

    return found_callsigns, restored_sentence

def find_similar_callsigns_in_area(script_dir: str, found_callsigns: list[str]) -> list[list[str, int]]:
    """
    エリア情報ファイルを読み込み、指定されたコールサインと類似するエリア内のコールサインを検索する。

    Parameters
    ----------
    script_dir : str
        エリア情報の JSON ファイルが存在するディレクトリのパス。
    found_callsigns : list[str]
        検索対象のコールサインリスト。

    Returns
    -------
    list[list[str, int]]
        類似するコールサインとその編集距離のリスト（例: [["ABC123", 1], ["XYZ456", 0]]）。
    """
    area_info_path = os.path.join(script_dir, "./test/area_info.json")
    area_info = load_json(area_info_path)

    in_area_callsigns = []

    for callsign in found_callsigns:
        for area_callsign in area_info:
            area_alpha_part = ''.join(filter(str.isalpha, area_callsign))
            extracted_alpha_part = ''.join(filter(str.isalpha, callsign))

            # アルファベット部分が異なる場合はスキップ
            if area_alpha_part != extracted_alpha_part:
                continue

            # 数字部分の編集距離を計算
            area_num_part = ''.join(filter(str.isdigit, area_callsign))
            extracted_num_part = ''.join(filter(str.isdigit, callsign))

            d = levenshtein_distance(area_num_part, extracted_num_part)

            if d < 2:
                in_area_callsigns.append([area_callsign, d])

    return in_area_callsigns

def filter_callsigns_by_lowest_distance(in_area_callsigns: list[list[str, int]]) -> list[list[str, int]]:
    """
    コールサインが重複する場合、数値が最小のペアのみを残す。

    Parameters
    ----------
    in_area_callsigns : list[list[str, int]]
        各要素が ["コールサイン", 数値] となる2次元リスト。

    Returns
    -------
    list[list[str, int]]
        数値が最小のペアのみを残したリスト。
    """
    callsign_dict = {}

    for callsign, distance in in_area_callsigns:
        if callsign not in callsign_dict or distance < callsign_dict[callsign]:
            callsign_dict[callsign] = distance

    return [[callsign, distance] for callsign, distance in callsign_dict.items()]

def process_word_list(word_list: list[str], register_word_list: list[str] | dict) -> list[str]:
    """単語リストを登録された単語と比較し、類似するものを置換"""
    replaced_words = []
    for word in word_list:
        if not isinstance(word, list):
            replaced_words.append(word)
            continue
        min_distance = float('inf')
        closest_word = word[0]

        for register_word in register_word_list:
            d = levenshtein_distance(word[0], register_word)
            if d < min_distance:
                min_distance = d
                closest_word = register_word

        if len(word[0]) * 2 / 3 > min_distance:
        # if max(len(word), len(closest_word)) * 2 / 3 > min_distance:
            if isinstance(register_word_list, dict):
                replaced_words.append([register_word_list[closest_word], word[1]])
            else:
                replaced_words.append([closest_word, word[1]])
        else:
            replaced_words.append(word[1])
    return replaced_words

def process_alternate_callsigns(word_list: list[str]) -> tuple[list[str], list[str]]:
    """Metaphone & G2P を使ってコールサインを探す"""
    key_array_metaphone = [[doublemetaphone(word)[0], word] if not word.isdigit() else word for word in word_list]
    key_array_g2p = [[generate_g2p(word), word] if not word.isdigit() else word for word in word_list]

    register_metaphone_dict = load_json(os.path.join(script_dir, "./generated_json/word_metaphone_dict.json"))
    register_g2p_dict = load_json(os.path.join(script_dir, "./generated_json/word_g2p_dict.json"))

    replaced_words_metaphone = process_word_list(key_array_metaphone, register_metaphone_dict)
    replaced_words_g2p = process_word_list(key_array_g2p, register_g2p_dict)

    found_callsigns_metaphone, restored_sentence_metaphone = extract_callsigns_and_restore_sentence(replace_to_three_letter_code(replaced_words_metaphone))
    found_callsigns_g2p, restored_sentence_g2p = extract_callsigns_and_restore_sentence(replace_to_three_letter_code(replaced_words_g2p))

    return found_callsigns_metaphone, found_callsigns_g2p

def main(text: str) -> list:
    is_callsign_found: bool = False

    """メイン処理"""
    formatted_text = format_sentence(text)
    print("0. ", formatted_text)

    word_list = formatted_text.split()
    register_word_list = load_json(os.path.join(script_dir, "./registered_json/word_register.json"))

    replaced_words = process_word_list(word_list, register_word_list)
    print("1. ", replaced_words)

    restoration_three_letter_code = replace_to_three_letter_code(replaced_words)
    print("3. ", restoration_three_letter_code)

    found_callsigns, restored_sentence = extract_callsigns_and_restore_sentence(restoration_three_letter_code)
    print("4. ", found_callsigns)

    in_area_callsigns = []

    if found_callsigns:
        is_callsign_found = True
        in_area_callsigns = find_similar_callsigns_in_area(script_dir, found_callsigns)

    # if in_area_callsigns:
    #     return in_area_callsigns

    found_callsigns_metaphone, found_callsigns_g2p = process_alternate_callsigns(word_list)

    found_callsigns = list(set(found_callsigns_metaphone) | set(found_callsigns_g2p))

    if found_callsigns:
        is_callsign_found = True
        in_area_callsigns = find_similar_callsigns_in_area(script_dir, found_callsigns)

    if in_area_callsigns:
        return filter_callsigns_by_lowest_distance(in_area_callsigns)

    even_combined, odd_combined = [], [word_list[0]]
    for i in range(len(word_list) - 1):
        # 現在の単語と次の単語
        current_word = word_list[i]
        next_word = word_list[i + 1]

        # 偶数インデックスの場合
        if i % 2 == 0:
            even_combined.append(
                f"{current_word}{next_word}" if not (
                        current_word.isdigit() or next_word.isdigit()) else current_word
            )
            if next_word.isdigit():
                even_combined.append(next_word)

        # 奇数インデックスの場合
        else:
            odd_combined.append(
                f"{current_word}{next_word}" if not (
                        current_word.isdigit() or next_word.isdigit()) else current_word
            )
            if next_word.isdigit():
                odd_combined.append(next_word)

    if len(word_list) % 2 == 1:
        even_combined.append(word_list[-1])

    found_callsigns_metaphone_even, found_callsigns_g2p_even = process_alternate_callsigns(even_combined)
    found_callsigns_metaphone_odd, found_callsigns_g2p_odd = process_alternate_callsigns(odd_combined)

    found_callsigns = list(set(found_callsigns_metaphone_even) | set(found_callsigns_g2p_even) | set(found_callsigns_metaphone_odd) | set(found_callsigns_g2p_odd))

    if found_callsigns:
        is_callsign_found = True
        in_area_callsigns = find_similar_callsigns_in_area(script_dir, found_callsigns)

    if in_area_callsigns:
        return filter_callsigns_by_lowest_distance(in_area_callsigns)

    return [["Callsign is not Found", is_callsign_found]]





if __name__ == '__main__':
    input_text: str = "Skymark 1 2 3c. Descend and maintain 5500 feet. Creanfall uploads."
    print(main(input_text))
