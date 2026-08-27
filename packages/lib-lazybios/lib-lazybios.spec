# SPDX-License-Identifier: Apache-2.0
Name:           lib-lazybios
Version:        1.3.0
Release:        1%{?dist}
Summary:        Lightweight SMBIOS/DMI parsing library
License:        LGPL-2.1-or-later
URL:            https://github.com/LazySeldi/lazybios
Source0:        lib-lazybios-1.3.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Lightweight SMBIOS/DMI parsing library

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
