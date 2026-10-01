# SPDX-License-Identifier: Apache-2.0
Name:           g3data
Version:        1.5.4
Release:        1%{?dist}
Summary:        A tool for extracting data from scanned graphs.
License:        GPL-2.0-or-later
URL:            https://github.com/pn2200/g3data
Source0:        g3data-1.5.4.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A tool for extracting data from scanned graphs.

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
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.4-1
- Initial openEuler RISC-V package from the full package inventory.
