from src.StrategySearch import find_best_strategy
from src.TimeFormatter import format_secs

if __name__ == "__main__":
    total_time, pit_lap = find_best_strategy(total_laps=50)
    print(f"Best strategy: Pit on lap {pit_lap}\nTotal time: {format_secs(total_time)}")