# SPDX-License-Identifier: Apache-2.0
Name:           libnpy
Version:        1.0.1
Release:        1%{?dist}
Summary:        Header-only C++14 library for NumPy array files
License:        MIT
URL:            https://github.com/llohse/libnpy
Source0:        libnpy-1.0.1.tar.gz
Patch0:         0001-catch2-v3-tests.patch
BuildArch:      noarch
BuildRequires:  gcc-c++
BuildRequires:  meson >= 0.55
BuildRequires:  ninja-build
BuildRequires:  pkgconf
BuildRequires:  python3-numpy
BuildRequires:  catch2-devel >= 3
Requires:       gcc-c++
Requires:       meson >= 0.55
Requires:       ninja-build
Requires:       pkgconf
Requires:       python3-numpy
Requires:       catch2-devel >= 3
Requires:       bash
Requires:       coreutils
Requires:       diffutils

%description
Read and write scalar numerical NumPy array files using a standalone C++14
header. The original test sources and fixture generator are retained for
installed-header verification; Catch2 and NumPy are test dependencies.

%prep
%setup -q -n libnpy-890ea4fcda302a580e633c624c6a63e2a5d422f6
%patch0 -p1

%build
# Original tests/ project; never download its optional Catch2 v2 wrap.
meson setup tests/builddir tests --wrap-mode=nodownload \
  -Dcpp_args="%{optflags} -UNDEBUG"
meson compile -C tests/builddir

%install
# Upstream is header-only and defines no install target.
install -D -m 0644 include/npy.hpp %{buildroot}%{_includedir}/npy.hpp
install -D -m 0644 include/npy.hpp %{buildroot}%{_datadir}/libnpy/include/npy.hpp
for file in meson.build test-read.cpp test-write.cpp createnpy.py; do
  install -D -m 0644 tests/$file %{buildroot}%{_datadir}/libnpy/tests/$file
done
(cd %{buildroot}%{_datadir}/libnpy; sha256sum include/npy.hpp tests/meson.build \
  tests/test-read.cpp tests/test-write.cpp tests/createnpy.py) \
  > %{buildroot}%{_datadir}/libnpy/SHA256SUMS
cat > %{buildroot}%{_datadir}/libnpy/run-tests.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
root=${1:-}
base="$root/usr/share/libnpy"
(cd "$base"; sha256sum -c SHA256SUMS)
cmp "$base/include/npy.hpp" "$root/usr/include/npy.hpp"
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
mkdir "$work/include" "$work/tests"
cp "$root/usr/include/npy.hpp" "$work/include/npy.hpp"
cp "$base/tests/meson.build" "$base/tests/test-read.cpp" \
  "$base/tests/test-write.cpp" "$base/tests/createnpy.py" "$work/tests/"
meson setup "$work/build" "$work/tests" --wrap-mode=nodownload -Dcpp_args=-UNDEBUG
meson test -C "$work/build" --print-errorlogs --verbose
python3 - "$work/build/data" <<'PY'
import pathlib,sys,numpy as np
p=pathlib.Path(sys.argv[1])
expected={
 'out11.npy':np.array([[1,2,3],[4,5,6]],dtype=np.float64),
 'out12.npy':np.array([1,2,3,4,5,6],dtype=np.float64),
 'out11_ptr.npy':np.array([[1,2,3],[4,5,6]],dtype=np.float64),
 'out21.npy':np.array([[[7]]],dtype=np.float64),
 'out22.npy':np.array(7,dtype=np.float64),
 'out31.npy':np.empty((4,0),dtype=np.float64),
}
for name,want in expected.items():
 got=np.load(p/name,allow_pickle=False)
 if got.dtype!=want.dtype or got.shape!=want.shape or not np.array_equal(got,want):
  raise SystemExit('writer interoperability mismatch: '+name)
print('PASS downstream installed-header=1 original-meson-tests=2 numpy-writer-checks=6 skips=0')
PY
SH
chmod 0755 %{buildroot}%{_datadir}/libnpy/run-tests.sh

%check
# Preserve upstream defaults, all 15 enabled read cases and write executable.
meson test -C tests/builddir --print-errorlogs --verbose
bash %{buildroot}%{_datadir}/libnpy/run-tests.sh "%{buildroot}"

%files
%license LICENSE
%doc README.md
%{_includedir}/npy.hpp
%{_datadir}/libnpy/

%changelog
* Sat Oct 17 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.1-1
- Initial package with original tests and a minimal Catch2 v3 interface patch.
