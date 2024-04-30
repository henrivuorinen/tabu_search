import unittest

from constraint_satisfaction_algorithm import is_blocking_set


class TestIsBlockingSet(unittest.TestCase):
    def test_empty_set(self):
        points = [(0, 0), (1, 1), (2, 2)]
        lines = [[(0, 0), (1, 1)], [(0, 0), (2, 2)]]
        self.assertFalse(is_blocking_set(set(), lines))

    def test_blocking_set(self):
        points = [(0, 0), (1, 1), (2, 2)]
        lines = [[(0, 0), (1, 1)], [(0, 0), (2, 2)]]
        self.assertTrue(is_blocking_set({(0, 0), (1, 1)}, lines))

    def test_non_blocking_set(self):
        points = [(0, 0), (1, 1), (2, 2)]
        lines = [[(0, 0), (1, 1)], [(0, 0), (2, 2)]]
        self.assertFalse(is_blocking_set({(0, 0)}, lines))

    def test_invalid_lines(self):
        points = [(0, 0), (1, 1), (2, 2)]
        lines = [[(0, 0), (1, 1)], [(0, 0), (2, 2)]]
        self.assertRaises(TypeError, is_blocking_set, {(0, 0)}, None)

if __name__ == '__main__':
    unittest.main()