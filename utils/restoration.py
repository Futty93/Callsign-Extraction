import json
import os
import json

# スクリプトのディレクトリを基準にしてtranscript.jsonのパスを設定
script_dir = os.path.dirname(os.path.abspath(__file__))

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

        word_type_dict_path = os.path.join(script_dir, f'../generated_json/word_{type}_dict.json')
        with open(word_type_dict_path, 'r', encoding='utf-8') as f:
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

    def restoration_callsign(self, word_list: list) -> str:
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
        # Load the airline code dictionary from a JSON file
        airline_code_dict_path = os.path.join(script_dir, '../registered_json/airline_code_dict.json')
        with open(airline_code_dict_path, 'r', encoding='utf-8') as file:
            airline_codes = json.load(file)

        restored_sentence = []
        index = 0

        while index < len(word_list) - 1:
            # Get current and next words
            current_word = self.get_first_element(word_list[index])
            next_word = self.get_first_element(word_list[index + 1])
            combined_word = f"{current_word} {next_word}"

            if current_word in airline_codes:
                if index + 1 < len(word_list) and word_list[index + 1][0].isdigit():
                    # Replace current word with code if followed by a number
                    restored_sentence.append(airline_codes[current_word])
                else:
                    # Append the original word if not followed by a number
                    restored_sentence.append(self.get_second_element(word_list[index]))
                index += 1
            elif combined_word in airline_codes:
                if index + 2 < len(word_list) and word_list[index + 2][0].isdigit():
                    # Replace combined word with code if followed by a number
                    restored_sentence.append(airline_codes[combined_word])
                    index += 2
                else:
                    # Append the original word if not followed by a number
                    restored_sentence.append(self.get_second_element(word_list[index]))
                    index += 1
            else:
                # Append the original word if no match in dictionary
                restored_sentence.append(self.get_second_element(word_list[index]))
                index += 1

        # Handle the last word
        if index == len(word_list) - 1:
            restored_sentence.append(self.get_second_element(word_list[index]))

        return ' '.join(restored_sentence)
