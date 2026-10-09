import unittest
from io import StringIO
from survey import SurveyProcessor


class TestSurveyProcessor(unittest.TestCase):
    def test_example(self):
        boundaries = [18, 25, 35, 45, 60, 80, 100]
        processor = SurveyProcessor(boundaries)
        input_data = """Соколов Андрей Сергеевич,15
Егоров Алан Петрович,7
Ярилова Розалия Трофимовна,29
Старостин Ростислав Ермолаевич,50
Дьячков Нисон Иринеевич,88
Иванов Варлам Якунович,88
Кошельков Захар Брониславович,105
END"""
        expected = """101+: Кошельков Захар Брониславович (105)

81-100: Дьячков Нисон Иринеевич (88), Иванов Варлам Якунович (88)

46-60: Старостин Ростислав Ермолаевич (50)

26-35: Ярилова Розалия Трофимовна (29)

0-18: Соколов Андрей Сергеевич (15), Егоров Алан Петрович (7)"""
        result = processor.process(StringIO(input_data))
        self.assertEqual(result.strip(), expected.strip())


if __name__ == '__main__':
    unittest.main()