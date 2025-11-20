import unittest

class TestDocumentValidator(unittest.TestCase):

    def setUp(self):
        from document_verifier import DocumentValidator
        self.validator = DocumentValidator()

    def test_correct_documents(self):
        """Проверка корректных номеров документов"""
        valid_documents = [
            "112-233-445 95",
            "089-456-321 12",
            "156-729-385 07"
        ]
        for doc in valid_documents:
            with self.subTest(document=doc):
                self.assertTrue(self.validator.validate_document_number(doc))

    def test_incorrect_verification(self):
        """Проверка номеров с неверным проверочным кодом"""
        invalid_documents = [
            "112-233-445 00",
            "156-729-385 99",
            "128-118-231 01"
        ]
        for doc in invalid_documents:
            with self.subTest(document=doc):
                self.assertFalse(self.validator.validate_document_number(doc))

    def test_wrong_format(self):
        """Проверка некорректных форматов"""
        malformed_documents = [
            "12345678901",
            "123-45-678 90", 
            "12-345-678 90",
            "123-456-78 90",
            "123-456-7890",
            "123-456-789 1",
            "123-456-789 123",
            "abc-def-ghi jk",
            "",
        ]
        for doc in malformed_documents:
            with self.subTest(document=doc):
                self.assertFalse(self.validator.validate_document_number(doc))

    def test_text_scanning(self):
        """Тест поиска номеров в текстовом содержимом"""
        sample_text = """
        Пример текста с номерами:
        Действительный номер: 112-233-445 95
        Неправильный формат: 123-45-678 90
        Неверный код: 112-233-445 00
        Еще действительный: 089-456-321 12
        И этот действителен: 156-729-385 07
        """
        results = self.validator.scan_text_content(sample_text)
        
        # Проверка количества найденных номеров
        self.assertEqual(len(results), 4)
        
        # Проверка конкретных номеров и их статуса
        found_numbers = [num for num, _ in results]
        self.assertIn("112-233-445 95", found_numbers)
        self.assertIn("112-233-445 00", found_numbers)
        self.assertIn("089-456-321 12", found_numbers)
        self.assertIn("156-729-385 07", found_numbers)
        
        # Проверка корректности валидации
        status_map = {num: valid for num, valid in results}
        self.assertTrue(status_map["112-233-445 95"])
        self.assertFalse(status_map["112-233-445 00"])
        self.assertTrue(status_map["089-456-321 12"])
        self.assertTrue(status_map["156-729-385 07"])

    def test_empty_content(self):
        """Тест обработки пустого текста"""
        results = self.validator.scan_text_content("")
        self.assertEqual(results, [])

    def test_no_matches_found(self):
        """Тест случая когда номера не найдены"""
        text_without_documents = "Этот текст не содержит номеров документов. 123-45-6789 не подходит."
        results = self.validator.scan_text_content(text_without_documents)
        self.assertEqual(results, [])

if __name__ == '__main__':
    unittest.main()
