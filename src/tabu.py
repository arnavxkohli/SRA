from collections import deque
from src.graph import Graph
from src.job import Job

class TabuGraph(Graph):
    def __init__(self, jobs: list[Job], edges: list[tuple[int, int]], schedule: list[int]):
        super().__init__(jobs, edges, schedule)

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
            tardiness += max(0, completion_time - job.due_date)
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

        for _ in range(max_iterations):
            found_neighbour = False
            schedule_index = 0

            while not found_neighbour and schedule_index < self.num_jobs - 1:
                if self.__check_valid_swap(schedule_index):
                    y_schedule = x_schedule.copy()
                    y_schedule[schedule_index], y_schedule[schedule_index + 1] = y_schedule[schedule_index + 1], y_schedule[schedule_index]
                    y_cost = self.__calculate_tardiness_sum(y_schedule)
                    delta = x_cost - y_cost

                    # Accept if:
                    # 1. Improves on best-known solution (aspiration criterion)
                    # 2. OR: Not tabu and within tolerance
                    swap_pair = tuple(sorted([x_schedule[schedule_index], x_schedule[schedule_index + 1]]))
                    if y_cost < lowest_cost or (delta > -tolerance and swap_pair not in tabu_list):
                        x_cost, x_schedule = y_cost, y_schedule.copy()
                        found_neighbour = True

                if not found_neighbour:
                    schedule_index += 1

            if not found_neighbour:
                return

            # Update tabu list and best-known solution if improved
            tabu_list.append(tuple(sorted([x_schedule[schedule_index], x_schedule[schedule_index + 1]])))
            if x_cost < lowest_cost:
                lowest_cost, self.schedule = x_cost, x_schedule.copy()
