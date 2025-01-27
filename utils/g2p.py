from g2p_en import G2p
import nltk

nltk.download('averaged_perceptron_tagger_eng')

class G2PClass:
    def __init__(self):
        self.g2p = G2p()

    def generate_g2p(self, word: str) -> str:
        """
        Generate the grapheme-to-phoneme (G2P) representation of a given word.

        Parameters
        ----------
        word : str
            The word to be converted to G2P.

        Returns
        -------
        str
            The G2P representation of the word.
        """
        pre_g2p = self.g2p(word)
        word_g2p: str = "".join(pre_g2p)
        return word_g2p

    def generate_g2p_list(self, sentence: str) -> list[str]:
        """
        Generate a list of words with their G2P representations for the given sentence.

        Parameters
        ----------
        sentence : str
            The sentence to be processed.

        Returns
        -------
        list
            A list containing the G2P representations of words in the sentence.
            For numeric words, the original word is returned.
        """
        word_list = sentence.split()
        word_g2p_list = []

        for word in word_list:
            if word.isdigit():
                word_g2p_list.append(word)
            else:
                word_g2p_list.append([self.generate_g2p(word), word])

        return word_g2p_list

if __name__ == '__main__':
    print(G2PClass().generate_g2p_list("Ski work 113, combat~"))
    print(G2PClass().generate_g2p_list("amakusa air"))
    print(G2PClass().generate_g2p_list("amakusaair"))
    print(G2PClass().generate_g2p_list("AMKSAR"))

    # [['AH0MAE1KSIY0AH0', 'amaxia']]
    # [['AA0MAA0KUW1SAH0', 'amakusa'], ['EH1R', 'air']]
    # [['AE2MAH0KAH0WEH1SKIY0', 'amakusaair']]
    # [['AE1MAH0KAH2SKER0', 'amakuser']]