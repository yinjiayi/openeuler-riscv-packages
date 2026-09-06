# SPDX-License-Identifier: Apache-2.0
Name:           ashwal
Version:        1.0.0
Release:        1%{?dist}
Summary:        Blazing-fast pywal-like color palette generator written in C, fork of cwal with extra features.
License:        GPL-3.0-or-later
URL:            https://github.com/shadowash8/ashwal
Source0:        ashwal-1.0.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Blazing-fast pywal-like color palette generator written in C, fork of cwal with extra features.

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
