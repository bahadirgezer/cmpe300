"""In this project, you will implement various versions of the Quick Sort algorithm, execute these algorithms with
different complexity cases and data sizes, report your results as execution times, and make comments on the results. """
from enum import IntEnum
from typing import Callable, List
from time import perf_counter

from analysis.algorithm import AlgorithmVersion, Algorithm
from analysis.input import InputType, Input


class CaseType(IntEnum):
    """This enum is used to specify the complexity case. """
    Average = 0
    Worst = 1


class Executor:
    """This class is used to execute the algorithm. """

    def __init__(self, version: AlgorithmVersion, case: CaseType, input_type: InputType, data_size: int):
        self.version: AlgorithmVersion = version
        self.case: CaseType = case
        self.input_type: InputType = input_type
        self.data_size: int = data_size
        self.cases: List[Callable] = [Executor.average_case, Executor.worst_case]
        self.input: Input = Input(self.input_type, self.data_size)
        self.algorithm: Algorithm = Algorithm(version, self.input.data.copy())

    def run(self) -> str:
        """This method is used to execute the algorithm with the given version, input type and analysis case . """
        # time the algorithm
        exec_time = self.cases[self.case](self)
        # print the results
        # format exec time to 3 decimal places and convert to the seconds to ms

        return f"{round(exec_time * 1000, 3)} ms"

        # return f"{self.version.name} {self.case.name} = {round(exec_time * 1000, 3)} ms"

        # return f"Version: {self.version.name},\t Case: {self.case.name},\t Input: {self.input_type.name},\t " \
        #       f"Data Size: {self.data_size},\t Execution Time: {round(exec_time * 1000, 3)} ms"

    def average_case(self) -> float:
        """This method is used to execute the algorithm with the average case. """
        # execute the algorithm 5 times and take the average
        exec_times = []
        for _ in range(5):
            start = perf_counter()
            self.algorithm.run()
            end = perf_counter()
            exec_times.append(end - start)
            self.algorithm.reset(self.input.data.copy())  # reset the algorithm with the original data
        return sum(exec_times) / len(exec_times)

    def worst_case(self) -> float:
        """This method is used to execute the algorithm with the worst case. """
        self.input.worst_case()
        self.algorithm.reset(self.input.data.copy())  # reset the algorithm with the worst case data
        start = perf_counter()
        self.algorithm.run()
        end = perf_counter()
        return end - start
