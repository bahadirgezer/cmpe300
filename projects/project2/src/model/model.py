"""
    Student Name: Bahadır Gezer / Muhammet Batuhan Ilhan
    Student Number: 2020400039 / 2019400243
    Compile Status: Compiling
    Program Status: Working
    Notes: The program is working as expected.
        Just run the mpiexec command using main.py with the required arguments inside the src/ folder.
"""
import sys


class Master:
    def __init__(self, argv: list[str], size: int):
        self.merge_method: str = ""
        self.test_file: str = ""
        self.input_file: str = ""
        self.data: list[list[str]] = []
        self.tests: list[str] = []
        self.freqs: dict = dict()
        self.parse_args(argv)
        self.divide_work(self.parse_corpus(), size)
        self.parse_test()

    def parse_args(self, argv: list[str]) -> None:
        # flag arguments can be in any order
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

    def parse_corpus(self) -> list[str]:
        with open(self.input_file, "r") as f:
            corpus: list[str] = f.readlines()
        return corpus

    def divide_work(self, work: list[str], workers: int) -> list[list[str]]:
        # divide the work equally among the workers,
        # if there are any left over, distribute them one at a time until all work is distributed
        work_per_worker: int = len(work) // workers
        for i in range(workers):
            start = i * work_per_worker
            end = (i + 1) * work_per_worker
            self.data.append(work[start:end])
        leftovers = len(work) % workers
        for i in range(leftovers):
            self.data[i].append(work[-1 - i])
        return self.data

    def parse_test(self) -> list[str]:
        with open(self.test_file, "r") as f:
            # split and strip the test file line by line
            lines = [line.strip() for line in f.readlines()]
            for line in lines:
                self.tests.append(" ".join(line.split()))
        return self.tests

    def display_results(self) -> None:
        # for each test
        for test in self.tests:
            freq_first_word: int = self.freqs.get(test.split()[0], 0)
            freq_test: int = self.freqs.get(test, 0)
            if freq_first_word == 0:
                print(f"{test} -> {0}")
            else:
                # probability of the bigram
                prob: float = freq_test / freq_first_word
                # format the probability to 4 decimal places
                print(f"{test} -> {format(prob, '.4f')}")

    def merge(self, calculated_ngrams: dict) -> None:
        self.freqs = {k: self.freqs.get(k, 0) + calculated_ngrams.get(k, 0)
                      for k in set(self.freqs).union(calculated_ngrams)}


class Slave:
    def __init__(self, rank: int, work: list[str]):
        self.rank: int = rank
        self.work: list[str] = work
        self.freqs: dict = dict()
        print(f"Rank: {rank}, Sentences: {len(work)}")

    def count_ngrams(self) -> dict:
        # count the ngrams
        for sentence in self.work:  # unigrams
            for word in sentence.split():
                self.freqs[word] = self.freqs.get(word, 0) + 1
        for sentence in self.work:  # bigrams
            words = sentence.split()
            for i in range(len(words) - 1):
                bigram = words[i] + " " + words[i + 1]
                self.freqs[bigram] = self.freqs.get(bigram, 0) + 1
        return self.freqs

    def merge(self, calculated_ngrams: dict) -> None:
        self.freqs = {k: self.freqs.get(k, 0) + calculated_ngrams.get(k, 0)
                      for k in set(self.freqs).union(calculated_ngrams)}


def merge_method(argv: list[str]) -> str:
    # return the merge method
    for i in range(len(sys.argv)):
        if argv[i] == "--merge_method":
            return sys.argv[i + 1]
    raise ValueError("Missing program arguments.")
