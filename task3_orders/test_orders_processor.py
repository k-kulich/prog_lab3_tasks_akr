import os
import tempfile
import unittest
from orders_processor import OrderProcessor


class TestOrderProcessor(unittest.TestCase):
    def setUp(self):
        self.input_content = """31987;Сыр, Колбаса, Сыр, Макароны, Колбаса;Петрова Анна;Россия. Ленинградская область. Санкт-Петербург. набережная реки Фонтанки;+7-921-456-78-90;MIDDLE
87459;Молоко, Яблоки, Хлеб, Яблоки, Молоко;Иванов Иван Иванович;Россия. Московская область. Москва. улица Пушкина;+7-912-345-67-89;MAX
31987;Сыр, Колбаса, Макароны, Сыр, Колбаса;Петрова Анна Сергеевна;Франция. Иль-де-Франс. Париж. Шанз-Элизе;+3-214-020-50-50;MIDDLE
56342;Хлеб, Молоко, Хлеб, Молоко;Смирнова Мария Леонидовна;Германия. Бавария. Мюнхен. Мариенплац;+4-989-234-56;LOW
48276;Яблоки, Макароны, Яблоки;Алексеев Алексей Алексеевич;Италия. Лацио. Рим. Колизей;+3-061-234-56-78;MAX
65829;Сок, Вода, Сок, Вода;Белова Екатерина Михайловна;Испания. Каталония. Барселона. Рамбла;+34-93-1234-567;LOW
72901;Чай, Кофе, Чай, Кофе;Михайлов Сергей Петрович;Великобритания. Англия. Лондон. Бейкер-стрит;+4-207-946-09-58;LOW
84756;Печенье, Сыр, Печенье, Сыр;Васильева Анна Владимировна;Япония. Шибуя. Шибуя-кроссинг;+8-131-234-5678;MAX
90385;Макароны, Сыр, Макароны, Сыр;Николаев Николай;;+1-416-123-45-67;LOW"""

        self.expected_valid = """87459;Молоко x2, Яблоки x2, Хлеб;Иванов Иван Иванович;Московская область. Москва. улица Пушкина;+7-912-345-67-89;MAX
31987;Сыр x2, Колбаса x2, Макароны;Петрова Анна;Ленинградская область. Санкт-Петербург. набережная реки Фонтанки;+7-921-456-78-90;MIDDLE
72901;Чай x2, Кофе x2;Михайлов Сергей Петрович;Англия. Лондон. Бейкер-стрит;+4-207-946-09-58;LOW
48276;Яблоки x2, Макароны;Алексеев Алексей Алексеевич;Лацио. Рим. Колизей;+3-061-234-56-78;MAX
31987;Сыр x2, Колбаса x2, Макароны;Петрова Анна Сергеевна;Иль-де-Франс. Париж. Шанз-Элизе;+3-214-020-50-50;MIDDLE
"""

        self.expected_invalid = """56342;2;+4-989-234-56
65829;2;+34-93-1234-567
84756;2;+8-131-234-5678
84756;1;Япония. Шибуя. Шибуя-кроссинг
90385;1;no data
"""

        self.input_file = tempfile.NamedTemporaryFile(
            mode='w+', delete=False, encoding='utf-8', suffix='.txt'
        )
        self.input_file.write(self.input_content)
        self.input_file.close()

        self.valid_file = tempfile.NamedTemporaryFile(
            mode='w+', delete=False, encoding='utf-8', suffix='.txt'
        )
        self.valid_file.close()

        self.invalid_file = tempfile.NamedTemporaryFile(
            mode='w+', delete=False, encoding='utf-8', suffix='.txt'
        )
        self.invalid_file.close()

    def tearDown(self):
        for path in (self.input_file.name, self.valid_file.name, self.invalid_file.name):
            if os.path.exists(path):
                os.unlink(path)

    def test_process_orders(self):
        processor = OrderProcessor(self.input_file.name)
        processor.process(self.valid_file.name, self.invalid_file.name)

        with open(self.valid_file.name, 'r', encoding='utf-8') as f:
            valid_result = f.read()

        with open(self.invalid_file.name, 'r', encoding='utf-8') as f:
            invalid_result = f.read()

        self.assertEqual(valid_result, self.expected_valid)
        self.assertEqual(invalid_result, self.expected_invalid)


if __name__ == '__main__':
    unittest.main()