class TyreCompound:
    def __init__(self, name, lap_time_multiplier, wear_rate, curve_rate, fuel_multiplier, warmup_penalty, stint_decay_laps, lap_time_sigma):
        self.name = name
        self.lap_time_multiplier = lap_time_multiplier
        self.wear_rate = wear_rate
        self.curve_rate = curve_rate
        self.fuel_multiplier = fuel_multiplier
        self.warmup_penalty = warmup_penalty
        self.stint_decay_laps = stint_decay_laps
        self.lap_time_sigma = lap_time_sigma

    def calculate_wear_multiplier(self, current_wear, current_fuel):
        fuel_multiplier = 0.9 * (11/9)**(current_fuel/110)
        tyre_multiplier = self.curve_rate**current_wear
        wear_multiplier = fuel_multiplier * tyre_multiplier
        return wear_multiplier

    

SOFT = TyreCompound("Soft", lap_time_multiplier=1.000, wear_rate=0.035, curve_rate=3, fuel_multiplier=1.01, warmup_penalty=[1.5], stint_decay_laps=5, lap_time_sigma=0.1)
MEDIUM = TyreCompound("Medium", lap_time_multiplier=1.006, wear_rate=0.024, curve_rate=2.2, fuel_multiplier=1.00, warmup_penalty=[2, 0.5], stint_decay_laps=8, lap_time_sigma=0.075)
HARD = TyreCompound("Hard", lap_time_multiplier=1.01, wear_rate=0.018, curve_rate=1.7, fuel_multiplier=0.99, warmup_penalty=[2.5, 1.2, 0.3], stint_decay_laps=10, lap_time_sigma=0.05)