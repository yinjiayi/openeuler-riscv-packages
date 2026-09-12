# SPDX-License-Identifier: Apache-2.0
Name:           netdiscover
Version:        0.21
Release:        1%{?dist}
Summary:        A network address discovering tool
License:        GPL-3.0-or-later
URL:            https://github.com/netdiscover-scanner/netdiscover
Source0:        netdiscover-0.21.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A network address discovering tool

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
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.21-1
- Initial openEuler RISC-V package from the full package inventory.
