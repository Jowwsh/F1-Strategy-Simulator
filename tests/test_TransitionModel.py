import unittest
from src.RaceState import RaceState
from src.Actions import Action
from src.TransitionModel import *

class TestTransitionModel(unittest.TestCase):

    def setUp(self):
        self.test_state = RaceState(1, 50, "medium", 0, 100, [], [])

    def test_tyre_wear_normal(self):
        tyre_wear(self.test_state, Action.NORMAL)
        self.assertEqual(self.test_state.tyre_wear, 0.035)

    def test_tyre_wear_push(self):
        tyre_wear(self.test_state, Action.PUSH)
        self.assertEqual(self.test_state.tyre_wear, 0.07)

    def test_tyre_wear_pit(self):
        self.test_state.tyre_wear = 0.8
        tyre_wear(self.test_state, Action.PIT)
        self.assertEqual(self.test_state.tyre_wear, 0)

    def test_fuel_decrease(self):
        decrease_fuel(self.test_state)
        self.assertEqual(self.test_state.fuel_load, 98)

    def test_lap_time_is_correct_normal(self):
        self.assertEqual(apply_action(self.test_state, Action.NORMAL), 93.03975)
        
    def test_lap_time_is_correct_push(self):
        self.assertEqual(apply_action(self.test_state, Action.PUSH), 92.1395)

    def test_lap_time_is_correct_pit(self):
        self.assertEqual(apply_action(self.test_state, Action.PIT), 115.94)

    def test_more_wear_means_slower_lap(self):
        for action in [Action.NORMAL, Action.PUSH]:
            self.setUp()
            first_lap = apply_action(self.test_state, action)
            self.setUp()
            self.test_state.tyre_wear = 0.1
            second_lap = apply_action(self.test_state, action)
            self.assertGreater(second_lap, first_lap)

    def test_less_fuel_means_faster_time(self):
        for action in [Action.NORMAL, Action.PUSH]:
            self.setUp()
            first_lap = apply_action(self.test_state, action)
            self.setUp()
            self.test_state.fuel_load = 25
            second_lap = apply_action(self.test_state, action)
            self.assertGreater(first_lap, second_lap)

    def test_pit_lap_is_recorded(self):
        apply_action(self.test_state, Action.PIT)
        self.assertEqual(self.test_state.pit_stops, [1])

    def test_lap_times_are_recorded(self):
        for _ in range(5):
            apply_action(self.test_state, Action.NORMAL)
        self.assertEqual(len(self.test_state.lap_time_history), 5)