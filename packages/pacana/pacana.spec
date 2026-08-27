# SPDX-License-Identifier: Apache-2.0
Name:           pacana
Version:        0.13
Release:        1%{?dist}
Summary:        Pacman repository analysis tool
License:        GPL-3.0-or-later
URL:            https://github.com/bbidulock/pacana
Source0:        pacana-0.13.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Pacman repository analysis tool

%prep
%autosetup -p1

%build
autoreconf -fi
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
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.13-1
- Initial openEuler RISC-V package from the full package inventory.
