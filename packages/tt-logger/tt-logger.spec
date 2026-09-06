# SPDX-License-Identifier: Apache-2.0
Name:           tt-logger
Version:        1.1.9
Release:        1%{?dist}
Summary:        A flexible and performant C++ logging library for Tenstorrent projects
License:        Apache-2.0
URL:            https://github.com/tenstorrent/tt-logger
Source0:        tt-logger-1.1.9.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A flexible and performant C++ logging library for Tenstorrent projects

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
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.9-1
- Initial openEuler RISC-V package from the full package inventory.
