class DiscreteState:

    def __init__(self, lap, tyre_compound_id, wear_bin, fuel_bin, stint_lap_bin, safety_car_flag, allowed_pit_strategy, continuous_wear, continuous_fuel, real_stint_lap):
        self.lap = lap
        self.tyre_compound_id = tyre_compound_id
        self.wear_bin = wear_bin
        self.fuel_bin = fuel_bin
        self.stint_lap_bin = stint_lap_bin
        self.safety_car_flag = safety_car_flag
        self.allowed_pit_strategy = allowed_pit_strategy
        self.continuous_wear = continuous_wear
        self.continuous_fuel = continuous_fuel
        self.real_stint_lap = real_stint_lap

    def state_to_tuple(self):
        return (self.lap, self.tyre_compound_id, self.wear_bin, self.fuel_bin, self.stint_lap_bin, self.safety_car_flag)


