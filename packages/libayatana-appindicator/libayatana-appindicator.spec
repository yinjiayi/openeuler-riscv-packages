# SPDX-License-Identifier: Apache-2.0
Name:           libayatana-appindicator
Version:        0.6.0
Release:        1%{?dist}
Summary:        Ayatana Application Indicators shared library
License:        LGPL-3.0-or-later
URL:            https://github.com/AyatanaIndicators/libayatana-appindicator
Source0:        libayatana-appindicator-0.6.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Ayatana Application Indicators shared library

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
%license COPYING.GPL.3
%license COPYING.LGPL.2.1
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.0-1
- Initial openEuler RISC-V package from the full package inventory.
