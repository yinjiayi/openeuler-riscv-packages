# SPDX-License-Identifier: Apache-2.0
Name:           tn5250
Version:        0.18.0
Release:        1%{?dist}
Summary:        A 5250 terminal emulator for IBM iSeries and AS400
License:        LGPL-2.1-or-later
URL:            https://github.com/tn5250/tn5250
Source0:        tn5250-0.18.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A 5250 terminal emulator for IBM iSeries and AS400

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
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.18.0-1
- Initial openEuler RISC-V package from the full package inventory.
