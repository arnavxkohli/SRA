from src.job import Job
from src.graph import Graph
from collections import deque


class TabuGraph(Graph):
    def __init__(self, jobs: list[Job], edges: list[tuple[int, int]],
                 list_length: int, max_iterations: int,
                 initial_schedule: list[int]):
        super().__init__(jobs, edges)

        self.schedule = initial_schedule
        self.max_iterations = max_iterations

        # Queue automatically flushed once the maximum length is reached
        self.tabu_list = deque(maxlen=list_length)

    def __calculate_tardiness_sum(self) -> int:
        '''
        Calculate the tardiness sum for the current schedule.

        return: int
        '''
        completion_time = 0
        tardiness = 0
        for job in self.schedule:
            completion_time += job.processing_time
            tardiness += max(0, completion_time - job.due_date)
        return tardiness

    def __check_valid_swap(self, schedule_index: int) -> bool:
        '''
        Check if a swap of the jobs at adjacent indices is valid:
        - The swap does not violate the precedence constraints between these
        two jobs.
        - The swap (unordered) is not in the tabu list.

        schedule_index: int

        return: bool
        '''
        prev_job, next_job = self.schedule[schedule_index], self.schedule[schedule_index + 1]

        if self.adj_matrix[next_job][prev_job]:
                raise ValueError("Current schedule violates precedence constraints")

        # Pair needs to be unordered - confirm this!
        if tuple(sorted([prev_job, next_job])) in self.tabu_list:
            return False

        # If the left job is a direct predecessor of the right job, the swap would cause
        # the right job to now be scheduled before the left job, violating the precedence
        return not self.adj_matrix[prev_job][next_job]

    def validate_schedule(self) -> bool:
        '''
        Utility function to check if the current schedule is valid.

        return: bool
        '''
        for src in range(self.num_jobs):
            for dst in range(self.num_jobs):
                if self.adj_matrix[src][dst] and self.schedule.index(src) > self.schedule.index(dst):
                    return False
        return True

    def schedule_jobs(self):
        return super().schedule_jobs()
