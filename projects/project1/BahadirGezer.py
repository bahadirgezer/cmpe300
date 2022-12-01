import random
import time
from enum import Enum
from math import floor


class InputCase(Enum):
    best = 1
    worst = 2
    average = 3


def function(n: int, case: InputCase) -> list[int]:
    if case == InputCase.best:
        arr: list[int] = [0] * n
    elif case == InputCase.worst:
        arr: list[int] = [2] * n
    elif case == InputCase.average:
        arr: list[int] = [random.randint(0, 2) for _ in range(n)]

    result: list[int] = [0] * 5
    for i in range(len(arr)):
        if arr[i] == 0:
            for t1 in range(i, len(arr)):
                p1: float = t1 ** (1 / 2)
                x1: int = n + 1
                while x1 >= 1:
                    x1 = floor(x1 / 2)
                    result[i % 5] = result[i % 5] + 1

        elif arr[i] == 1:
            for t2 in range(n, 0, -1):
                for p2 in range(1, n):
                    x2: int = n + 1
                    while x2 > 0:
                        x2 = floor(x2 / 2)
                        result[i % 5] = result[i % 5] + 1

        elif arr[i] == 2:
            for t3 in range(1, n + 1):
                # noinspection PyUnusedLocal
                x3: int = t3 + 1
                # for p3 = 0 to t3^2 - 1 do
                for p3 in range(0, t3 ** 2):
                    result[i % 5] = result[i % 5] + 1

    return result


if __name__ == "__main__":
    # n: int = 100
    input_sizes: list[int] = [1, 5, 10, 25, 50, 75, 100, 150, 200, 250]
    for input_case in InputCase:
        if input_case == InputCase.best:
            continue
        if input_case == InputCase.worst:
            continue

        for n in input_sizes:
            if input_case == InputCase.average:
                total_time: float = 0
                for _ in range(3):
                    start_time: float = time.time()
                    function(n, input_case)
                    end_time: float = time.time()
                    total_time += end_time - start_time
                print(f"Case: {input_case.name} Size: {n} Elapsed Time: {(total_time / 3)*1000:.9f}ms")
            else:
                start: float = time.time()
                function(n, input_case)
                end: float = time.time()
                print(f"Case: {input_case.name} Size: {n} Elapsed Time: {(end - start)*1000:.9f}ms")
