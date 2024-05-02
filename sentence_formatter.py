import re

class SentenceFormatter:
    def insert_space_before_number(self, word: str) -> str:
        """
        Insert a space before the first digit in the given word.
        数字の前にスペースを挿入する。

        Parameters
        ----------
        word : str
            The word to be processed.

        Returns
        -------
        str
            The processed word with a space inserted before the first digit.
        """
        if word.isdigit():
            return word

        result = ''
        digit_found = False
        for char in word:
            if char.isdigit() and not digit_found:
                result += ' ' + char
                digit_found = True
            else:
                result += char
        return result

    def extract_number(self, word: str) -> str:
        """
        Extract the leading numeric part from the given word.
        与えられた単語から先頭の数字部分を抽出する。

        Parameters
        ----------
        word : str
            The word to be processed.

        Returns
        -------
        str
            The leading numeric part of the word, or the original word if it doesn't start with a digit.
        """
        # 最初の文字が数字であるかどうかをチェック
        if word and not word[0].isdigit():
            return word

        return ''.join([char for char in word if char.isdigit()])

    def format_sentence(self, text: str) -> str:
        """
        Format the given text by removing unwanted characters, replacing hyphens with spaces,
        and separating words and numbers.
        入力された文章から , . ' " を削除し、- を半角スペースに置換し、数字と数字が連続している場合のスペースを削除する。

        Parameters
        ----------
        text : str
            The text to be formatted.

        Returns
        -------
        str
            The formatted text.
        """
        # 不要な記号を削除
        text = text.replace(',', '').replace('.', '').replace("'", "").replace('"', '')

        # ハイフンをスペースに置換
        text = text.replace('-', ' ')

        # 数字と数字が連続している場合のスペースを削除する正規表現パターン
        pattern = re.compile(r'(\d+)\s+(\d+)')

        # パターンにマッチする箇所を探し、間のスペースを削除する
        modified_text = re.sub(pattern, r'\1\2', text)

        modified_text_list = modified_text.split()

        # 単語と数字が1つのまとまりとして文字起こしされた場合に、単語と数字を分割する
        for i in range(len(modified_text_list)):
            modified_text_list[i] = self.extract_number(modified_text_list[i])
            modified_text_list[i] = self.insert_space_before_number(modified_text_list[i])
        
        modified_text = ' '.join(modified_text_list)

        # もし修正されたテキストにパターンにマッチする部分があれば再度関数を呼び出す
        if modified_text != text:
            return self.format_sentence(modified_text)
        else:
            return modified_text

    def word_combination_formatter(self, sentence: str) -> list[str, str]:
        """
        Format the given sentence by combining consecutive words, except for numbers.

        Parameters
        ----------
        sentence : str
            The sentence to be formatted.

        Returns
        -------
        list
            A list containing two strings:
                - The first string is the sentence with even-indexed words combined.
                - The second string is the sentence with odd-indexed words combined.
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

def format_sentence(text: str) -> str:
    """
    Wrapper function to call the format_sentence method from the SentenceFormatter class.
    """
    formatter = SentenceFormatter()
    return formatter.format_sentence(text)

def word_combination_formatter(sentence: str) -> list[str, str]:
    """
    Wrapper function to call the word_combination_formatter method from the SentenceFormatter class.
    """
    formatter = SentenceFormatter()
    return formatter.word_combination_formatter(sentence)