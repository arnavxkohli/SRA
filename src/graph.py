from src.job import Job
from typing import List, Tuple


class Graph:
    def __init__(self, processing_times: List[int], due_dates: List[int],
                 precedences: List[Tuple[int, int]],
                 schedule: List[int] =None,
                 weights: List[int]=None,
                 log_file_path: str=None) -> None:

        self.jobs = [Job(p, d) for p, d in zip(processing_times, due_dates)]
        if weights is not None:
            for i, weight in enumerate(weights):
                self.jobs[i].weight = weight
        self.num_jobs = len(self.jobs)
        self.precedences = precedences

        self.log_file = open(log_file_path, "w") if log_file_path else None

        # Adjacency matrix initialization
        self.adj_matrix = [[0] * self.num_jobs for _ in range(self.num_jobs)]

        # Build the adjacency matrix and track successors
        for src, dst in precedences:
            self.adj_matrix[src][dst] = 1

        if schedule is None:
            self.schedule = []
        else:
            self.schedule = schedule

    def schedule_jobs(self):
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.log_file:
            self.log_file.close()
