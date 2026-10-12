# SPDX-License-Identifier: Apache-2.0
Name:           radiotray-ng
Version:        0.2.10.1
Release:        1%{?dist}
Summary:        An Internet radio player for Linux
License:        GPL-3.0-or-later
URL:            https://github.com/ebruck/radiotray-ng
Source0:        radiotray-ng-0.2.10.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
An Internet radio player for Linux

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
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.10.1-1
- Initial openEuler RISC-V package from the full package inventory.
