# SPDX-License-Identifier: Apache-2.0
Name:           tilda
Version:        2.0.0
Release:        1%{?dist}
Summary:        A Gtk based drop down terminal for Linux and Unix
License:        GPL-2.0-or-later
URL:            https://github.com/lanoxx/tilda
Source0:        tilda-2.0.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A Gtk based drop down terminal for Linux and Unix

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
%license COPYING.GPLv3
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
