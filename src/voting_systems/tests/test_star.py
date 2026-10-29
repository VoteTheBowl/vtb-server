from unittest import TestCase

from .. import star
from ..base import VotingResultException


class Star(TestCase):
    def test_small_result(self):
        result = star.get_result(
            ["Blue", "Red"],
            [{"Blue": 4, "Red": 2}, {"Blue": 4, "Red": 5}, {"Blue": 2, "Red": 1}],
        )

        assert result == {
            "scores": [
                star.Score(choice="Blue", score=10),
                star.Score(choice="Red", score=8),
            ],
            "gold": ["Blue"],
            "silver": ["Red"],
            "bronze": [],
        }

    def test_small_tie_result(self):
        result = star.get_result(
            ["Blue", "Red"],
            [
                {"Blue": 4, "Red": 2},
                {"Blue": 2, "Red": 4},
                {"Blue": 4, "Red": 2},
                {"Blue": 2, "Red": 4},
            ],
        )

        assert result == {
            "scores": [
                star.Score(choice="Blue", score=12),
                star.Score(choice="Red", score=12),
            ],
            "gold": ["Blue", "Red"],
            "silver": [],
            "bronze": [],
        }

    def test_large_result(self):
        result = star.get_result(
            ["Blue", "Red", "Green", "Brown"],
            [
                {"Blue": 5, "Red": 2, "Green": 5, "Brown": 2},
                {"Blue": 2, "Red": 3, "Green": 1, "Brown": 1},
                {"Blue": 1, "Red": 2, "Green": 3, "Brown": 3},
                {"Blue": 0, "Red": 0, "Green": 2, "Brown": 5},
                {"Blue": 0, "Red": 4, "Green": 0, "Brown": 0},
                {"Blue": 4, "Red": 4, "Green": 2, "Brown": 2},
                {"Blue": 2, "Red": 0, "Green": 1, "Brown": 5},
                {"Blue": 0, "Red": 4, "Green": 5, "Brown": 0},
                {"Blue": 1, "Red": 4, "Green": 2, "Brown": 5},
            ],
        )

        assert result == {
            "scores": [
                {"choice": "Red", "score": 23},
                {"choice": "Brown", "score": 23},
                {"choice": "Green", "score": 21},
                {"choice": "Blue", "score": 15},
            ],
            "gold": ["Brown"],
            "silver": ["Red"],
            "bronze": ["Green"],
        }

    def test_raise_error_when_less_than_two_choices(self):
        with self.assertRaises(VotingResultException):
            star.get_result(["Blue"], [{"Blue": 5}])

    def test_scores_tie_breaks_by_pairwise_majority(self):
        result = star.get_result(
            ["Blue", "Red"],
            [
                {"Blue": 2, "Red": 1},
                {"Blue": 2, "Red": 1},
                {"Blue": 0, "Red": 2},
            ],
        )

        assert result == {
            "scores": [
                star.Score(choice="Blue", score=4),
                star.Score(choice="Red", score=4),
            ],
            "gold": ["Blue"],
            "silver": ["Red"],
            "bronze": [],
        }

    def test_scores_tie_breaks_by_five_star_count(self):
        result = star.get_result(
            ["Blue", "Red"],
            [
                {"Blue": 0, "Red": 0},
                {"Blue": 0, "Red": 0},
                {"Blue": 0, "Red": 1},
                {"Blue": 5, "Red": 4},
            ],
        )

        assert result == {
            "scores": [
                star.Score(choice="Blue", score=5),
                star.Score(choice="Red", score=5),
            ],
            "gold": ["Blue"],
            "silver": ["Red"],
            "bronze": [],
        }
