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
bash -c 'cat << EOF > /etc/yum.repos.d/oneAPI.repo
[oneAPI]
name=Intel(R) oneAPI repository
baseurl=https://yum.repos.intel.com/oneapi
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://yum.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB
EOF'
rpm --import https://yum.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB
yum -y install intel-oneapi-ifort
source /opt/intel/oneapi/setvars.sh intel64

# Compile wheels
for PYBIN in /opt/python/*/bin; do
#    "${PYBIN}/pip" install -r /io/dev-requirements.txt
    "${PYBIN}/pip" wheel /io/ --no-deps --use-feature=in-tree-build -w /io/dist/
    rm -rf /io/build/
done

# Bundle external shared libraries into the wheels
for whl in /io/dist/*.whl; do
    repair_wheel "$whl"
done

# Install packages and test
for PYBIN in /opt/python/*/bin/; do
    "${PYBIN}/pip" install CFML --no-index -f /io/dist
#    (cd "$HOME"; "${PYBIN}/nosetests" pymanylinuxdemo)
done
