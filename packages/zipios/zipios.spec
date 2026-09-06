# SPDX-License-Identifier: Apache-2.0
Name:           zipios
Version:        2.3.2
Release:        1%{?dist}
Summary:        C++ Library for Reading and Writing Zip Files
License:        LGPL-2.1-or-later
URL:            https://github.com/Zipios/Zipios
Source0:        zipios-2.3.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
C++ Library for Reading and Writing Zip Files

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.2-1
- Initial openEuler RISC-V package from the full package inventory.
