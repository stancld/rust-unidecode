#!/bin/bash
set -ex

curl https://sh.rustup.rs -sSf | sh -s -- -y
export PATH="$HOME/.cargo/bin:$PATH"

for PYBIN in /opt/python/{cp38-cp38,cp39-cp39,cp310-cp310}/bin; do
    export PYTHON_SYS_EXECUTABLE="$PYBIN/python"
    export python3=${PYTHON_SYS_EXECUTABLE}
    alias python3=${PYTHON_SYS_EXECUTABLE}

    "${PYBIN}/pip" install maturin

    ${PYTHON_SYS_EXECUTABLE} -m maturin build --release
done
