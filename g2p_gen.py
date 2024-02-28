from g2p_en import G2p

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
        word_g2p: list[str]
            文章の単語ごとにg2pに変換し、リストを返す
        """
        word_list = sentence.split()
        g2p_word_list = []
        
        for word in word_list:
            if word.isdigit():
                g2p_word_list.append(word)
            else:
                g2p_word_list.append(self.generate_g2p(word))

        return g2p_word_list

print(G2PClass().generate_g2p_list("I refuse to collect the refuse around her"))