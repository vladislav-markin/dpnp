#!/bin/bash

if [ ! -z "${ONEAPI_ROOT}" ]; then
    . ${ONEAPI_ROOT}/mkl/latest/env/vars.sh
    . ${ONEAPI_ROOT}/compiler/latest/env/vars.sh
    . ${ONEAPI_ROOT}/tbb/latest/env/vars.sh
fi
