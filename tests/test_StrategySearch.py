import unittest
from src.StrategySearch import generate_strategies

class TestTransitionModel(unittest.TestCase):

    def setUp(self):
        self.strategies = generate_strategies()

    def test_all_strategies_generated(self):
        self.assertEqual(len(self.strategies), 108)

    def test_all_strategies_valid(self):
        for strategy in self.strategies:
            self.assertFalse(all(tyre == strategy[0] for tyre in strategy))
