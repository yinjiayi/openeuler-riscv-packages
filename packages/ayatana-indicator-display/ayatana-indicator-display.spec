# SPDX-License-Identifier: Apache-2.0
Name:           ayatana-indicator-display
Version:        24.5.2
Release:        1%{?dist}
Summary:        Ayatana Indicator Display
License:        GPL-3.0-or-later
URL:            https://github.com/AyatanaIndicators/ayatana-indicator-display
Source0:        ayatana-indicator-display-24.5.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Ayatana Indicator Display

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
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 24.5.2-1
- Initial openEuler RISC-V package from the full package inventory.
