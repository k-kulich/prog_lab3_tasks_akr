import sys
from typing import List, Dict, Optional
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MOVIES_FILE = BASE_DIR / 'data' / 'movies.txt'
HISTORY_FILE = BASE_DIR / 'data' / 'history.txt'


class Movie:
    def __init__(self, movie_id: int, title: str):
        self.movie_id = movie_id
        self.title = title

    def __repr__(self):
        return f"Movie({self.movie_id}, {self.title})"


class MovieRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.movies: Dict[int, Movie] = {}
        self._load()

    def _load(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',', 1)
                if len(parts) != 2:
                    continue
                movie_id = int(parts[0].strip())
                title = parts[1].strip()
                self.movies[movie_id] = Movie(movie_id, title)

    def get_title(self, movie_id: int) -> Optional[str]:
        movie = self.movies.get(movie_id)
        return movie.title if movie else None


class ViewHistory:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.histories: List[List[int]] = []
        self._load()

    def _load(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                movie_ids = [int(x.strip()) for x in line.split(',') if x.strip()]
                self.histories.append(movie_ids)


class Recommender:
    def __init__(self, movie_repo: MovieRepository, view_history: ViewHistory, use_weights: bool = False):
        self.movie_repo = movie_repo
        self.view_history = view_history
        self.use_weights = use_weights

    def recommend(self, user_movies: List[int]) -> Optional[str]:
        if not user_movies:
            return None
        user_set = set(user_movies)
        movie_scores = defaultdict(float)

        for history in self.view_history.histories:
            history_set = set(history)
            intersection = user_set & history_set
            if not intersection:
                continue
            match_ratio = len(intersection) / len(user_set)
            if match_ratio < 0.5:
                continue
            weight = match_ratio if self.use_weights else 1.0
            for movie_id in history_set:
                if movie_id in user_set:
                    continue
                movie_scores[movie_id] += weight

        if not movie_scores:
            return None

        best_movie_id = max(movie_scores.items(), key=lambda x: x[1])[0]
        return self.movie_repo.get_title(best_movie_id)


if __name__ == '__main__':
    movie_repo = MovieRepository(MOVIES_FILE)
    view_history = ViewHistory(HISTORY_FILE)
    recommender = Recommender(movie_repo, view_history, use_weights=False)

    print("Введите список просмотренных фильмов (id через запятую):")
    user_input = sys.stdin.readline().strip()
    if user_input:
        user_movies = [int(x.strip()) for x in user_input.split(',') if x.strip()]
        recommendation = recommender.recommend(user_movies)
        if recommendation:
            print(recommendation)
        else:
            print("Нет рекомендаций")
    else:
        print("Пустой ввод")