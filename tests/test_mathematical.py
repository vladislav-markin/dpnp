import pytest

import dpnp as inp

import numpy


@pytest.mark.parametrize("array",
                         [[[0, 0], [0, 0]],
                          [[1, 2], [1, 2]],
                          [[1, 2], [3, 4]],
                          [[[1, 2], [3, 4]], [[1, 2], [2, 1]], [[1, 3], [3, 1]]],
                          [[[[1, 2], [3, 4]], [[1, 2], [2, 1]]], [[[1, 3], [3, 1]], [[0, 1], [1, 3]]]]
                          ],
                         ids=['[[0, 0], [0, 0]]',
                              '[[1, 2], [1, 2]]',
                              '[[1, 2], [3, 4]]',
                              '[[[1, 2], [3, 4]], [[1, 2], [2, 1]], [[1, 3], [3, 1]]]',
                              '[[[[1, 2], [3, 4]], [[1, 2], [2, 1]]], [[[1, 3], [3, 1]], [[0, 1], [1, 3]]]]'
                              ])
def test_diff(array):
    a = numpy.array(array)
    ia = inp.array(a)
    expected = numpy.diff(a)
    result = inp.diff(ia)
    numpy.testing.assert_allclose(expected, result)


class TestEdiff1d:

    def test_ediff1d_int(self):
        a = numpy.array([1, 2, 4, 7, 0])
        ia = inp.array(a)

        result = inp.ediff1d(ia)
        expected = numpy.ediff1d(a)
        numpy.testing.assert_array_equal(expected, result)


    def test_ediff1d_args(self):
        a = numpy.array([1, 2, 4, 7, 0])
        ia = inp.array(a)

        to_begin=numpy.array([-20, -30])
        i_to_begin = inp.array(to_begin)

        to_end=numpy.array([20, 15])
        i_to_end = inp.array(to_end)

        result = inp.ediff1d(ia, to_end=i_to_end, to_begin=i_to_begin)
        expected = numpy.ediff1d(a, to_end=to_end, to_begin=to_begin)
        numpy.testing.assert_array_equal(expected, result)


    def test_ediff1d_float(self):
        a = numpy.array([1., 2.5, 6., 7., 3.])
        ia = inp.array(a)

        result = inp.ediff1d(ia)
        expected = numpy.ediff1d(a)
        numpy.testing.assert_array_equal(expected, result)