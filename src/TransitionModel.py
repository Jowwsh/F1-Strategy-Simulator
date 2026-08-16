from src.Actions import Action
from src.RaceState import RaceState

def tyre_wear(race_state, action):
    WEAR_RATE = 0.035
    PUSH_MULTIPLIER = 2
    if action == Action.PIT:
        race_state.tyre_wear = 0
    elif action == Action.PUSH:
        race_state.tyre_wear += WEAR_RATE * PUSH_MULTIPLIER
    else:
        race_state.tyre_wear += WEAR_RATE
    race_state.tyre_wear = round(race_state.tyre_wear, 7)

def decrease_fuel(race_state):
    FUEL_RATE = 2
    race_state.fuel_load -= FUEL_RATE

def compute_lap_time(race_state, action):
    BASE_LAP_TIME = 90
    TYRE_WEAR_PENALTY = 2.85
    FUEL_PENALTY = 0.03
    PUSH_TIME_SAVE = 1
    PIT_STOP_TIME = 23
    lap_time = BASE_LAP_TIME = 90
    lap_time += race_state.tyre_wear * TYRE_WEAR_PENALTY
    lap_time += race_state.fuel_load * FUEL_PENALTY
    if action == Action.PUSH:
        lap_time -= PUSH_TIME_SAVE
    if action == Action.PIT:
        lap_time += PIT_STOP_TIME
        race_state.pit_stops.append(race_state.current_lap)
    return round(lap_time, 7)
        

def apply_action(race_state, action):
    tyre_wear(race_state, action)
    decrease_fuel(race_state)
    lap_time = compute_lap_time(race_state, action)
    race_state.current_lap += 1
    return lap_time



