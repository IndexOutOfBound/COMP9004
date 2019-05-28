# Wealthy Distribution Model

## Team member

- Rui Zhao : 860411
- Weikai Zeng : 893814
- Yang Zhang: 956835
  
## Doc Structure

- `./src` : source code folder
  - `Simulator.py` : Run this file to simulate the Wealthy Distribution Model
  - `default.conf`: Default configuration for parameters.
  - `World.py`: Class of the original World object
  - `People.py`: Class of the original people object
  - `WorldExtension.py` Class of the extend world object
  - `PeopleExtension.py` Class of the extend people obect
  - `./result`: 
    - `result.csv`: The result for a single simulation. 1st row is each tickets' gini index. 2nd row is each ticket's number of rich. 3rd row is each ticket's number of middle. 4th row is each ticket's number of poor.
    - `lorenz_result.csv`: The lorenz points for each ticket.
    - `Experiment_data.csv`: The result of Experiment.
    - `class_plot.png`: The line chart for the poor, the middle and the rich number.
    - `gini_index.png`: The line chart for the Gini index
    - `lorenz_{i}`: the lorenz curve for ticket _{i}_
- `./data`: Several pre-exported data from NetLogo.

## Dependencies

This Model need `python3` and packages: `numpy` and `matplotlib`

## Running Simulation

run `Simulator.py` or add some extra options.

```
python3 src/Simulator.py
```

### Parameters

```
-h --help           help info
-c --clock [int]    running times, default == 1000
-l --lorenz [int]   save lorenz graph, The var is the step when store
-i --id [int]       Load a predefined configuration under <../data/> and compare.Otherwise it will load the default.conf
-e --extend         Compare the result of original and extend model
```

## Running Experiment

Run `Experiment.py` or add some extra options.

```
python3 src/Experiment.py
```

### Options

```
-h --help            help info 
-l --loop [integer]  running times for each group of parameters, default=1
-s --step [integer]  step for change parameter, default=1
```