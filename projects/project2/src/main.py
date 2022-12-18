from mpi4py import MPI
import sys

from mpi4py.MPI import Request

from bigram.Bigram import Master


# mpiexec -n 4 python main.py --input_file ../resources/sample_text.txt --merge_method MASTER --test_file ../resources/test.txt
def main() -> None:
    # use the mpi framework to distribute the work across multiple workers. It will be a master salve architecture.
    # The master will be responsible for reading the csv file and distributing the work to the slaves.
    comm: MPI.Intracomm = MPI.COMM_WORLD
    rank: int = comm.rank
    size = comm.size
    freqs: dict = dict()
    master: Master = Master(sys.argv, size - 1)

    if rank == 0:
        # the master will be rank 0, so we need to subtract 1 from the size

        for worker in range(1, size):
            comm.send(master.data[worker - 1], dest=worker)
        # comm.barrier()

        # the master will be rank 0, so we need to subtract 1 from the size
        if master.merge_method == "MASTER":
            for worker in range(1, size):
                calculated: dict = comm.recv(source=worker)
                freqs = {k: freqs.get(k, 0) + calculated.get(k, 0) for k in set(freqs).union(calculated)}

        elif master.merge_method == "WORKERS":
            calculated: dict = comm.recv(source=size - 1)
            freqs = {k: freqs.get(k, 0) + calculated.get(k, 0) for k in set(freqs).union(calculated)}

        # print the largest 20 values in the dictionary with the key and value pair in a sorted order
        print(sorted(freqs.items(), key=lambda x: x[1], reverse=True)[:20])

        for test in master.tests:
            # conditional probability of the test, which is a bigram
            freq_first_word: int = freqs.get(test.split()[0], 0)
            freq_test: int = freqs.get(test, 0)
            if freq_first_word == 0:
                print(f"{test} -> {0}")
            else:
                # format the probability to 4 decimal places
                print(f"{test} -> {format(freq_test / freq_first_word, '.4f')}")

    else:
        # slaves
        work: list[str] = comm.recv(source=0)
        print(f"Rank: {rank}, Sentences: {len(work)}")

        for sentence in work:  # unigrams
            for word in sentence.split():
                freqs[word] = freqs.get(word, 0) + 1

        for sentence in work:  # bigrams
            words = sentence.split()
            for i in range(len(words) - 1):
                bigram = words[i] + " " + words[i + 1]
                freqs[bigram] = freqs.get(bigram, 0) + 1

        if master.merge_method == "MASTER":
            comm.send(freqs, dest=0)

        elif master.merge_method == "WORKERS":
            # receive data from previous worker
            calculated: dict = dict()  # empty dict for the first worker
            if rank != 1:
                calculated: dict = comm.recv(source=rank - 1)
                freqs = {k: freqs.get(k, 0) + calculated.get(k, 0) for k in set(freqs).union(calculated)}
            dest_rank = rank + 1 if rank + 1 < size else 0
            comm.send(freqs, dest=dest_rank)

        else:
            raise ValueError("Invalid merge method.")

    return None


if __name__ == '__main__':
    main()

