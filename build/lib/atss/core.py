# atss/core.py
import os
import codecs
from .dictionary import DictionaryChecker
from .strategies import StegoAnalyzer

class Config:
    def __init__(self):
        self.defaults = {
            "ru": "russian_words.txt",
            "en": "english_words.txt",
            "min_length": 5
        }

atss_conf = Config()

class ATSS:
    def __init__(self, input_file=None, text=None, wordlist=None, lang="ru", threshold=0.3, min_length=None):
        self.lang = lang
        self.min_length = min_length if min_length is not None else atss_conf.defaults.get("min_length", 5)

        #словарь
        if wordlist:
            wl_path = wordlist
        else:
            wl_path = atss_conf.defaults[lang]
        
        #передача файла в чекер
        self.checker = DictionaryChecker(dictionary_path=wl_path, lang=self.lang, min_length=self.min_length)
        self.analyzer = StegoAnalyzer()
        self.threshold = threshold
        
        self.raw_text = ""
        self.ex_words = {} 

        if input_file:
            self._load_from_file(input_file)
        elif text:
            self.raw_text = text
        
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
            ("ROT13", lambda s: codecs.encode(s, 'rot_13')) if (self.lang == "en") else None
        ]

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