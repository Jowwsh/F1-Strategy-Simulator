from src.DiscreteState import DiscreteState
from src.MDPController import *
from src.Actions import Action
from collections import defaultdict
from math import inf

def generate_states(track):
    states = []
    for tyre_compound_id in range(3):
        for wear_bin in range(10):
            for fuel_bin in range(10):
                for stint_lap_bin in range(track.laps // 8 + 1):
                    for safety_car_flag in range(2):
                        for is_final_lap in range(2):
                            states.append(DiscreteState(
                                1, tyre_compound_id, wear_bin, fuel_bin,
                                stint_lap_bin, safety_car_flag,
                                True, wear_bin/3,
                                fuel_bin*(109.999/9),
                                stint_lap_bin*8,
                                is_final_lap
                            ))
    return states

def bellman_update(V, state, track, transition_cache):
    GAMMA = 0.99
    if state.is_final_lap:
        action = Action.STAY_OUT
        outcomes = transition_distribution(transition_cache, state, action, track, samples=200)
        expected_value = sum(reward for (_, reward) in outcomes) / len(outcomes)
        return expected_value
    best_value = -inf 
    for action in Action:
        outcomes = transition_distribution(transition_cache, state, action, track, samples=200)
        expected_value = 0
        for (next_state_tuple, reward) in outcomes:
            expected_value += (reward + GAMMA * V[next_state_tuple]) / len(outcomes)
        best_value = max(best_value, expected_value)
    return best_value

def iterate_until_convergence(track, transition_cache):
    MAX_ITERATIONS = 100000
    THRESHOLD = 0.01
    states = generate_states(track)
    V = defaultdict(float)
    for iteration in range(MAX_ITERATIONS):
        delta = 0
        for state in states:
            state_tuple = state.state_to_tuple()
            new_value = bellman_update(V, state, track, transition_cache)
            if abs(V[state_tuple] - new_value) > delta:
                delta = abs(V[state_tuple] - new_value)
                delta_state = state_tuple
            # delta = max(delta, abs(V[state_tuple] - new_value))
            V[state_tuple] = new_value
        print(iteration, delta_state, delta)
        if delta < THRESHOLD:
            return V

def get_optimal_policy(V, track, transition_cache):
    GAMMA = 0.99
    policy = {}
    states = generate_states(track)
    for state in states:
        if state.is_final_lap:
            policy[state.state_to_tuple()] = Action.STAY_OUT
            continue
        best_action = None
        best_value = -inf
        for action in Action:
            outcomes = transition_distribution(transition_cache, state, action, track, samples=200)
            expected_value = 0
            for (next_state_tuple, reward) in outcomes:
                expected_value += (reward + GAMMA * V[next_state_tuple]) / len(outcomes)
            if expected_value > best_value:
                best_value = expected_value
                best_action = action
        policy[state.state_to_tuple()] = best_action
    return policy

