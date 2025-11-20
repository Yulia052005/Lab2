import re
import requests

class DocumentValidator:
    """
    Класс для проверки специальных номеров документов.
    """

    def __init__(self):
        # Шаблон для номеров формата XXX-XXX-XXX YY
        self.format_template = re.compile(r'\b\d{3}-\d{3}-\d{3}\s\d{2}\b')

    def validate_document_number(self, doc_string):
        """
        Проверяет корректность номера документа.
        Возвращает True если номер прошел все проверки.
        """
        # Первичная проверка структуры
        if not self.format_template.match(doc_string):
            return False

        # Очистка от разделителей
        clean_digits = re.sub(r'[-\s]', '', doc_string)
        # Основная числовая последовательность
        main_sequence = clean_digits[:9]
        # Проверочный код
        verification_code = int(clean_digits[9:])

        # Вычисление проверочной суммы
        checksum = 0
        for position, numeral in enumerate(main_sequence):
            checksum += int(numeral) * (9 - position)

        # Нормализация проверочного кода
        computed_code = checksum % 101
        # Особый случай: код 100 преобразуется в 00
        if computed_code == 100:
            computed_code = 0

        return verification_code == computed_code

    def scan_text_content(self, text_content):
        """
        Сканирует текст на наличие номеров документов.
        Возвращает список найденных номеров с статусом проверки.
        """
        # Ищем номера во всем тексте
        possible_numbers = self.format_template.findall(text_content)
        found_items = []
        
        for number in possible_numbers:
            is_valid = self.validate_document_number(number)
            found_items.append((number, is_valid))
        
        return found_items

    def load_file_content(self, file_path):
        """Загружает содержимое файла."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Файл {file_path} не обнаружен.")
            return None
        except Exception as error:
            print(f"Ошибка чтения файла: {error}")
            return None

    def fetch_web_content(self, web_address):
        """Получает содержимое веб-страницы."""
        try:
            response = requests.get(web_address, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as error:
            print(f"Ошибка загрузки страницы: {error}")
            return None

    def start_verification(self):
        """Запускает процесс проверки."""
        print("=" * 50)
        print("Система проверки номеров документов")
        print("=" * 50)

        while True:
            print("\nВыберите источник данных:")
            print("1 - Ручной ввод текста")
            print("2 - Загрузка из файла")
            print("3 - Загрузка из интернета")
            print("0 - Завершение работы")

            user_choice = input("Ваш выбор: ").strip()

            if user_choice == '0':
                print("Работа завершена.")
                break

            input_text = ""
            source_description = ""

            if user_choice == '1':
                print("Введите текст для анализа:")
                input_text = input()
                source_description = "введенный текст"

            elif user_choice == '2':
                file_path = input("Укажите путь к файлу: ").strip()
                input_text = self.load_file_content(file_path)
                source_description = f"файл {file_path}"

            elif user_choice == '3':
                url = input("Введите адрес сайта: ").strip()
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                input_text = self.fetch_web_content(url)
                source_description = f"сайт {url}"

            else:
                print("Неверная команда. Попробуйте еще раз.")
                continue

            if input_text is None:
                print(f"Не удалось получить данные из {source_description}.")
                continue

            if not input_text.strip():
                print("Текст для анализа отсутствует.")
                continue

            # Выполнение проверки
            print(f"\nРезультаты проверки ({source_description}):")
            verification_results = self.scan_text_content(input_text)

            if not verification_results:
                print("Номера документов не обнаружены.")
            else:
                correct_count = 0
                print("\nОбнаруженные номера:")
                for index, (doc_number, is_correct) in enumerate(verification_results, 1):
                    status = "✓ ДЕЙСТВИТЕЛЕН" if is_correct else "✗ НЕДЕЙСТВИТЕЛЕН"
                    if is_correct:
                        correct_count += 1
                    print(f"  {index}. {doc_number} - {status}")
                print(f"\nВсего обнаружено: {len(verification_results)} номеров, из них действительных: {correct_count}")

if __name__ == "__main__":
    validator = DocumentValidator()
    validator.start_verification()
