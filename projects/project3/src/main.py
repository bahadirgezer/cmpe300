import sys
from typing import List

from analysis.algorithm import AlgorithmVersion
from analysis.executor import CaseType, Executor
from analysis.input import InputType, Input

data_sizes: List[int] = [100, 1_000, 10_000]
input_types: List[InputType] = [InputType.InpType1, InputType.InpType2, InputType.InpType3, InputType.InpType4]
algorithm_versions: List[AlgorithmVersion] = [AlgorithmVersion.Ver1, AlgorithmVersion.Ver2, AlgorithmVersion.Ver3,
                                              AlgorithmVersion.Ver4]
analysis_cases: List[CaseType] = [CaseType.Average, CaseType.Worst]


def format_data(data: List[int]) -> str:
    """This method is used to format the data. """
    # the list values should be seperated by hyphens without spaces and square brackets should be removed
    return str(data).replace(" ", "").replace("[", "").replace("]", "").replace(",", "-")


def answer_sheet_1():
    sys.stdout = open("answersheet1.txt", "w")
    for data_size in data_sizes:
        print(f"\n*** n = {data_size}\n")
        for input_type in input_types:
            print(f"\n{input_type.name}")
            for i in range(1, 7):
                generated_input = Input(input_type, data_size)
                if i == 6:
                    generated_input.worst_case()
                    print(f"Input (worst) = {format_data(generated_input.data)}")
                else:
                    print(f"Input{i} (average) = {format_data(generated_input.data)}")
            print()
            for algorithm_version in algorithm_versions:
                for analysis_case in analysis_cases:
                    executor = Executor(algorithm_version, analysis_case, input_type, data_size)
                    output: str = executor.run()
                    print(output)
            print()
        print()

    sys.stdout.close()


def answer_sheet_2():
    for case in analysis_cases:
        print(f"{case.name}")
        for version in algorithm_versions:
            print(f"{version.name}")
            for input_type in input_types:
                for data_size in data_sizes:
                    executor = Executor(version, case, input_type, data_size)
                    output: str = executor.run()
                    print(output, end=" ")
            print()
        print("\n")


if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    # set system out to a file
    answer_sheet_2()
