import re

class SentenceFormatter:
    def __init__(self):
        pass

    def format_sentence(self, text):
        """
        文章のフォーマットを行います。

        Args:
        - text (str): フォーマットする文章

        Returns:
        - str: フォーマットされた文章
        """
        # 不要な記号を削除
        text = text.replace(',', '').replace('.', '').replace("'", "").replace('"', '')

        # ハイフンをスペースに置換
        text = text.replace('-', ' ')

        # 数字と数字が連続している場合のスペースを削除する正規表現パターン
        pattern = re.compile(r'(\d+)\s+(\d+)')

        # パターンにマッチする箇所を探し、間のスペースを削除する
        modified_text = re.sub(pattern, r'\1\2', text)

        # もし修正されたテキストにパターンにマッチする部分があれば再度関数を呼び出す
        if modified_text != text:
            return self.format_sentence(modified_text)
        else:
            return modified_text

        
    def word_combination_formatter(self, sentence: str) -> list[str, str]:
        """
        整形済みの文章を受け取り、奇数番目と偶数番目に分けて連続する単語を接続して返す

        Parameter
        ---
            sentence: str
                整形済みの文章

        Returne
        ---
            even_word_sentence: str
                偶数番目の単語とその次の単語を接続した文章を返す。ただし偶数番目が数字の場合は数字だけを追加し、偶数番目の次の単語が数字の場合は接合せずに2つの単語を並べて返す

            odd_word_sentence: str
                奇数番目の単語とその次の単語を接続した文章を返す。ただし奇数番目が数字の場合は数字だけを追加し、奇数番目の次の単語が数字の場合は接合せずに2つの単語を並べて返す
        """
        word_list = sentence.split()
        even_word_sentence = []
        odd_word_sentence = []

        for i in range(len(word_list)-1):
            current_word = word_list[i]
            next_word = word_list[i+1]

            if i % 2 == 0:
                if next_word.isdigit():
                    even_word_sentence.extend([current_word, next_word])
                elif current_word.isdigit():
                    even_word_sentence.append(current_word)
                else:
                    even_word_sentence.append(current_word + next_word)
            else:
                if next_word.isdigit():
                    odd_word_sentence.extend([current_word, next_word])
                elif current_word.isdigit():
                    odd_word_sentence.append(current_word)
                else:
                    odd_word_sentence.append(current_word + next_word)

        even_word_sentence = ' '.join(even_word_sentence)
        odd_word_sentence = ' '.join(odd_word_sentence)

        return [even_word_sentence, odd_word_sentence]


if __name__ == "__main__":
    # クラスのインスタンス化
    formatter = SentenceFormatter()

    # テスト用の文章
    sample_text = "Morning phone 133 Hold position Traffic from final approach"

    # テキストのフォーマット
    formatted_text = formatter.format_sentence(sample_text)

    # フォーマットされたテキストの表示
    print("Formatted text:", formatted_text)

    print(SentenceFormatter().word_combination_formatter(sample_text))
