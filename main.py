from src.StrategySearch import find_best_strategy
from src.TimeFormatter import format_secs
from src.Tracks import MONACO, MONZA, SILVERSTONE, BAHRAIN, SPA

if __name__ == "__main__":
    total_time, start_tyres, race_state = find_best_strategy(track=SPA)
    pit_strategy = race_state.pit_stops
    print(f"{race_state.total_laps} laps around {race_state.track.name}")
    print(f"\nBest strategy: {len(pit_strategy)} stop strategy\nStart on {start_tyres.name} tyres\nPit on lap {pit_strategy[0][0]} for {pit_strategy[0][1].name} tyres")
    if len(pit_strategy) >= 2:
        print(f"Pit on lap {pit_strategy[1][0]} for {pit_strategy[1][1].name} tyres")
    if len(pit_strategy) == 3:
        print(f"Pit on lap {pit_strategy[2][0]} for {pit_strategy[2][1].name} tyres")
    print(f"Total time: {format_secs(total_time)}\n")
    print("Lap time history:")
    print(race_state.lap_time_history)


