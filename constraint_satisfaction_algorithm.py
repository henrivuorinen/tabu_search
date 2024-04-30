# NOTE THAT THIS IS STILL AN EXPERIMENTAL AND NOT A FINISHED CODE
from itertools import permutations

# Define constants
Q = 11  # Field size
N_POINTS = Q ** 2 + Q + 1  # Number of points in PG(2, 11)
N_LINES = N_POINTS + Q + 1  # Number of lines in PG(2, 11)

# Function to generate PG(2, q) matrix
def generate_PG_matrix(q):
    points = [(x, y) for x in range(q) for y in range(q)]
    lines = []
    for point in points:
        x, y = point
        for i in range(q):
            lines.append([(x, (i - x) % q), ((i, y), point)])  # Changed this line
    return points, lines

# Function to check if a subset forms a minimal blocking set
def is_blocking_set(subset, lines):
    # Implement this function based on the definition of a minimal blocking set
    for line in lines:
        intersection = [point for point in line if point in subset]
        if len(intersection) == 0:
            return False
    return True

# Function to check if a subset has a non-trivial automorphism group
def has_non_trivial_automorphism_group(subset):
    # Implement this function based on the definition of non-trivial automorphism group
    if len(subset) <= 1:
        # Trivial automorphism group for subset of size 0 or 1
        return False
    original_set = set(subset)
    for perm in permutations(subset):
        if set(perm) == original_set:
            # Found a non-trivial automorphism
            return True
    # No non-trivial automorphims found
    return False

# Function to perform constraint propagation
def propagate_constraints(subset, lines):
    # Implement constraint propagation techniques to reduce the search space
    # Check if adding the last added point to the subset violates any constrains
    if not is_blocking_set(subset, lines):
        return False # Violates the blocking set property
    if has_non_trivial_automorphism_group(subset):
        return False # Violates the non-trivial automorphism group property
    return True

# Function to search for solutions using backtracking
def backtracking_search(subset):
    # Implement backtracking search algorithm to explore the search space
    if len(subset) == desired_size:
        if is_blocking_set(subset, lines) and has_non_trivial_automorphism_group(subset):
            solutions.append(subset)
        return
    for point in points:
        new_subset = subset.union({point})
        if propagate_constraints(new_subset):
            backtracking_search(new_subset)

# Main function to generate minimal blocking sets with non-trivial automorphism groups
def generate_minimal_blocking_sets():
    points, lines = generate_PG_matrix(Q)
    solutions = []

    def backtrack(subset):
        if len(subset) == desired_size:
            if is_blocking_set(subset, lines) and has_non_trivial_automorphism_group(subset):
                solutions.append(subset)
            return
        for point in points:
            new_subset = subset.union({point})
            if propagate_constraints(new_subset, lines):
                backtrack(new_subset)

    for point in points:
        backtrack({point})

    return solutions

# Example usage
desired_size = Q + 1  # Size of minimal blocking sets
solutions = generate_minimal_blocking_sets()
for sol in solutions:
    print(sol)
