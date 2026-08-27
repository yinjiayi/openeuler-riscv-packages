# SPDX-License-Identifier: Apache-2.0
Name:           consolekit
Version:        2.0.0
Release:        1%{?dist}
Summary:        A framework for defining and tracking users, login sessions, and seats
License:        GPL-2.0-or-later
URL:            https://github.com/ConsoleKit2/ConsoleKit2
Source0:        consolekit-2.0.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A framework for defining and tracking users, login sessions, and seats

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
%doc README
%doc NEWS
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
