# SPDX-License-Identifier: Apache-2.0
Name:           sparrow
Version:        0.6.0
Release:        1%{?dist}
Summary:        C++20 idiomatic APIs for the Apache Arrow Columnar Format
License:        Apache-2.0
URL:            https://github.com/man-group/sparrow
Source0:        sparrow-0.6.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
C++20 idiomatic APIs for the Apache Arrow Columnar Format

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.0-1
- Initial openEuler RISC-V package from the full package inventory.
