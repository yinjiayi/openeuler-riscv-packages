# SPDX-License-Identifier: Apache-2.0
Name:           maeparser
Version:        1.3.3
Release:        1%{?dist}
Summary:        Maestro file parser
License:        MIT
URL:            https://github.com/schrodinger/maeparser
Source0:        maeparser-1.3.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Maestro file parser

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
%license LICENSE.txt
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.3-1
- Initial openEuler RISC-V package from the full package inventory.
