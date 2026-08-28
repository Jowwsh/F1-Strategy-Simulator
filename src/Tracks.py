class Track:

    def __init__(self, name, base_lap_time, laps, grip, evolution_rate, tyre_wear_factor, fuel_factor, sc_probability):
        self.name = name
        self.base_lap_time = base_lap_time
        self.laps = laps
        self.grip = grip
        self.evolution_rate = evolution_rate
        self.tyre_wear_factor = tyre_wear_factor
        self.fuel_factor = fuel_factor
        self.sc_probability = sc_probability

MONACO = Track(name="Monaco", base_lap_time=72, laps=78, grip=0.94, evolution_rate=0.015, tyre_wear_factor=0.75, fuel_factor=0.85, sc_probability=0.06)
MONZA = Track(name="Monza", base_lap_time=80, laps=53, grip=1.02, evolution_rate=0.010, tyre_wear_factor=0.90, fuel_factor=1.25, sc_probability=0.02)
SILVERSTONE = Track(name="Silverstone", base_lap_time=88, laps=52, grip=1.05, evolution_rate=0.025, tyre_wear_factor=1.25, fuel_factor=1.05, sc_probability=0.035)
BAHRAIN = Track(name="Bahrain", base_lap_time=92, laps=57, grip=1.00, evolution_rate=0.020, tyre_wear_factor=1.10, fuel_factor=1.10, sc_probability=0.03)
SPA = Track(name="Spa", base_lap_time=100, laps=44, grip=1.03, evolution_rate=0.030, tyre_wear_factor=1.30, fuel_factor=1.15, sc_probability=0.025)