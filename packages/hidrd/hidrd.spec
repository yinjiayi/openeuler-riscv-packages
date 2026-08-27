# SPDX-License-Identifier: Apache-2.0
Name:           hidrd
Version:        0.2.0
Release:        1%{?dist}
Summary:        HID report descriptor I/O library and conversion tool
License:        GPL-2.0-or-later
URL:            https://github.com/DIGImend/hidrd
Source0:        hidrd-0.2.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
HID report descriptor I/O library and conversion tool

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
%doc NEWS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
