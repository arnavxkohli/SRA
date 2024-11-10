from src.job import Job


class Graph:
    def __init__(self, jobs: list[Job], edges: list[tuple[int, int]]):
        self.jobs = jobs
        self.num_jobs = len(jobs)

        # Adjacency matrix initialization
        self.adj_matrix = [[0] * self.num_jobs for _ in range(self.num_jobs)]

        # Build the adjacency matrix and track successors
        for src, dst in edges:
            self.adj_matrix[src][dst] = 1

        self.schedule = []

    def schedule_jobs(self):
        raise NotImplementedError
