# SPDX-License-Identifier: Apache-2.0
Name:           ayatana-indicator-a11y
Version:        25.4.0
Release:        1%{?dist}
Summary:        Ayatana Indicator for Accessibility Settings
License:        GPL-3.0-or-later
URL:            https://github.com/AyatanaIndicators/ayatana-indicator-a11y
Source0:        ayatana-indicator-a11y-25.4.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Ayatana Indicator for Accessibility Settings

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 25.4.0-1
- Initial openEuler RISC-V package from the full package inventory.
