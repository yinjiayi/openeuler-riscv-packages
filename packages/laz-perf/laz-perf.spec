# SPDX-License-Identifier: Apache-2.0
Name:           laz-perf
Version:        3.4.0
Release:        1%{?dist}
Summary:        Alternative LAZ implementation for C++ and JavaScript
License:        Apache-2.0
URL:            https://github.com/hobu/laz-perf
Source0:        laz-perf-3.4.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Alternative LAZ implementation for C++ and JavaScript

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

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.4.0-1
- Initial openEuler RISC-V package from the full package inventory.
