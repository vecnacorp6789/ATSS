from atss import *

a = ATSS(input_file="tests/data/zaklinatel.txt", wordlist="ruwords.txt", threshold=0)
words = a.ex_words['Первые буквы предложений']['text'].split()

for w in words:
    if len(w) >= 5:
        print(w)
        
print(a.ex_words)