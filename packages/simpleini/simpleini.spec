# SPDX-License-Identifier: Apache-2.0
Name:           simpleini
Version:        4.26
Release:        1%{?dist}
Summary:        Cross-platform C++ library providing a simple API to read and write INI-style configuration files
License:        MIT
URL:            https://github.com/brofield/simpleini
Source0:        simpleini-4.26.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Cross-platform C++ library providing a simple API to read and write INI-style configuration files

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
%license LICENCE.txt
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.26-1
- Initial openEuler RISC-V package from the full package inventory.
