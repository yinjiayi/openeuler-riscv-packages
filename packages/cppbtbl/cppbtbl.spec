# SPDX-License-Identifier: Apache-2.0
Name:           cppbtbl
Version:        0.2.1
Release:        1%{?dist}
Summary:        A C++ wrapper around the UPower DBus API to get bluetooth devices' battery
License:        MIT
URL:            https://github.com/pato05/cppbtbl
Source0:        cppbtbl-0.2.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A C++ wrapper around the UPower DBus API to get bluetooth devices' battery

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
