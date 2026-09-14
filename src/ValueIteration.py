from src.DiscreteState import DiscreteState
from src.MDPController import *
from src.Actions import Action
from collections import defaultdict
from math import inf
from os import makedirs
from pickle import dump

def generate_states(track):
    states = []
    for lap in range(1, track.laps + 1):
        for tyre_compound_id in range(3):
            for wear_bin in range(30):
                for fuel_bin in range(10):
                    for stint_lap_bin in range(track.laps // 5 + 3):
                        for safety_car_flag in range(2):
                            for allowed_pit_strategy in range(2):
                                if stint_lap_bin >= 3:
                                    real_stint_lap = (stint_lap_bin - 2) * 5
                                else:
                                    real_stint_lap = stint_lap_bin
                                states.append(DiscreteState(
                                    lap, tyre_compound_id, wear_bin, fuel_bin,
                                    stint_lap_bin, safety_car_flag,
                                    allowed_pit_strategy, wear_bin/10,
                                    fuel_bin*(109.999/9),
                                    real_stint_lap
                                ))
    return states

def bellman_update(V, state, track, transition_cache):
    GAMMA = 0.99
    if state.lap == track.laps:
        action = Action.STAY_OUT
        outcomes = transition_distribution(transition_cache, state, action, track, samples=20)
        expected_value = sum(reward for (_, reward) in outcomes) / len(outcomes)
        return expected_value
    best_value = -inf 
    for action in Action:
        outcomes = transition_distribution(transition_cache, state, action, track, samples=20)
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
        # print(f"On iteration {iteration}")
        delta = 0
        for x, state in enumerate(states):
            if iteration == 0 and x % 1000 == 0:
                print(f"state {x} of {len(states)}")
            state_tuple = state.state_to_tuple()
            new_value = bellman_update(V, state, track, transition_cache)
            if abs(V[state_tuple] - new_value) > delta:
                delta = abs(V[state_tuple] - new_value)
                delta_state = state_tuple
            # delta = max(delta, abs(V[state_tuple] - new_value))
            V[state_tuple] = new_value
        print(iteration, delta_state, delta)
        if delta < THRESHOLD:
            return V, transition_cache

def get_optimal_policy(V, track, transition_cache):
    GAMMA = 0.99
    policy = {}
    states = generate_states(track)
    for x, state in enumerate(states):
        print(f"optimal policy: state {x} of {len(states)}")
        if state.lap == track.laps:
            policy[state.state_to_tuple()] = Action.STAY_OUT
            continue
        best_action = None
        best_value = -inf
        for action in Action:
            outcomes = transition_distribution(transition_cache, state, action, track, samples=20)
            expected_value = 0
            for (next_state_tuple, reward) in outcomes:
                expected_value += (reward + GAMMA * V[next_state_tuple]) / len(outcomes)
            if expected_value > best_value:
                best_value = expected_value
                best_action = action
        policy[state.state_to_tuple()] = best_action
    return policy

def get_optimal_start_tyre(V):
    initial_states = []
    for tyre_compound_id in range(3):
        initial_states.append(DiscreteState(
            lap=1,
            tyre_compound_id=tyre_compound_id,
            wear_bin=0,
            fuel_bin=9,
            stint_lap_bin=0,
            safety_car_flag=0,
            allowed_pit_strategy=False,
            continuous_wear=0,
            continuous_fuel=109.999,
            real_stint_lap=0
        ))
    best_state = max(initial_states, key=lambda s: V[s.state_to_tuple()])
    return ["Soft", "Medium", "Hard"][best_state.tyre_compound_id]

def train_and_save_policy(track):
    print(f"Training optimal policy for {track.name}")
    V, transition_cache = iterate_until_convergence(track, {})
    optimal_policy = get_optimal_policy(V, track, transition_cache)
    optimal_start_tyre = get_optimal_start_tyre(V)
    makedirs("policies", exist_ok=True)
    path = f"policies/{track.name.lower()}_policy.pkl"
    object_to_save = {"policy": optimal_policy, "start tyre": optimal_start_tyre}
    with open(path, "wb") as f:
        dump(object_to_save, f)
    print(f"Saved optimal policy for {track.name} to {path}. Optimal start tyre: {optimal_start_tyre}")
    return optimal_policy, optimal_start_tyre
