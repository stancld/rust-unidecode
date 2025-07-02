#!/bin/bash
set -ex

curl https://sh.rustup.rs -sSf | sh -s -- -y
export PATH="$HOME/.cargo/bin:$PATH"

for PYBIN in /opt/python/{cp310-cp310,cp311-cp311,cp312-cp312,cp313-cp313}/bin; do
    export PYTHON_SYS_EXECUTABLE="$PYBIN/python"

    ${PYTHON_SYS_EXECUTABLE} -m pip install maturin

    ${PYTHON_SYS_EXECUTABLE} -m maturin build --release --interpreter ${PYTHON_SYS_EXECUTABLE}
done
