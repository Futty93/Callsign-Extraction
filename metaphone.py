from doublemetaphone import doublemetaphone

def get_metaphone_key(sentence):
    metaphone_keys = []
    words = sentence.split()
    for word in words:
        if word.isdigit():
            metaphone_keys.append(word)
        else:
            metaphone_key = doublemetaphone(word)[0]
            # metaphone_key = metaphone_key.decode()
            metaphone_keys.append(metaphone_key)
    return metaphone_keys
