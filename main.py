from src.StrategySearch import find_best_strategy
from src.TimeFormatter import format_secs
from src.Tracks import MONACO, MONZA, SILVERSTONE, BAHRAIN, SPA
from src.ValueIteration import *
from src.MDPController import simulate_policy
from pickle import load

if __name__ == "__main__":
    # policy, start_tyre = train_and_save_policy(track=SPA)
    with open("policies/spa_policy.pkl", "rb") as f:
        data = load(f)
    policy = data["policy"]
    start_tyre = data["start tyre"]
    print("loaded policy")
    race_state = simulate_policy(track=SPA, policy=policy, start_tyre_name=start_tyre)
    pit_strategy = race_state.pit_stops
    print(pit_strategy)
    print("\n")
    print(f"{race_state.total_laps} laps around {race_state.track.name}")
    print(f"\nBest strategy: {len(pit_strategy)} stop strategy\nStart on {start_tyre} tyres")
    for i in range(0, len(pit_strategy)):
        print(f"Pit on lap {pit_strategy[i][0]} for {pit_strategy[i][1]} tyres")
    # if len(pit_strategy) >= 2:
    #     print(f"Pit on lap {pit_strategy[1][0]} for {pit_strategy[1][1]} tyres")
    # if len(pit_strategy) >= 3:
    #     print(f"Pit on lap {pit_strategy[2][0]} for {pit_strategy[2][1]} tyres")
    # if len(pit_strategy) >= 4:
    #     print(f"Pit on lap {pit_strategy[3][0]} for {pit_strategy[3][1]} tyres")
    print(f"Total time: {format_secs(sum(race_state.lap_time_history))}\n")
    print("Lap time history:")
    print(race_state.lap_time_history)

