from src.RaceState import RaceState
from src.Actions import Action
from src.TransitionModel import apply_action


def find_best_strategy(total_laps=50):
    total_times = []
    for pit_lap in range(1, total_laps):
        race_state = RaceState(1, total_laps, "medium", 0, 100, [], [])
        for lap in range(1, total_laps+1):
            if lap == pit_lap:
                apply_action(race_state, Action.PIT)
            else:
                apply_action(race_state, Action.NORMAL)
        total_times.append(sum(race_state.lap_time_history))
    best_time = min(total_times)
    best_pit_lap = total_times.index(best_time) + 1
    return best_time, best_pit_lap


    
