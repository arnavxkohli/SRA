from src.job import Job
from src.graph import Graph


class LCLGraph(Graph):
    def __init__(self, processing_times: list[int], due_dates: list[int],
                 edges: list[tuple[int, int]],
                 weights: list[int] | None = None):
        '''
        Initialize LCL graph for job scheduling.

        Parameters:
        - jobs (list[Job]): List of jobs to schedule
        - edges (list[tuple[int, int]]): List of precedence relationships between jobs

        Updates:
        - self.successors: Count of successors for each job
        - self.L: Set of jobs with no successors
        '''
        super().__init__(processing_times=processing_times,
                         due_dates=due_dates, edges=edges, weights=weights)
        self.successors = [0] * self.num_jobs

        # Successors initialization using edges
        for src, _ in self.edges:
            self.successors[src] += 1

        # Find jobs with no successors (L)
        self.L = set([i for i in range(self.num_jobs) if self.successors[i] == 0])

    def __find_next_job(self, completion_time: int) -> int:
        '''
        Find next job to schedule based on minimum tardiness among available jobs.

        Parameters:
        - completion_time (int): Current completion time to evaluate tardiness

        Returns:
        - int: Index of job with minimum tardiness from available jobs
        '''
        min_tardiness = float("inf")
        next_job = None

        # Select job with minimum tardiness
        for job_index in self.L:
            tardiness = self.jobs[job_index].tardiness(completion_time)
            if tardiness < min_tardiness:
                min_tardiness = tardiness
                next_job = job_index

        return next_job

    def schedule_jobs(self):
        '''
        Perform Least Cost Last (LCL) scheduling algorithm.

        Algorithm schedules jobs backwards starting with jobs that have no successors,
        selecting at each step the job with minimum tardiness. Aims to minimize
        total tardiness while respecting precedence constraints.

        Updates:
        - self.schedule: Fills with optimal job order
        - Completion times for each job
        '''
        # Initial total completion time
        completion_time = sum(job.processing_time for job in self.jobs)

        while self.L:
            next_job = self.__find_next_job(completion_time)
            self.schedule.append(next_job)

            # Update completion time
            self.jobs[next_job].completion_time = completion_time
            completion_time -= self.jobs[next_job].processing_time

            # Update L and successors, add to L if all dependencies are met
            self.L.remove(next_job)
            for src in range(self.num_jobs):
                if self.adj_matrix[src][next_job]:
                    self.successors[src] -= 1
                    if self.successors[src] == 0:
                        self.L.add(src)

        # Reverse the schedule to get the correct order
        self.schedule.reverse()
