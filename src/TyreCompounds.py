class TyreCompound:
    def __init__(self, name, lap_time_multiplier, wear_rate, curve_rate):
        self.name = name
        self.lap_time_multiplier = lap_time_multiplier
        self.wear_rate = wear_rate
        self.curve_rate = curve_rate

    def calculate_wear_multiplier(self, current_wear, current_fuel):
        fuel_multiplier = 0.9 * (11/9)**(current_fuel/100)
        tyre_multiplier = self.curve_rate**current_wear
        wear_multiplier = fuel_multiplier * tyre_multiplier
        return wear_multiplier

    

SOFT = TyreCompound("Soft", lap_time_multiplier=1.002, wear_rate=0.035, curve_rate = 3)
MEDIUM = TyreCompound("Medium", lap_time_multiplier=1.004, wear_rate=0.024, curve_rate = 2.2)
HARD = TyreCompound("Hard", lap_time_multiplier=1.01, wear_rate=0.018, curve_rate = 1.7)