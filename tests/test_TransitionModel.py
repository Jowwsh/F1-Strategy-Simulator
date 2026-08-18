import unittest
from src.RaceState import RaceState
from src.Actions import Action
from src.TransitionModel import *
from src.TyreCompounds import SOFT, MEDIUM, HARD

class TestTransitionModel(unittest.TestCase):

    def setUp(self):
        self.test_state = RaceState(1, 50, SOFT, 0, 100, [], [(1, MEDIUM)], 1)

    def test_tyre_wear_normal(self):
        tyre_wear(self.test_state, Action.NORMAL)
        self.assertEqual(self.test_state.tyre_wear, 0.035)

    def test_tyre_wear_push(self):
        tyre_wear(self.test_state, Action.PUSH)
        self.assertEqual(self.test_state.tyre_wear, 0.07)

    def test_tyre_wear_pit(self):
        self.test_state.tyre_wear = 0.8
        apply_action(self.test_state, Action.PIT)
        self.assertEqual(self.test_state.tyre_wear, 0)

    def test_fuel_decrease(self):
        decrease_fuel(self.test_state)
        self.assertEqual(self.test_state.fuel_load, 98)

    def test_lap_time_is_correct_normal(self):
        self.assertEqual(apply_action(self.test_state, Action.NORMAL), 93.03975)
        
    def test_lap_time_is_correct_push(self):
        self.assertEqual(apply_action(self.test_state, Action.PUSH), 92.1395)

    def test_lap_time_is_correct_pit(self):
        self.assertEqual(apply_action(self.test_state, Action.PIT), 116.03975)

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


    def test_lap_times_are_recorded(self):
        for _ in range(5):
            apply_action(self.test_state, Action.NORMAL)
        self.assertEqual(len(self.test_state.lap_time_history), 5)

    def test_medium_tyre_wears_slower_than_soft(self):
        apply_action(self.test_state, Action.NORMAL)
        soft_wear = self.test_state.tyre_wear
        self.setUp()
        self.test_state.tyre_compound = MEDIUM
        apply_action(self.test_state, Action.NORMAL)
        medium_wear = self.test_state.tyre_wear
        self.assertGreater(soft_wear, medium_wear)

    def test_hard_tyre_wears_slower_than_medium(self):
        self.test_state.tyre_compound = MEDIUM
        apply_action(self.test_state, Action.NORMAL)
        medium_wear = self.test_state.tyre_wear
        self.setUp()
        self.test_state.tyre_compound = HARD
        apply_action(self.test_state, Action.NORMAL)
        hard_wear = self.test_state.tyre_wear
        self.assertGreater(medium_wear, hard_wear)

    def test_medium_tyre_slower_than_soft(self):
        soft_lap = apply_action(self.test_state, Action.NORMAL)
        self.setUp()
        self.test_state.tyre_compound = MEDIUM
        medium_lap = apply_action(self.test_state, Action.NORMAL)
        self.assertGreater(medium_lap, soft_lap)

    def test_hard_tyre_slower_than_medium(self):
        self.test_state.tyre_compound = MEDIUM
        medium_lap = apply_action(self.test_state, Action.NORMAL)
        self.setUp()
        self.test_state.tyre_compound = HARD
        hard_lap = apply_action(self.test_state, Action.NORMAL)
        self.assertGreater(hard_lap, medium_lap)

    def test_stint_number_increase_when_pit(self):
        apply_action(self.test_state, Action.PIT)
        self.assertEqual(self.test_state.stint_num, 2)

    def test_tyre_change_when_pitting(self):
        apply_action(self.test_state, Action.PIT)
        self.assertEqual(self.test_state.tyre_compound, MEDIUM)
