# SPDX-License-Identifier: Apache-2.0
Name:           dunedynasty
Version:        1.6.4
Release:        1%{?dist}
Summary:        Maintained fork of an enhanced continuation of the classic real-time strategy game Dune II
License:        GPL-2.0-or-later
URL:            https://github.com/gameflorist/dunedynasty
Source0:        dunedynasty-1.6.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Maintained fork of an enhanced continuation of the classic real-time strategy game Dune II

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
%license LICENSE.txt
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.4-1
- Initial openEuler RISC-V package from the full package inventory.
