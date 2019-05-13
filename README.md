# Running
```
$ python src/Simulator.py
```

**Parameters**
```
-h --help 	 help info
-c --clock 	 running times, default == 100
-g --graph 	 Generate graph results with this parameter
```

# Result
- `lorenz_result.csv`: Each clock's lorenz curve points.
- `gini_result.csv`: Each clock's gini index.
- `graph/gini_index.jpg`: the gini_index's graph for wholr simulation
- `graph/lorenz_{i}`: the lorenz curve for clock _{i}_