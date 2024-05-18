from typing import List, Tuple
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

def score_blocking_set(blocking_set: List[Tuple[int, int, int]], lines: List[List[Tuple[int, int, int]]]) -> int:
    return sum(1 for line in lines if any(point in blocking_set for point in line))

def uncovered_lines_count(blocking_set: List[Tuple[int, int, int]], lines: List[List[Tuple[int, int, int]]]) -> int:
    blocking_set_set = set(blocking_set)
    return sum(1 for line in lines if not any(point in blocking_set_set for point in line))

def is_valid_blocking_set(blocking_set: List[Tuple[int, int, int]], lines: List[List[Tuple[int, int, int]]]) -> bool:
    blocking_set_set = set(blocking_set)
    return all(any(point in blocking_set_set for point in line) for line in lines)

def generate_initial_solution(points: List[Tuple[int, int, int]], lines: List[List[Tuple[int, int, int]]], target_size: int) -> List[Tuple[int, int, int]]:
    potential_points = sorted(points, key=lambda p: -sum(p in line for line in lines))
    initial_solution = potential_points[:target_size]
    print(f"Generated initial solution of size {target_size}.")
    return initial_solution

def generate_neighborhood(solution: List[Tuple[int, int, int]], points: List[Tuple[int, int, int]], lines: List[List[Tuple[int, int, int]]], target_size: int, sample_size: int) -> List[List[Tuple[int, int, int]]]:
    neighborhood = []
    solution_set = set(solution)
    for _ in range(sample_size):
        new_solution = solution[:]
        num_changes = random.randint(1, 3)
        for _ in range(num_changes):
            point_to_remove = random.choice(new_solution)
            point_to_add = random.choice([p for p in points if p not in new_solution])
            new_solution.remove(point_to_remove)
            new_solution.append(point_to_add)
        neighborhood.append(new_solution)
    neighborhood.sort(key=lambda sol: uncovered_lines_count(sol, lines))
    print(f"Generated neighborhood of size {sample_size}.")
    return neighborhood

def tabu_search_random_start(points: List[Tuple[int, int, int]], lines: List[List[Tuple[int, int, int]]], target_size: int, tabu_tenure: int = 10, max_iterations: int = 1000) -> List[Tuple[int, int, int]]:
    current_solution = generate_initial_solution(points, lines, target_size)
    best_solution = current_solution[:]
    best_score = uncovered_lines_count(best_solution, lines)
    tabu_list = []

    for iteration in range(max_iterations):
        if best_score == 0:
            break

        neighborhood_size = max(10, 100 - 10 * (iteration // 10))
        neighborhood = generate_neighborhood(current_solution, points, lines, target_size, neighborhood_size)
        neighborhood = [sol for sol in neighborhood if sol not in tabu_list]

        if not neighborhood:
            break

        best_neighbor = neighborhood[0]
        best_neighbor_score = uncovered_lines_count(best_neighbor, lines)

        if best_neighbor_score < best_score:
            best_solution = best_neighbor[:]
            best_score = best_neighbor_score

        current_solution = best_neighbor[:]
        tabu_list.append(best_neighbor)
        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)

        # Dynamic Tabu Tenure
        tabu_tenure = max(5, int(tabu_tenure * 0.9)) if best_score == 0 else min(20, tabu_tenure + 1)

        print(f"Iteration {iteration + 1}/{max_iterations}, best score: {best_score}")

    print(f"Tabu search completed with best solution size {len(best_solution)} after {iteration + 1} iterations.")
    return best_solution

def explore_blocking_set_sizes(points, lines, min_size, max_size, max_time):
    min_target_size = 16  # Minimum size of a blocking set for PG(2, 11)
    max_target_size = 24  # Your upper range

    start_time = time.time()
    blocking_set_counts = {size: 0 for size in range(min_size, max_size + 1)}

    iteration = 0
    while time.time() - start_time < max_time:
        target_size = random.randint(min_target_size, max_target_size)
        print(f"Starting tabu search for target size {target_size}, iteration {iteration + 1}")

        blocking_set = tabu_search_random_start(points, lines, target_size=target_size, tabu_tenure=10, max_iterations=100)

        if is_valid_blocking_set(blocking_set, lines):
            if len(blocking_set) >= min_target_size:
                blocking_set_counts[len(blocking_set)] += 1
                print(f"Blocking set of size {len(blocking_set)} found for target size {target_size}.")
            else:
                print(f"Found solution of size {len(blocking_set)} is too small, skipping.")

        iteration += 1

    return blocking_set_counts

if __name__ == "__main__":
    points, lines = generate_PG_matrix(11)
    min_size = 12
    max_size = 24
    max_time = 60  # in seconds

    blocking_set_counts = explore_blocking_set_sizes(points, lines, min_size, max_size, max_time)

    for size, count in blocking_set_counts.items():
        print(f"Size {size} blocking sets found: {count}")
