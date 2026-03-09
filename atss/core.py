# atss/core.py
import os
import codecs
from .dictionary import DictionaryChecker
from .strategies import StegoAnalyzer
import string
from typing import Optional


ALPHABETS = {
    "en": string.ascii_uppercase,
    "ru": "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
}

class Config:
    def __init__(self):
        self.defaults = {
            "ru": "russian_words.txt",
            "en": "english_words.txt",
            "min_length": 5
        }

atss_conf = Config()

class ATSS:
    def __init__(self,
             input_file=None,
             directory=None,
             wordlist=None,
             lang="ru",
             min_length=5,
             threshold=0,
             json=False,
             caesar=False,
             caesar_lang=None,
             **kwargs):

        self.input_file = input_file
        self.directory = directory
        self.wordlist = wordlist
        self.lang = lang.lower()
        self.min_length = min_length
        self.threshold = threshold
        self.json = json
        self.caesar = caesar
        self.caesar_lang = self.lang

        if self.caesar and not self.caesar_lang:
            raise ValueError("--caesar требует lang en или ru")
        

        #словарь
        if wordlist:
            wl_path = wordlist
        else:
            wl_path = atss_conf.defaults[lang]
        
        self.lang = lang.lower()
        self.caesar = caesar
        self.caesar_lang = caesar_lang

        if self.caesar and self.caesar_lang not in ("en", "ru"):
            raise ValueError("При caesar=True обязательно указывать lang='en' или 'ru'")

        #передача файла в чекер
        self.checker = DictionaryChecker(dictionary_path=wl_path, lang=self.lang, min_length=self.min_length)
        self.analyzer = StegoAnalyzer()
        self.threshold = threshold
        
        self.raw_text = ""
        self.ex_words = {} 

        if input_file:
            self._load_from_file(input_file)
        
        if self.raw_text:
            self._run_analysis()

    def _load_from_file(self, path):
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                self.raw_text = f.read()
        else:
            print(f"[ATSS] Файл '{path}' не найден.")

    def _run_analysis(self):
        candidates = self.analyzer.analyze(self.raw_text)
        
        transforms = [
            ("Plain", lambda s: s),
        ]
        #CAESAR
        if self.caesar:
            cl = self.caesar_lang
            alphabet = ALPHABETS.get(cl.lower())
            if alphabet:
                alpha_len = len(alphabet)
                for shift in range(1, alpha_len):
                    t_name = f"Caesar-{cl.upper()}-shift-{shift}"
                    transforms.append((
                        t_name,
                        lambda s, sh=shift, lg=cl: self._caesar_decrypt(s, sh, lg)
                    ))

        for method, raw_string in candidates.items():
            for t_name, t_func in transforms:
                processed_string = t_func(raw_string)
                score, segmented = self.checker.calculate_score_and_segment(processed_string)
                
                key_method = method if t_name == "Plain" else f"{method} [{t_name}]"

                if score > self.threshold:
                    self.ex_words[key_method] = {
                        "text": segmented,
                        "raw": processed_string,
                        "score": round(score, 4),
                        "transformation": t_name,
                        "original_method": method
                    }

        transforms = [t for t in transforms if t is not None]

        for method, raw_string in candidates.items():
            for t_name, t_func in transforms:
                processed_string = t_func(raw_string)
                score, segmented = self.checker.calculate_score_and_segment(processed_string)
                
                key_method = method if t_name == "Plain" else f"{method} [{t_name}]"

                if score > self.threshold:
                    self.ex_words[key_method] = {
                        "text": segmented,
                        "raw": processed_string,
                        "score": round(score, 4),
                        "transformation": t_name,
                        "original_method": method
                    }
    def _caesar_decrypt(self, text: str, shift: int, lang: str) -> str:
        """Расшифровка Цезаря с сохранением регистра и не-букв"""
        alphabet = ALPHABETS.get(lang.lower())
        if not alphabet:
            return text

        result = []
        alpha_len = len(alphabet)

        for char in text:
            upper = char.upper()
            if upper in alphabet:
                idx = alphabet.index(upper)
                new_idx = (idx - shift) % alpha_len
                new_char = alphabet[new_idx]
                result.append(new_char if char.isupper() else new_char.lower())
            else:
                result.append(char)
        return "".join(result)
