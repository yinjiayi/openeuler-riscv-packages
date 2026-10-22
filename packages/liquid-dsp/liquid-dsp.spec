# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
# Packaging recipe only; distributed software license set is specified below.
# Review draft: hosted target build/install acceptance is not yet established.
%global upstream_commit 10041f70cebbe3b97887e75bb41e48b73dda1b23
%global fftw_version 3.3.10
%global fftw_release 3.oe2403sp3

Name:           liquid-dsp
Version:        1.8.3
Release:        1%{?dist}
Summary:        Digital signal processing library for software-defined radio
License:        MIT AND GPL-2.0-or-later AND (GPL-3.0-or-later WITH Autoconf-exception-macro) AND (GPL-3.0-or-later WITH Autoconf-exception-generic-3.0) AND X11 AND FSFAP
URL:            https://liquidsdr.org/
Source0:        https://codeload.github.com/jgaeddert/liquid-dsp/tar.gz/%{upstream_commit}#/liquid-dsp-%{version}.tar.gz
Source1:        https://ftp.gnu.org/gnu/Licenses/gpl-2.0.txt#/GPL-2.0.txt
Source2:        https://ftp.gnu.org/gnu/Licenses/gpl-3.0.txt#/GPL-3.0.txt
Source3:        https://repo.openeuler.org/openEuler-24.03-LTS-SP3/source/Packages/fftw-%{fftw_version}-%{fftw_release}.src.rpm
Patch0:         0001-add-installed-checks.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  fftw-devel = %{fftw_version}-%{fftw_release}
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  binutils
BuildRequires:  grep
Requires:       fftw-libs-single = %{fftw_version}-%{fftw_release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Liquid is a digital signal processing library for software-defined radios.
The default shared-library, FFTW, threads, SIMD discovery, complete examples,
autotests and benchmark build are preserved. This distribution includes the
exact corresponding-source FFTW SRPM used for its default FFTW dependency.

%package devel
Summary:        Headers and original pkg-config/CMake interfaces for Liquid
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       fftw-devel = %{fftw_version}-%{fftw_release}

%description devel
Original public header, shared-library development link, pkg-config file and
relocatable CMake target liquid::liquid.

%package tests
Summary:        Unmodified original Liquid examples and full autotest registry
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       cmake
Requires:       make
Requires:       pkgconf-pkg-config
Requires:       python3
Requires:       bash
Requires:       coreutils
Requires:       rpm
Requires:       binutils
Requires:       grep

%description tests
All 191 original example programs, the complete original 1349-entry autotest
registry, and the default-built benchmark/autoscript tools. Benchmark timing is
not part of this package's acceptance. Additional downstream interface checks
do not replace or weaken any upstream test.

%prep
%setup -q -n %{name}-%{upstream_commit}
%patch0 -p1
mkdir -p distribution-licenses corresponding-source
install -m 0644 %{SOURCE1} distribution-licenses/GPL-2.0.txt
install -m 0644 %{SOURCE2} distribution-licenses/GPL-3.0.txt
install -m 0644 %{SOURCE3} corresponding-source/fftw-%{fftw_version}-%{fftw_release}.src.rpm
# Generate exact manifests from the unchanged original build and registry.
python3 - <<'PY'
from pathlib import Path
import re
examples = re.search(r'set\(EXAMPLES\s+(.*?)\n\s*\)', Path('examples/CMakeLists.txt').read_text(), re.S).group(1).split()
registry = Path('autotest/liquid_autotest_registry.h').read_text()
decls = re.findall(r'^extern struct liquid_autotest_s (\w+);$', registry, re.M)
pointers = re.findall(r'^\s*&([A-Za-z0-9_]+),?\s*$', registry, re.M)
assert len(examples) == len(set(examples)) == 191
assert len(decls) == len(set(decls)) == 1349 and pointers == decls
assert all(name.endswith('_s') for name in decls)
Path('downstream/examples.list').write_text('\n'.join(examples) + '\n')
Path('downstream/registry-names.list').write_text('\n'.join(name[:-2] for name in decls) + '\n')
PY

%build
# Relative GNUInstallDirs retain relocatable upstream exports. Default FFTW
# discovery stays enabled; these exact supplied paths remove lib/lib64 ambiguity.
cmake -S . -B build \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=lib64 \
    -DCMAKE_INSTALL_INCLUDEDIR=include \
    -DCMAKE_SKIP_RPATH=ON \
    -DCMAKE_C_FLAGS="%{optflags}" \
    -DCMAKE_CXX_FLAGS="%{optflags}" \
    -Dfftw3f_LIBRARY=%{_libdir}/libfftw3f.so \
    -Dfftw3f_INCLUDE_DIR=%{_includedir}
cmake --build build --parallel %{?_smp_build_ncpus}
test -x build/xautotest
test -x build/benchmark
test -x build/autoscript

%install
DESTDIR=%{buildroot} cmake --install build
install -d %{buildroot}%{_libexecdir}/%{name}/examples
install -m 0755 build/xautotest build/benchmark build/autoscript %{buildroot}%{_libexecdir}/%{name}/
while IFS= read -r example; do
    install -m 0755 "build/examples/$example" "%{buildroot}%{_libexecdir}/%{name}/examples/$example"
done < downstream/examples.list
install -d %{buildroot}%{_datadir}/%{name}/tests
install -m 0644 downstream/consumer.c downstream/CMakeLists.txt downstream/run-originals.py \
    downstream/examples.list downstream/registry-names.list %{buildroot}%{_datadir}/%{name}/tests/
install -m 0755 downstream/run-tests.sh %{buildroot}%{_datadir}/%{name}/run-tests.sh
install -d %{buildroot}%{_datadir}/%{name}/corresponding-source
install -m 0644 corresponding-source/*.src.rpm %{buildroot}%{_datadir}/%{name}/corresponding-source/
install -m 0644 downstream/CORRESPONDING-SOURCE.txt %{buildroot}%{_datadir}/%{name}/corresponding-source/

%check
# No test filter, timeout relaxation, skip, test-body patch or feature reduction.
ctest --test-dir build --show-only=json-v1 > build/ctest-registered.json
python3 - <<'PY'
import json
from pathlib import Path
expected = ['autotest'] + Path('downstream/examples.list').read_text().splitlines()
actual = json.loads(Path('build/ctest-registered.json').read_text())['tests']
assert len(actual) == 192 and {x['name'] for x in actual} == set(expected)
PY
LD_LIBRARY_PATH="$PWD/build" ctest --test-dir build --output-on-failure
# Repeat installed originals once using staged library and original interfaces.
LD_LIBRARY_PATH=%{buildroot}%{_libdir} \
    bash %{buildroot}%{_datadir}/%{name}/run-tests.sh --staged %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE distribution-licenses/GPL-2.0.txt distribution-licenses/GPL-3.0.txt
%doc README.rst
%{_libdir}/libliquid.so.1*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/corresponding-source/

%files devel
%{_includedir}/liquid/
%{_libdir}/libliquid.so
%{_libdir}/pkgconfig/liquid-dsp.pc
%{_libdir}/cmake/liquid/

%files tests
%{_libexecdir}/%{name}/
%{_datadir}/%{name}/tests/
%{_datadir}/%{name}/run-tests.sh

%changelog
* Sat Oct 17 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.8.3-1
- Package fixed official release with defaults, original tests and corresponding FFTW source.
