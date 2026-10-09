import unittest
import tempfile
import os
from recommender import MovieRepository, ViewHistory, Recommender


class TestRecommender(unittest.TestCase):
    def setUp(self):
        self.movies_content = """1,Мстители: Финал
2,Хатико
3,Дюна
4,Унесенные призраками"""
        self.history_content = """2,1,3
1,4,3
2,2,2,2,2,3"""

        self.movies_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8')
        self.movies_file.write(self.movies_content)
        self.movies_file.close()

        self.history_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8')
        self.history_file.write(self.history_content)
        self.history_file.close()

        self.movie_repo = MovieRepository(self.movies_file.name)
        self.view_history = ViewHistory(self.history_file.name)

    def tearDown(self):
        os.unlink(self.movies_file.name)
        os.unlink(self.history_file.name)

    def test_basic_recommendation(self):
        recommender = Recommender(self.movie_repo, self.view_history, use_weights=False)
        result = recommender.recommend([2, 4])
        self.assertEqual(result, "Дюна")

    def test_no_recommendation(self):
        recommender = Recommender(self.movie_repo, self.view_history, use_weights=False)
        result = recommender.recommend([5])  # фильма 5 нет в истории
        self.assertIsNone(result)

    def test_all_watched(self):
        recommender = Recommender(self.movie_repo, self.view_history, use_weights=False)
        result = recommender.recommend([2, 1, 3, 4])
        self.assertIsNone(result)

    def test_weights(self):
        recommender = Recommender(self.movie_repo, self.view_history, use_weights=True)
        result = recommender.recommend([2, 4])
        self.assertEqual(result, "Дюна")

    def test_empty_input(self):
        recommender = Recommender(self.movie_repo, self.view_history, use_weights=False)
        result = recommender.recommend([])
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()