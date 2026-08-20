from src.StrategySearch import find_best_strategy
from src.TimeFormatter import format_secs

if __name__ == "__main__":
    total_time, start_tyres, race_state = find_best_strategy(total_laps=50)
    pit_strategy = race_state.pit_stops
    print(f"Best strategy: {len(pit_strategy)} stop strategy\nStart on {start_tyres.name} tyres\nPit on lap {pit_strategy[0][0]} for {pit_strategy[0][1].name} tyres")
    if len(pit_strategy) >= 2:
        print(f"Pit on lap {pit_strategy[1][0]} for {pit_strategy[1][1].name} tyres")
    if len(pit_strategy) == 3:
        print(f"Pit on lap {pit_strategy[2][0]} for {pit_strategy[2][1].name} tyres")
    print(f"Total time: {format_secs(total_time)}\n")


