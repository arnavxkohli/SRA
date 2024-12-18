# Scheduling and Resource Allocation Coursework

This repository contains the code for the coursework of the Scheduling and Resource Allocation coursework implemented by `sk1421` and `rs2221`

## Repository Structure

The repository is structured as follows:

``` tree
SRA
├── README.md
├── main.py
├── out
│   ├── lcl_schedule.txt
│   ├── tabu_1.txt
│   ├── tabu_2.txt
│   ├── tabu_3.txt
│   ├── tabu_best_schedule.txt
│   ├── tabu_list_length_plot.png
│   ├── tabu_schedule.txt
│   └── tabu_tolerance_plot.png
├── requirements.txt
├── spec.pdf
└── src
    ├── __init__.py
    ├── graph.py
    ├── job.py
    ├── lcl.py
    ├── parser.py
    └── tabu.py
```

- `README.md`: This file, contains an explanation of the repository structure and the code.
- `main.py`: The main script that runs the Least Cost Rule (LCL) Search and Tabu Search algorithms.
- `out/`: The directory where the output files are stored.
  - `lcl_schedule.txt`: The output file for the general LCL Search algorithm, when saving is enabled with the `-s` flag.
  - `tabu_1.txt`: The output file for the Tabu Search algorithm with the `tolerance = 10`, `tabu list length = 20` and `iterations = 10`.
  - `tabu_2.txt`: The output file for the Tabu Search algorithm with the `tolerance = 10`, `tabu list length = 20` and `iterations = 100`.
  - `tabu_3.txt`: The output file for the Tabu Search algorithm with the `tolerance = 10`, `tabu list length = 20` and `iterations = 1000`.
  - `tabu_best_schedule.txt`: The output file for the best schedule based on minimum tardiness sum found by the Tabu Search algorithm while varying the `tolerance` and `tabu list length`, when saving is enabled with the `-s` flag.
  - `tabu_list_length_plot.png`: A plot showing the effect of varying the `tabu list length` on the best tardiness sum.
  - `tabu_schedule.txt`: The output file for the general Tabu Search algorithm, when saving is enabled with the `-s` flag.
  - `tabu_tolerance_plot.png`: A plot showing the effect of varying the `tolerance` on the best tardiness sum.
- `requirements.txt`: The file containing the required packages to run the code.
- `spec.pdf`: The specification of the coursework.
- `src/`: The directory containing the source code.
  - `graph.py`: The file containing the `Graph` class that represents the graph of the jobs.
  - `job.py`: The file containing the `Job` class that represents a job.
  - `lcl.py`: The file containing the `LCL` class that implements the Least Cost Rule (LCL) Search algorithm.
  - `parser.py`: The file containing the `Parser` class that parses the command line arguments to the application.
  - `tabu.py`: The file containing the `Tabu` class that implements the Tabu Search algorithm.

All of the outputs in the log files are 1-indexed, while the variables in code are meant to be 0-indexed.

## Running the Code

To run the code, we first need to set-up the virtual environment and install the required packages. This can be done by running the following commands:

``` bash
# Create the virtual environment
python3 -m venv venv
# Activate the virtual environment
source venv/bin/activate
# Install the required packages
pip install -r requirements.txt
```

Once this is done, the instructions for each parameter are:

``` bash
usage: main.py [-h] [-n] [-l LIST_LENGTH] [-m MAX_ITERATIONS] [-t TOLERANCE] [-s] [-r {tabu,lcl,both}] [-p]

Scheduling Coursework CLI

options:
  -h, --help            show this help message and exit
  -n, --no-initial-schedule
                        Use provided initial schedule if not set
  -l, --list_length LIST_LENGTH
                        List length for Tabu search
  -m, --max_iterations MAX_ITERATIONS
                        Maximum iterations for Tabu search
  -t, --tolerance TOLERANCE
                        Tolerance for Tabu search
  -s, --save_output     Save output to files
  -r, --run {tabu,lcl,both}
                        Select which algorithm to run: tabu, lcl, or both
  -p, --plot            Plot the results
```

When saving the result of the least cost rule schedule, the output will be saved in `out/lcl_schedule.txt`. When saving the result of the tabu search schedule, the output will be saved in `out/tabu_schedule.txt`. If `-s` is not set, the output will be printed to the console. To test the code without using the provided initial schedule, use the `-n` flag.

The `-p` flag plots the results of the varying `tolerance` and `tabu list length` on the best tardiness sum. This flag does nothing if `-r` is set to `lcl`.

## Testing the code against the specification

To test [3.1](out/lcl_schedule.txt):

``` bash
python3 main.py -r lcl -s
```

To test 3.2:

Note that in the [log files](out/), the outputs given are for all of the iterations, keeping the constraints mentioned in the specification in mind. The log files generated with the below commands will just output the iterations where an improvement on the lowest cost (lowest tardiness sum) was made.

- For 3.2.1:
  - [For `list_length = 20`, `max_iterations = 10`, `tolerance = 10`](out/tabu_1.txt):

  ``` bash
  python3 main.py -r tabu -l 20 -m 10 -t 10 -s # Outputs to out/tabu_schedule.txt
  ```

  - [For `list_length = 20`, `max_iterations = 100`, `tolerance = 10`](out/tabu_2.txt):

  ``` bash
  python3 main.py -r tabu -l 20 -m 100 -t 10 -s # Outputs to out/tabu_schedule.txt
  ```

  - (For `list_length = 20`, `max_iterations = 1000`, `tolerance = 10`)[out/tabu_3.txt]:

  ``` bash
  python3 main.py -r tabu -l 20 -m 1000 -t 10 -s # Outputs to out/tabu_schedule.txt
  ```

- For 3.2.2:
  [To get the best schedule based on the minimum tardiness sum found by the Tabu Search algorithm while varying the `tolerance` and `tabu list length`](out/tabu_best_schedule.txt):

  ``` bash
  python3 main.py -r tabu -s # Outputs to out/tabu_schedule.txt
  ```
