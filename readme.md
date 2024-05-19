# Tabu Search for blocking sets in Projective Geometry PG(2,11)

## Overview
This project implements Tabu Search algorithm to find unique blocking sets in the projective plane PG(2,11). The
algorithm identifies blocking sets of various sizes and ensures that each blocking set is unique.

## Usage
Clone the repository to your machine with ```git clone https://github.com/henrivuorinen/tabu_search/tree/master```. 
then run the script with ```python tabu_search_improved.py```. 

### Output
The script will output a number of unique blocking sets found for each size within the specific range.

## Functions
### generate_PG_matrix()
This function generates the points and lines of the projective plane PG(2,q).
```
Parameters: q (int) - The order of the projective plane
Returns: A tuple containing a list of points and list of lines.
```

### score_blocking_set()
Scores blocking set based on how many lines it blocks
```
Parameters:
    - blocking_set: (List[Tuple[int, int, int]]) - the blocking set.
    - lines: (List(List[Tuple[int, int, int]]]) - The lines of the projective plane.

Returns: The score of the blocking set (int).
```

### uncovered_lines_count()
Counts the number of uncovered lines by a blocking set.

```
Parameters:
    - blocking_set: (List[Tuple[int, int, int]]) - The blocking set
    - lines: (List[List[Tuple[int, int, int]]]) - The lines of the projective plane.
    
Returns: The number of uncovered lines (int).
```

### is_valid_blocking_set()
Checks if blocking set is valid.
```
Parameters:
    - blocking_set: (List[Tuple[int, int, int]]) - The blocking set.
    - lines: (List[List[Tuple[int, int, int]]])- The lines of the projective plane.
    
Returns: Boolean indicating whether the blocking set is valid.
```

### generate_initial_solution()
Generates an initial solution for the Tabu Search.

```
Parameters:
    - points: (List[Tuple[int, int, int]]) - The points of the projective plane.
    - lines: (List[List[Tuple[int, int, int]]]) - The lines of the projective plane.
    - target_size: (int) - The target size for the initial solution.
    
Returns: A list representing the initial solution
```

### generate_neighborhood()
Generates a neighborhood of solutions for the Tabu Search
```
Parameters:
    - solution: (List[Tuple[int, int, int]]) - The current solution.
    - points: (List[Tuple[int, int, int]]) - The points of the projective plane.
    - lines: (List[List[Tuple[int, int, int]]]) - The lines of the projective plane.
    - target_size: (int) - The target size for solutions.
    - sample_size: (int) - The number of solutions in the neighborhood.
    
Returns: A list of solutions representing the neighborhood.
```

### tabu_search_random_start(points:List[Tuple[int, int, int]], lines:List[List[Tuple[int, int, int]]], target_size:int,
tabu_tenure:int=10, max_iteration:int=1000)
Performs the tabu search to find a blocking set
```
Parameters:
    - points: (List[Tuple[int, int, int]]) - points of the projective plane
    - lines: (List[List[Tuple[int, int, int]]])- lines of the projective plane
    - target_size: (int) - target size for the blocking set
    - tabu_tenure: (int) - tabu tenure, the length of the tabu list.
    - max_iteration: (int) - maximum number of iterations.
    
Returns: A list representing the best blocking set found.
```

### explore_blocking_set_size(points, lines, min_size, max_size, max_time)
Explores blocking sets of various sizes within a specified time limit.
```
Parameters:
    - points: (List[Tuple[int, int, int]]) - point of the projective plane.
    - lines: (List[List[Tuple[int, int, int]]]) - lines of the projective plane.
    - min_size : (int) - maximum size for blocking sets.
    - min_size: (int) - minimum size for blocking ests.
    - max_time: (int) - maximum time for the search in seconds.
    
Returns: A dictinonary with blocking set sizes as keys and the counts of unique blocking sets found as values.
```

## Parameters
`min_size` : Minimum size of blocking sets to explore.
`max_size` : Maximum size of blocking sets to explore.
`max_time` : Maximum time (seconds) to run the search.

## Output
The script will output the number of unique blocking sets found for each size within the specific range.

```
Generated 133 points and 1320 lines.
Starting tabu search for target size 23, iteration 1
Generated initial solution of size 23.
Generated neighborhood of size 100.
...
Blocking set of size 23 found for target size 23.
Size 12 blocking sets found: 0
Size 13 blocking sets found: 0
Size 14 blocking sets found: 0
Size 15 blocking sets found: 0
Size 16 blocking sets found: 22
Size 17 blocking sets found: 23
Size 18 blocking sets found: 21
Size 19 blocking sets found: 21
Size 20 blocking sets found: 22
Size 21 blocking sets found: 18
Size 22 blocking sets found: 27
Size 23 blocking sets found: 23
Size 24 blocking sets found: 19
```

## License
This project is licensed under the MIT License - see the License file for details