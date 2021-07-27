#!/bin/bash
set -e -u -x

function repair_wheel {
    wheel="$1"
    if ! auditwheel show "$wheel"; then
        echo "Skipping non-platform wheel $wheel"
    else
        auditwheel repair "$wheel" --plat "$PLAT" -w /io/dist/
    fi
}


# Install a system package required by our library
#yum install -y atlas-devel
# yum install -y libaec-dev libz-dev libsz2

mv /io/__init__.py /io/GSASII/

# Compile wheels
for PYBIN in /opt/python/*/bin; do
  "${PYBIN}/pip" install numpy scons
  export SCONS_PATH=${PYBIN}/scons
  cd /io
  ${PYBIN}/python /io/setup.py bdist_wheel
  rm -rf /io/build/
done

# Bundle external shared libraries into the wheels
for whl in /io/dist/*.whl; do
    repair_wheel "$whl"
done

# Install packages and test
for PYBIN in /opt/python/*/bin/; do
  "${PYBIN}/pip" install GSASII --no-index -f /io/dist
  "${PYBIN}/python" -c 'from GSASII import GSASIIscriptable as GS2; exit()'
done
