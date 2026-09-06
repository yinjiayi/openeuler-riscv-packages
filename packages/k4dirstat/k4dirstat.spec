# SPDX-License-Identifier: Apache-2.0
Name:           k4dirstat
Version:        3.4.3
Release:        1%{?dist}
Summary:        A graphical disk usage utility for KDE
License:        GPL-2.0-or-later
URL:            https://github.com/jeromerobert/k4dirstat
Source0:        k4dirstat-3.4.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A graphical disk usage utility for KDE

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
%license COPYING.LIB
%doc README.md
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.4.3-1
- Initial openEuler RISC-V package from the full package inventory.
