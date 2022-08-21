#!/bin/bash
set -ex

curl https://sh.rustup.rs -sSf | sh -s -- -y
export PATH="$HOME/.cargo/bin:$PATH"

for PYBIN in /opt/python/{cp38-cp38,cp39-cp39,cp310-cp310}/bin; do
    export PYTHON_SYS_EXECUTABLE="$PYBIN/python"

    "${PYBIN}/pip" install maturin
done
