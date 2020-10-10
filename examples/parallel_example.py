#!/usr/bin/env python
# coding: utf-8

r"""Parallel helpers example use"""

from typing import Callable, List, Tuple
import logging
import time

from ydeos_parallel.parallel import parallel_run, number_of_cores


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s '
                           ':: %(lineno)3d :: %(message)s')


def __sample_iter_func(atomic_func: Callable, cases: List, other_args: List, process_nb: int = -1):
    r"""Sample iteration function"""
    for j, case in enumerate(cases):
        msg = "%s [process %i - %i out of %i]" % (str(case),
                                                  process_nb,
                                                  j + 1,
                                                  len(cases))
        print(msg)
        t0 = time.time()
        try:
            atomic_func(case, *other_args)
        except:  # Intentionally wide except clause
            msg = f"Something went wrong while running {atomic_func.__name__}"
            print(msg)
        t1 = time.time()

        msg = "%s took %.4f minutes" % (str(case), (t1 - t0) / 60)
        print(msg)


def __sample_atomic_func(case: Tuple, p1, p2, p3="Z"):
    r"""Sample 'atomic' procedure that actually does something with a case

    case : tuple
    p1 : whatever, specific to this function
    p2 : whatever, specific to this function
    p3 : whatever, specific to this function"""
    my_list = []

    # here the function can handle a case with any number of params,
    # which may not always be so
    for param in case:
        my_list.append(param)
    my_list.append(p1)
    my_list.append(p2)
    my_list.append(p3)
    print(''.join(my_list))


# Whenever we use the multiprocessing library to start a new process, it imports the main module
# in a new Python interpreter. Therefore it’s important to ensure the main module can be safely
# imported by a new Python interpreter without causing unintended side effects such as re-creating
# a new process and failing with a RuntimeError.
# The key is to protect the entry point of the program by using:
# if __name__ == '__main__:
#    # create new process
if __name__ == "__main__":

    l1 = ['a', 'b', 'c', 'd']
    l2 = ['1', '2', '3', '4']
    l3 = ['+', '-', '*', '/']

    parallel_run(iter_func=__sample_iter_func,
                 atomic_func=__sample_atomic_func,
                 iter_args=[l1, l2, l3],
                 args=['lorem', "ipsum", "dolor"],
                 nb_cores=number_of_cores())