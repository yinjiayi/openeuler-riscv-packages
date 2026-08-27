# SPDX-License-Identifier: Apache-2.0
Name:           libmodbuspp
Version:        0.2.3
Release:        1%{?dist}
Summary:        C++ wrapper for the libmodbus library
License:        LGPL-2.1-or-later
URL:            https://github.com/epsilonrt/libmodbuspp
Source0:        libmodbuspp-0.2.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
C++ wrapper for the libmodbus library

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
%license COPYING.LESSER
%doc README.md
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.3-1
- Initial openEuler RISC-V package from the full package inventory.
