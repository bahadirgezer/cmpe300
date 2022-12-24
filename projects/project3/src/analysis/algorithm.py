"""You will implement four versions of the Quick Sort algorithm as shown below: Ver1. The classical deterministic
algorithm. The pivot is chosen as the first element of the list. Ver2. The randomized algorithm. The pivot is chosen
randomly. This is the algorithm “Quicksort (1st version)” in the course slides. Ver3. The randomized algorithm. The
list is first randomly permuted and then the classical deterministic algorithm is called where the pivot is chosen as
the first element of the list. This is the algorithm “Quicksort (2nd version)” in the course slides. Ver4. The
deterministic algorithm. The pivot is chosen according to the “median of three” rule. """
import random
from enum import IntEnum
from typing import Callable


# enum for version where the version are 1, 2, 3, 4
class AlgorithmVersion(IntEnum):
    """This enum is used to specify the version of the algorithm. """
    Ver1 = 0
    Ver2 = 1
    Ver3 = 2
    Ver4 = 3


class Algorithm:

    def __init__(self, version: AlgorithmVersion, data: list[int]):
        self.version: AlgorithmVersion = version
        self.data: list[int] = data
        self.partitions: list[Callable] = [Algorithm.partition1, Algorithm.partition2,
                                           Algorithm.partition3, Algorithm.partition4]

    def run(self) -> None:  # run the algorithm
        self.quick_sort(0, len(self.data) - 1)

    def quick_sort(self, low: int, high: int) -> None:
        """This is the quick sort algorithm. It calls the partition function and then recursively calls itself on the
        two sublist. """
        if low < high:
            # choose partition function based on version
            pivot = self.partitions[self.version](self, low, high)
            self.quick_sort(low, pivot - 1)  # left
            self.quick_sort(pivot + 1, high)  # right

    def partition1(self, low: int, high: int) -> int:
        """This is the partition function for the classical deterministic algorithm. The pivot is chosen as the
        first element of the list. """
        pivot = self.data[low]
        i = low + 1  # index of smaller element
        for j in range(low + 1, high + 1):  # from low + 1 to high
            if self.data[j] < pivot:
                self.data[i], self.data[j] = self.data[j], self.data[i]  # swap
                i += 1
        self.data[low], self.data[i - 1] = self.data[i - 1], self.data[low]  # swap pivot with last element
        return i - 1

    def partition2(self, low: int, high: int) -> int:
        """This is the partition function for the randomized algorithm. The pivot is chosen randomly. """
        pivot = random.choice(self.data[low:high + 1])

        return 0

    def partition3(self, low: int, high: int) -> int:
        """The randomized algorithm. The list is first randomly permuted and then the classical deterministic
        algorithm is called where the pivot is chosen as the first element of the list. """
        return 0

    def partition4(self, low: int, high: int) -> int:
        """This is the partition function for the deterministic algorithm. The pivot is chosen according to the
        “median of three” rule. """
        return 0

    def reset(self, data: list[int]) -> None:
        """This method is used to reset the data. """
        self.data = data
