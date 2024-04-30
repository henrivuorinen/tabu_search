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
            lines.append([(x, (i - x) % q), ((i, y), point)])  # Changed this line
    return points, lines


# Check if a set of points forms a minimal blocking set
def is_blocking_set(points, lines):
    """
    Check if a set of points forms a minimal blocking set.

    Args:
        points (list): List of points.
        lines (list): List of lines.

    Returns:
        bool: True if the set of points forms a minimal blocking set, False otherwise.
    """
    for line in lines:
        intersection = [point for point in line if point in points]
        if len(intersection) == 0:
            return False
    return True


# Function to generate an initial solution
def initial_solution(points):
    """
    Generate an initial solution (random set of points).

    Args:
        points (list): List of points.

    Returns:
        set: Random set of points.
    """
    return set(random.sample(points, Q + 1))


# Function to generate neighboring solutions
def generate_neighbors(solution, points):
    """
    Generate neighboring solutions by applying small modifications to the current solution.

    Args:
        solution (set): Current solution (set of points).
        points (list): List of points.

    Returns:
        list: List of neighboring solutions.
    """
    neighbors = []
    for point in points:
        neighbor = solution.symmetric_difference({point})
        if len(neighbor) <= Q + 1:
            neighbors.append(neighbor)
    return neighbors


# Function to evaluate the quality of a solution (minimal blocking set)
def evaluate_solution(solution, lines):
    """
    Evaluate the quality of a solution by checking if it forms a minimal blocking set.
    :param solution: The solution to evaluate set of points
    :param lines: List of lines
    :return: bool: True if the solution forms a minimal blocking set, False otherwise.
    """
    # Check if solution forms a blocking set
    if not is_blocking_set(solution, lines):
        return False
    # Check if solution is minimal
    for point in solution:
        if is_blocking_set(solution - {point}, lines):
            return False
    return True


# Tabu search function
def tabu_search(max_iterations):
    """
    Implement the Tabu Search algorithm to find a minimal blocking set.

    Args:
        max_iterations (int): Maximum number of iterations.

    Returns:
        tuple: Best solution found (minimal blocking set), set of all minimal blocking sets, and minimum blocking set found.
    """
    points, lines = generate_PG_matrix(Q)
    current_solution = initial_solution(points)
    best_solution = current_solution
    minimal_blocking_sets = set()
    minimal_blocking_sets.add(tuple(best_solution))
    min_blocking_set = tuple(best_solution.copy())
    tabu_list = []
    tabu_tenure = 6  # Tabu tenure parameter

    iteration = 0
    while iteration < max_iterations:
        neighbors = generate_neighbors(current_solution, points)
        best_neighbor = None
        best_neighbor_eval = float('inf')

        for neighbor in neighbors:
            if neighbor not in tabu_list:
                neighbor_eval = evaluate_solution(neighbor, lines)
                if neighbor_eval:
                    if len(neighbor) < len(best_solution) or neighbor == best_solution:
                        best_neighbor = neighbor
                        best_neighbor_eval = len(neighbor)
                    if neighbor not in minimal_blocking_sets:
                        minimal_blocking_sets.add(neighbor)
                        if len(neighbor) < len(min_blocking_set):
                            min_blocking_set = neighbor

        if best_neighbor is not None:
            current_solution = best_neighbor
            tabu_list.append(best_neighbor)
            if len(tabu_list) > tabu_tenure:
                tabu_list.pop(0)
            if len(best_neighbor) < len(best_solution):
                best_solution = best_neighbor

        iteration += 1

    return best_solution, minimal_blocking_sets, min_blocking_set


# Example usage:
best_solution, minimal_blocking_sets, min_blocking_set = tabu_search(max_iterations=5000)

print("Best Blocking Set found:", best_solution)
print("Minimal Blocking Sets found:", minimal_blocking_sets)
print("Minimum Blocking Set found:", min_blocking_set)
