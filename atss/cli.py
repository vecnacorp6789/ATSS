# atss/cli.py
import argparse
import os
import sys
import json
from .core import ATSS, atss_conf 


def process_file(filepath, args):
    if not os.path.exists(filepath):
        print(f"[ATSS] Файл '{filepath}' не найден.", file=sys.stderr)
        return None

    try:
        app = ATSS(
            input_file=filepath, 
            wordlist=args.wordlist, 
            lang=args.lang,
            min_length=args.min_length,
            threshold=args.threshold,
        )
        return app
    except Exception as e:
        print(f"[ATSS] Ошибка при обработке '{filepath}': {e}", file=sys.stderr)
        return None

def print_text_report(filepath, app):
    print(f"\n=== Файл: {filepath} ===")
    
    if not app or not app.ex_words:
        print("  -> Скрытых сообщений не обнаружено.")
    else:
        sorted_items = sorted(app.ex_words.items(), key=lambda x: x[1]['score'], reverse=True)
        print(f"  {'МЕТОД / ТРАНСФОРМАЦИЯ':<40} | {'SCORE':<6} | {'ТЕКСТ'}")
        print("  " + "-" * 88)
        
        for method_key, data in sorted_items:
            text = data['text']
            score = data['score']
            display_text = (text[:40] + '...') if len(text) > 40 else text
            print(f"  {method_key:<40} | {score:<6} | {display_text}")
    print("-" * 90)

def main():
    parser = argparse.ArgumentParser(description="ATSS: AcroText Steganography Solver")
    
    # --- Mutually Exclusive Group (Main Modes) ---
    group = parser.add_mutually_exclusive_group(required=True)
    
    #файл
    group.add_argument("-in", "--input", dest="input_file",
                        help="Путь к одному входному файлу (.txt) для анализа")
    
    #директория
    group.add_argument("-d", "--directory", dest="directory",
                        help="Путь к директории с файлами для пакетного анализа")

    #options
    parser.add_argument("-wl", "--wordlist", dest="wordlist", default=None,
                        help="Путь к файлу словаря")
    parser.add_argument("--lang", dest="lang", default="ru", choices=["ru", "en"],
                        help="Язык анализа: 'ru' или 'en' (default: ru)")
    
    parser.add_argument("-ml", "--min-length", dest="min_length", type=int, default=5,
                        help="Минимальная длина слова для валидации (default: 5)")

    parser.add_argument("--json", dest="json_output", action="store_true",
                        help="Вывести результат анализа в формате JSON")
    parser.add_argument("-s", "--threshold", dest="threshold", type=float, default=0.3,
                        help="Пороговое значение для определения скрытых сообщений (default: 0.3)")

    args = parser.parse_args()

    #analysis
    files_to_process = []
    if args.input_file:
        files_to_process.append(args.input_file)
    elif args.directory:
        if not os.path.isdir(args.directory):
            print(f"[ATSS] Ошибка: Директория '{args.directory}' не найдена.")
            sys.exit(1)
        for root, dirs, files in os.walk(args.directory):
            for file in files:
                if file.endswith(".txt"):
                    files_to_process.append(os.path.join(root, file))
        
        if not files_to_process:
            print(f"[ATSS] В директории '{args.directory}' не найдено .txt файлов.")
            sys.exit(0)

    json_results = []
    if not args.json_output:
        print(f"--- ATSS Start | Lang: {args.lang} | MinLen: {args.min_length} | Files: {len(files_to_process)} ---")

    for filepath in files_to_process:
        app = process_file(filepath, args)
        if not app:
            continue

        if args.json_output:
            file_result = {
                "file": filepath,
                "language": args.lang,
                "min_length": args.min_length,
                "found_messages": app.ex_words
            }
            json_results.append(file_result)
        else:
            print_text_report(filepath, app)

    if args.json_output:
        if args.input_file:
            print(json.dumps(json_results[0] if json_results else {}, ensure_ascii=False, indent=4))
        else:
            print(json.dumps(json_results, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main()