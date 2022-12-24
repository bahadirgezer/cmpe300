import sys
from typing import List

from analysis.algorithm import AlgorithmVersion
from analysis.executor import CaseType, Executor
from analysis.input import InputType

data_sizes: List[int] = [100, 1_000, 10_000]
input_types: List[InputType] = [InputType.InpType1, InputType.InpType2, InputType.InpType3, InputType.InpType4]
algorithm_versions: List[AlgorithmVersion] = [AlgorithmVersion.Ver1, AlgorithmVersion.Ver2, AlgorithmVersion.Ver3,
                                              AlgorithmVersion.Ver4]
analysis_cases: List[CaseType] = [CaseType.Average, CaseType.Worst]

if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    for data_size in data_sizes:
        for input_type in input_types:
            for algorithm_version in algorithm_versions:
                if algorithm_version != AlgorithmVersion.Ver1:
                    continue  # temporary

                for analysis_case in analysis_cases:
                    executor = Executor(algorithm_version, analysis_case, input_type, data_size)
                    output: str = executor.run()
                    print(output)
        print()