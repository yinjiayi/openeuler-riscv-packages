# SPDX-License-Identifier: Apache-2.0
Name:           libmcl
Version:        3.04
Release:        1%{?dist}
Summary:        Portable and fast pairing-based cryptography library
License:        BSD-3-Clause
URL:            https://github.com/herumi/mcl
Source0:        libmcl-3.04.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Portable and fast pairing-based cryptography library

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
%license COPYRIGHT


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.04-1
- Initial openEuler RISC-V package from the full package inventory.
