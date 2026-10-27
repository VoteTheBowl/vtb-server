from unittest import TestCase

from .. import ranked_choice
from ..base import VotingResultException


class RankedChoice(TestCase):
    def test_small_result(self):
        result = ranked_choice.get_result(
            ["Blue", "Red"],
            [["Blue", "Red"], ["Blue", "Red"], ["Red", "Blue"]],
        )

        assert result == {
            "rounds": [{"tally": {"Blue": 2, "Red": 1}, "exhausted": 0}],
            "roundWinner": "Blue",
        }

    def test_small_tie_result(self):
        result = ranked_choice.get_result(
            ["Blue", "Red"],
            [
                ["Blue", "Red"],
                ["Blue", "Red"],
                ["Red", "Blue"],
                ["Red", "Blue"],
                ["Blue", "Red"],
                ["Red", "Blue"],
            ],
        )

        assert result == {
            "rounds": [{"tally": {"Blue": 3, "Red": 3}, "exhausted": 0}],
            "roundWinner": "__TIE_FLAG__",
        }

    def test_large_result(self):
        result = ranked_choice.get_result(
            ["Blue", "Red", "Green", "Brown"],
            [
                ["Blue", "Green", "Red", "Brown"],
                ["Blue", "Red", "Brown", "Green"],
                ["Blue", "Red", "Green", "Brown"],
                ["Blue", "Brown", "Green", "Red"],
                ["Blue", "Green", "Red", "Brown"],
                ["Red", "Green", "Brown", "Blue"],
                ["Red", "Green", "Blue", "Brown"],
                ["Green", "Blue", "Red", "Brown"],
                ["Green", "Blue", "Red", "Brown"],
                ["Green", "Blue", "Red", "Brown"],
                ["Green", "Brown", "Red", "Blue"],
                ["Brown", "Red", "Green", "Blue"],
                ["Brown", "Red", "Blue", "Green"],
                ["Brown", "Blue", "Green", "Red"],
                ["Brown", "Blue", "Red", "Green"],
                ["Brown", "Blue", "Red", "Green"],
                ["Brown", "Red", "Blue", "Green"],
            ],
        )

        assert result == {
            "rounds": [
                {
                    "tally": {"Blue": 5, "Red": 2, "Green": 4, "Brown": 6},
                    "exhausted": 0,
                },
                {"tally": {"Blue": 5, "Green": 6, "Brown": 6}, "exhausted": 0},
                {"tally": {"Green": 9, "Brown": 8}, "exhausted": 0},
            ],
            "roundWinner": "Green",
        }


"""
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
 """
