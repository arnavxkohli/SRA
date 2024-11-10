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
        self.list_length = list_length

        self.tabu_list = deque(maxlen=self.list_length)

    def __calculate_tardiness_sum(self):
        completion_time = 0
        tardiness = 0
        for job in self.schedule:
            completion_time += job.processing_time
            tardiness += max(0, completion_time - job.due_date)
        return tardiness

    def __check_valid_swap(self, left_job: int, right_job: int):
        position_map = {job: i for i, job in enumerate(self.schedule)}
        # Perform the swap
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
