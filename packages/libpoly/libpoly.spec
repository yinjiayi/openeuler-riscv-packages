# SPDX-License-Identifier: Apache-2.0
Name:           libpoly
Version:        0.2.1
Release:        1%{?dist}
Summary:        C library for manipulating polynomials
License:        LGPL-3.0-or-later
URL:            https://github.com/SRI-CSL/libpoly
Source0:        libpoly-0.2.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
C library for manipulating polynomials

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
%license LICENCE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
