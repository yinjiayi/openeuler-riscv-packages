# SPDX-License-Identifier: Apache-2.0
Name:           aribb24
Version:        1.0.3
Release:        1%{?dist}
Summary:        A library for ARIB STD-B24, decoding JIS 8 bit characters and parsing MPEG-TS stream.
License:        LGPL-3.0-or-later
URL:            https://github.com/nkoriyama/aribb24
Source0:        aribb24-1.0.3.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A library for ARIB STD-B24, decoding JIS 8 bit characters and parsing MPEG-TS stream.

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-1
- Initial openEuler RISC-V package from the full package inventory.
