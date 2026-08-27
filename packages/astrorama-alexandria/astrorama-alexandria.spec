# SPDX-License-Identifier: Apache-2.0
Name:           astrorama-alexandria
Version:        2.32.0
Release:        1%{?dist}
Summary:        SDC-CH common library for the Euclid project
License:        LGPL-3.0-or-later
URL:            https://github.com/astrorama/Alexandria
Source0:        astrorama-alexandria-2.32.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
SDC-CH common library for the Euclid project

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.32.0-1
- Initial openEuler RISC-V package from the full package inventory.
