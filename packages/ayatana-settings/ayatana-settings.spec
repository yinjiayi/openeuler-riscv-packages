# SPDX-License-Identifier: Apache-2.0
Name:           ayatana-settings
Version:        24.10.1
Release:        1%{?dist}
Summary:        Configuration tool for tweaking all Ayatana system indicators
License:        GPL-3.0-or-later
URL:            https://github.com/AyatanaIndicators/ayatana-settings
Source0:        ayatana-settings-24.10.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Configuration tool for tweaking all Ayatana system indicators

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 24.10.1-1
- Initial openEuler RISC-V package from the full package inventory.
