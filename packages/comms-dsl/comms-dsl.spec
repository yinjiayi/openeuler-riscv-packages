# SPDX-License-Identifier: Apache-2.0
Name:           comms-dsl
Version:        6.3.4
Release:        1%{?dist}
Summary:        DSL schemas parser and code generator for CommsChampion Ecosystem
License:        Apache-2.0
URL:            https://github.com/commschamp/commsdsl
Source0:        comms-dsl-6.3.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
DSL schemas parser and code generator for CommsChampion Ecosystem

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.3.4-1
- Initial openEuler RISC-V package from the full package inventory.
