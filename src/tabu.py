from src.job import Job
from src.graph import Graph
from collections import deque


class TabuGraph(Graph):
    def __init__(self, jobs: list[Job], edges: list[tuple[int, int]],
                 list_length: int, max_iterations: int,
                 initial_schedule: list[int]):
        super().__init__(jobs, edges)

        self.schedule = initial_schedule

        # Initialize the predecessors and successors
        self.predecessors = [[] for _ in range(self.num_jobs)]
        self.successors = [[] for _ in range(self.num_jobs)]

        for src, dst in self.edges:
            self.successors[src].append(dst)
            self.predecessors[dst].append(src)

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

    def __check_valid_swap(self, left_index: int, right_index: int) -> bool:
        '''
        Check if a swap of the jobs at given indices if the schedule is valid:
        - The swap does not violate the precedence constraints.
        - The swap (unordered) is not in the tabu list.

        left_index: int
        right_index: int

        return: bool

        Under this convention, left_index and right_index are the indices within
        the schedule of the jobs meant to be swapped. left_job and right_job
        are the indices of jobs derived from the Job object on creation (within
        the adjacency matrix).
        '''
        position_map = {job: i for i, job in enumerate(self.schedule)}
        left_job, right_job = self.schedule[left_index], self.schedule[right_index]

        # Pair needs to be unordered - confirm this!
        if tuple(sorted([left_job, right_job])) in self.tabu_list:
            return False

        # Simulate the swap
        position_map[left_job], position_map[right_job] = position_map[right_job], position_map[left_job]

        for job in (left_job, right_job):
            # Check all predecessors of this job
            for predecessor in self.predecessors[job]:
                if position_map[predecessor] > position_map[job]:
                    return False

            # Check all successors of this job
            for successor in self.successors[job]:
                if position_map[successor] < position_map[job]:
                    return False

        return True

    def schedule_jobs(self):
        return super().schedule_jobs()
