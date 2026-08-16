# Design Overview

## The race state

* The race state is what tracks the different parameters of the race at any given time.
* In the first prototype, this includes the current lap, total laps, current tyre compound, tyre wear and fuel load
* It is updated per lap, based on its current value, and action being taken by the racing driver, which is decided by the strategy choice

## Actions

* Actions are what the race driver is currently doing
* I used an enum to make this clean, and more error-proof
* These include just normal racing, pushing, and pitting in the first prototype

## The transition model

* This is the code that updates the race state lap by lap
* I separated this code into multiple standalone functions, to assist with readability and testing
* It firstly updates tyre wear. As of the first prototype, this uses a linear model, with a constant wear rate that I chose that represents an average wear rate per lap, represented as a decimal.
* It also considers whether the driver was pushing or pitting, increasing or resetting tyre wear automatically. It does not consider tyre compounds yet.
* The fuel load transition is currently very simple, decreasing fuel linearly always, and fuel is ensured to never run out
* Computing the lap time takes a base lap time, then adds penalties for tyre wear, fuel load and pit stops. I picked the multipliers for these based on average real F1 values, but they do not evolve over time
* The lap count is then incremented by one


