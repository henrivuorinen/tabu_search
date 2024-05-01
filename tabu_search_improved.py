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

def is_affine_blocking_set(points, q):
    """
    Check if a set of points forms an affine blocking set.

    Args:
        points (list): List of points.
        q (int): Field size.

    Returns:
        bool: True if the set of points forms an affine blocking set, False otherwise.
    """
    for x in range(q):
        for y in range(q):
            if (x, y) not in points and ((x, y), (x, (x - y) % q)) not in points:
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
def evaluate_solution(solution, lines, q):
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
    # Check if solution is a affine blocking set
    if not is_affine_blocking_set(solution, q):
        return False
    return True

def validate_affine_blocking_set(blocking_set, q):
    """
    Validate whether a given set of points forms an affine blocking set in PG(2, q).

    Args:
        blocking_set (set): Set of points to validate.
        q (int): Field size.

    Returns:
        bool: True if the set forms an affine blocking set, False otherwise.
    """
    # Define all affine lines in the plane
    affine_lines = []
    for x in range(q):
        for y in range(q):
            if (x, y) not in blocking_set:
                affine_lines.append([(x, y), (x, (x - y) % q)])

    # check intersection with each affine line
    for line in affine_lines:
        intersection = set(line) & blocking_set
        if not intersection: # If no intersection, its not an affine blocking set
            return False

    # check if it contains poinst in the line at in infinity
    for point in blocking_set:
        if point[1] == 0: # point lies on the line at infinity
            return False

    return True


# Tabu search function
def tabu_search(max_iterations):
    """
    Implement the Tabu Search algorithm to find both minimal blocking sets and affine blocking sets.

    Args:
        max_iterations (int): Maximum number of iterations.

    Returns:
        tuple: Best solution found (blocking set), set of all blocking sets, and minimum blocking set found.
    """
    points, lines = generate_PG_matrix(Q)
    current_solution = initial_solution(points)
    best_solution = current_solution
    blocking_sets = set()
    blocking_sets.add(tuple(best_solution))
    min_blocking_set = tuple(best_solution.copy())

    tabu_list = []  # List of tabu moves
    tabu_tenure = 6  # Initial tabu tenure parameter
    max_tabu_tenure = 10  # Maximum tabu tenure parameter
    aspiration_threshold = len(best_solution) - 1  # Aspiration criteria threshold

    iteration = 0
    while iteration < max_iterations:
        neighbors = generate_neighbors(current_solution, points)
        best_neighbor = None
        best_neighbor_eval = float('inf')

        for neighbor in neighbors:
            # Generate tabu move
            tabu_move = (current_solution - neighbor, neighbor - current_solution)
            if tabu_move not in tabu_list:
                neighbor_eval = evaluate_solution(neighbor, lines, Q)
                if neighbor_eval:
                    if len(neighbor) < len(best_solution) or neighbor == best_solution:
                        best_neighbor = neighbor
                        best_neighbor_eval = len(neighbor)
                    if neighbor not in blocking_sets:
                        blocking_sets.add(neighbor)
                        if len(neighbor) < len(min_blocking_set):
                            min_blocking_set = neighbor

        if best_neighbor is not None:
            current_solution = best_neighbor
            tabu_list.append(tabu_move)  # Add tabu move to the tabu list
            if len(tabu_list) > tabu_tenure:
                tabu_list.pop(0)  # Remove oldest tabu move from the tabu list
            if len(best_neighbor) < len(best_solution):
                best_solution = best_neighbor

        # Update tabu tenure dynamically
        if len(tabu_list) > aspiration_threshold:
            tabu_tenure = min(tabu_tenure + 1, max_tabu_tenure)
        elif tabu_tenure > 1:
            tabu_tenure -= 1

        iteration += 1

    return best_solution, blocking_sets, min_blocking_set

# Example usage:
best_solution, blocking_sets, min_blocking_set = tabu_search(max_iterations=5000)

print("Best Blocking Set found:", best_solution)
print("All Blocking Sets found:", blocking_sets)
print("Minimum Blocking Set found:", min_blocking_set)

# Validate and print affine blocking sets
affine_blocking_sets = []
for block in blocking_sets:
    if validate_affine_blocking_set(set(block), Q):
        affine_blocking_sets.append(block)

if affine_blocking_sets:
    print("\nBest Affine Blocking Set found:", affine_blocking_sets[0])  # Display the first affine blocking set found
    print("All Affine Blocking Sets found:", affine_blocking_sets)
else:
    print("\nNo Affine Blocking Sets found.")
