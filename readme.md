# Minimal blocking sets of PG(2, q)

The goal of this project is to construct an algorithm that can find minimal and minimul blocking
sets of PG(2, q) matrix.

This is achieved by using Tabu search algorithm. In the project two variations of the algorithm can
be found, **tabu_search.py** and **tabu_search_improved.py**

The **tabu_search.py** can be thought as a basic implementation of this method, and the improved version
finds the minimal and minimul blocking sets of the PG(2, 11), that was given for the algorithm.

## Blockings sets

### Difference between minimal and mimimum blocking sets.

A minimal blocking set refers to a set of points in a projective geometrical space (or any other space) such
that removing any point from the set would result in a configuration that no longer blocks all the lines in 
the given space. Meaning that the minimal blocking set is the smallest set of points that still blocks all the
lines in the geometrical space.

A minimum blocking set refers to a minimal blocking set with the fewest possible number of points. It is the 
smallest possible minimal blocking set in terms of cardinality, number of points. In a nutshell, minimum blocking
set is the smallest minimal blocking set among all possible minimal blocking sets.


## Example output

When executing for example the **tabu_search_improved.py** with ```python tabu_search_improved.py``` you will see an
output like this:
```
Best Blocking Set found: {(9, 10), (4, 4), (4, 0), (0, 4), (6, 1), (10, 7), (5, 1), (3, 0), (10, 0), (6, 10), (7, 2), (1, 6)}
Minimal Blocking Sets found: {((9, 10), (4, 4), (4, 0), (0, 4), (6, 1), (10, 7), (5, 1), (3, 0), (10, 0), (6, 10), (7, 2), (1, 6))}
Minimum Blocking Set found: ((9, 10), (4, 4), (4, 0), (0, 4), (6, 1), (10, 7), (5, 1), (3, 0), (10, 0), (6, 10), (7, 2), (1, 6))

```

This displays the set of points that the Tabu Search algorithm considers to be the best blocking set. In this case, the set
of points is represented as a tuple ```(x, y)``` indicating its coordinates. 

In this case the output indicates that the Tabu Search algorithm found a single minimal blocking set, which is considered
the best blocking set and the minimum blocking set found. 