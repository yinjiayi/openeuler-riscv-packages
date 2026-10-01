# SPDX-License-Identifier: Apache-2.0
Name:           mednaffe
Version:        0.9.3
Release:        1%{?dist}
Summary:        front-end (GUI) for mednafen emulator
License:        GPL-3.0-or-later
URL:            https://github.com/AmatCoder/mednaffe
Source0:        mednaffe-0.9.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
front-end (GUI) for mednafen emulator

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license COPYING
%doc README
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.3-1
- Initial openEuler RISC-V package from the full package inventory.
