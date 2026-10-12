# SPDX-License-Identifier: Apache-2.0
Name:           xlsxio
Version:        0.2.36
Release:        1%{?dist}
Summary:        C library for reading and writing .xlsx files
License:        MIT
URL:            https://github.com/brechtsanders/xlsxio
Source0:        xlsxio-0.2.36.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
C library for reading and writing .xlsx files

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.36-1
- Initial openEuler RISC-V package from the full package inventory.
