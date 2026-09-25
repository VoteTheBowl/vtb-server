from unittest import TestCase

from .. import plurality


class Plurality(TestCase):
    def test_ignore_invalid_answer(self):
        result = plurality.get_result(["Beef", "Chicken"], ["Chickne", "Sausage", "turkey", "Chicken", "Beef", "Beef", "Chicken", "Chicken"])
        assert result == {"Beef": 2, "Chicken": 3}