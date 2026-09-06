from src.DiscreteState import DiscreteState
from src.RaceState import RaceState
from src.TransitionModel import apply_action
from src.TyreCompounds import SOFT, MEDIUM, HARD

def discretise_wear(wear):
    return min(int(wear * 5), 15)

def discretise_fuel(fuel_load):
    MAX_FUEL = 109.999
    return min(int(fuel_load * (15/MAX_FUEL)), 15)

def discrete_to_race_state(discrete_state, track):
    MAX_FUEL = 109.999
    wear = discrete_state.wear_bin / 5
    fuel = discrete_state.fuel_bin / (15/MAX_FUEL)
    tyre = [SOFT, MEDIUM, HARD][discrete_state.tyre_compound_id]
    return RaceState (
        current_lap=discrete_state.lap,
        total_laps=track.laps,
        tyre_compound=tyre,
        tyre_wear=wear,
        fuel_load=fuel,
        lap_time_history=[],
        pit_stops=None,
        stint_num=None,
        dnf=False,
        stint_length=discrete_state.stint_lap,
        track=track,
        safety_car=bool(discrete_state.safety_car_flag)
    )

def race_to_discrete_state(race_state):
    tyre_id = {"Soft": 0, "Medium": 1, "Hard": 2}[race_state.tyre_compound.name]
    return DiscreteState(
        lap=race_state.current_lap,
        tyre_compound_id=tyre_id,
        wear_bin=discretise_wear(race_state.tyre_wear),
        fuel_bin=discretise_fuel(race_state.fuel_load),
        stint_lap=race_state.stint_length,
        safety_car_flag=int(race_state.safety_car)
    )

def calculate_reward(lap_time, dnf):
    if dnf:
        return -1000
    return -lap_time

def transition(state, action, track):
    race_state = discrete_to_race_state(state, track)
    lap_time = apply_action(race_state, action)
    next_state = race_to_discrete_state(race_state)
    reward = calculate_reward(lap_time, race_state.dnf)
    return (next_state, reward)

def transition_distribution(state, action, track, samples=20):
    outcomes = []
    for _ in range(samples):
        next_state, reward = transition(state, action, track)
        outcomes.append((next_state.state_to_tuple(), reward))
    return outcomes