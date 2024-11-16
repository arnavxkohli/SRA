from collections import deque
from src.graph import Graph


class TabuGraph(Graph):
    def __init__(self,
                 processing_times: list[int],
                 due_dates: list[int],
                 precedences: list[tuple[int, int]],
                 schedule: list[int],
                 weights: list[int] | None=None,
                 log_file_path: str | None=None) -> None:

        super().__init__(processing_times=processing_times,
                         due_dates=due_dates,
                         precedences=precedences,
                         schedule=schedule,
                         weights=weights,
                         log_file_path=log_file_path)

    def __calculate_tardiness_sum(self, schedule: list[int]) -> int:
        completion_time, tardiness = 0, 0

        for job in map(lambda job_index: self.jobs[job_index], schedule):
            completion_time += job.processing_time
            tardiness += job.weight * max(0, completion_time - job.due_date)
        return tardiness

    def __is_valid_swap(self, schedule: list[int], i: int, j: int) -> bool:
        schedule[i], schedule[j] = schedule[j], schedule[i]

        # Check all possible precedences
        valid_swap = all(schedule.index(src) <= schedule.index(dst) for src, dst in self.precedences)

        schedule[i], schedule[j] = schedule[j], schedule[i]
        return valid_swap

    def get_interchanges(self, previous_interchange: int | None=None) -> list[tuple[int, int]]:
        interchanges = [(i, i+1) for i in range(self.num_jobs - 1)]

        # Rotate based on previous_interchange
        return interchanges[previous_interchange+1:] + \
            interchanges[:previous_interchange+1] if previous_interchange \
                is not None else interchanges

    def schedule_jobs(self, list_length: int, max_iterations: int,
                      tolerance: int) -> None:
        tabu_list = deque(maxlen=list_length)
        best_schedule = self.schedule.copy()
        best_tardiness = self.__calculate_tardiness_sum(best_schedule)
        current_schedule = best_schedule.copy()
        current_tardiness = best_tardiness
        previous_interchange = None

        for iteration in range(max_iterations):
            interchanges = self.get_interchanges(previous_interchange)
            swap_pair = None

            for i, j in interchanges:
                if self.__is_valid_swap(current_schedule, i, j):
                    new_schedule = current_schedule.copy()
                    new_schedule[i], new_schedule[j] = new_schedule[j], new_schedule[i]
                    new_tardiness = self.__calculate_tardiness_sum(new_schedule)
                    swap_pair = tuple(sorted([current_schedule[i], current_schedule[j]]))
                    if (current_tardiness - new_tardiness > -tolerance and swap_pair not in tabu_list) or new_tardiness < best_tardiness:
                        current_tardiness = new_tardiness
                        current_schedule = new_schedule.copy()
                        previous_interchange = i
                        break

            if swap_pair is None:
                text = f"Iteration {iteration + 1}: No interchange found, terminating\n"
                if self.log_file:
                    self.log_file.write(text)
                else:
                    print(f"No interchange found, terminating at iteration {iteration + 1}")
                break

            if current_tardiness < best_tardiness:
                text = f"Iteration {iteration + 1}: New best tardiness: {current_tardiness} with schedule: {[s+1 for s in current_schedule]}\n"
                if self.log_file:
                    self.log_file.write(text)
                else:
                    print(text)
                best_tardiness = current_tardiness
                best_schedule = current_schedule.copy()

            tabu_list.append(swap_pair)

        self.schedule = best_schedule
