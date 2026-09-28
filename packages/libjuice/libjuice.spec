# SPDX-License-Identifier: Apache-2.0
Name:           libjuice
Version:        1.7.3
Release:        2%{?dist}
Summary:        UDP Interactive Connectivity Establishment (ICE) library
License:        MPL-2.0
URL:            https://github.com/paullouisageneau/libjuice
Source0:        libjuice-1.7.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
UDP Interactive Connectivity Establishment (ICE) library

%prep
%autosetup -p1

%build
%cmake_conf -DNO_TESTS=OFF
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%{_vpath_builddir}/tests

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.7.3-2
- Use the openEuler out-of-source CMake workflow and run the upstream test binary.

* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.7.3-1
- Initial openEuler RISC-V package from the full package inventory.
