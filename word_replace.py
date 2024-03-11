import json
from Levenshtein import distance
from g2p_metaphone_gen import G2PClass, MetaphoneClass

class WordReplaceClass:
    def replace_words_spell(sentence: str) -> list:
        """
        与えられた整形済みの文章を単語ごとに区切り、スペルを元に距離を計算し
        登録されている近い単語に置き換える。

        Parameters
        ---
            sentence: str
                コンマなどを取り除いた整形済みの文章

        Returns
        ---
            replaced_word: list[srt]
                単語を置き換えた場合は[置き換えた単語, 距離]の配列を返す
                単語の距離が一定以上ある場合は単語をそのまま返す
        """
        word_list: list[str] = sentence.split()

        # JSONファイルから単語を読み込む
        with open('./registered_json/word_register.json', 'r') as f:
            register_word_list = json.load(f)

        replaced_words: list[str] = []

        # 各単語に対してループを実行し、最も近い単語に置き換える
        for word in word_list:
            if word.isdigit():
                replaced_words.append(word)
                continue
            min_distance = float('inf')
            closest_word = word

            # 単語のメタフォンキーに対応する単語との距離を計算し、最小距離を見つける
            for register_word in register_word_list:
                d = distance(word, register_word)
                if d < min_distance:
                    min_distance = d
                    closest_word = register_word

            if len(word)*2/3 > min_distance:
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

            if len(word[0])*2/3 > min_distance:
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

            if len(word[0])*2/3 > min_distance:
                replaced_words.append([closest_word, word[1]])
            else:
                replaced_words.append(word[1])

        return replaced_words


if __name__ == '__main__':
    sentence: str = "Morningphone 133 positionTraffic fromfinal"
    # print(WordReplaceClass.replace_words_spell(sentence))
    # print(WordReplaceClass.replace_words_g2p(G2PClass().generate_g2p_list(sentence)))
    # print(WordReplaceClass.replace_words_metaphone(MetaphoneClass().generate_metaphone_key_list(sentence)))
    
    print(WordReplaceClass.replace_words_g2p([["JHAH0PAE1NYAH0", "japania"]]))