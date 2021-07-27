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
  cd /io/GSASII/fsource
  "${PYBIN}/scons"
  cd  /io/GSASII
  rm -rf bindist
  mv ./bin ./bindist
  for n1 in bindist/*.so ; do
    export n2="$( cut -d '.' -f 1 <<< "$n1" ).so"
    mv ${n1} ${n2}
  done
  rm fsource/*.so
  rm fsource/*.a
  "${PYBIN}/pip" wheel /io/ --no-deps --use-feature=in-tree-build -w /io/dist/
  ls /io/dist/
  rm -rf /io/build/
done

# Bundle external shared libraries into the wheels
for whl in /io/dist/*.whl; do
    repair_wheel "$whl"
done

# Install packages and test
for PYBIN in /opt/python/*/bin/; do
  "${PYBIN}/pip" install GSASII --no-index -f /io/dist
done
