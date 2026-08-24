import unittest
from src.RaceState import RaceState
from src.Actions import Action
from src.TransitionModel import *
from src.TyreCompounds import SOFT, MEDIUM, HARD
from src.Tracks import MONACO, MONZA, SILVERSTONE, BAHRAIN, SPA

class TestTransitionModel(unittest.TestCase):

    def setUp(self):
        self.test_state = RaceState(1, 50, SOFT, 0, 110, [], [(1, MEDIUM)], 1, False, 0, SILVERSTONE)

    def test_more_tyre_wear_when_pushing(self):
        tyre_wear(self.test_state, Action.NORMAL)
        normal_wear = self.test_state.tyre_wear
        self.setUp()
        tyre_wear(self.test_state, Action.PUSH)
        push_wear = self.test_state.tyre_wear
        self.assertLess(normal_wear, push_wear)

    def test_tyre_wear_pit(self):
        self.test_state.tyre_wear = 0.8
        apply_action(self.test_state, Action.PIT)
        self.assertEqual(self.test_state.tyre_wear, 0)

    def test_fuel_decrease(self):
        original_fuel = self.test_state.fuel_load
        decrease_fuel(self.test_state, Action.NORMAL)
        self.assertLess(self.test_state.fuel_load, original_fuel)

    def test_push_faster_than_normal(self):
        normal_lap = apply_action(self.test_state, Action.NORMAL)
        self.setUp()
        push_lap = apply_action(self.test_state, Action.PUSH)
        self.assertLess(push_lap, normal_lap)

    def test_normal_faster_than_pit(self):
        normal_lap = apply_action(self.test_state, Action.NORMAL)
        self.setUp()
        pit_lap = apply_action(self.test_state, Action.PIT)
        self.assertLess(normal_lap, pit_lap)

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

    def test_tyre_wear_never_more_than_one(self):
        self.test_state.tyre_wear = 0.999999
        tyre_wear(self.test_state, Action.PUSH)
        self.assertEqual(self.test_state.tyre_wear, 1)
        self.test_state.tyre_wear = 0.999999
        tyre_wear(self.test_state, Action.NORMAL)
        self.assertEqual(self.test_state.tyre_wear, 1)

    def test_fuel_multiplier_endpoints(self):
        self.assertEqual(0.9 * (11/9)**(self.test_state.fuel_load/110), 1.1)
        self.test_state.fuel_load = 0
        self.assertEqual(0.9 * (11/9)**(self.test_state.fuel_load/110), 0.9)

    def test_fuel_multiplier_is_non_linear(self):
        self.assertNotEqual((0.9 * (11/9)**(100/100)) - (0.9 * (11/9)**(98/100)), (0.9 * (11/9)**(99/100)) - (0.9 * (11/9)**(96/100)))

    def test_tyre_wear_is_non_linear(self):
        wear1 = self.test_state.tyre_wear
        tyre_wear(self.test_state, Action.NORMAL)
        wear2 = self.test_state.tyre_wear
        tyre_wear(self.test_state, Action.NORMAL)
        wear3 = self.test_state.tyre_wear
        self.assertNotEqual(wear2 - wear1, wear3 - wear2)

    def test_more_fuel_burn_when_more_fuel(self):
        decrease_fuel(self.test_state, Action.NORMAL)
        burn1 = 110 - self.test_state.fuel_load
        self.test_state.fuel_load = 10
        decrease_fuel(self.test_state, Action.NORMAL)
        burn2 = 10 - self.test_state.fuel_load
        self.assertGreater(burn2, burn1)

    def test_push_increases_fuel_burn(self):
        decrease_fuel(self.test_state, Action.NORMAL)
        normal_burn = 110 - self.test_state.fuel_load
        self.setUp()
        decrease_fuel(self.test_state, Action.PUSH)
        push_burn = 110 - self.test_state.fuel_load
        self.assertGreater(push_burn, normal_burn)

    def test_out_of_fuel_triggers_dnf(self):
        self.test_state.fuel_load = 1
        decrease_fuel(self.test_state, Action.NORMAL)
        self.assertTrue(self.test_state.dnf)

    def test_stint_length_resets_on_pit(self):
        apply_action(self.test_state, Action.PIT)
        self.assertEqual(self.test_state.stint_length, 0)

    def test_stint_length_increases(self):
        apply_action(self.test_state, Action.NORMAL)
        self.assertEqual(self.test_state.stint_length, 1)

    def test_tyre_warmup_penalty_soft(self):
        self.assertEqual(tyre_warmup_penalty(self.test_state), 1.5)

    def test_tyre_warmup_penalty_medium(self):
        apply_action(self.test_state, Action.PIT)
        penalty = tyre_warmup_penalty(self.test_state)
        apply_action(self.test_state, Action.NORMAL)
        penalty += tyre_warmup_penalty(self.test_state)
        self.assertEqual(penalty, 2.5)

    def test_tyre_warmup_penalty_hard(self):
        self.test_state.tyre_compound = HARD
        penalty = tyre_warmup_penalty(self.test_state)
        apply_action(self.test_state, Action.NORMAL)
        penalty += tyre_warmup_penalty(self.test_state)
        apply_action(self.test_state, Action.NORMAL)
        penalty += tyre_warmup_penalty(self.test_state)
        self.assertEqual(penalty, 4)

    def test_stint_decay(self):
        self.test_state.stint_length = 12
        penalty = stint_decay_penalty(self.test_state)
        self.assertEqual(penalty, 0.2)

    def test_more_tyre_wear_on_higher_wear_track(self):
        tyre_wear(self.test_state, Action.NORMAL)
        higher_wear = self.test_state.tyre_wear
        self.setUp()
        self.test_state.track = MONZA
        tyre_wear(self.test_state, Action.NORMAL)
        lower_wear = self.test_state.tyre_wear
        self.assertGreater(higher_wear, lower_wear)

    def test_more_fuel_burn_on_higher_burn_track(self):
        decrease_fuel(self.test_state, Action.NORMAL)
        higher_fuel = self.test_state.fuel_load
        self.setUp()
        self.test_state.track = MONZA
        decrease_fuel(self.test_state, Action.NORMAL)
        lower_fuel = self.test_state.fuel_load
        self.assertGreater(higher_fuel, lower_fuel)

    def test_faster_lap_time_on_quicker_track(self):
        lap1 = apply_action(self.test_state, Action.NORMAL)
        self.setUp()
        self.test_state.track = MONACO
        lap2 = apply_action(self.test_state, Action.NORMAL)
        self.assertGreater(lap1, lap2)

    def test_track_evolution(self):
        lap1 = apply_action(self.test_state, Action.NORMAL)
        self.setUp()
        self.test_state.current_lap = 2
        lap2 = apply_action(self.test_state, Action.NORMAL)
        self.assertGreater(lap1, lap2)

