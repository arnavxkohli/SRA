class Job:
    # 1-index the jobs for visualization
    _index_counter = 1

    def __init__(self, processing_time: int, due_date: int):
        self.index = Job.assign_index()
        self.processing_time = processing_time
        self.due_date = due_date
        self.completion_time = None

    @staticmethod
    def assign_index():
        # For debugging and output representation
        Job._index_counter += 1
        return Job._index_counter - 1

    def tardiness(self, completion_time):
        return max(0, completion_time - self.due_date)

    def __repr__(self):
        if self.completion_time is None:
            return f"Job {self.index} is incomplete"
        return f"Job {self.index} complete at {self.completion_time} with tardiness: {self.tardiness(self.completion_time)}"
