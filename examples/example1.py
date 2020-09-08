# cython: language_level=3
# -*- coding: utf-8 -*-
# *****************************************************************************
# Copyright (c) 2016-2020, Intel Corporation
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# - Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
# *****************************************************************************

"""Example 1.

This example shows simple usage of the Intel NumPy
to calculate square matrix multiplication

Also, it produces performance comparison between regular NumPy
and Intel NumPy for several matrix multiplication

"""


import numpy
import time

try:
    import dpnp
except ImportError:
    import sys
    import os

    root_dir = os.path.join(os.path.dirname(__file__), os.pardir)
    sys.path.append(root_dir)

    import dpnp


def run_dgemm(executor, name, size, test_type, repetition):
    x = executor.arange(size * size, dtype=test_type).reshape((size, size))
    y = executor.arange(size * size, dtype=test_type).reshape((size, size))

    times = []
    for iteration in range(repetition):
        start_time = time.perf_counter()
        result = executor.matmul(x, y)
        # print("result[5]=%f" % (result.item(5)))
        end_time = time.perf_counter()
        times.append(end_time - start_time)

    execution_time = numpy.median(times)
    # print("%s gemm() execution time: %f  verification result[5]=%f" % (name, execution_time, result.item(5)))
    return execution_time, result.item(5)


if __name__ == '__main__':
    test_repetition = 5
    for test_type in [numpy.float64, numpy.float32, numpy.int64, numpy.int32]:
        type_name = numpy.dtype(test_type).name
        print(f"...Test data type is {test_type}, each test repetitions {test_repetition}")

        for size in [16, 32, 64, 128]:  # , 256, 512, 1024, 2048, 4096]:
            time_python, result_python = run_dgemm(numpy, "    <NumPy>", size, test_type, test_repetition)
            time_mkl, result_mkl = run_dgemm(dpnp, "<Intel MKL>", size, test_type, test_repetition)

            verification = False
            if result_mkl == result_python:
                verification = True

            print(
                f"type:{type_name}:N:{size:4}:NumPy:{time_python:.3e}:SYCL:{time_mkl:.3e}:ratio:{time_python/time_mkl:6.2f}:verification:{verification}")