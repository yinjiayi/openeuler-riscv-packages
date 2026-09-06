# SPDX-License-Identifier: Apache-2.0
Name:           ayatana-indicator-application
Version:        22.2.0
Release:        1%{?dist}
Summary:        Ayatana Application Indicators
License:        GPL-3.0-or-later
URL:            https://github.com/AyatanaIndicators/ayatana-indicator-application
Source0:        ayatana-indicator-application-22.2.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Ayatana Application Indicators

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 22.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
