# SPDX-License-Identifier: Apache-2.0
# Header-only noarch payload: compilation and tests still run on the target.
%global debug_package %{nil}
Name:           libhpptools
Version:        1.1.3
Release:        1%{?dist}
Summary:        C++ header-only utilities and compression stream wrappers
License:        MIT AND BSL-1.0 AND LicenseRef-Public-Domain
URL:            https://github.com/mateidavid/hpptools
Source0:        https://codeload.github.com/mateidavid/hpptools/tar.gz/93bb758cd02cb58b14be80a0f181819d83145af0#/libhpptools-1.1.3.tar.gz
Source1:        https://raw.githubusercontent.com/boostorg/boost/4f2bdeb93a4be13ba0dc5e9f44920a2bf67191fc/LICENSE_1_0.txt#/BOOST-LICENSE_1_0.txt
BuildArch:      noarch
BuildRequires:  gcc gcc-c++ make boost-devel zlib-devel glibc-devel libstdc++-devel
BuildRequires:  bash coreutils binutils rpm gzip tar grep gawk sed findutils diffutils patch
Requires:       gcc-c++ make boost-devel zlib-devel bash coreutils gzip diffutils rpm

%description
C++11 header-only utility collection with compression streams. Includes the
original functional test sources and a downstream installed-header replay.
Headers are installed under the hpptools include namespace.

%prep
%setup -q -n hpptools-93bb758cd02cb58b14be80a0f181819d83145af0
cp -p %{SOURCE1} BOOST-LICENSE_1_0.txt
sha256sum include/*.hpp examples/*.cpp examples/*.make examples/catch.hpp > original.sha256
cat > run-tests.sh <<'SH'
#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
test "$#" -le 1
root=${1:-/}
prefix=${root%/}/usr
self=$(cd -- "$(dirname -- "$0")" && pwd)
work=$(mktemp -d)
cleanup() { rc=$?; if test "$rc" -eq 0; then rm -r -- "$work"; else printf 'Failed replay retained: %%s\n' "$work" >&2; fi; exit "$rc"; }
trap cleanup EXIT
ln -s "$prefix/include/hpptools" "$work/include"
mkdir "$work/examples"
cp -p "$self"/examples/* "$work/examples/"
cp -p "$self/original.sha256" "$work/"
cd "$work"
sha256sum -c original.sha256
cd examples
make -f test-alg.make all CXX=g++ DOCKER_CMD=
make -f test-zstr.make all CXX=g++ DOCKER_CMD=
make -f test-alg.make test CXX=g++ DOCKER_CMD= '.SHELLFLAGS=-e -o pipefail -c'
make -f test-zstr.make test CXX=g++ DOCKER_CMD= '.SHELLFLAGS=-e -o pipefail -c'
printf 'PASS downstream installed-header replay: both unchanged original test targets\n'
SH

%build
make -C examples -f test-alg.make all CXX=%{__cxx} DOCKER_CMD=
make -C examples -f test-zstr.make all CXX=%{__cxx} DOCKER_CMD=

%install
install -d %{buildroot}%{_includedir}/hpptools %{buildroot}%{_datadir}/%{name}/tests/examples
install -pm0644 include/*.hpp %{buildroot}%{_includedir}/hpptools/
install -pm0644 examples/*.cpp examples/*.make examples/catch.hpp %{buildroot}%{_datadir}/%{name}/tests/examples/
install -pm0644 original.sha256 %{buildroot}%{_datadir}/%{name}/tests/
install -pm0755 run-tests.sh %{buildroot}%{_datadir}/%{name}/tests/

%check
sha256sum -c original.sha256
make -C examples -f test-alg.make test CXX=%{__cxx} DOCKER_CMD= '.SHELLFLAGS=-e -o pipefail -c'
make -C examples -f test-zstr.make test CXX=%{__cxx} DOCKER_CMD= '.SHELLFLAGS=-e -o pipefail -c'
bash %{buildroot}%{_datadir}/%{name}/tests/run-tests.sh %{buildroot}

%files
%license LICENSE BOOST-LICENSE_1_0.txt
%doc README.org VERSION
%{_includedir}/hpptools/
%{_datadir}/%{name}/

%changelog
* Fri Oct 16 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.1.3-1
- Preserve both original functional test targets and installed-header replays.
