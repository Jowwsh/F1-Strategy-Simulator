from src.Actions import Action
from src.RaceState import RaceState
from src.TyreCompounds import SOFT, MEDIUM, HARD

def tyre_wear(race_state, action):
    wear_rate = race_state.tyre_compound.wear_rate
    PUSH_MULTIPLIER = 2
    if action == Action.PUSH:
        race_state.tyre_wear += wear_rate * race_state.tyre_compound.calculate_wear_multiplier(race_state.tyre_wear, race_state.fuel_load) * PUSH_MULTIPLIER
    else:
        race_state.tyre_wear += wear_rate * race_state.tyre_compound.calculate_wear_multiplier(race_state.tyre_wear, race_state.fuel_load)
    if race_state.tyre_wear <= 1:
        race_state.tyre_wear = round(race_state.tyre_wear, 7)
    else:
        race_state.tyre_wear = 1

def decrease_fuel(race_state, action):
    MAX_FUEL = 110
    BASE_FUEL_RATE = 100 / race_state.total_laps
    PUSH_MULTIPLIER = 1.5
    if action == Action.PUSH:
        race_state.fuel_load -= BASE_FUEL_RATE * race_state.tyre_compound.fuel_multiplier * (1.15 - (race_state.fuel_load / MAX_FUEL) * 0.3) * PUSH_MULTIPLIER
    else:
        race_state.fuel_load -= BASE_FUEL_RATE * race_state.tyre_compound.fuel_multiplier * (1.15 - (race_state.fuel_load / MAX_FUEL) * 0.3)
    if race_state.fuel_load <= 0:
        race_state.dnf = True



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
    decrease_fuel(race_state, action)
    lap_time = compute_lap_time(race_state, action)
    race_state.current_lap += 1
    race_state.lap_time_history.append(lap_time)
    return lap_time



