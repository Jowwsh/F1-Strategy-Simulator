from src.Actions import Action
from src.RaceState import RaceState
from src.TyreCompounds import SOFT, MEDIUM, HARD

def tyre_wear(race_state, action):
    wear_rate = race_state.tyre_compound.wear_rate
    PUSH_MULTIPLIER = 2
    if action == Action.PUSH:
        race_state.tyre_wear += wear_rate * race_state.tyre_compound.calculate_wear_multiplier(race_state.tyre_wear, race_state.fuel_load) * PUSH_MULTIPLIER * race_state.track.tyre_wear_factor
    else:
        race_state.tyre_wear += wear_rate * race_state.tyre_compound.calculate_wear_multiplier(race_state.tyre_wear, race_state.fuel_load) * race_state.track.tyre_wear_factor
    if race_state.tyre_wear <= 3:
        race_state.tyre_wear = round(race_state.tyre_wear, 7)
    else:
        race_state.tyre_wear = 3

def decrease_fuel(race_state, action):
    MAX_FUEL = 110
    BASE_FUEL_RATE = (86 * race_state.track.fuel_factor) / race_state.total_laps
    PUSH_MULTIPLIER = 1.5
    if action == Action.PUSH:
        race_state.fuel_load -= BASE_FUEL_RATE * race_state.tyre_compound.fuel_multiplier * (1.15 - (race_state.fuel_load / MAX_FUEL) * 0.3) * PUSH_MULTIPLIER
    else:
        race_state.fuel_load -= BASE_FUEL_RATE * race_state.tyre_compound.fuel_multiplier * (1.15 - (race_state.fuel_load / MAX_FUEL) * 0.3)
    if race_state.fuel_load <= 0:
        race_state.fuel_load = 0
        race_state.dnf = True



def pit_stop(race_state, lap_time):
        PIT_STOP_TIME = 23
        lap_time += PIT_STOP_TIME
        race_state.tyre_compound = race_state.pit_stops[race_state.stint_num-1][1]
        race_state.stint_num += 1
        race_state.tyre_wear = 0
        race_state.stint_length = -1
        return lap_time

def tyre_warmup_penalty(race_state):
    if race_state.stint_length < len(race_state.tyre_compound.warmup_penalty):
        return race_state.tyre_compound.warmup_penalty[race_state.stint_length]
    else:
        return 0

def stint_decay_penalty(race_state):
    STINT_LENGTH_PENALTY = 0.1
    return STINT_LENGTH_PENALTY * (race_state.stint_length // race_state.tyre_compound.stint_decay_laps)

def compute_lap_time(race_state, action):
    BASE_LAP_TIME = race_state.track.base_lap_time
    TYRE_WEAR_PENALTY = 4
    FUEL_PENALTY = 0.03
    PUSH_TIME_SAVE = 1
    lap_time = BASE_LAP_TIME
    lap_time /= race_state.track.grip
    lap_time /= 1 + (race_state.current_lap / race_state.total_laps) * race_state.track.evolution_rate
    lap_time *= race_state.tyre_compound.lap_time_multiplier
    lap_time += race_state.tyre_wear * TYRE_WEAR_PENALTY
    lap_time += race_state.fuel_load * FUEL_PENALTY
    lap_time += tyre_warmup_penalty(race_state)
    lap_time += stint_decay_penalty(race_state)
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
    race_state.stint_length += 1
    race_state.lap_time_history.append(lap_time)
    return lap_time



