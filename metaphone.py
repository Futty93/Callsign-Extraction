import sys
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


def main(argv):
    testwords = ["There", "Their", "They're", "George", "Sally", "week", "weak", "phil", "fill", "Smith", "Schmidt", "morning phone", "morningphone", "two", "too", "tea"]
    for testword in testwords:
        print (testword + " - ", end="")
        print (doublemetaphone(testword))
    return 0

main(sys.argv[1:])