# SPDX-License-Identifier: Apache-2.0
Name:           ecos
Version:        2.0.10
Release:        1%{?dist}
Summary:        A lightweight conic solver for second-order cone programming
License:        GPL-3.0-or-later
URL:            https://github.com/embotech/ecos
Source0:        ecos-2.0.10.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A lightweight conic solver for second-order cone programming

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.10-1
- Initial openEuler RISC-V package from the full package inventory.
