import json

class Restoration():
    """
    g2pやmetaphoneに置き換えられているものを単語に置き換えるメソッドを保持するクラス
    """

    def restoration_sentence(word_list: list, type: str) -> str:
        """
        Parameters
        ---
            word_list: list[str]
                変換された文章の単語ごとの配列。置き換えられている単語は配列となっている。

            type: str
                g2pなのかmetaphoneなのかを指定する。
        
        Returns
        ---
            restored_sentence: str
                復元した単語を文章として返す
        """

        restored_sentence = []

        with open(f'./generated_json/word_{type}_dict.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for word in word_list:
            # もしwordがlistだったら辞書を利用して元の単語に置き換える
            if isinstance(word, list):
                restored_sentence.append((data[word[0]]))
            else:
                restored_sentence.append(word)

        restored_sentence = ' '.join(restored_sentence)

        return restored_sentence
    
    def restoration_callSign(sentence: str) -> str:
        """
        登録された単語に戻した文章を受け取り、その中にコールサインとして登録されている部分があれば3レターコードに置き換える関数

        Parameters
        ---
            sentence: str
                登録さてれている単語に復元した文章

        Returns
        ---
            restored_sentence: str
                コールサインに置き換えた文章
        """

        with open(f'./registered_json/airline_code_dict.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        word_list: list = sentence.split()

        restored_sentence = []

        i: int = 0
        while i < len(word_list) - 1:
            joined_word = word_list[i] + " " + word_list[i + 1]
            if word_list[i] in data:    # 1単語で辞書に登録されている部分があれば変換する
                restored_sentence.append(data[word_list[i]])
                i += 1
            elif joined_word in data:   # 連続する2単語で辞書に登録されている場合はまとめて置き換える
                restored_sentence.append(data[joined_word])
                i += 2  # i を1回飛ばす
            else:                       # 登録されているものがない場合はそのままのものを返す
                restored_sentence.append(word_list[i])
                i += 1


        restored_sentence = ' '.join(restored_sentence)

        return restored_sentence

    

if __name__ == '__main__':
    word_list = [['AO1L NIH2PAA1N', 8], '567', 'KWAA1', 'SUW1LAH0N', 'WEY1', 'TWEH1NTIY0FWEH1LT', ['NAY1NER0', 7], ['AH0ND', 4], ['AO1L', 2], 'DHAH0', ['NAY1NER0', 4], ['AO1L', 3]]
    sentence = Restoration.restoration_sentence(word_list, "g2p")
    print(sentence)

    print(Restoration.restoration_callSign(sentence))