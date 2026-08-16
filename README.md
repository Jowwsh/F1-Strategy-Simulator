# F1 Strategy Simulator

## Project Intro

This project will calculate the best strategy for an F1 race using a variety of different pieces of data, including tyre wear, fuel loads and lap counts, finding optimal pit windows and tyre choices
The core of this project is a Markov Decision Process and value iteration, to find the optimal policy (strategy) under uncertainty

## Planned Features

* Varied, and extensive input data
* Lap-by-lap transition model
* Use of MDPs
* Basic UI
* Database usage
* Using real world data

## Project Roadmap

I plan to build this in an agile manner, producing multiple prototypes from the ground up. 
The first prototype is simply be a brute force search, a one-stop strategy, linear models, and no regard to tyre compounds
Further prototypes will use better models, calculate when to push or conserve fuel and tyres, have multiple stops with different tyre compounds, and use MDPs as the main strategy search engine

**Current Status: Completed first prototype**

## Testing

This project uses Python's built-in unittest framework.
Tests cover the transition model (tyre wear, fuel load, lap time, pit stops)
to ensure the simulation behaves predictably before strategy search is implemented

![Passing transition model tests](docs/img/transition_model_tests_pass.png)

## Prototype 1 Strategy Search

The simulator performs a brute-force linear search over all possible pit laps
It assumes only one pit stop, and does not consider different tyre compounds
The race is simulated using a lap-by-lap transition model, the total race time is recorded
The strategy with the lowest total time is selected

## How to run

python main.py

## Prototype 1 example output

![Prototype 1 strategy search output](docs/img/prototype_1_example_output.png)
