import json

class Restoration():
    """
    g2pやmetaphoneに置き換えられているものを単語に置き換えるメソッドを保持するクラス
    """

    def __init__(self):
        pass


    def restoration_sentence(self, word_list: list, type: str) -> list:
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
                if word[0] in data:
                    restored_sentence.append([data[word[0]], word[1]])
                else:
                    restored_sentence.append(word[1])
            else:
                restored_sentence.append(word)

        return restored_sentence
    
    def get_first_element(self, word_list) -> str:
        """
        配列の1つを受け取ってそれが配列であれば最初の要素を返し、文字列であればそのまま文字列を返す
        """
        if isinstance(word_list, list):
            return word_list[0]
        else:
            return word_list

    def get_second_element(self, word_list) -> str:
        """
        配列の1つを受け取ってそれが配列であれば2番目の要素を返し、文字列であればそのまま文字列を返す
        """
        if isinstance(word_list, list):
            return word_list[1]
        else:
            return word_list
    
    def restoration_callSign(self, word_list: list) -> str:
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

        restored_sentence = []

        i: int = 0
        while i < len(word_list) - 1:
            word = self.get_first_element(word_list[i])
            next_word = self.get_first_element(word_list[i+1])
            joined_word = word + " " + next_word

            if word in data:    # 1単語で辞書に登録されている部分があれば変換する
                if word_list[i+1][0].isdigit():
                    restored_sentence.append(data[word])
                else:
                    restored_sentence.append(self.get_second_element(word_list[i]))
                i += 1
            elif joined_word in data:   # 連続する2単語で辞書に登録されている場合はまとめて置き換える
                if i + 2 < len(word_list) and word_list[i+2][0].isdigit():
                    restored_sentence.append(data[joined_word])
                    i += 2
                else:
                    restored_sentence.append(self.get_second_element(word_list[i]))
                    i += 1  # i を1回飛ばす
            else:                       # 登録されているものがない場合はそのままのものを返す
                restored_sentence.append(self.get_second_element(word_list[i]))
                i += 1

        restored_sentence.append(self.get_second_element(word_list[len(word_list)-1]))

        restored_sentence = ' '.join(restored_sentence)

        return restored_sentence

    

if __name__ == '__main__':
    word_list = [['AO1L', 'all'], ['NIH2PAA1N', 'phone'], '133', ['AO1L', 'Hold'], 'position', ['AY1BEH0KS', 'Traffic'], 'from', ['NAY1NER0', 'final'], ['PIY1CH', 'approach']]
    sentence = Restoration().restoration_sentence(word_list, "g2p")
    print(sentence)

    print(Restoration().restoration_callSign(sentence))