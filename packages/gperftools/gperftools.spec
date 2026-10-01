# SPDX-License-Identifier: Apache-2.0
Name:           gperftools
Version:        2.18.1
Release:        1%{?dist}
Summary:        Fast, multi-threaded malloc and nifty performance analysis tools
License:        BSD-3-Clause
URL:            https://github.com/gperftools/gperftools
Source0:        gperftools-2.18.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Fast, multi-threaded malloc and nifty performance analysis tools

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
%doc README
%doc NEWS
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.18.1-1
- Initial openEuler RISC-V package from the full package inventory.
