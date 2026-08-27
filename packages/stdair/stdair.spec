# SPDX-License-Identifier: Apache-2.0
Name:           stdair
Version:        1.00.26
Release:        1%{?dist}
Summary:        C++ Standard Airline IT Object Library
License:        LGPL-2.1-or-later
URL:            https://github.com/airsim/stdair
Source0:        stdair-1.00.26.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
C++ Standard Airline IT Object Library

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
%license COPYING
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.00.26-1
- Initial openEuler RISC-V package from the full package inventory.
