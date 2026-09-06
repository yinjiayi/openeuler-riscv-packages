# SPDX-License-Identifier: Apache-2.0
Name:           libperseus-sdr
Version:        0.8.2
Release:        1%{?dist}
Summary:        Perseus Software Defined Radio Control Library
License:        LGPL-3.0-or-later
URL:            https://github.com/Microtelecom/libperseus-sdr
Source0:        libperseus-sdr-0.8.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Perseus Software Defined Radio Control Library

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
%license COPYING.LESSER
%doc README
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.2-1
- Initial openEuler RISC-V package from the full package inventory.
