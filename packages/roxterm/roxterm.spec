# SPDX-License-Identifier: Apache-2.0
Name:           roxterm
Version:        3.15.3
Release:        1%{?dist}
Summary:        Tabbed, VTE-based terminal emulator
License:        GPL-2.0-or-later
URL:            https://github.com/realh/roxterm
Source0:        roxterm-3.15.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Tabbed, VTE-based terminal emulator

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
%doc README
%doc README.md
%doc NEWS
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.15.3-1
- Initial openEuler RISC-V package from the full package inventory.
