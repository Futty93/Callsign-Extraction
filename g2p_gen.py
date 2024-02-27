from g2p_en import G2p

def generate_g2p_list(sentence: str):
        """
        """
        g2p = G2p()
        row_list = g2p(sentence)

        g2p_word: str = ""
        g2p_word_list: list[str] = []
        for value in row_list:
            if value == ' ':
                g2p_word_list.append(g2p_word)
                g2p_word = ""
            else:
                g2p_word += value
        
        return g2p_word_list
    

print(generate_g2p_list("popular pets, e.g. cats and dogs"))