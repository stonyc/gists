#!/usr/bin/env bash

export ROOT=$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")

BASE_PYTHON="python3.8"  # Replace with desired version of installed Python.
VENV_NAME="venv"
VENV_PATH="${ROOT}/${VENV_NAME}"
PEX_NAME="venv.pex"
PEX_PATH="./${PEX_NAME}"

rm -rf ${VENV_PATH}
${BASE_PYTHON} -m venv ${VENV_PATH}
source ${VENV_PATH}/bin/activate

rm -r ${ROOT}/*.egg-info
python -m pip install --upgrade pip setuptools wheel pex
pip3 install -r requirements.txt

rm -r ${ROOT}/dist
rm -f ${ROOT}/*.pex

python -m pex -r requirements.txt -o ${PEX_PATH}
