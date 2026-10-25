# SPDX-License-Identifier: Apache-2.0
Name:           libobjectbox
Version:        5.3.2
Release:        1%{?dist}
Summary:        C/C++ database for objects and structs
License:        Apache-2.0
URL:            https://github.com/objectbox/objectbox-c
Source0:        libobjectbox-5.3.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
C/C++ database for objects and structs

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.3.2-1
- Initial openEuler RISC-V package from the full package inventory.
