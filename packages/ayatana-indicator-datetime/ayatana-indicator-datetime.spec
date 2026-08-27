# SPDX-License-Identifier: Apache-2.0
Name:           ayatana-indicator-datetime
Version:        25.4.0
Release:        1%{?dist}
Summary:        Ayatana Indicator providing clock and calendar
License:        GPL-3.0-or-later
URL:            https://github.com/AyatanaIndicators/ayatana-indicator-datetime
Source0:        ayatana-indicator-datetime-25.4.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Ayatana Indicator providing clock and calendar

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
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 25.4.0-1
- Initial openEuler RISC-V package from the full package inventory.
