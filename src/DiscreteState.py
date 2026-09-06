class DiscreteState:

    def __init__(self, lap, tyre_compound_id, wear_bin, fuel_bin, stint_lap, safety_car_flag):
        self.lap = lap
        self.tyre_compound_id = tyre_compound_id
        self.wear_bin = wear_bin
        self.fuel_bin = fuel_bin
        self.stint_lap = stint_lap
        self.safety_car_flag = safety_car_flag

    def state_to_tuple(self):
        return (self.lap, self.tyre_compound_id, self.wear_bin, self.fuel_bin, self.stint_lap, self.safety_car_flag)


