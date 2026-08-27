# SPDX-License-Identifier: Apache-2.0
Name:           libexsid
Version:        2.1
Release:        1%{?dist}
Summary:        Driver for exSID USB
License:        GPL-2.0-or-later
URL:            https://github.com/libsidplayfp/exsid-driver
Source0:        libexsid-2.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Driver for exSID USB

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
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1-1
- Initial openEuler RISC-V package from the full package inventory.
