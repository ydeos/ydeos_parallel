#!/usr/bin/env python
# coding: utf-8

r"""Tests for the parallel.py module"""

from ydeos_parallel.parallel import chunks, nb_per_process


def test_chunks():
    r"""test chunks happy path"""
    input_list = range(10)
    c = chunks(input_list, nb_items=3)
    assert len(c) == 4
    assert c[0] == [0, 1, 2]
    assert c[1] == [3, 4, 5]
    assert c[2] == [6, 7, 8]
    assert c[3] == [9]

    input_list = list(range(10))
    c = chunks(input_list, nb_items=3)
    assert len(c) == 4
    assert c[0] == [0, 1, 2]
    assert c[1] == [3, 4, 5]
    assert c[2] == [6, 7, 8]
    assert c[3] == [9]

    input_list = tuple(range(10))
    c = chunks(input_list, nb_items=3)
    assert len(c) == 4
    assert c[0] == [0, 1, 2]
    assert c[1] == [3, 4, 5]
    assert c[2] == [6, 7, 8]
    assert c[3] == [9]


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
