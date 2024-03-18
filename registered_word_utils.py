import json
from doublemetaphone import doublemetaphone
from g2p import G2PClass

class GenerateJsonDataClass:
    def __init__(self):
        self.g2p = G2PClass()

    def generate_metaphone_keys(self, input_file: str, output_dict_file: str, output_list_file: str) -> None:
        """
        登録されている単語のリストを受け取り、metaphone_keyだけのリストと、キーがmetaphone_key、バリューが登録された単語となる辞書型のリストを生成します。

        Parameters
        --------------
            input_file: str
                登録されている単語のファイル名
            output_dict_file: str
                生成する辞書型のリストのファイル名
            output_list_file: str
                生成するmetaphone_keyのリストのファイル名

        Returns
        --------------
            None
        """

        # 入力ファイルを読み込む
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # metaphoneキーを計算し、新しい辞書に保存
        word_metaphone_dict = {}
        word_metaphone_key = []
        for word in data:
            metaphone_key = doublemetaphone(word)[0]  # DMetaphone()でメタフォンキーを生成
            metaphone_key = metaphone_key.decode('utf-8') if isinstance(metaphone_key, bytes) else metaphone_key # metaphoneが謎の型で返ってくるのでstrに変換
            word_metaphone_dict[metaphone_key] = word
            word_metaphone_key.append(metaphone_key)

        # 結果を新しいJSONファイルに書き込む
        with open(output_dict_file, 'w', encoding='utf-8') as f:
            json.dump(word_metaphone_dict, f, indent=4, ensure_ascii=False)

        with open(output_list_file, 'w', encoding='utf-8') as f:
            json.dump(word_metaphone_key, f, indent=4, ensure_ascii=False)

    def generate_g2p_list_and_dict(self, input_file: str, output_dict_file: str, output_list_file: str) -> None:
        """
        登録されている単語のリストを受け取り、g2p_keyだけのリストと、キーがg2p_key、バリューが登録された単語となる辞書型のリストを生成します。

        Parameters
        --------------
            input_file: str
                登録されている単語のファイル名
            output_dict_file: str
                生成する辞書型のリストのファイル名
            output_list_file: str
                生成するg2p_keyのリストのファイル名

        Returns
        --------------
            None
        """
        # 入力ファイルを読み込む
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # g2pを計算し、新しい辞書に保存
        word_g2p_dict = {}
        word_g2p_list = []
        for word in data:
            g2p_key = self.g2p.generate_g2p(word)
            word_g2p_dict[g2p_key] = word
            word_g2p_list.append(g2p_key)

        # 結果を新しいJSONファイルに書き込む
        with open(output_dict_file, 'w', encoding='utf-8') as f:
            json.dump(word_g2p_dict, f, indent=4, ensure_ascii=False)

        with open(output_list_file, 'w', encoding='utf-8') as f:
            json.dump(word_g2p_list, f, indent=4, ensure_ascii=False)




if __name__ == '__main__':
    GenerateJsonDataClass().generate_metaphone_keys('./registered_json/word_register.json', './generated_json/word_metaphone_dict.json', './generated_json/word_metaphone_list.json')
    GenerateJsonDataClass().generate_g2p_list_and_dict('./registered_json/word_register.json', './generated_json/word_g2p_dict.json', './generated_json/word_g2p_list.json')
