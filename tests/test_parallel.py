#!/usr/bin/env python
# coding: utf-8

r"""Tests for the parallel.py module"""

from typing import Callable, List, Tuple

from ydeos_parallel.parallel import chunks, nb_per_process, physical_memory, \
    processor, number_of_cpus, number_of_cores, number_of_threads, \
    parallel_run


def _ten_by_four_chunks_verification(chunks_):
    assert len(chunks_) == 4
    assert chunks_[0] == [0, 1, 2]
    assert chunks_[1] == [3, 4, 5]
    assert chunks_[2] == [6, 7, 8]
    assert chunks_[3] == [9]


def test_chunks():
    r"""test chunks happy path"""
    input_range = range(10)
    nb = 3

    chunks_ = chunks(input_range, nb_items=nb)
    _ten_by_four_chunks_verification(chunks_)

    input_range = list(input_range)
    chunks_ = chunks(input_range, nb_items=nb)
    _ten_by_four_chunks_verification(chunks_)

    input_range = tuple(input_range)
    chunks_ = chunks(input_range, nb_items=nb)
    _ten_by_four_chunks_verification(chunks_)


def test_nb_per_process():
    r"""Test nb_per_process() happy path"""
    assert nb_per_process(10, 2) == 5
    assert nb_per_process(9, 2) == 5
    assert nb_per_process(8, 2) == 4
    assert nb_per_process(7, 2) == 4

    assert nb_per_process(10, 4) == 3
    assert nb_per_process(9, 4) == 3
    assert nb_per_process(8, 4) == 2
    assert nb_per_process(7, 4) == 2


def test_physical_memory():
    r"""Test that we get a positive integer."""
    assert isinstance(physical_memory(), int)
    assert physical_memory() > 0


def test_processor():
    r"""Test we get a string description"""
    assert isinstance(processor(), str)
    assert processor()  # The description should contain something


def test_number_of_cpus():
    r"""Test that we get a positive integer."""
    assert isinstance(number_of_cpus(), int)
    assert number_of_cpus() > 0


def test_number_of_cores():
    r"""Test that we get a positive integer."""
    assert isinstance(number_of_cores(), int)
    assert number_of_cores() > 0


def test_number_of_threads():
    r"""Test that we get a positive integer."""
    assert isinstance(number_of_threads(), int)
    assert number_of_threads() > 0


def __sample_iter_func(atomic_func: Callable,
                       cases: List,
                       other_args: List,
                       process_nb: int = -1):
    r"""Sample iteration function."""
    print(f"This is process {process_nb}")
    for _, case in enumerate(cases):
        atomic_func(case, *other_args)


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


def test_parallel_run():
    r"""Test parallel run happy path"""
    list_1 = ['a', 'b', 'c', 'd']
    list_2 = ['1', '2', '3', '4']
    list_3 = ['+', '-', '*', '/']

    assert parallel_run(iter_func=__sample_iter_func,
                        atomic_func=__sample_atomic_func,
                        iter_args=[list_1, list_2, list_3],
                        args=['lorem', "ipsum", "dolor"],
                        nb_cores=number_of_cores()) is None
