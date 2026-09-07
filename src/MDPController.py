from src.DiscreteState import DiscreteState
from src.RaceState import RaceState
from src.TransitionModel import apply_action
from src.TyreCompounds import SOFT, MEDIUM, HARD

def discretise_wear(wear):
    wear_bin = int(wear * 3)
    return min(max(wear_bin, 0), 9)

def discretise_fuel(fuel_load):
    MAX_FUEL = 109.999
    fuel_bin = int(fuel_load * (9/MAX_FUEL))
    return min(max(fuel_bin, 0), 9)


def discrete_to_race_state(discrete_state, track):
    tyre = [SOFT, MEDIUM, HARD][discrete_state.tyre_compound_id]
    return RaceState (
        current_lap=discrete_state.lap,
        total_laps=track.laps,
        tyre_compound=tyre,
        tyre_wear=discrete_state.continuous_wear,
        fuel_load=discrete_state.continuous_fuel,
        lap_time_history=[],
        pit_stops=None,
        stint_num=None,
        dnf=False,
        stint_length=discrete_state.real_stint_lap,
        track=track,
        safety_car=bool(discrete_state.safety_car_flag),
        allowed_pit_strategy=discrete_state.allowed_pit_strategy,
        is_final_lap=discrete_state.is_final_lap
    )

def race_to_discrete_state(race_state):
    tyre_id = {"Soft": 0, "Medium": 1, "Hard": 2}[race_state.tyre_compound.name]
    return DiscreteState(
        lap=race_state.current_lap,
        tyre_compound_id=tyre_id,
        wear_bin=discretise_wear(race_state.tyre_wear),
        fuel_bin=discretise_fuel(race_state.fuel_load),
        stint_lap_bin=min(race_state.stint_length // 8, race_state.total_laps // 8),
        safety_car_flag=int(race_state.safety_car),
        allowed_pit_strategy=race_state.allowed_pit_strategy,
        continuous_wear=race_state.tyre_wear,
        continuous_fuel=race_state.fuel_load,
        real_stint_lap=race_state.stint_length,
        is_final_lap=race_state.is_final_lap
    )

def calculate_reward(lap_time, dnf):
    if dnf:
        return -1000
    return -lap_time

def transition(discrete_state, action, track):
    race_state = discrete_to_race_state(discrete_state, track)
    lap_time = apply_action(race_state, action)
    next_state = race_to_discrete_state(race_state)
    reward = calculate_reward(lap_time, race_state.dnf)
    return (next_state, reward)

def transition_distribution(transition_cache, state, action, track, samples=200):
    
    key = (state.state_to_tuple(), action)
    if key in transition_cache:
        return transition_cache[key]
    outcomes = []
    for _ in range(samples):
        next_state, reward = transition(state, action, track)
        outcomes.append((next_state.state_to_tuple(), reward))
    transition_cache[key] = outcomes
    return outcomes