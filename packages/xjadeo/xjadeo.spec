# SPDX-License-Identifier: Apache-2.0
Name:           xjadeo
Version:        0.8.15
Release:        1%{?dist}
Summary:        A simple video player that is synchronized to jack transport
License:        GPL-2.0-or-later
URL:            https://github.com/x42/xjadeo
Source0:        xjadeo-0.8.15.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A simple video player that is synchronized to jack transport

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.15-1
- Initial openEuler RISC-V package from the full package inventory.
