#!/usr/bin/env python
# coding: utf-8

r"""Parallel helpers example use."""

from typing import Callable, List, Tuple
import logging
import time

from ydeos_parallel.parallel import parallel_run, number_of_cores


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s '
                           ':: %(lineno)3d :: %(message)s')


ATOMIC_FUNC_SLEEP_TIME = 10


def __sample_iter_func(atomic_func: Callable,
                       cases: List,
                       other_args: List,
                       process_nb: int = -1):
    r"""Sample iteration function."""
    for j, case in enumerate(cases):
        msg = f"{case} [process {process_nb} - {j + 1} out of {len(cases)}]"
        print(msg)
        time_0 = time.time()
        atomic_func(case, *other_args)
        time_1 = time.time()

        msg = f"{case} took {time_1 - time_0:.8f} seconds"
        print(msg)


def __sample_atomic_func(case: Tuple, p_1, p_2, p_3="Z"):
    r"""Sample 'atomic' procedure that actually does something with a case.

    Parameters
    ----------
    case : tuple
    p_1 : whatever, specific to this function
    p_2 : whatever, specific to this function
    p_3 : whatever, specific to this function

    """
    my_list = []

    # here the function can handle a case with any number of params,
    # which may not always be so
    for param in case:
        my_list.append(param)
    my_list.append(p_1)
    my_list.append(p_2)
    my_list.append(p_3)
    print(''.join(my_list))
    time.sleep(ATOMIC_FUNC_SLEEP_TIME)


# Whenever we use the multiprocessing library to start a new process,
# it imports the main module in a new Python interpreter.
# Therefore it’s important to ensure the main module can be safely
# imported by a new Python interpreter without causing unintended side effects
# such as re-creating a new process and failing with a RuntimeError.
# The key is to protect the entry point of the program by using:
# if __name__ == '__main__:
#    # create new process
if __name__ == "__main__":

    list_1 = ['a', 'b', 'c', 'd']
    list_2 = ['1', '2', '3', '4']
    list_3 = ['+', '-', '*', '/']
    t_0 = time.time()
    parallel_run(iter_func=__sample_iter_func,
                 atomic_func=__sample_atomic_func,
                 iter_args=[list_1, list_2, list_3],
                 args=['lorem', "ipsum", "dolor"],
                 nb_cores=number_of_cores())
    t_1 = time.time()
    print(f"Total clock time : {t_1 - t_0} s")
