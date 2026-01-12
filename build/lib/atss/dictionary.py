# atss/dictionary.py
import os

class DictionaryChecker:
    def __init__(self, dictionary_path=None, lang="ru", min_length=5):
        self.words = set()
        self.lang = lang
        self.min_length = min_length  # Сохраняем параметр
        
        # Загружаем словарь с учетом фильтра длины
        self.load_dictionary(dictionary_path)

    def load_dictionary(self, path):
        """Загружает словарь. Игнорирует слова короче self.min_length."""
        loaded_from_file = False
        
        if path and os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    for line in f:
                        word = line.strip().lower()
                        # ФИЛЬТР: только слова >= min_length
                        if len(word) >= self.min_length: 
                            self.words.add(word)
                loaded_from_file = True
            except Exception as e:
                print(f"[ATSS] Ошибка чтения словаря: {e}")

        #встроенные словари
        if not loaded_from_file or not self.words:
            raw_words = set()
            if self.lang == "en":
                raw_words = {
                    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
                    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
                    "this", "but", "his", "by", "from", "bird", "cage", "fly", "sky",
                    "freedom", "eagle", "fate", "garden", "secret", "code", "hidden",
                    "message", "steganography", "agent", "spy", "system", "data",
                    "tree", "water", "river", "moon", "sun", "stars", "night", "day",
                    "help", "sos", "save", "me", "danger", "look", "first", "last"
                }
            else:
                raw_words = {
                    "птичка", "клетке", "птичку", "воле", "саду", "орёл", "судьбе",
                    "в", "на", "с", "по", "из", 
                    "лит", "хабаровск", "стеганография",
                    "лицей", "храм", "науки", "добра", "интеллект",
                    "технологий", "будущего", "светлые", "умы",
                    "базы", "данных", "код", "охрана", "вирусов",
                    "системы", "каждый", "бит", "сокрытие", "тайны",
                    "единый", "глубоко", "алгоритмы", "научились",
                    "агент", "шпион",
                    "лес", "шумел", "ивы", "вода", "трава",
                    "ворона", "будет", "три", "пруду",
                    "золотистые", "привет"
                }
            
            #фильтр ml
            for w in raw_words:
                if len(w) >= self.min_length:
                    self.words.add(w)

    def calculate_score_and_segment(self, text):
        """
        Жадный алгоритм поиска слов
        ret (score, readable_text)
        """
        if not text:
            return 0.0, ""

        clean_text = text.lower()
        n = len(clean_text)
        if n == 0:
            return 0.0, ""

        recognized_chars = 0
        result_segments = []
        i = 0
        
        while i < n:
            found_word = None
            max_len = min(25, n - i)
            
            #ищем свлов с длины ml
            for length in range(max_len, 1, -1):
                sub = clean_text[i : i + length]
                if sub in self.words:
                    found_word = sub
                    break
            
            if found_word:
                result_segments.append(found_word.upper()) 
                recognized_chars += len(found_word)
                i += len(found_word)
            else:
                result_segments.append(clean_text[i])
                i += 1

        score = recognized_chars / n
        readable_text = " ".join(result_segments)
        return score, readable_text