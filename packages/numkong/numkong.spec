# SPDX-License-Identifier: Apache-2.0
Name:           numkong
Version:        7.7.1
Release:        1%{?dist}
Summary:        SIMD kernels for mixed-precision BLAS-like numerics.
License:        Apache-2.0
URL:            https://github.com/ashvardanian/NumKong
Source0:        numkong-7.7.1.tar.gz
Patch0:         0001-riscv-use-serial-u64-saturating-multiply.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
SIMD kernels for mixed-precision BLAS-like numerics.

%prep
%autosetup -p1 -n NumKong-%{version}

%build
%cmake_conf -DNK_BUILD_TEST=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 7.7.1-1
- Initial openEuler RISC-V package from the full package inventory.
