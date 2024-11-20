from src.lcl import LCLGraph
from src.tabu import TabuGraph


def main():
    processing_times = [
        3, 10, 2, 2, 5, 2, 14, 5, 6, 5, 5, 2, 3, 3, 5, 6, 6, 6, 2, 3, 2, 3, 14, 5, 18,
        10, 2, 3, 6, 2, 10
    ]

    due_dates = [
        172, 82, 18, 61, 93, 71, 217, 295, 290, 287, 253, 307, 279, 73, 355, 34,
        233, 77, 88, 122, 71, 181, 340, 141, 209, 217, 256, 144, 307, 329, 269
    ]

    precedences = [
        (0, 30), (1, 0), (2, 7), (3, 2), (4, 1), (5, 15), (6, 5), (7, 6), (8, 7),
        (9, 8), (10, 0), (11, 4), (12, 11), (13, 12), (16, 14), (14, 10), (15, 4),
        (16, 15), (17, 16), (18, 17), (19, 18), (20, 17), (21, 20), (22, 21), (23, 4),
        (24, 23), (25, 24), (26, 25), (27, 25), (28, 26), (28, 27), (29, 3), (29, 9),
        (29, 13), (29, 19), (29, 22), (29, 28)
    ]

    initial_schedule = [
        29, 28, 22, 9, 8, 13, 12, 11, 3, 19, 21, 2, 26, 27, 7,
        6, 18, 20, 25, 17, 24, 16, 14, 5, 23, 15, 4, 10, 1, 0,
        30
    ]

    lcl_graph = LCLGraph(processing_times=processing_times,
                         due_dates=due_dates,
                         precedences=precedences)

    tabu_simulation = [
        {
            "log_file_path": "out/tabu_1.txt",
            "list_length": 20,
            "max_iterations": 10,
            "tolerance": 10
        },
        {
            "log_file_path": "out/tabu_2.txt",
            "list_length": 20,
            "max_iterations": 100,
            "tolerance": 10
        },
        {
            "log_file_path": "out/tabu_3.txt",
            "list_length": 20,
            "max_iterations": 1000,
            "tolerance": 10
        },
        {
            "log_file_path": "out/tabu_best_schedule.txt",
            "list_length": 100,
            "max_iterations": 10000,
            "tolerance": 20
        },
    ]

    for simulation in tabu_simulation:
        with TabuGraph(processing_times=processing_times,
                       due_dates=due_dates,
                       precedences=precedences,
                       schedule=initial_schedule,
                       log_file_path=simulation["log_file_path"]) as tabu_graph:

            tabu_graph.schedule_jobs(list_length=simulation["list_length"],
                                     max_iterations=simulation["max_iterations"],
                                     tolerance=simulation["tolerance"])

if __name__ == "__main__":
    main()
