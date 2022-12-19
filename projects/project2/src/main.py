"""
    Student Name: Bahadır Gezer / Muhammet Batuhan Ilhan
    Student Number: 2020400039 / 2019400243
    Compile Status: Compiling
    Program Status: Working
    Notes: The program is working as expected.
        Just run the mpiexec command using main.py with the required arguments inside the src/ folder.
"""
import sys

from mpi4py import MPI

from model.model import Master, Slave
import model.model

'''
    Use the mpi framework to distribute the work across multiple workers. It will be a master salve architecture.
    The master will be responsible for reading the csv file and distributing the work to the slaves. 
    The slaves will be responsible for counting the bigrams and returning the results to the master.
    The master will then merge the results and return the final result to the user.
'''


def main() -> None:
    comm: MPI.Intracomm = MPI.COMM_WORLD
    # the master will be rank 0, so we need to subtract 1 from the size to get the number of workers
    size: int = comm.size
    rank: int = comm.rank
    merge_method: str = model.model.merge_method(sys.argv)

    if size == 1:
        raise ValueError("There must be at least one slave.")
    if rank == 0:
        # master
        master: Master = Master(sys.argv, size - 1)
        # send the distributed data to the workers
        for worker in range(1, size):
            comm.send(master.data[worker - 1], dest=worker)
        # receive the results from the workers based on the merge method
        if merge_method == "MASTER":
            # merge the results on the master
            for worker in range(1, size):
                calculated: dict = comm.recv(source=worker)
                master.merge(calculated)
        # master will merge the result from the last worker
        elif merge_method == "WORKERS":
            calculated: dict = comm.recv(source=size - 1)
            master.merge(calculated)
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
        if merge_method == "MASTER":
            # send the result to the master directly
            comm.send(slave.freqs, dest=0)
        elif merge_method == "WORKERS":
            # receive the result from the last worker, merge the results and send it to the master
            # the first worker does not receive anything
            if rank != 1:
                calculated: dict = comm.recv(source=rank - 1)
                slave.merge(calculated)
            # last worker sends the result to the master
            dest_rank = rank + 1 if rank + 1 < size else 0
            comm.send(slave.freqs, dest=dest_rank)
        else:
            raise ValueError("Invalid merge method.")
    return None


# mpiexec -n 4 python main.py --input_file ../resources/sample_text.txt --merge_method MASTER --test_file ../resources/test.txt
if __name__ == '__main__':
    main()
