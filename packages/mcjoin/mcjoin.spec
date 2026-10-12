# SPDX-License-Identifier: Apache-2.0
Name:           mcjoin
Version:        2.12
Release:        1%{?dist}
Summary:        A simple and easy-to-use tool to test IPv4 and IPv6 multicast
License:        ISC
URL:            https://github.com/troglobit/mcjoin
Source0:        mcjoin-2.12.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A simple and easy-to-use tool to test IPv4 and IPv6 multicast

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
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.12-1
- Initial openEuler RISC-V package from the full package inventory.
