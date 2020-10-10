# coding: utf-8

r"""Code parallelization"""

from typing import List, Callable, Sized
import psutil
import platform
import logging
from multiprocessing import Process, cpu_count
from itertools import product


logger = logging.getLogger(__name__)


def physical_memory() -> int:
    r"""Total physical memory - Returns the total memory in bytes"""
    mem = psutil.virtual_memory()
    return mem.total


def processor() -> str:
    r"""CPU description"""
    return platform.processor()


def number_of_cpus() -> int:
    r"""Number of CPUs"""
    # TODO : what if cpu_count() returns 1 or an odd number?
    return cpu_count() / 2


def number_of_cores() -> int:
    r"""Number of cores for the CPU"""
    return psutil.cpu_count(logical=False)


def number_of_threads() -> int:
    r"""Number of threads for the CPU"""
    return psutil.cpu_count(logical=True)


def chunks(a_list: Sized, n: int) -> List[List]:
    """Yield successive n-sized chunks from a_list.

    a_list : The list to split in_ chunks
    n : The target numbers of items in_ each chunk

    Returns a List of chunks

    """
    pieces = []
    for i in range(0, len(a_list), n):
        pieces.append(list(a_list[i:i + n]))
    return pieces


def nb_per_process(cases_len: int, nb_cores: int) -> int:
    r"""Target number of 'cases' per process that optimizes parallelization

    cases_len : Total number of cases to deal with
    nb_cores : number of cores to parallelize on

    Returns the target number of cases by process

    """
    if cases_len % nb_cores == 0:
        return int(cases_len / nb_cores)
    else:
        return int(cases_len / nb_cores + 1)


def parallel_run(iter_func: Callable,
                 atomic_func: Callable,
                 iter_args: List[List],
                 args: List,
                 nb_cores: int):
    r"""Launch a parallel run

    iter_func : Function that deals with the iteration over the cases.
        This is the function that could be directly used with the list of all cases
        if no parallelization was intended.
    atomic_func : Procedure that actually does something for a case
    iter_args : List of lists of possible values of the case defining params
    args : Other args
    nb_cores : number of cores to parallelize on

    """
    all_cases = list(product(*iter_args))
    cases_decomposition = chunks(all_cases, nb_per_process(len(all_cases), nb_cores))
    msg = "Decomposed in %i parts" % len(cases_decomposition)
    logger.info(msg)

    for i, cases_partial in enumerate(cases_decomposition):
        msg = "  #%i -> %i cases" % (i, len(cases_partial))
        logger.info(msg)

    processes = []

    for i, cases_partial in enumerate(cases_decomposition):
        p = Process(target=iter_func, args=(atomic_func, cases_partial, args, i))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
