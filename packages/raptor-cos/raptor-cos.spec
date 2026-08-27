# SPDX-License-Identifier: Apache-2.0
Name:           raptor-cos
Version:        0.8.1
Release:        1%{?dist}
Summary:        Vertically-scrolling shoot 'em up from 1994
License:        GPL-2.0-or-later
URL:            https://github.com/skynettx/raptor
Source0:        raptor-cos-0.8.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Vertically-scrolling shoot 'em up from 1994

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.1-1
- Initial openEuler RISC-V package from the full package inventory.
