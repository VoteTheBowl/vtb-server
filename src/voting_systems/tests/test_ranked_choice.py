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
            "winner": "Blue",
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
            "winner": "__TIE_FLAG__",
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
            "winner": "Green",
        }

    def test_raise_error_when_less_than_two_choices(self):
        with self.assertRaises(VotingResultException):
            ranked_choice.get_result(["Blue"], [{"Blue": 5}])

    def test_loser_tie_elimination(self):
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
                ["Blue", "Blue", "Red", "Brown"],
                ["Brown", "Blue", "Red", "Brown"],
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
                    "tally": {"Blue": 6, "Red": 2, "Green": 2, "Brown": 7},
                    "exhausted": 0,
                },
                {"tally": {"Blue": 8, "Brown": 9}, "exhausted": 0},
            ],
            "winner": "Brown",
        }
