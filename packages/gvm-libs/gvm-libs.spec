# SPDX-License-Identifier: Apache-2.0
Name:           gvm-libs
Version:        23.9.1
Release:        1%{?dist}
Summary:        greenbone-vulnerability-manager libraries
License:        GPL-2.0-or-later
URL:            https://github.com/greenbone/gvm-libs
Source0:        gvm-libs-23.9.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
greenbone-vulnerability-manager libraries

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
%license COPYING
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 23.9.1-1
- Initial openEuler RISC-V package from the full package inventory.
