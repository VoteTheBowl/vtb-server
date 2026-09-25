from unittest import TestCase

from .. import star


class Star(TestCase):
    def test_test(self):
        print(star.get_result(['Blue', 'Red'], [{'Blue': 4, 'Red': 2}, {'Blue': 4, 'Red': 5}, {'Blue': 2, 'Red': 1}]))