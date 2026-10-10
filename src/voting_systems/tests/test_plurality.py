from unittest import TestCase

from voting_systems.base import VotingResultException

from .. import plurality


class Plurality(TestCase):
    def test_calculate_results(self):
        result = plurality.get_result(
            ["Chicken", "Pork"],
            ["Chicken", "Pork", "Chicken", "Chicken", "Chicken", "Pork", "Pork"],
        )
        assert result == {"Chicken": 4, "Pork": 3}

    def test_calculate_tie(self):
        result = plurality.get_result(
            ["Chicken", "Pork"],
            ["Chicken", "Pork"],
        )
        assert result == {"Chicken": 1, "Pork": 1}

    def test_ignore_invalid_answer(self):
        result = plurality.get_result(
            ["Beef", "Chicken"],
            [
                "Chickne",
                "Sausage",
                "turkey",
                "Chicken",
                "Beef",
                "Beef",
                "Chicken",
                "Chicken",
            ],
        )
        assert result == {"Beef": 2, "Chicken": 3}

    def test_raise_error_when_less_than_two(self):
        with self.assertRaises(VotingResultException):
            plurality.get_result(["Chicken"], ["Chicken", "Chicken"])

    def test_empty_submissions_keeps_all_choices_at_zero(self):
        result = plurality.get_result(["Beef", "Chicken", "Pork"], [])
        assert result == {"Beef": 0, "Chicken": 0, "Pork": 0}

    def test_none_submissions_are_ignored(self):
        result = plurality.get_result(
            ["Beef", "Chicken"],
            [None, "Beef", None, "Chicken", "Beef"],
        )
        assert result == {"Beef": 2, "Chicken": 1}

    def test_all_invalid_submissions_are_ignored(self):
        result = plurality.get_result(
            ["Beef", "Chicken"],
            ["Turkey", "Lamb", "Tofu"],
        )
        assert result == {"Beef": 0, "Chicken": 0}

    def test_unselected_choices_remain_zero(self):
        result = plurality.get_result(
            ["Beef", "Chicken", "Pork"],
            ["Beef", "Beef"],
        )
        assert result == {"Beef": 2, "Chicken": 0, "Pork": 0}
