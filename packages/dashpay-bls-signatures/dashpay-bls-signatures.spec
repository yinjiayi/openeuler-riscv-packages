# SPDX-License-Identifier: Apache-2.0
Name:           dashpay-bls-signatures
Version:        1.3.5
Release:        3%{?dist}
Summary:        Chia Networks BLS Signatures implementation fork for Dashcore
License:        Apache-2.0
URL:            https://github.com/dashpay/bls-signatures
Source0:        dashpay-bls-signatures-1.3.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gmp-devel
BuildRequires:  make

%description
Chia Networks BLS Signatures implementation fork for Dashcore

%prep
%autosetup -p1 -n bls-signatures-%{version}

%build
%cmake -S . -B %{_vpath_builddir} \
  -DBUILD_BLS_BENCHMARKS=OFF \
  -DBUILD_BLS_PYTHON_BINDINGS=OFF \
  -DBUILD_BLS_TESTS=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%{_vpath_builddir}/src/runtest

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.5-3
- Configure and build in the same explicit out-of-source directory while retaining the C++ test.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.5-2
- Match the verified archive root and build the tested C++ library without optional bindings or benchmarks.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.5-1
- Initial openEuler RISC-V package from the full package inventory.
