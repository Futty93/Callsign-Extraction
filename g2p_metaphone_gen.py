from g2p_en import G2p
from doublemetaphone import doublemetaphone

class G2PClass:
    def __init__(self):
        self.g2p = G2p()

    def generate_g2p(self, word: str) -> str:
        """
        Parameters
        ----------
        word : str
            g2pを生成する単語を引数とする

        Return
        ----------
        word_g2p: str
            受け取った単語のg2pを1つに結合して返す
        """
        pre_g2p = self.g2p(word)

        word_g2p: str = ""
        for value in pre_g2p:
            word_g2p += value
        
        return word_g2p
    
    def generate_g2p_list(self, sentence: str) -> list[str]:
        """
        Parameters
        ----------
        sentence : str
            コンマなどを取り除いた整形済みの文章を引数とする

        Return
        ----------
        word_g2p_list: list[str]
            文章の単語ごとにg2pに変換し、リストを返す
        """
        word_list = sentence.split()
        word_g2p_list = []
        
        for word in word_list:
            if word.isdigit():
                word_g2p_list.append(word)
            else:
                word_g2p_list.append(self.generate_g2p(word))

        return word_g2p_list
    
class MetaphoneClass:

    def generate_metaphone_key_list(self, sentence: str):
        """
        Parameters
        ----------
        sentence : str
            コンマなどを取り除いた整形済みの文章を引数とする

        Return
        ----------
        word_metaphone_key_list: list[str]
            文章の単語ごとにmetaphone keyに変換し、リストを返す
        """
        word_list = sentence.split()
        word_metaphone_key_list = []

        for word in word_list:
            if word.isdigit():
                word_metaphone_key_list.append(word)
            else:
                word_metaphone_key_list.append(doublemetaphone(word)[0])

        return word_metaphone_key_list


if __name__ == '__main__':
    sentence: str = "Borneepong 567 Kwa Sulan Way 24L contact ground on the other side"
    print(G2PClass().generate_g2p_list(sentence))
    print(MetaphoneClass().generate_metaphone_key_list(sentence))