import sys


class Master:
    def __init__(self, argv, size: int):
        self.merge_method = None
        self.test_file = None
        self.input_file = None
        self.data: list[list[str]] = []
        self.tests: list[str] = []
        self.parse_args(argv)
        self.divide_work(self.parse_corpus(), size)
        self.parse_test()

    def parse_args(self, argv):
        for i in range(len(sys.argv)):
            if argv[i] == "--test_file":
                self.test_file = sys.argv[i + 1]
            if argv[i] == "--input_file":
                self.input_file = sys.argv[i + 1]
            if argv[i] == "--merge_method":
                self.merge_method = sys.argv[i + 1]

        if self.input_file is None or self.test_file is None or self.merge_method is None:
            # raise an error for missing arguments
            raise ValueError("Missing program arguments.")

    def parse_corpus(self):
        with open(self.input_file, "r") as f:
            corpus: list[str] = f.readlines()
        return corpus

    def divide_work(self, work: list[str], workers: int) -> list[list[str]]:
        # divide the work evenly among the workers, if there are any left over, distribute them evenly (one at a time)
        # until all work is distributed
        # return a list where the work is divided among the workers, each worker has a list of work
        # e.g. [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        # e.g. [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11]] leftovers are distributed evenly
        work_per_worker: int = len(work) // workers
        for i in range(workers):
            start = i * work_per_worker
            end = (i + 1) * work_per_worker
            self.data.append(work[start:end])
        leftovers = len(work) % workers
        for i in range(leftovers):
            self.data[i].append(work[-1 - i])
        return self.data

    def parse_test(self):
        with open(self.test_file, "r") as f:
            # split and strip the test file line by line
            lines = [line.strip() for line in f.readlines()]
            for line in lines:
                self.tests.append(" ".join(line.split()))
        return self.tests
