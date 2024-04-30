import numpy as np
import random

# Constants
Q = 11  # Field size
N_POINTS = Q ** 2 + Q + 1  # Number of points in PG(2, 11)
N_LINES = N_POINTS + Q + 1  # Number of lines in PG(2, 11)


# Generate PG(2, q) matrix
def generate_PG_matrix(q):
    """
    Generate points and lines of PG(2, q) projective geometry space.
    Args:
        q (int): Field size.
    Returns:
        tuple: Tuple containing lists of points and lines.
    """
    points = []
    for x in range(q):
        for y in range(q):
            points.append((x, y))
    lines = []
    for point in points:
        x, y = point
        for i in range(q):
            lines.append([(x, (i - x) % q), ((i, y), point)])
    return points, lines

"""points, lines = generate_PG_matrix(Q)

print("Points:")
for point in points:
    print(point)

# Print lines
print("\nLines:")
for line in lines:
    print(line)"""


# Check if a set of points forms a minimal blocking set
def is_blocking_set(points, lines):
    """
    Check if a set of points forms a minimal blocking set

    Args:
        points (list): List of points
        lines (list): List of lines
    Returns:
        bool: True if the set of points form a minimal blocking set, False otherwise.
    """
    for line in lines:
        intersection = [point for point in line if point in points]
        if len(intersection) == 0:
            return False
    return True


# Function to generate an initial solution
def initial_solution():
    """
    Generate an initial solution, a random set of points.
    Returns:
        set: Random set of points.
    """
    return set(random.sample(points, Q + 1))


# Function to generate neighboring solutions
def generate_neighbors(solution):
    """
    Generate neighboring solutions by applying small modifications to the solution to the current solution.

    Args:
        solution (set): Current solution, set of points.

    Returns:
        list: List of neighboring solutions.
    """
    neighbors = []
    for point in points:
        neighbor = solution.symmetric_difference({point})
        if len(neighbor) <= Q + 1:
            neighbors.append(neighbor)
    return neighbors


# Function to evaluate the quality of a solution
def evaluate_solution(solution):
    """
    Evaluate the quality of a solution by checking if it forms a minimal blocking set.

    Args:
        solution (set): Solution to evaluate (set of points).

    Returns:
        bool: True if the solution forms a minimal blocking set, False otherwise.
    """
    return is_blocking_set(solution, lines)


# Tabu search function
def tabu_search(max_iterations):
    """
    Implement the Tabu Search Algorithm to find a minimal blocking set.

    Args:
        max_iterations (int): Maximum number of iterations.

    Returns:
        set: Best solution found (minimal blocking set)
    """
    current_solution = initial_solution() # Holds the current solution found by the algorithm
    best_solution = current_solution # initially the best solution os set to the current solution
    tabu_list = [] # List to keep track of recent explored solutions
    tabu_tenure = 5  # Tabu tenure parameter, determines how long a solution remains in the tabu list.

    iteration = 0
    while iteration < max_iterations: # Algorithm iterates until a maximum number of iterations is reached.
        neighbors = generate_neighbors(current_solution) # generates neighboring solutions by applying small modifications to the current solution
        best_neighbor = None
        best_neighbor_eval = float('inf')
        best_neighbor_size = float('inf')

        for neighbor in neighbors: # iterate through the neighbors and evaluates each one.
            if neighbor not in tabu_list: # If a neighbor is not in the tabu list, its evaluation value is computed
                neighbor_eval = evaluate_solution(neighbor)
                neighbor_size = len(neighbor)
                # Update best neighbor if it has better evaluation value or smaller size
                # The algorithm selects the neighbor with the best evaluation value. If two neighbors have the same evaluation value, it selects the one with the smaller size.
                if neighbor_eval and (neighbor_eval < best_neighbor_eval or
                                      (neighbor_eval == best_neighbor_eval and neighbor_size < best_neighbor_size)):
                    best_neighbor = neighbor
                    best_neighbor_eval = neighbor_eval
                    best_neighbor_size = neighbor_size

        if best_neighbor is not None:
            current_solution = best_neighbor # if a best neighbor is found, the current solution is updated
            tabu_list.append(best_neighbor) # the best neighbor is added to tabu list. If the list exceeds maximum size, oldest solution is removed.
            if len(tabu_list) > tabu_tenure:
                tabu_list.pop(0)
            if len(best_neighbor) < len(best_solution):
                best_solution = best_neighbor

        iteration += 1 # incremented at the end of each iteration.

    return best_solution # returns the best solution after completing the specified number of iterations.



# Generate PG(2, 11) matrix
points, lines = generate_PG_matrix(Q)

# Example usage:
best_solution = tabu_search(max_iterations=10000)
print("Minimal Blocking Set found:", best_solution)
