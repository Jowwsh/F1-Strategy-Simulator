import unittest
from src.MDPController import *
from src.DiscreteState import DiscreteState
from src.Tracks import MONZA

class TestMDPController(unittest.TestCase):

    def test_discretise_wear(self):
        wear = discretise_wear(1.14154325)
        self.assertEqual(wear, 5)
        wear = discretise_wear(3.2)
        self.assertEqual(wear, 15)

    def test_discretise_fuel(self):
        fuel = discretise_fuel(110)
        self.assertEqual(fuel, 15)
        fuel = discretise_fuel(50)
        self.assertEqual(fuel, 6)

    def test_no_changes_when_converting(self):
        test_discrete_state = DiscreteState(1, 1, 3, 5, 2, 0)
        race_state = discrete_to_race_state(test_discrete_state, MONZA)
        new_discrete_state = race_to_discrete_state(race_state)
        self.assertEqual(test_discrete_state.state_to_tuple(), new_discrete_state.state_to_tuple())

    def test_reward_function(self):
        reward = calculate_reward(89.324, False)
        self.assertEqual(reward, -89.324)
        reward = calculate_reward(91.526, True)
        self.assertEqual(reward, -1000)
