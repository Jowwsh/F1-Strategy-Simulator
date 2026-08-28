# Design Overview

## The race state

* The race state is what tracks the different parameters of the race at any given time.
* In the first prototype, this included the current lap, total laps, current tyre compound, tyre wear and fuel load
* It has been expanded to include lap time history, pit stop strategy, the stint number, a DNF flag, and the stint length
* It is updated per lap, based on its current value, and action being taken by the racing driver, which is decided by the strategy choice

## Actions

* Actions are what the race driver is currently doing
* I used an enum to make this clean, and more error-proof
* These include just normal racing, pushing, and pitting in the first prototype

## The transition model

* This is the code that updates the race state lap by lap
* I separated this code into multiple standalone functions, to assist with readability and testing
* It firstly updates tyre wear. The first prototype of this used a linear model, but it now uses the non-linear model described in the **Tyre wear models** section
* It also considers whether the driver was pushing or pitting, increasing or resetting tyre wear automatically
* The first fuel model was a linear model, but is now modelled as described in **Fuel burn models**
* Computing the lap time takes a base lap time, then adds penalties for tyre wear, fuel load and pit stops. These multipliers were picked the multipliers for these based on average real F1 values
* Additional penalties are added for colder tyres after a recent pit stop or race start, and general degradation over long stints, different for each tyre compound
* The lap count is then incremented by one

## The time formatter

* This is a simple function that converts time in the form seconds.milliseconds into hours:minutes:seconds.milliseconds, using modulus and floor division operations
* This is done before the full race time is printed for readability

## Tyre compounds

* The soft, medium and hard tyre compounds are constant objects of the `TyreCompound` class
* They have different curves for tyre wear, multipliers for fuel burn, and lap time multipliers, all as attributes

## Tracks

* The simulator can currently find the optimal strategy on five different F1 tracks: Monaco, Monza, Silverstone, Bahrain, and Spa
* Each track has the following attributes: name, base lap time, total laps, grip, evolution rate, tyre wear factor, and fuel factor
* Grip is a divisor of total lap time, so higher grip means a faster lap
* The evolution rate is a divisor of lap time that increases with respect to the current lap, simulating how an F1 track gets faster as rubber from the tyres is laid down
* The tyre wear factor is a multiplier influencing how much each track wears out the tyres - Spa wears much more than Monaco, for example
* Fuel factor is a multiplier defining how much fuel is burned per lap - Monza burns more fuel than Monaco for example, meaning pushing at Monza is more risky
* The current values are representative, but not entirely realistic. This is to create a variety of different types of tracks

## Randomness

* In order for an MDP to be viable as opposed to a brute force search, the transitions between states (laps) must feature stochastic elements
* Lap time has been given random noise, using a gaussian distribution. The standard deviation of this distribution depends on the tyre choice, with softer tyres having more variance
* Tyre wear has also been modified with the addition of a uniform distribution to the base tyre wear, simulating the realism tyre wear in F1
* Safety cars have a set probability to appear each lap, dependent on the chosen track. They then last between 2 and 5 laps
* Safety cars increase base lap time (but decrease lap time variance), decrease tyre wear and fuel burn, and importantly, reduce pit stop time
* I tested these probabilities and effects by running simulations many times to confirm the expected value was accurate, and analysing the lap times.

## The strategy search

### First prototype
* The first prototype of the strategy search is a linear brute-force search, to achieve a minimum viable product (MVP)
* It finds the optimum pit stop lap by simulating a full race with each possible pit stop lap, and finding the one with the minimum time
* It only changes between the actions NORMAL and PIT
* It simulates a race using the transition model for each lap, therefore is making the same linear modelling assumptions as previously discussed
* It returns a tuple with the best full race time, and the corresponding best pit lap
* This tuple is then formatted and printed by main.py

### Second prototype
* The second prototype is still a linear brute-force search, but searches many more strategies (over 15 million for a 50 lap race)
* It tests one, two and three stop strategies, and the usage of soft, medium and hard compound tyres, all with different stats
* This greatly expands the search space. In particular, all possible three stop strategies can take time to search through
* It has no form of pruning, searching strategies that clearly are bad, for example pitting in the first 3 laps of the race, then not pitting for the rest of the race on soft tyres
* It still only distinguishes between the actions NORMAL and PIT, not accounting for pushing. It still uses linear modelling assumptions
* It returns a tuple containing the best full race time, the starting tyre for the optimal strategy, and the full race state (containing lap time history and details of pit stops)
* It works by generating all possible tyre strategies, then simulating a full racw with every pit lap combination on every tyre strategy
* This tuple is formatted and printed by main.py

## Mathematical modelling

### Tyre wear models
* The first model for tyre wear was linear, increasing by the same amount each lap
* The improved tyre wear model uses compound-specific exponential curves
* Each compound has a base wear amount, a lap-time multiplier, and a set curve steepness
* The tyre compound class has a function `calculate_wear_multiplier()`
* This function uses the current tyre wear, and current fuel load, to output a tyre wear multiplier
* Tyre wear is modelled exponentially based on existing tyre wear. It is then multiplied with a fuel multiplier, which is also created through an exponential curve
* These multipliers are then also multiplied with a set multiplier if the car is in push mode
* This simulates tyre 'cliffs' the effect of heavy fuel increasing tyre wear, and further distinguishes between the different compounds, increasing the realism of the simulator

### Fuel burn models
* The first model for fuel burn was also linear
* Fuel is now burnt in a non-linear fashion. It depends on how much fuel is already in the tank, choice of tyre, and if the driver is in push mode
* Less fuel means a lighter car which means less fuel is burnt per lap
* Softer tyres and pushing means more aggressive driving which increases fuel consumption
* Tyre compounds store this fuel burn multiplier as an attribute
* Pushing increases fuel burn multiplicatively, which in combination with the non-linear model means pushing early burns significantly more fuel than pushing late in the race
* If in a race simulation the car runs out of fuel, a flag is raised in the `RaceState` class, which then records that strategy as invalid with a race time of 99999999999999999
* The cars are fuelled with 110kg in this model, and will use 100kg if they do not push, and on the medium tyre. 10kg is reserved for pushing and softer compounds
* This strategically makes pushing late in the race more efficient, and pushing too hard at the start can mean you run out of fuel, but will decrease tyre wear for the rest of the race