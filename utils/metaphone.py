from doublemetaphone import doublemetaphone

class MetaphoneClass:
    def generate_metaphone_key_list(self, sentence: str) -> list[str]:
        """
        Generate a list of words with their Metaphone keys for the given sentence.

        Parameters
        ----------
        sentence : str
            The sentence to be processed.

        Returns
        -------
        list
            A list containing the Metaphone keys of words in the sentence.
            For numeric words, the original word is returned.
        """
        word_list = sentence.split()
        word_metaphone_key_list = []

        for word in word_list:
            if word.isdigit():
                word_metaphone_key_list.append(word)
            else:
                word_metaphone_key_list.append([doublemetaphone(word)[0], word])

        return word_metaphone_key_list
    
if __name__ == '__main__':
    print(MetaphoneClass().generate_metaphone_key_list("amaxia"))
    print(MetaphoneClass().generate_metaphone_key_list("amakusa air"))
    print(MetaphoneClass().generate_metaphone_key_list("amakusaair"))
    print(MetaphoneClass().generate_metaphone_key_list("amakuser"))

    # [['AMKS', 'amaxia']]
    # [['AMKS', 'amakusa'], ['AR', 'air']]
    # [['AMKSR', 'amakusaair']]
    # [['AMKSR', 'amakuser']]