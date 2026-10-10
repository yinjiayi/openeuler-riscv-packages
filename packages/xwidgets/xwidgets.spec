# SPDX-License-Identifier: Apache-2.0
Name:           xwidgets
Version:        0.29.0
Release:        1%{?dist}
Summary:        C++ backend for Jupyter interactive widgets
License:        BSD-3-Clause
URL:            https://github.com/jupyter-xeus/xwidgets
Source0:        xwidgets-0.29.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
C++ backend for Jupyter interactive widgets

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.29.0-1
- Initial openEuler RISC-V package from the full package inventory.
