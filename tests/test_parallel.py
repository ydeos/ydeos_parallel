#!/usr/bin/env python
# coding: utf-8

r"""Tests for the parallel.py module"""

from ydeos_parallel.parallel import chunks, nb_per_process


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
