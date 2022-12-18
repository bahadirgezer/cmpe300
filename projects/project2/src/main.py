from mpi4py import MPI
import sys

from master_slave.Model import Master, Slave

'''
    Use the mpi framework to distribute the work across multiple workers. It will be a master salve architecture.
    The master will be responsible for reading the csv file and distributing the work to the slaves. 
    The slaves will be responsible for counting the bigrams and returning the results to the master.
    The master will then merge the results and return the final result to the user.
'''


def main() -> None:
    comm: MPI.Intracomm = MPI.COMM_WORLD

    # the master will be rank 0, so we need to subtract 1 from the size to get the number of workers
    size = comm.size
    rank: int = comm.rank
    master: Master = Master(sys.argv, size - 1)

    if rank == 0:
        # master
        # send the distributed data to the workers
        for worker in range(1, size):
            comm.send(master.data[worker - 1], dest=worker)

        # receive the results from the workers based on the merge method
        if master.merge_method == "MASTER":
            # merge the results on the master
            for worker in range(1, size):
                calculated: dict = comm.recv(source=worker)
                master.freqs = {k: master.freqs.get(k, 0) + calculated.get(k, 0)
                                for k in set(master.freqs).union(calculated)}
        # master will merge the result from the last worker
        elif master.merge_method == "WORKERS":
            calculated: dict = comm.recv(source=size - 1)
            master.freqs = {k: master.freqs.get(k, 0) + calculated.get(k, 0)
                            for k in set(master.freqs).union(calculated)}
        else:
            raise ValueError("Invalid merge method.")

        # display the results
        master.display_results()

    else:
        # slaves
        # receive the data from the master
        work: list[str] = comm.recv(source=0)
        slave: Slave = Slave(rank, work)
        slave.count_ngrams()

        # send the results back to the master based on the merge method
        if master.merge_method == "MASTER":
            # send the result to the master directly
            comm.send(slave.freqs, dest=0)
        elif master.merge_method == "WORKERS":
            # receive the result from the last worker, merge the results and send it to the master
            # the first worker does not receive anything
            if rank != 1:
                calculated: dict = comm.recv(source=rank - 1)
                slave.freqs = {k: slave.freqs.get(k, 0) + calculated.get(k, 0) for k in
                               set(slave.freqs).union(calculated)}
            # last worker sends the result to the master
            dest_rank = rank + 1 if rank + 1 < size else 0
            comm.send(slave.freqs, dest=dest_rank)
        else:
            raise ValueError("Invalid merge method.")

    return None


# mpiexec -n 4 python main.py --input_file ../resources/sample_text.txt --merge_method MASTER --test_file ../resources/test.txt
if __name__ == '__main__':
    main()
