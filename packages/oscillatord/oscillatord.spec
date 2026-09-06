# SPDX-License-Identifier: Apache-2.0
Name:           oscillatord
Version:        3.8.4
Release:        1%{?dist}
Summary:        Daemon for disciplining an oscillator
License:        GPL-2.0-or-later
URL:            https://github.com/Orolia2s/oscillatord
Source0:        oscillatord-3.8.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Daemon for disciplining an oscillator

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.8.4-1
- Initial openEuler RISC-V package from the full package inventory.
