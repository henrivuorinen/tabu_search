from typing import List, Tuple, Set
import random
import time

def generate_PG_matrix(q: int) -> Tuple[List[Tuple[int, int, int]], List[List[Tuple[int, int, int]]]]:
    points = [(x, y, 1) for x in range(q) for y in range(q)]
    points.extend([(x, 1, 0) for x in range(q)])
    points.append((1, 0, 0))

    lines = []
    for a in range(q):
        for b in range(q):
            if a == 0 and b == 0:
                continue
            for c in range(q):
                line = [point for point in points if (a * point[0] + b * point[1] + c * point[2]) % q == 0]
                lines.append(line)

    print(f"Generated {len(points)} points and {len(lines)} lines.")
    return points, lines

def uncovered_lines_count(blocking_set: Set[Tuple[int, int, int]], lines: List[List[Tuple[int, int, int]]]) -> int:
    return sum(1 for line in lines if not any(point in blocking_set for point in line))

def is_valid_blocking_set(blocking_set: Set[Tuple[int, int, int]], lines: List[List[Tuple[int, int, int]]]) -> bool:
    return all(any(point in blocking_set for point in line) for line in lines)

def cost_function(blocking_set: Set[Tuple[int, int, int]], lines: List[List[Tuple[int, int, int]]]) -> float:
    uncovered = uncovered_lines_count(blocking_set, lines)
    return uncovered  # Only penalize for uncovered lines

def ensure_minimality(blocking_set: Set[Tuple[int, int, int]], lines: List[List[Tuple[int, int, int]]]) -> Set[Tuple[int, int, int]]:
    for point in list(blocking_set):
        temp_set = blocking_set.copy()
        temp_set.remove(point)
        if is_valid_blocking_set(temp_set, lines):
            blocking_set.remove(point)
    return blocking_set

def generate_initial_solution(points: List[Tuple[int, int, int]], target_size: int) -> Set[Tuple[int, int, int]]:
    random.shuffle(points)
    initial_solution = set(points[:target_size])
    print(f"Generated initial solution of size {target_size}.")
    return initial_solution

def generate_neighborhood(solution: Set[Tuple[int, int, int]], points: List[Tuple[int, int, int]], sample_size: int) -> List[Set[Tuple[int, int, int]]]:
    neighborhood = []
    points_list = list(points)
    for _ in range(sample_size):
        new_solution = solution.copy()
        num_changes = random.randint(1, 3)
        for _ in range(num_changes):
            if random.random() < 0.5 and len(new_solution) > 0:
                point_to_remove = random.choice(list(new_solution))
                new_solution.remove(point_to_remove)
            point_to_add = random.choice(points_list)
            new_solution.add(point_to_add)
        neighborhood.append(new_solution)
    neighborhood.sort(key=lambda sol: cost_function(sol, lines))
    print(f"Generated neighborhood of size {sample_size}.")
    return neighborhood

def tabu_search_random_start(points: List[Tuple[int, int, int]], lines: List[List[Tuple[int, int, int]]], target_size: int, tabu_tenure: int = 10, max_iterations: int = 100) -> Tuple[Set[Tuple[int, int, int]], bool]:
    current_solution = generate_initial_solution(points, target_size)
    best_solution = ensure_minimality(current_solution.copy(), lines)
    best_cost = cost_function(best_solution, lines)
    tabu_set = set()
    no_improvement_iterations = 0

    for iteration in range(max_iterations):
        if is_valid_blocking_set(best_solution, lines):
            return best_solution, True

        neighborhood_size = max(10, 100 - 10 * (iteration // 10))
        neighborhood = generate_neighborhood(current_solution, points, neighborhood_size)
        neighborhood = [sol for sol in neighborhood if frozenset(sol) not in tabu_set]

        if not neighborhood:
            break

        best_neighbor = ensure_minimality(neighborhood[0], lines)
        best_neighbor_cost = cost_function(best_neighbor, lines)

        if best_neighbor_cost < best_cost:
            best_solution = best_neighbor.copy()
            best_cost = best_neighbor_cost
            no_improvement_iterations = 0  # Reset no improvement counter
        else:
            no_improvement_iterations += 1

        current_solution = best_neighbor.copy()
        tabu_set.add(frozenset(best_neighbor))
        if len(tabu_set) > tabu_tenure:
            tabu_set.pop()

        # Adjust Tabu Tenure based on improvement
        if no_improvement_iterations > 10:
            tabu_tenure = min(20, tabu_tenure + 1)  # Increase tenure if no improvement
        else:
            tabu_tenure = max(5, tabu_tenure - 1)  # Decrease tenure if improvement found

        print(f"Iteration {iteration + 1}/{max_iterations}, best cost: {best_cost}")

    print(f"Tabu search completed with best solution size {len(best_solution)} after {iteration + 1} iterations.")
    return best_solution, is_valid_blocking_set(best_solution, lines)


def explore_blocking_set_sizes(points, lines, min_size, max_size, max_time):
    min_target_size = 16
    max_target_size = 36

    start_time = time.time()
    blocking_set_counts = {size: 0 for size in range(min_size, max_size + 1)}
    found_blocking_sets: Set[Tuple[Tuple[int, int, int], ...]] = set()

    iteration = 0
    while time.time() - start_time < max_time:
        target_size = min_size + (iteration % (max_size - min_size + 1))
        print(f"Starting tabu search for target size {target_size}, iteration {iteration + 1}")

        blocking_set, found = tabu_search_random_start(points, lines, target_size=target_size, tabu_tenure=10,
                                                       max_iterations=100)

        if found:
            blocking_set = ensure_minimality(blocking_set, lines)  # Ensure minimality before storing
            blocking_set_tuple = tuple(sorted(blocking_set))
            if len(blocking_set) >= min_target_size and blocking_set_tuple not in found_blocking_sets:
                found_blocking_sets.add(blocking_set_tuple)

                # Dynamically adjust the dictionary to include new sizes
                if len(blocking_set) not in blocking_set_counts:
                    blocking_set_counts[len(blocking_set)] = 0

                blocking_set_counts[len(blocking_set)] += 1
                print(f"Blocking set of size {len(blocking_set)} found for target size {target_size}. Total found: {blocking_set_counts[len(blocking_set)]}")
            else:
                if blocking_set_tuple in found_blocking_sets:
                    print(f"Duplicate blocking set of size {len(blocking_set)} found and skipped.")
                else:
                    print(f"Found solution of size {len(blocking_set)} is too small, skipping.")

        iteration += 1

    return blocking_set_counts

if __name__ == "__main__":
    points, lines = generate_PG_matrix(11)
    min_size = 16
    max_size = 36
    max_time = 3600  # Run for 3 hours

    blocking_set_counts = explore_blocking_set_sizes(points, lines, min_size, max_size, max_time)

    for size, count in blocking_set_counts.items():
        print(f"Size {size} blocking sets found: {count}")