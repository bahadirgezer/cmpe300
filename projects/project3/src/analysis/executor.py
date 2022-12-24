"""In this project, you will implement various versions of the Quick Sort algorithm, execute these algorithms with
different complexity cases and data sizes, report your results as execution times, and make comments on the results. """
import time
from enum import IntEnum
from typing import Callable

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
        self.cases: list[Callable] = [Executor.average_case, Executor.worst_case]
        self.input: Input = Input(self.input_type, self.data_size)
        self.algorithm: Algorithm = Algorithm(version, self.input.data)

    def run(self) -> None:
        """This method is used to execute the algorithm with the given version, input type and analysis case . """
        # time the algorithm
        exec_time = self.cases[self.case]()
        # print the results
        print(f"Algorithm: {self.version.name}, Case: {self.case.name}, Input: {self.input_type.name}, "
              f"Size: {self.data_size}, Time: {exec_time}")

    def average_case(self) -> float:
        """This method is used to execute the algorithm with the average case. """
        pass

    def worst_case(self) -> float:
        """This method is used to execute the algorithm with the worst case. """
        pass