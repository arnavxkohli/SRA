from src.job import Job
from src.graph import Graph


class LCLGraph(Graph):

    def __init__(self, processing_times: list[int], due_dates: list[int],
                 precedences: list[tuple[int, int]],
                 weights: list[int] | None = None,
                 log_file_path: str | None = None) -> None:
        super().__init__(processing_times=processing_times,
                         due_dates=due_dates, precedences=precedences,
                         weights=weights, log_file_path=log_file_path)
        self.successors = [0] * self.num_jobs

        # Successors initialization using precedences
        for src, _ in self.precedences:
            self.successors[src] += 1

        # Find jobs with no successors (L)
        self.L = set([i for i in range(self.num_jobs) if self.successors[i] == 0])

    def __find_next_job(self, completion_time: int) -> tuple[int, int]:
        min_tardiness = float("inf")
        next_job = None

        # Select job with minimum tardiness
        for job_index in self.L:
            tardiness = self.jobs[job_index].tardiness(completion_time)
            if tardiness < min_tardiness:
                min_tardiness = tardiness
                next_job = job_index

        return next_job, min_tardiness

    def schedule_jobs(self) -> None:
        # Initial total completion time
        completion_time = sum(job.processing_time for job in self.jobs)
        iteration = 0
        max_tardiness = 0

        while self.L:
            next_job, min_tardiness = self.__find_next_job(completion_time)
            self.schedule.append(next_job)

            max_tardiness = max(max_tardiness, min_tardiness)

            # Update completion time of selected job and total completion time
            self.jobs[next_job].completion_time = completion_time
            completion_time -= self.jobs[next_job].processing_time

            if self.log_file:
                self.log_file.write(f"Iteration {iteration + 1}: Job {next_job+1} with tardiness {min_tardiness}\n")
                self.log_file.write(f"Intermediate schedule: {[s+1 for s in self.schedule[::-1]]}\n\n")

            # Update L and successors, add to L if all dependencies are met
            self.L.remove(next_job)
            for src in range(self.num_jobs):
                if self.adj_matrix[src][next_job]:
                    self.successors[src] -= 1
                    if self.successors[src] == 0:
                        self.L.add(src)

            iteration += 1

        # Reverse the schedule to get the correct order
        self.schedule.reverse()
        if self.log_file:
            self.log_file.write(f"Final schedule: {[s+1 for s in self.schedule]}\n")
            self.log_file.write(f"Maximum tardiness: {max_tardiness}\n")
