# SPDX-License-Identifier: Apache-2.0
Name:           qucs-rflayout
Version:        2.1.2
Release:        2%{?dist}
Summary:        Export Qucs RF schematics to KiCad layouts & OpenEMS scripts
License:        GPL-3.0-or-later
URL:            https://github.com/thomaslepoix/Qucs-RFlayout
Source0:        qucs-rflayout-2.1.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  mesa-libGL-devel
BuildRequires:  qt6-qtbase-devel

%description
Export Qucs RF schematics to KiCad layouts & OpenEMS scripts

%prep
%autosetup -n Qucs-RFlayout-%{version} -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%cmake_build --target check

%files -f %{name}.files
%license LICENSE
%doc README.md
%doc CHANGELOG

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.2-2
- Match the official archive root and add the Qt 6 and OpenGL development files.
- Run the upstream check target so its excluded unit-test executable is built before CTest.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.2-1
- Initial openEuler RISC-V package from the full package inventory.
