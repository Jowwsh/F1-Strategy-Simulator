from src.Actions import Action
from src.RaceState import RaceState

def tyre_wear(race_state, action):
    wear_rate = race_state.tyre_compound.wear_rate
    PUSH_MULTIPLIER = 2
    if action == Action.PUSH:
        race_state.tyre_wear += wear_rate * PUSH_MULTIPLIER
    else:
        race_state.tyre_wear += wear_rate
    race_state.tyre_wear = round(race_state.tyre_wear, 7)

def decrease_fuel(race_state):
    FUEL_RATE = 100 / race_state.total_laps
    race_state.fuel_load -= FUEL_RATE

def pit_stop(race_state, lap_time):
        PIT_STOP_TIME = 23
        lap_time += PIT_STOP_TIME
        race_state.tyre_compound = race_state.pit_stops[race_state.stint_num-1][1]
        race_state.stint_num += 1
        race_state.tyre_wear = 0
        return lap_time


def compute_lap_time(race_state, action):
    BASE_LAP_TIME = 90
    TYRE_WEAR_PENALTY = 2.85
    FUEL_PENALTY = 0.03
    PUSH_TIME_SAVE = 1
    lap_time = BASE_LAP_TIME
    lap_time += race_state.tyre_wear * TYRE_WEAR_PENALTY
    lap_time += race_state.fuel_load * FUEL_PENALTY
    lap_time *= race_state.tyre_compound.lap_time_multiplier
    if action == Action.PUSH:
        lap_time -= PUSH_TIME_SAVE
    if action == Action.PIT:
        lap_time = pit_stop(race_state, lap_time)
    return round(lap_time, 7)
        

def apply_action(race_state, action):
    tyre_wear(race_state, action)
    decrease_fuel(race_state)
    lap_time = compute_lap_time(race_state, action)
    race_state.current_lap += 1
    race_state.lap_time_history.append(lap_time)
    return lap_time



