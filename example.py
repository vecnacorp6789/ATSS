from atss import *

atss_conf.defaults["ru"] = "ruwords.txt"
atss_conf.defaults["min_length"] = 1

a = ATSS(input_file="tests/data/ru-pikalka.txt")
words = a.ex_words['Первые буквы строк']['text'].split()
# a = ATSS(input_file="tests/data/ru-pikalka-r.txt", wordlist="ruwords.txt", lang="ru", min_length=1)
for w in words:
    if len(w) >= 5:
        print(w)

"""
Example usage of this program, this code extracts the hidden nazi message.
"""
