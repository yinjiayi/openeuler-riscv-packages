# SPDX-License-Identifier: Apache-2.0
Name:           orcania
Version:        2.3.3
Release:        1%{?dist}
Summary:        Potluck with different functions for different purposes that can be shared among C programs
License:        LGPL-2.1-or-later
URL:            https://github.com/babelouest/orcania
Source0:        orcania-2.3.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Potluck with different functions for different purposes that can be shared among C programs

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.3-1
- Initial openEuler RISC-V package from the full package inventory.
