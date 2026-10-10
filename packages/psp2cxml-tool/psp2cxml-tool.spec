# SPDX-License-Identifier: Apache-2.0
Name:           psp2cxml-tool
Version:        1.3
Release:        1%{?dist}
Summary:        A tool for compiling xml files to cxml/rco/rcs format
License:        GPL-3.0-or-later
URL:            https://github.com/Princess-of-Sleeping/psp2cxml-tool
Source0:        psp2cxml-tool-1.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A tool for compiling xml files to cxml/rco/rcs format

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3-1
- Initial openEuler RISC-V package from the full package inventory.
