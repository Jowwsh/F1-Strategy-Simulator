from src.RaceState import RaceState
from src.Actions import Action
from src.TransitionModel import apply_action
from src.TyreCompounds import SOFT, MEDIUM, HARD


def simulate_race(race_state):
    start_tyres = race_state.tyre_compound
    pit_laps = [x[0] for x in race_state.pit_stops]
    for lap in range(1, race_state.total_laps+1):
        if lap in pit_laps:
            lap_time = apply_action(race_state, Action.PIT)
        else:
            lap_time = apply_action(race_state, Action.NORMAL)
        if race_state.dnf:
            return (99999999999999999, start_tyres, race_state)
    return (sum(race_state.lap_time_history), start_tyres, race_state)

def generate_strategies():
    strategies = []
    TYRES = [SOFT, MEDIUM, HARD]
    strategies += [[tyre1, tyre2] for tyre1 in TYRES for tyre2 in TYRES if tyre1 != tyre2]
    strategies += [[tyre1, tyre2, tyre3] for tyre1 in TYRES for tyre2 in TYRES for tyre3 in TYRES if not(tyre1 == tyre2 == tyre3)]
    strategies += [[tyre1, tyre2, tyre3, tyre4] for tyre1 in TYRES for tyre2 in TYRES for tyre3 in TYRES for tyre4 in TYRES if not(tyre1 == tyre2 == tyre3 == tyre4)]
    return strategies

def find_best_strategy(track):
    MAX_FUEL = 110
    total_laps = track.laps
    race_info = []
    strategies = generate_strategies()
    strategies = [[MEDIUM, HARD]]
    for i, strategy in enumerate(strategies):
        print(f"On strategy {i+1} out of {len(strategies)}")
        # one stop
        if len(strategy) == 2:
            for pit_lap in range(1, total_laps):
                race_state = RaceState(1, total_laps, strategy[0], 0, MAX_FUEL, [], [(pit_lap, strategy[1])], 1, False, 0, track)
                race_info.append(simulate_race(race_state))
        # two stops
        elif len(strategy) == 3:
            for pit_lap_1 in range(1, total_laps-1):
                for pit_lap_2 in range(pit_lap_1+1, total_laps):
                    race_state = RaceState(1, total_laps, strategy[0], 0, MAX_FUEL, [], [(pit_lap_1, strategy[1]), (pit_lap_2, strategy[2])], 1, False, 0, track)
                    race_info.append(simulate_race(race_state))
        # 3 stops
        else:
            for pit_lap_1 in range(1, total_laps-2):
                for pit_lap_2 in range(pit_lap_1+1, total_laps-1):
                    for pit_lap_3 in range(pit_lap_2+1, total_laps):
                        race_state = RaceState(1, total_laps, strategy[0], 0, MAX_FUEL, [], [(pit_lap_1, strategy[1]), (pit_lap_2, strategy[2]), (pit_lap_3, strategy[3])], 1, False, 0, track)
                        race_info.append(simulate_race(race_state))
                        

    best_time, best_start_tyres, best_race_state = min(race_info, key=lambda x : x[0])
    return best_time, best_start_tyres, best_race_state



