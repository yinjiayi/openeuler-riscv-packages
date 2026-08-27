# SPDX-License-Identifier: Apache-2.0
Name:           hmat-oss
Version:        1.11.1
Release:        1%{?dist}
Summary:        A hierarchical matrix C/C++ library
License:        GPL-2.0-or-later
URL:            https://github.com/jeromerobert/hmat-oss
Source0:        hmat-oss-1.11.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A hierarchical matrix C/C++ library

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
%license LICENSE.md
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.11.1-1
- Initial openEuler RISC-V package from the full package inventory.
