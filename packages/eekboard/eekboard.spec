# SPDX-License-Identifier: Apache-2.0
Name:           eekboard
Version:        1.0.8
Release:        1%{?dist}
Summary:        An easy to use virtual keyboard toolkit
License:        GPL-3.0-or-later
URL:            https://github.com/ueno/eekboard
Source0:        eekboard-1.0.8.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
An easy to use virtual keyboard toolkit

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.8-1
- Initial openEuler RISC-V package from the full package inventory.
