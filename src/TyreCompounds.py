class TyreCompound:
    def __init__(self, name, lap_time_multiplier, wear_rate):
        self.name = name
        self.lap_time_multiplier = lap_time_multiplier
        self.wear_rate = wear_rate

    

SOFT = TyreCompound("Soft", lap_time_multiplier=1.0, wear_rate=0.035)
MEDIUM = TyreCompound("Medium", lap_time_multiplier=1.004, wear_rate=0.024)
HARD = TyreCompound("Hard", lap_time_multiplier=1.01, wear_rate=0.018)