# SPDX-License-Identifier: Apache-2.0
Name:           ayatana-indicator-messages
Version:        24.5.1
Release:        1%{?dist}
Summary:        Ayatana Indicator that collects messages that need a response
License:        GPL-3.0-or-later
URL:            https://github.com/AyatanaIndicators/ayatana-indicator-messages
Source0:        ayatana-indicator-messages-24.5.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Ayatana Indicator that collects messages that need a response

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 24.5.1-1
- Initial openEuler RISC-V package from the full package inventory.
