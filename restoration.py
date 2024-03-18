import json

class Restoration:
    def restoration_sentence(self, word_list: list, type: str) -> list:
        """
        A function that returns a sentence that has been replaced with the closest word in the key state to the word corresponding to the key.

        Parameters
        ----------
        word_list : list
            A list of words, where replaced words are represented as lists [replaced_word_key, original_word].
        type : str
            The type of processing used ("g2p" or "metaphone").

        Returns
        -------
        list
            A list containing the restored words.
        """
        restored_sentence = []

        with open(f'generated_json/word_{type}_dict.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for word in word_list:
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
        Get the first element of a list, or return the original string if it's not a list.

        Parameters
        ----------
        word_list : list or str
            A list or a string.

        Returns
        -------
        str
            The first element of the list, or the original string if it's not a list.
        """
        if isinstance(word_list, list):
            return word_list[0]
        else:
            return word_list

    def get_second_element(self, word_list) -> str:
        """
        Get the second element of a list, or return the original string if it's not a list.

        Parameters
        ----------
        word_list : list or str
            A list or a string.

        Returns
        -------
        str
            The second element of the list, or the original string if it's not a list.
        """
        if isinstance(word_list, list):
            return word_list[1]
        else:
            return word_list

    def restoration_callSign(self, word_list: list) -> str:
        """
        Restore callsigns in the given word list by replacing them with 3-letter codes.

        Parameters
        ----------
        word_list : list
            A list of words, where replaced words are represented as lists [replaced_word, original_word].

        Returns
        -------
        str
            The sentence with callsigns replaced by 3-letter codes.
        """
        with open('registered_json/airline_code_dict.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        restored_sentence = []

        i: int = 0
        while i < len(word_list) - 1:
            word = self.get_first_element(word_list[i])
            next_word = self.get_first_element(word_list[i + 1])
            joined_word = word + " " + next_word

            if word in data:
                if i + 1 < len(word_list) and word_list[i + 1][0].isdigit():
                    restored_sentence.append(data[word])
                else:
                    restored_sentence.append(self.get_second_element(word_list[i]))
                i += 1
            elif joined_word in data:
                if i + 2 < len(word_list) and word_list[i + 2][0].isdigit():
                    restored_sentence.append(data[joined_word])
                    i += 2
                else:
                    restored_sentence.append(self.get_second_element(word_list[i]))
                    i += 1
            else:
                restored_sentence.append(self.get_second_element(word_list[i]))
                i += 1

        restored_sentence.append(self.get_second_element(word_list[len(word_list) - 1]))

        restored_sentence = ' '.join(restored_sentence)

        return restored_sentence