"""You will implement four versions of the Quick Sort algorithm as shown below: Ver1. The classical deterministic
algorithm. The pivot is chosen as the first element of the list. Ver2. The randomized algorithm. The pivot is chosen
randomly. This is the algorithm “Quicksort (1st version)” in the course slides. Ver3. The randomized algorithm. The
list is first randomly permuted and then the classical deterministic algorithm is called where the pivot is chosen as
the first element of the list. This is the algorithm “Quicksort (2nd version)” in the course slides. Ver4. The
deterministic algorithm. The pivot is chosen according to the “median of three” rule. """
import random
from enum import IntEnum
from typing import Callable, List


# enum for version where the version are 1, 2, 3, 4
class AlgorithmVersion(IntEnum):
    """This enum is used to specify the version of the algorithm. """
    Ver1 = 0
    Ver2 = 1
    Ver3 = 2
    Ver4 = 3


class Algorithm:

    def __init__(self, version: AlgorithmVersion, data: List[int]):
        self.version: AlgorithmVersion = version
        self.data: List[int] = data
        self.partitions: List[Callable] = [Algorithm.partition1, Algorithm.partition2,
                                           Algorithm.partition3, Algorithm.partition4]

    def run(self) -> None:  # run the algorithm
        self.quick_sort(0, len(self.data) - 1)
        self.check_if_sorted()

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
        return self.make_swaps(low, high, pivot)

    def partition2(self, low: int, high: int) -> int:
        """This is the partition function for the randomized algorithm. The pivot is chosen randomly. """
        pivot_index = random.randint(low, high)
        pivot = self.data[pivot_index]
        self.data[pivot_index], self.data[low] = self.data[low], self.data[pivot_index]
        return self.make_swaps(low, high, pivot)

    def partition3(self, low: int, high: int) -> int:
        """The randomized algorithm. The list is first randomly permuted and then the classical deterministic
        algorithm is called where the pivot is chosen as the first element of the list. """
        random.shuffle(self.data[low:high + 1])
        pivot = self.data[low]
        return self.make_swaps(low, high, pivot)

    def partition4(self, low: int, high: int) -> int:
        """This is the partition function for the deterministic algorithm. The pivot is chosen according to the
        “median of three” rule. """
        pivots = {self.data[low]: low, self.data[(high + low) // 2]: (high + low) // 2, self.data[high]: high}
        values = sorted([self.data[low], self.data[(high + low) // 2], self.data[high]])
        median = pivots[values[1]]  # get the median
        pivot = self.data[median]
        self.data[median], self.data[low] = self.data[low], self.data[median]
        return self.make_swaps(low, high, pivot)

    def make_swaps(self, low: int, high: int, pivot: int) -> int:
        i = low + 1
        for j in range(low + 1, high + 1):  # from low + 1 to high
            if self.data[j] < pivot:
                self.data[i], self.data[j] = self.data[j], self.data[i]  # swap
                i += 1
        self.data[low], self.data[i - 1] = self.data[i - 1], self.data[low]  # swap pivot with last element
        return i - 1

    def check_if_sorted(self):
        for i in range(1, len(self.data)):
            if self.data[i - 1] > self.data[i]:
                raise ValueError("NOT SORTED")

    def reset(self, data: List[int]) -> None:
        """This method is used to reset the data. """
        self.data = data
