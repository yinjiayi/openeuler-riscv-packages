# SPDX-License-Identifier: Apache-2.0
Name:           simpleini
Version:        4.26
Release:        2%{?dist}
Summary:        Cross-platform C++ library providing a simple API to read and write INI-style configuration files
License:        MIT
URL:            https://github.com/brofield/simpleini
Source0:        simpleini-4.26.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gtest-devel
BuildRequires:  make

%description
Cross-platform C++ library providing a simple API to read and write INI-style configuration files

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} \
  -DBUILD_TESTING=ON \
  -DSIMPLEINI_USE_SYSTEM_GTEST=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENCE.txt
%doc README.md

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.26-2
- Build the upstream test suite against the matching system GoogleTest package.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.26-1
- Initial openEuler RISC-V package from the full package inventory.
