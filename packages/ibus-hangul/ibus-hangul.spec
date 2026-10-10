# SPDX-License-Identifier: Apache-2.0
Name:           ibus-hangul
Version:        1.5.5
Release:        1%{?dist}
Summary:        Korean input engine for IBus
License:        GPL-2.0-or-later
URL:            https://github.com/libhangul/ibus-hangul
Source0:        ibus-hangul-1.5.5.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Korean input engine for IBus

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.5-1
- Initial openEuler RISC-V package from the full package inventory.
