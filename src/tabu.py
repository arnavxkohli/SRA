from collections import deque
from src.graph import Graph
import matplotlib.pyplot as plt


class TabuGraph(Graph):

    def __init__(self,
                 processing_times: list[int],
                 due_dates: list[int],
                 precedences: list[tuple[int, int]],
                 schedule: list[int] | None=None,
                 weights: list[int] | None=None,
                 log_file_path: str | None=None) -> None:
        super().__init__(processing_times=processing_times,
                         due_dates=due_dates,
                         precedences=precedences,
                         schedule=schedule,
                         weights=weights,
                         log_file_path=log_file_path)
        if self.log_file:
            if schedule is None:
                schedule = self.generate_initial_schedule()
                self.schedule = schedule
            self.log_file.write(f"Tabu search initialized with schedule: {[s+1 for s in schedule]}\n")

    def __calculate_tardiness_sum(self, schedule: list[int]) -> int:
        completion_time, tardiness = 0, 0

        for job in map(lambda job_index: self.jobs[job_index], schedule):
            completion_time += job.processing_time
            tardiness += job.weight * max(0, completion_time - job.due_date)
        return tardiness

    def generate_initial_schedule(self) -> list[int]:
        # Topological Sort
        initial_schedule = []

        in_degree = [0] * self.num_jobs
        for src, dst in self.precedences:
            in_degree[dst] += 1

        # Start with jobs that have no depdendencies
        queue = deque([i for i in range(self.num_jobs) if in_degree[i] == 0])

        while queue:
            current_job = queue.popleft()
            initial_schedule.append(current_job)

            for src, dst in self.precedences:
                if src == current_job:
                    in_degree[dst] -= 1
                    if in_degree[dst] == 0:
                        queue.append(dst)

        if len(initial_schedule) != self.num_jobs:
            raise ValueError("Precedences are cyclic, cannot generate valid initial schedule")

        # Logically shouldn't happen, but just in case
        if any(initial_schedule.index(src) > initial_schedule.index(dst) for src, dst in self.precedences):
            raise ValueError("Invalid initial schedule")

        self.schedule = initial_schedule

        return initial_schedule

    def __is_valid_swap(self, schedule: list[int], i: int, j: int) -> bool:
        test_schedule = schedule.copy()

        if any(test_schedule.index(src) > test_schedule.index(dst) for src, dst in self.precedences):
            raise ValueError("Something went wrong, ran into invalid schedule pre-swap")

        test_schedule[i], test_schedule[j] = test_schedule[j], test_schedule[i]

        return all(test_schedule.index(src) < test_schedule.index(dst) for src, dst in self.precedences)

    def get_interchanges(self, previous_interchange: int | None=None) -> list[tuple[int, int]]:
        interchanges = [(i, i+1) for i in range(self.num_jobs - 1)]

        return interchanges[previous_interchange+1:] + \
            interchanges[:previous_interchange+1] if previous_interchange \
                is not None else interchanges

    def schedule_jobs(self, list_length: int, max_iterations: int,
                      tolerance: int) -> None:
        if self.log_file:
            self.log_file.write(f"List Length: {list_length}, Iterations: {max_iterations}, Tolerance: {tolerance}\n\n")

        # Basic setup
        tabu_list = deque(maxlen=list_length)
        best_schedule = self.schedule.copy()
        best_tardiness = self.__calculate_tardiness_sum(best_schedule)
        current_schedule = best_schedule.copy()
        current_tardiness = best_tardiness
        previous_interchange = None

        for iteration in range(max_iterations):
            aspiration_criteria_met = False

            # Use previous interchange to find the next possible interchanges in cyclic manner
            interchanges = self.get_interchanges(previous_interchange)
            swap_pair = None

            # Find the first valid swap
            for i, j in interchanges:
                if self.__is_valid_swap(current_schedule, i, j):
                    new_schedule = current_schedule.copy()
                    new_schedule[i], new_schedule[j] = new_schedule[j], new_schedule[i]
                    new_tardiness = self.__calculate_tardiness_sum(new_schedule)
                    swap_pair = tuple(sorted([new_schedule[i], new_schedule[j]]))
                    aspiration_criteria_met = new_tardiness < best_tardiness

                    if (current_tardiness - new_tardiness > -tolerance and swap_pair not in tabu_list) or aspiration_criteria_met:
                        current_tardiness = new_tardiness
                        current_schedule = new_schedule.copy()
                        previous_interchange = i
                        break

            # If no valid swap, terminate
            if swap_pair is None:
                text = f"Iteration {iteration + 1}: No interchange found, terminating\n"
                if self.log_file:
                    self.log_file.write(text)
                else:
                    print(text)
                break

            # Update best schedule if necessary
            if current_tardiness < best_tardiness:
                text = f"Iteration {iteration + 1}: New best tardiness: {current_tardiness} with schedule: {[s+1 for s in current_schedule]}\n"
                if self.log_file:
                    self.log_file.write(text)
                else:
                    print(text)
                best_tardiness = current_tardiness
                best_schedule = current_schedule.copy()

            # Update tabu list only if the swap is not already in the list (so that no duplicate entries are made)
            if not aspiration_criteria_met or swap_pair not in tabu_list:
                tabu_list.append(swap_pair)

        if self.log_file:
            self.log_file.write(f"\nBest schedule found: {[s+1 for s in best_schedule]}\n")
            self.log_file.write(f"Best tardiness: {best_tardiness}\n")

        self.schedule = best_schedule

    def plot_schedule(self) -> None:
        list_lengths, tolerances = [(i * 5) for i in range(1, 40)], [(i) for i in range(1, 101)]
        initial_schedule = self.schedule.copy()

        list_length_tardiness, tolerance_tardiness = [], []

        for list_length in list_lengths:
            self.schedule_jobs(list_length=list_length, max_iterations=1000, tolerance=10)
            list_length_tardiness.append(self.__calculate_tardiness_sum(self.schedule))
            self.schedule = initial_schedule.copy()

        for tolerance in tolerances:
            self.schedule_jobs(list_length=20, max_iterations=1000, tolerance=tolerance)
            tolerance_tardiness.append(self.__calculate_tardiness_sum(self.schedule))
            self.schedule = initial_schedule.copy()

        plt.figure(figsize=(10, 6))
        plt.plot(list_lengths, list_length_tardiness)
        plt.title('Tardiness vs List Length')
        plt.xlabel('List Length')
        plt.ylabel('Total Tardiness')
        plt.tight_layout()
        plt.savefig('out/tabu_list_length_plot.png')
        plt.close()

        plt.figure(figsize=(10, 6))
        plt.plot(tolerances, tolerance_tardiness)
        plt.title('Tardiness vs Tolerance')
        plt.xlabel('Tolerance')
        plt.ylabel('Total Tardiness')
        plt.tight_layout()
        plt.savefig('out/tabu_tolerance_plot.png')
        plt.close()
