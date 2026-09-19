from django.test import TestCase

from vote.systems.plurality import results


class Plurality(TestCase):
    def test_ignore_invalid_answer(self):
        result = results(["Beef", "Chicken"], ["Chickne", "Sausage", "turkey", "Chicken", "Beef", "Beef", "Chicken", "Chicken"])
        assert result == {"Beef": 2, "Chicken": 3}