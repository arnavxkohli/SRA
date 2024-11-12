from src.job import Job


class Graph:
    def __init__(self, processing_times: list[int], due_dates: list[int],
                 precedences: list[tuple[int, int]],
                 schedule: list[int] | None = None,
                 weights: list[int] | None=None):
        self.jobs = [Job(p, d) for p, d in zip(processing_times, due_dates)]
        if weights is not None:
            for i, weight in enumerate(weights):
                self.jobs[i].weight = weight
        self.num_jobs = len(self.jobs)
        self.precedences = precedences

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
