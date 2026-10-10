# SPDX-License-Identifier: Apache-2.0
Name:           libleidenalg
Version:        0.13.0
Release:        1%{?dist}
Summary:        Leiden algorithm
License:        GPL-3.0-or-later
URL:            https://github.com/vtraag/libleidenalg
Source0:        libleidenalg-0.13.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Leiden algorithm

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
%doc CHANGELOG

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.13.0-1
- Initial openEuler RISC-V package from the full package inventory.
