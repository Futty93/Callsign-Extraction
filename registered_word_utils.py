import json
from doublemetaphone import doublemetaphone
import g2p_en as G2p

g2p = G2p.G2p()
def generate_g2p(word: str) -> str:
    return "".join(g2p(word))

class GenerateJsonDataClass:

    def generate_metaphone_keys(self, input_file: str, output_dict_file: str) -> None:
        """
        登録されている単語のリストを受け取り、metaphone_keyだけのリストと、キーがmetaphone_key、バリューが登録された単語となる辞書型のリストを生成します。

        Parameters
        --------------
            input_file: str
                登録されている単語のファイル名
            output_dict_file: str
                生成する辞書型のリストのファイル名

        Returns
        --------------
            None
        """

        # 入力ファイルを読み込む
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # metaphoneキーを計算し、新しい辞書に保存
        word_metaphone_dict = {}
        for word in data:
            metaphone_key = doublemetaphone(word)[0]  # DMetaphone()でメタフォンキーを生成
            metaphone_key = metaphone_key.decode('utf-8') if isinstance(metaphone_key, bytes) else metaphone_key # metaphoneが謎の型で返ってくるのでstrに変換
            word_metaphone_dict[metaphone_key] = word
            multiple_words: list[str] = word.split()
            # 2つの単語からなり、かつ2つ目の単語が母音から始まる場合には、結合したものも登録
            if len(multiple_words) >= 2:
                if self._is_vowel(multiple_words[1][0]):
                    if self._is_vowel(multiple_words[0][-1]):
                        multiple_word: str = multiple_words[0][:-1] + multiple_words[1]
                    else:
                        multiple_word: str = multiple_words[0] + multiple_words[1]
                    metaphone_key = doublemetaphone(multiple_word)[0]
                    metaphone_key = metaphone_key.decode('utf-8') if isinstance(metaphone_key, bytes) else metaphone_key
                    word_metaphone_dict[metaphone_key] = word

        # 結果を新しいJSONファイルに書き込む
        with open(output_dict_file, 'w', encoding='utf-8') as f:
            json.dump(word_metaphone_dict, f, indent=4, ensure_ascii=False)

    def generate_g2p_list_and_dict(self, input_file: str, output_dict_file: str) -> None:
        """
        登録されている単語のリストを受け取り、g2p_keyだけのリストと、キーがg2p_key、バリューが登録された単語となる辞書型のリストを生成します。

        Parameters
        --------------
            input_file: str
                登録されている単語のファイル名
            output_dict_file: str
                生成する辞書型のリストのファイル名

        Returns
        --------------
            None
        """
        # 入力ファイルを読み込む
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # g2pを計算し、新しい辞書に保存
        word_g2p_dict = {}
        for word in data:
            g2p_key = generate_g2p(word)
            word_g2p_dict[g2p_key] = word
            multiple_words: list[str] = word.split()
            # 2つの単語からなり、かつ2つ目の単語が母音から始まる場合には、結合したものも登録
            if len(multiple_words) >= 2:
                if self._is_vowel(multiple_words[1][0]):
                    if self._is_vowel(multiple_words[0][-1]):
                        multiple_word: str = multiple_words[0][:-1] + multiple_words[1]
                    else:
                        multiple_word: str = multiple_words[0] + multiple_words[1]
                    g2p_key = generate_g2p(multiple_word)
                    word_g2p_dict[g2p_key] = word

        # 結果を新しいJSONファイルに書き込む
        with open(output_dict_file, 'w', encoding='utf-8') as f:
            json.dump(word_g2p_dict, f, indent=4, ensure_ascii=False)

    @staticmethod
    def _is_vowel(char: str) -> bool:
        """文字が母音かどうかを判定"""
        return char.lower() in 'aeiou'


if __name__ == '__main__':
    GenerateJsonDataClass().generate_metaphone_keys('./registered_json/word_register.json', './generated_json/word_metaphone_dict.json')
    GenerateJsonDataClass().generate_g2p_list_and_dict('./registered_json/word_register.json', './generated_json/word_g2p_dict.json')
