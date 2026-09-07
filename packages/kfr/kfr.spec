# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           kfr
Version:        7.0.1
Release:        4%{?dist}
Summary:        Fast, modern C++ DSP framework, FFT, Sample Rate Conversion, FIR/IIR/Biquad Filters
License:        GPL-2.0-or-later
URL:            https://github.com/kfrlib/kfr
Source0:        kfr-7.0.1.tar.gz
BuildRequires:  cmake
BuildRequires:  clang
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Fast, modern C++ DSP framework, FFT, Sample Rate Conversion, FIR/IIR/Biquad Filters

%prep
%autosetup -p1

%build
export CC=clang
export CXX=clang++
export CFLAGS="${CFLAGS} -march=rv64gcv"
export CXXFLAGS="${CXXFLAGS} -march=rv64gcv"
%cmake -S . -B %{_vpath_builddir} \
  -DKFR_ARCH=rvv \
  -DCMAKE_RUNTIME_OUTPUT_DIRECTORY=%{_vpath_builddir}/bin \
  -DENABLE_TESTS=ON \
  -DENABLE_EXAMPLES=OFF
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
test "$(ctest --test-dir %{_vpath_builddir}/tests -N | awk '/^Total Tests:/{print $3}')" -gt 0
ctest --test-dir %{_vpath_builddir}/tests --output-on-failure

%files -f %{name}.files
%license LICENSE.txt
%doc README.md

%changelog
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 7.0.1-4
- Place test executables in the runtime directory referenced by upstream CTest registrations.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 7.0.1-3
- Run the registered upstream tests from their CTest subdirectory.
- Disable the empty automatic debuginfo subpackage for static-only output.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 7.0.1-2
- Build the supported RISC-V Vector backend with Clang and register upstream tests.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 7.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
