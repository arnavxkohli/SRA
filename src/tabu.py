from collections import deque
from src.graph import Graph
from src.job import Job


class TabuGraph(Graph):
    def __init__(self, processing_times: list[int], due_dates: list[int],
                 precedences: list[tuple[int, int]], schedule: list[int],
                 weights: list[int] | None=None, aggressive: bool=False):
        super().__init__(processing_times=processing_times,
                         due_dates=due_dates, precedences=precedences,
                         schedule=schedule, weights=weights)
        # Aggression decides neighbor selection
        self.aggressive = aggressive

    def calculate_tardiness_sum(self, schedule: list[int]) -> int:
        completion_time = 0
        tardiness = 0
        for job in map(lambda job_index: self.jobs[job_index], schedule):
            completion_time += job.processing_time
            tardiness += job.weight * max(0, completion_time - job.due_date)
        return tardiness

    def is_valid_swap(self, schedule: list[int], i: int, j: int) -> bool:
        schedule[i], schedule[j] = schedule[j], schedule[i]
        # Check all possible precedences
        valid_swap = all(schedule.index(src) <= schedule.index(dst) for src, dst in self.precedences)
        schedule[i], schedule[j] = schedule[j], schedule[i]
        return valid_swap

    def get_all_neighbours(self, schedule: list[int]) -> list[tuple[list[int], tuple[int, int]]]:
        """Get all valid neighbor schedules and their corresponding swap pairs"""
        neighbors = []
        for i in range(self.num_jobs - 1):
            for j in range(i + 1, self.num_jobs):
                if self.is_valid_swap(schedule, i, j):
                    new_schedule = schedule.copy()
                    new_schedule[i], new_schedule[j] = new_schedule[j], new_schedule[i]
                    swap_pair = tuple(sorted([schedule[i], schedule[j]]))
                    neighbors.append((new_schedule, swap_pair))
        return neighbors

    def get_adjacent_neighbours(self, schedule: list[int]) -> list[tuple[list[int], tuple[int, int]]]:
        """Get all the adjacent neighbors of the current schedule and swap pairs"""
        neighbors = []
        for i in range(self.num_jobs - 1):
            if self.is_valid_swap(schedule, i, i + 1):
                new_schedule = schedule.copy()
                new_schedule[i], new_schedule[i + 1] = new_schedule[i + 1], new_schedule[i]
                swap_pair = tuple(sorted([schedule[i], schedule[i + 1]]))
                neighbors.append((new_schedule, swap_pair))
        return neighbors

    def schedule_jobs(self, list_length: int, max_iterations: int, tolerance: int):
        tabu_list = deque(maxlen=list_length)
        current_schedule = self.schedule.copy()
        current_cost = self.calculate_tardiness_sum(current_schedule)
        best_schedule = current_schedule.copy()
        best_cost = current_cost

        for iteration in range(max_iterations):
            # Depending on aggression, get neighbours
            neighbors = []
            if self.aggressive:
                neighbors = self.get_all_neighbours(current_schedule)
            else:
                neighbors = self.get_adjacent_neighbours(current_schedule)
            if not neighbors:
                print(f"Terminating at iteration {iteration}, no valid neighbors found.")
                break

            # Find best non-tabu neighbor or neighbor that beats best known solution
            best_neighbor = None
            best_neighbor_cost = float('inf')
            best_swap = None

            for neighbor_schedule, swap_pair in neighbors:
                cost = self.calculate_tardiness_sum(neighbor_schedule)

                # Accept if not tabu or if better than best known
                if swap_pair not in tabu_list or cost < best_cost:
                    # Accept moves within tolerance
                    if cost <= current_cost + tolerance and cost < best_neighbor_cost:
                        best_neighbor = neighbor_schedule
                        best_neighbor_cost = cost
                        best_swap = swap_pair

            if best_neighbor is None:
                print(f"Terminating at iteration {iteration}, no improving moves found.")
                break

            # Update current solution
            current_schedule = best_neighbor
            current_cost = best_neighbor_cost
            tabu_list.append(best_swap)

            # Update best solution if improved
            if current_cost < best_cost:
                print(f"New best solution found at iteration {iteration}: {current_cost}")
                best_cost = current_cost
                best_schedule = current_schedule.copy()
                self.schedule = best_schedule.copy()
