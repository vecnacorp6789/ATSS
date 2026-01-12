## Setup
``` bash
pip install atss
```

## Use (python script)
``` python
from atss import ATSS, atss_conf

# Global
atss_conf.defaults["ru"] = "ruwords.txt" #<- словарь для русского языка
atss_conf.defaults["en"] = "enwords.txt" #<- словарь для русского языка
atss_conf.defaults["min_length"] = 1

a = ATSS(input_file="letter.txt", wordlist="ruwords.txt", lang="ru", min_length=1)

print(a.ex_words)
```

## Use (CLI)
``` bash
atss -in "letter.txt" -wl "russian_words.txt"
```
Режимы работы
```
-in <file>	Анализ одного текстового файла (.txt).
-d <dir>	Пакетный анализ всех .txt файлов в указанной директории.
```

Настройки
```
-wl <path>	Путь к файлу словаря (список слов, разделенных переносом строки). По умолчанию None
-ml <int>	Min Length. Минимальная длина слова для валидации. По умолчанию 5
--lang <str>	Язык анализа: ru или en. По умолчанию ru
-o <file>	Путь к выходному файлу (обязательно для --refactor).
--json	Вывод результата в формате JSON вместо текстового отчета.
```

Russian 1.5M wordlist -> https://github.com/danakt/russian-words
