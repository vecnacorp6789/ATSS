#atss/strategies.py
import re

class StegoAnalyzer:
    def __init__(self):
        self.strategies = [
            #База
            ("Первые буквы строк", self.get_first_letters),
            ("Последние буквы строк", self.get_last_letters),
            ("Первые буквы предложений", self.get_first_letters_sentences_strict),
            
            #Начало и конец
            #("Первые буквы (Начало - 50 строк)", self.get_first_letters_head),
            #("Первые буквы (Конец - 50 строк)", self.get_first_letters_tail),
            
            # мезостих
            ("Вторые буквы строк", self.get_second_letters_clean),
            ("Третьи буквы строк", self.get_third_letters_clean),
            ("Первые буквы ВТОРОГО слова", self.get_first_letters_second_word),
            ("Края строк (1-я + Последняя)", self.get_first_and_last_combined),
            #diagoinal
            ("Диагональ (Слева -> Направо)", self.get_diagonal_ltr),
            ("Диагональ (Справа -> Налево)", self.get_diagonal_rtl),
        ]

    def prepare_lines(self, text):
        if not text:
            return []
        return [line.strip() for line in text.split('\n') if line.strip()]

    def analyze(self, text):
        lines = self.prepare_lines(text)
        results = {}
        if not text:
            return results

        for name, strategy_func in self.strategies:
            try:
                if strategy_func == self.get_first_letters_sentences_strict:
                    candidate = strategy_func(text)
                else:
                    candidate = strategy_func(lines)
                
                candidate_clean = re.sub(r'[^а-яА-Яa-zA-Z]', '', candidate)
                
                if len(candidate_clean) > 2:
                    results[name] = candidate_clean
            except Exception:
                continue
        return results

    # Методы

    def get_diagonal_ltr(self, lines):
        res = []
        for i, line in enumerate(lines):
            clean = re.sub(r'[^а-яА-Яa-zA-Z]', '', line)
            if len(clean) > i:
                res.append(clean[i])
        return "".join(res)

    def get_diagonal_rtl(self, lines):
        res = []
        for i, line in enumerate(lines):
            clean = re.sub(r'[^а-яА-Яa-zA-Z]', '', line)
            idx = -(i + 1)
            if len(clean) >= abs(idx):
                res.append(clean[idx])
        return "".join(res)

    def get_first_letters_head(self, lines):
        limit = 50
        subset = lines[:limit]
        return self.get_first_letters(subset)

    def get_first_letters_tail(self, lines):
        limit = 50
        if len(lines) < limit:
            return self.get_first_letters(lines)
        subset = lines[-limit:]
        return self.get_first_letters(subset)

    def get_first_letters_sentences_strict(self, text):
        one_line = text.replace('\n', ' ')
        sentences = re.split(r'(?<=[.!?])\s+', one_line)
        res = []
        for s in sentences:
            match = re.search(r'[а-яА-Яa-zA-Z]', s.strip())
            if match: res.append(match.group(0))
        return "".join(res)

    def get_first_letters(self, lines):
        res = []
        for line in lines:
            clean = re.sub(r'[^а-яА-Яa-zA-Z]', '', line)
            if clean: res.append(clean[0])
        return "".join(res)

    def get_last_letters(self, lines):
        res = []
        for line in lines:
            clean = re.sub(r'[^а-яА-Яa-zA-Z]', '', line)
            if clean: res.append(clean[-1])
        return "".join(res)

    def get_first_and_last_combined(self, lines):
        res = []
        for line in lines:
            clean = re.sub(r'[^а-яА-Яa-zA-Z]', '', line)
            if len(clean) >= 2: res.append(clean[0] + clean[-1])
            elif len(clean) == 1: res.append(clean[0])
        return "".join(res)

    def get_second_letters_clean(self, lines):
        res = []
        for line in lines:
            clean = re.sub(r'[^а-яА-Яa-zA-Z]', '', line)
            if len(clean) >= 2: res.append(clean[1])
        return "".join(res)

    def get_third_letters_clean(self, lines):
        res = []
        for line in lines:
            clean = re.sub(r'[^а-яА-Яa-zA-Z]', '', line)
            if len(clean) >= 3:
                res.append(clean[2])
        return "".join(res)

    def get_first_letters_second_word(self, lines):
        res = []
        for line in lines:
            words = line.split()
            if len(words) >= 2:
                word = re.sub(r'[^а-яА-Яa-zA-Z]', '', words[1])
                if word: res.append(word[0])
        return "".join(res)