from collections import deque
from src.graph import Graph
from src.job import Job

class TabuGraph(Graph):
    def __init__(self, processing_times: list[int], due_dates: list[int],
                 precedences: list[tuple[int, int]], schedule: list[int],
                 weights: list[int] | None=None):
        super().__init__(processing_times=processing_times,
                         due_dates=due_dates, precedences=precedences,
                         schedule=schedule, weights=weights)

    def __calculate_tardiness_sum(self, schedule: list[int]) -> int:
        '''
        Calculate the tardiness sum for a given schedule.

        Parameters:
        - schedule (list[int]): Job order to evaluate

        Returns:
        - int: The total tardiness for the given schedule
        '''
        completion_time = 0
        tardiness = 0
        for job in map(lambda job_index: self.jobs[job_index], schedule):
            completion_time += job.processing_time
            tardiness += job.weight * max(0, completion_time - job.due_date)
        return tardiness

    def __check_valid_swap(self, schedule_index: int) -> bool:
        '''
        Check if a swap of jobs at adjacent indices is valid (does not violate precedence constraints embedded in the)
        DAG.

        Parameters:
        - schedule_index (int): Index of the job in the schedule to check for a valid swap with the next job

        Returns:
        - bool: True if swap is valid; False otherwise
        '''
        prev_job, next_job = self.schedule[schedule_index], self.schedule[schedule_index + 1]

        # Check for precedence violation
        if self.adj_matrix[next_job][prev_job]:
            print(f"Invalid schedule: {prev_job} should precede {next_job}. Schedule: {self.schedule}")
            return False

        return not self.adj_matrix[prev_job][next_job]

    def validate_schedule(self) -> bool:
        '''
        Validates the current schedule against precedence constraints.

        Returns:
        - bool: True if schedule is valid; False otherwise
        '''
        for src in range(self.num_jobs):
            for dst in range(self.num_jobs):
                if self.adj_matrix[src][dst] and self.schedule.index(src) > self.schedule.index(dst):
                    return False
        return True

    def schedule_jobs(self, list_length: int, max_iterations: int, tolerance: int):
        '''
        Tabu search minimizing tardiness sum.

        Parameters:
        - list_length (int): Max length of tabu list
        - max_iterations (int): Max number of iterations for the search
        - tolerance (int): Tolerance level for accepting worse solutions

        Updates:
        - self.schedule: Updates to the best-found schedule.
        '''
        tabu_list = deque(maxlen=list_length)
        x_schedule = self.schedule.copy()
        lowest_cost = self.__calculate_tardiness_sum(x_schedule)
        x_cost = lowest_cost

        for iteration in map(lambda i: i+1, range(max_iterations)):
            best_y_schedule = None
            best_y_cost = float('inf')
            best_swap_pair = None

            # Check all neighbours to find best possible valid swap at this point, greedy approach
            for schedule_index in range(self.num_jobs - 1):
                if self.__check_valid_swap(schedule_index):
                    # Confirm if this is a pair which can be swapped in this iteration
                    swap_pair = tuple(sorted([x_schedule[schedule_index], x_schedule[schedule_index + 1]]))
                    if swap_pair in tabu_list:
                        continue
                    y_schedule = x_schedule.copy()
                    y_schedule[schedule_index], y_schedule[schedule_index + 1] = y_schedule[schedule_index + 1], y_schedule[schedule_index]
                    y_cost = self.__calculate_tardiness_sum(y_schedule)

                    # If improvement over best cost this iteration, update best cost, schedule and swap pair
                    if y_cost < best_y_cost:
                        best_y_cost, best_y_schedule = y_cost, y_schedule.copy()
                        best_swap_pair = swap_pair

            if best_y_schedule:
                delta = x_cost - best_y_cost
                if best_y_cost < lowest_cost or (delta > -tolerance and best_swap_pair not in tabu_list):
                    x_cost, x_schedule = best_y_cost, best_y_schedule.copy()
            else:
                print(f"Terminating at iteration {iteration}, no valid swaps found.")
                return

            # Update tabu list and best-known solution if improved
            tabu_list.append(best_swap_pair)
            if x_cost < lowest_cost:
                print(f"New best solution found at iteration {iteration}: {x_cost} for schedule: {x_schedule}")
                lowest_cost, self.schedule = x_cost, x_schedule.copy()
